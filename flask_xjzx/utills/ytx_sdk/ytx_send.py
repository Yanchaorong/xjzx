from .CCPRestSDK import REST
# 需要该自己的信息
accountSid = '8a216da86391c1fa0163a05622a40228'

# 主帐号Token
accountToken = '52deee279d224018bbb4de38b2b165c9'

# 应用Id
appId = '8a216da86391c1fa0163a0562304022f'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def sendTemplateSMS(to,datas, tempId):

    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS('18279690395',{'12','34'}, tempId)
    return result.get('statusCode')