import logging
from flask import Flask, request, jsonify
import hashlib
import xmltodict
from database import save_user_info, log_message

app = Flask(__name__)

# 设置日志级别为INFO
logging.basicConfig(level=logging.INFO)

# 根路由，用于验证部署成功
@app.route('/')
def index():
    
    return jsonify({'message': 'Deployment successful!'})

# 设置你的Token，用于验证微信服务器发送的请求
TOKEN = "one"

def handle_text_message(msg_dict):
    try:
        content = msg_dict['Content']
        reply = {
            'ToUserName': msg_dict['FromUserName'],
            'FromUserName': msg_dict['ToUserName'],
            'CreateTime': msg_dict['CreateTime'],
            'MsgType': 'text',
            'Content': f"You said: {content}"
        }
        log_message(msg_dict['FromUserName'], msg_dict, reply)
        return xmltodict.unparse({'xml': reply}, pretty=True)
    except Exception as e:
            app.logger.error("Error handling text message: %s", e)
            return 'success'

def handle_subscribe_event(msg_dict):
    try:
        openid = msg_dict['FromUserName']
        # 保存用户信息到MySQL数据库
        save_user_info(openid)

        reply = {
            'ToUserName': openid,
            'FromUserName': msg_dict['ToUserName'],
            'CreateTime': msg_dict['CreateTime'],
            'MsgType': 'text',
            'Content': "欢迎关注！"
        }
        log_message(msg_dict['FromUserName'], msg_dict, reply)
        return xmltodict.unparse({'xml': reply}, pretty=True)
    except Exception as e:
            app.logger.error("Error handling subscribe event: %s", e)
            return 'success'

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
            app.logger.error("Invalid signature")
            return 'Invalid signature', 403
    elif request.method == 'POST':
        # 处理接收到的消息
        try:
            data = request.data
            msg_dict = xmltodict.parse(data)['xml']
            msg_type = msg_dict['MsgType']
            if msg_type == 'text':
                return handle_text_message(msg_dict)
            elif msg_type == 'event':
                event = msg_dict['Event']
                if event == 'subscribe':
                    return handle_subscribe_event(msg_dict)
                else:
                    app.logger.error("Unsupported message type: %s", msg_type)
                    return 'success'
        except Exception as e:
            app.logger.error("Error handling message: %s", e)
            return 'success'       
    else:
        # 处理其他类型消息
        # 在这里添加你需要处理的其他类型消息的代码
        return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
