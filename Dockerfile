# 使用官方 Python 3 基础镜像
FROM python:3

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录下
COPY . /app

# 安装 Flask 和其它依赖包
RUN pip install --requirement requirements.txt

# 暴露端口 80
EXPOSE 80

# 定义环境变量
ENV FLASK_APP app.py

# 运行应用程序
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
