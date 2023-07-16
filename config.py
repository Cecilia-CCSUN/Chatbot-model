#!/usr/bin/env python
# encoding: utf-8

# 注意，这里每一个意图下都有"Disease"这个槽位
# 只要在最开始将该槽位填充后，后面就可以不断的就填充的槽值进行多轮对话
# 因为槽位填充的逻辑里面有一个是获取上一步的槽值
semantic_slot = {
    "属于":{
        "slot_list":["entity"],
        "slot_values":None,
        "cql_template": "MATCH(p:Entity)-[r:categories]->(q) WHERE p.entity='{entity}' RETURN p.entity,q.level3",
        "reply_template": "'{entity}'属于的三级文明模式是：\n",
        "ask_template": "您问的是 '{entity}' 属于哪种三级生态文明模式吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },

    "地址":{
        "slot_list" : ["entity"],
        "slot_values":None,
        "cql_template" : "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN p.entity,p.address",
        "reply_template" : "'{entity}' 的地址在：\n",
        "ask_template" : "您问的是实例 '{entity}' 的地址吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "基本信息":{
        "slot_list" : ["entity"],
        "slot_values":None,
        "cql_template" : "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN p.entity,p.address, p.rainfall, p.soil, p.climate, p.productivity, p.altitude, p.landscape",
        "reply_template" : "'{entity}' 的基本信息有：\n",
        "ask_template" : "请问您问的是实例 '{entity}' 的基本信息吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~"
    },

    "资源丰富程度": {
        "slot_list": ["entity"],
        "slot_values": None,
        "cql_template": "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN p.entity, p.arable, p.grassland, p.perwater, p.forest",
        "reply_template": "'{entity}' 的资源丰富程度：\n",
        "ask_template": "请问您问的是实例 '{Entity}' 的资源丰富程度吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },

    "经济发达程度": {
        "slot_list": ["entity"],
        "slot_values": None,
        "cql_template": "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN  p.entity, p.GDP, p.perGDP, p.permoney, p.twoGDP, p.threeGDP",
        "reply_template": "'{entity}' 的资源丰富程度：\n",
        "ask_template": "请问您问的是实例 '{entity}' 的经济发达程度吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },

    "环境友好程度": {
        "slot_list": ["entity"],
        "slot_values": None,
        "cql_template": "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN  p.entity, p.waterquality, p.reosion, p.habitat, p.reserve, p.disasters",
        "reply_template": "'{entity}' 的环境友好程度：\n",
        "ask_template": "请问您问的是实例 '{entity}' 的环境友好程度吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },

    "社会发展程度": {
        "slot_list": ["entity"],
        "slot_values": None,
        "cql_template": "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN  p.entity,p.density, p.medical,p.travel",
        "reply_template": "'{entity}' 的社会发展程度：\n",
        "ask_template": "请问您问的是实例 '{entity}' 的社会发展程度吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },

    "文化信息": {
        "slot_list": ["entity"],
        "slot_values": None,
        "cql_template": "MATCH(p:Entity) WHERE p.entity='{entity}' RETURN  p.national, p.dialect, p.culture, p.culnum, p.cultype",
        "reply_template": "'{entity}' 的文化信息有：\n",
        "ask_template": "请问您问的是实例 '{entity}' 的文化信息吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },
    "属于": {
        "slot_list": ["level3"],
        "slot_values": None,
        "cql_template": "MATCH(p:Level3)-[r:belongsto]->(q) WHERE p.name='{level3}' RETURN p.level3,q.level2",
        "reply_template": "'{level3}'属于的二级文明模式是：\n",
        "ask_template": "您问的是 '{level3}' 属于哪种二级生态文明模式吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },
    "属于": {
        "slot_list": ["level2"],
        "slot_values": None,
        "cql_template": "MATCH(p:Level2)-[r:belongsto]->(q) WHERE p.level2='{level2}' RETURN p.level2,q.level1",
        "reply_template": "'{level2}'属于的一级文明模式是：\n",
        "ask_template": "您问的是 '{level2}' 属于哪种一级生态文明模式吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },

    "分类": {
        "slot_list": ["level2"],
        "slot_values": None,
        "cql_template": "MATCH(p:Level2)-[r:has]->(q) WHERE p.level2='{level2}' RETURN p.level2,q.level3",
        "reply_template": "'{level2}'的分类有：\n",
        "ask_template": "您问的是 '{level2}' 的分类有哪些吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },

    "分类": {
        "slot_list": ["level1"],
        "slot_values": None,
        "cql_template": "MATCH(p:Level1)-[r:has]->(q) WHERE p.level1='{level1}' RETURN p.level1,q.level2",
        "reply_template": "'{level1}'的分类有：\n",
        "ask_template": "您问的是 '{level1}' 的分类有哪些吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },

    "实例": {
        "slot_list": ["level3"],
        "slot_values": None,
        "cql_template": "MATCH(p:Level3)-[r:instantiates]->(q) WHERE p.level3='{level3}' RETURN p.level3,q.entity",
        "reply_template": "'{level3}'的分类有：\n",
        "ask_template": "您问的是 '{level3}' 的实例具体有？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },

    "unrecognized":{
        "slot_values":None,
        "replay_answer" : "非常抱歉，我还不知道如何回答您，我正在努力学习中~",
    }
}

intent_threshold_config = {
    "accept":0.8,
    "deny":0.4
}

default_answer = """抱歉我还不知道回答你这个问题\n
                    你可以问我一些有关美丽中国生态文明模式的问题\n
                    实例的基本信息、资源丰富程度、经济发达程度、环境友好程度、社会发展程度、文化信息\n
                    一、二、三级生态文明模式的分类~
                    """

chitchat_corpus = {
    "greet":[
        "hi",
        "你好呀",
        "我是智能机器人，有什么可以帮助你吗",
        "hi，你好，你可以叫我小智",
        "你好，你可以问我一些关于美丽中国生态文明模式的问题哦"
    ],
    "goodbye":[
        "再见，很高兴为您服务",
        "bye",
        "再见，感谢使用我的服务",
        "再见啦！"
    ],
    "deny":[
        "很抱歉没帮到您",
        "I am sorry",
        "那您可以试着问我其他问题哟"
    ],
    "isbot":[
        "我是小智，你的智能机器人",
        "你可以叫我小智哦~",
        "我是机器人小智"
    ]
}
