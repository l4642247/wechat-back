# 使用官方 Python 3.12 基础镜像
FROM python:3.12

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录下
COPY . /app

# 创建虚拟环境
RUN python3 -m venv /app/venv

# 激活虚拟环境
ENV PATH="/app/venv/bin:$PATH"

# 更新pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制
COPY requirements.txt .

# 安装 Flask 和其它依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口 80
EXPOSE 80

# 定义环境变量
ENV FLASK_APP app.py

# 运行应用程序
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
