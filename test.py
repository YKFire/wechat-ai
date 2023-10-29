import SparkApi
#coding=utf9
import requests
import itchat
from itchat.content import *

#以下密钥信息从控制台获取
appid = ""     #填写控制台中获取的 APPID 信息
api_secret = ""   #填写控制台中获取的 APISecret 信息
api_key =""    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    


# if __name__ == '__main__':
#     text.clear
#     while(1):
#         Input = input("\n" +"我:")
#         question = checklen(getText("user",Input))
#         SparkApi.answer =""
#         print("星火:",end = "")
#         SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
#         getText("assistant",SparkApi.answer)
#         # print(str(text))

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
        question = checklen(getText("user",msg['Text']))
        SparkApi.answer =""
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        return SparkApi.answer


@itchat.msg_register(TEXT, isGroupChat=True)
def tuling_reply(msg):
    if msg.isAt:
        question = checklen(getText("user",msg['Text']))
        SparkApi.answer =""
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        msg.user.send(u'@%s %s' % (msg.actualNickName, SparkApi.answer))


# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(enableCmdQR=2)
itchat.run()

