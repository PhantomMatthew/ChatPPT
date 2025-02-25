# 使用官方的 Python 镜像
FROM python:3.12.9-slim-bullseye

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制应用程序代码
COPY . .

#RUN chmod +x src/openai_whisper.py

# 暴露端口
EXPOSE 5000

# 启动应用程序
CMD ["python", "src/openai_whisper.py"]
