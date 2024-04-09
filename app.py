import logging
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# 配置日志记录器
logging.basicConfig(filename='wechat.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 根路由，用于验证部署成功
@app.route('/')
def index():
    return jsonify({'message': 'Deployment successful!'})

# 用于验证 token 的路由
@app.route('/wechat', methods=['GET'])
def verify_token():
    token = 'one'  # 将此处的 'your_token' 替换为你在公众号设置中设置的 token
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
     # 打印日志：接收到微信消息
    logging.info('Received message from WeChat.')
    
    # 从请求中获取用户发送的消息
    message = request.form['xml']

    # 解析用户发送的消息，这里需要根据实际情况进行处理

    # 获取用户发送的消息内容
    user_message = message['Content'].strip()

    # 如果用户发送的消息是问号，则返回帮助信息
    if user_message == '?':
        # 打印日志：用户请求帮助信息
        logging.info('User requested help message.')
        
        help_message = '欢迎使用我们的服务！\n\n您可以输入以下指令来获取相关信息：\n1. 输入 "帮助" 获取帮助信息\n2. 输入其他内容获取相应的服务'
        reply_message = generate_reply_message(message, help_message)
    else:
        # 打印日志：用户发送其他消息
        logging.info('User sent message: %s', user_message)
        
        # 构造自动回复消息，这里需要根据实际情况进行处理
        reply_message = generate_reply_message(message, 'Hello')

    # 返回自动回复消息
    return reply_message

def generate_reply_message(message, content):
    # 构造自动回复消息
    reply_message = '<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{}]]></Content></xml>'.format(
        message['FromUserName'], message['ToUserName'], int(time.time()), content)
    return reply_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
