#!/usr/bin/env python
# encoding: utf-8


from bert4keras.backend import keras,set_gelu
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import Adam
import keras
import keras.backend as K
import numpy as np

set_gelu('tanh')
def textcnn(inputs, kernel_initializer):
    """
    基于keras实现的textcnn
    :param inputs:
    :param kernel_initializer:
    :return:
    """
    # 3,4,5
    cnn1 = keras.layers.Conv1D(256,
                               3,
                               strides=1,
                               padding='same',
                               activation='relu',
                               kernel_initializer=kernel_initializer)(inputs) # shape=[batch_size,maxlen-2,256]
    cnn1 = keras.layers.GlobalMaxPooling1D()(cnn1)

    cnn2 = keras.layers.Conv1D(256,
                               4,
                               strides=1,
                               padding='same',
                               activation='relu',
                               kernel_initializer=kernel_initializer)(inputs)
    cnn2 = keras.layers.GlobalMaxPooling1D()(cnn2)

    cnn3 = keras.layers.Conv1D(256,
                               5,
                               strides=1,
                               padding='same',
                               kernel_initializer=kernel_initializer)(inputs)
    cnn3 = keras.layers.GlobalMaxPooling1D()(cnn3)

    output = keras.layers.concatenate([cnn1, cnn2, cnn3],axis=-1)
    output = keras.layers.Dropout(0.2)(output)

    return output


def build_bert_model(config_path, checkpoint_path, class_nums):
    """
    构建bert模型用来进行医疗意图的识别
    :param config_path:
    :param checkpoint_path:
    :param class_nums:
    :return:
    """
    # 预加载bert模型
    bert = build_transformer_model(
        config_path=config_path,
        checkpoint_path=checkpoint_path,
        model='bert',
        return_keras_model=False
    )

    # 抽取cls 这个token
    cls_features = keras.layers.Lambda(
        lambda x: x[:,0], # 所有行的第一列
        name='cls-token')(bert.model.output) #shape=[batch_size,768]
    # 抽取所有的token，从第二个到倒数第二个
    all_token_embedding = keras.layers.Lambda(
        lambda x: x[:,1:-1],
        name='all-token')(bert.model.output) #shape=[batch_size,maxlen-2,768]

    cnn_features = textcnn(all_token_embedding, bert.initializer) #shape=[batch_size,cnn_output_dim]

    # 特征拼接
    concat_features = keras.layers.concatenate([cls_features, cnn_features], axis=-1)

    dense = keras.layers.Dense(units=512,
                               activation='relu',
                               kernel_initializer=bert.initializer)(concat_features)

    output = keras.layers.Dense(units=class_nums,
                                activation='softmax',
                                kernel_initializer=bert.initializer)(dense)

    model = keras.models.Model(bert.model.input, output)
    print(model.summary())

    return model

def search_layer(inputs, name, exclude=None):
    """根据inputs和name来搜索层
    说明：inputs为某个层或某个层的输出；name为目标层的名字。
    实现：根据inputs一直往上递归搜索，直到发现名字为name的层为止；
         如果找不到，那就返回None。
    """
    if exclude is None:
        exclude = set()

    if isinstance(inputs, keras.layers.Layer):
        layer = inputs
    else:
        layer = inputs._keras_history[0]

    if layer.name == name:
        return layer
    elif layer in exclude:
        return None
    else:
        exclude.add(layer)
        inbound_layers = layer._inbound_nodes[0].inbound_layers
        if not isinstance(inbound_layers, list):
            inbound_layers = [inbound_layers]
        if len(inbound_layers) > 0:
            for layer in inbound_layers:
                layer = search_layer(layer, name, exclude)
                if layer is not None:
                    return layer

def adversarial_training(model, embedding_name, epsilon=1):
    """给模型添加对抗训练
    其中model是需要添加对抗训练的keras模型，embedding_name
    则是model里边Embedding层的名字。要在模型compile之后使用。
    """
    if model.train_function is None:  # 如果还没有训练函数
        model._make_train_function()  # 手动make
    old_train_function = model.train_function  # 备份旧的训练函数

    # 查找Embedding层
    for output in model.outputs:
        embedding_layer = search_layer(output, embedding_name)
        if embedding_layer is not None:
            break
    if embedding_layer is None:
        raise Exception('Embedding layer not found')

    # 求Embedding梯度
    embeddings = embedding_layer.embeddings  # Embedding矩阵
    gradients = K.gradients(model.total_loss, [embeddings])  # Embedding梯度
    gradients = K.zeros_like(embeddings) + gradients[0]  # 转为dense tensor

    # 封装为函数
    inputs = (model._feed_inputs +
              model._feed_targets +
              model._feed_sample_weights)  # 所有输入层
    embedding_gradients = K.function(
        inputs=inputs,
        outputs=[gradients],
        name='embedding_gradients',
    )  # 封装为函数

    def train_function(inputs):  # 重新定义训练函数
        grads = embedding_gradients(inputs)[0]  # Embedding梯度
        delta = epsilon * grads / (np.sqrt((grads**2).sum()) + 1e-8)  # 计算扰动
        K.set_value(embeddings, K.eval(embeddings) + delta)  # 注入扰动
        outputs = old_train_function(inputs)  # 梯度下降
        K.set_value(embeddings, K.eval(embeddings) - delta)  # 删除扰动
        return outputs

    model.train_function = train_function  # 覆盖原训练函数

if __name__ == '__main__':
    config_path = 'D:/bert_weight_files/bert_config.json'
    checkpoint_path = 'D:/bert_weight_files/bert_model.ckpt'
    class_nums = 11
    build_bert_model(config_path, checkpoint_path, class_nums)

