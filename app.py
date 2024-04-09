from flask import Flask, request, jsonify
import hashlib
import xmltodict

app = Flask(__name__)

# 根路由，用于验证部署成功
@app.route('/')
def index():
    return jsonify({'message': 'Deployment successful!'})

# 设置你的Token，用于验证微信服务器发送的请求
TOKEN = "one"

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证服务器地址有效性
        token = request.args.get('token', '')
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')

        # 排序后进行sha1加密
        sorted_params = ''.join(sorted([TOKEN, timestamp, nonce]))
        sha1 = hashlib.sha1()
        sha1.update(sorted_params.encode())
        hashcode = sha1.hexdigest()

        # 对比加密后的结果和微信发送的signature，如果一致则返回echostr，验证成功
        if hashcode == signature:
            return echostr
        else:
            return 'Invalid signature', 403
    elif request.method == 'POST':
        # 处理接收到的消息
        data = request.data
        msg_dict = xmltodict.parse(data)['xml']
        msg_type = msg_dict['MsgType']
        if msg_type == 'text':
            # 处理文本消息
            content = msg_dict['Content']
            reply = {
                'ToUserName': msg_dict['FromUserName'],
                'FromUserName': msg_dict['ToUserName'],
                'CreateTime': msg_dict['CreateTime'],
                'MsgType': 'text',
                'Content': f"You said: {content}"
            }
            # 将回复消息转换为XML格式
            reply_xml = xmltodict.unparse({'xml': reply}, pretty=True)
            return reply_xml
        else:
            # 处理其他类型消息
            # 在这里添加你需要处理的其他类型消息的代码
            return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
