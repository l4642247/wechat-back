from flask import Flask, request, jsonify

app = Flask(__name__)

# 根路由，用于验证部署成功
@app.route('/')
def index():
    return jsonify({'message': 'Deployment successful!'})

# 用于验证 token 的路由
@app.route('/wechat', methods=['GET'])
def verify_token():
    token = 'your_token'  # 将此处的 'your_token' 替换为你在公众号设置中设置的 token
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    # 排序并加密
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = ''.join(tmp_arr)
    import hashlib
    sha1 = hashlib.sha1()
    sha1.update(tmp_str.encode('utf-8'))
    tmp_str = sha1.hexdigest()

    # 对比签名
    if tmp_str == signature:
        return echostr
    else:
        return 'Token verification failed'

# 用于自动回复的路由
@app.route('/wechat', methods=['POST'])
def auto_reply():
    # 从请求中获取用户发送的消息
    message = request.form['xml']

    # 解析用户发送的消息，这里需要根据实际情况进行处理

    # 构造自动回复消息
    reply_message = '<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[Hello]]></Content></xml>'.format(
        message['FromUserName'], message['ToUserName'], int(time.time()))

    # 返回自动回复消息
    return reply_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
