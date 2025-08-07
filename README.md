# FunASR 本地部署项目

基于FunASR的语音识别服务，支持通过Docker构建和部署，提供异步处理识别任务的API。

## 功能特性

- 基于FunASR的中文语音识别
- 支持异步处理长时间音频文件
- 提供RESTful API接口
- 提供简单的Web UI界面
- 支持Docker容器化部署
- 使用Redis作为任务队列后端

## 项目结构

```
.
├── asr_service.py      # ASR服务实现
├── config.py           # 配置文件
├── Dockerfile          # Docker构建文件
├── docker-compose.yml  # Docker Compose配置
├── main.py             # FastAPI应用入口
├── requirements.txt    # Python依赖
├── tasks.py            # Celery任务定义
├── templates/          # Web页面模板
│   └── index.html      # 主页
├── uploads/            # 上传文件目录（运行时创建）
└── results/            # 结果文件目录（运行时创建）
```

## 环境要求

- Docker
- Docker Compose

## 快速开始

1. 克隆项目代码：
   ```bash
   git clone <repository-url>
   cd my_funasr
   ```

2. 使用Docker Compose启动服务：
   ```bash
   docker-compose up -d
   ```

3. 访问应用：
   - Web UI: http://localhost:8000
   - API文档: http://localhost:8000/docs

## API接口

### 1. 上传音频文件并启动转录

```
POST /transcribe/
```

**参数:**
- `file`: 音频文件（WAV, MP3, FLAC等格式）

**响应:**
```json
{
  "task_id": "任务ID",
  "status": "Processing",
  "message": "Transcription task started successfully"
}
```

### 2. 获取任务状态和结果

```
GET /task/{task_id}
```

**响应:**
```json
{
  "task_id": "任务ID",
  "status": "SUCCESS",
  "result": {
    "text": "转录文本内容"
  }
}
```

## Web UI使用

1. 打开浏览器访问 http://localhost:8000
2. 点击"选择文件"按钮上传音频文件
3. 点击"开始转录"按钮
4. 等待转录完成，结果将显示在页面上

## 开发指南

### 本地开发环境

1. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动Redis服务器（需要单独安装Redis）

3. 启动Celery工作进程：
   ```bash
   celery -A tasks.celery_app worker --loglevel=info
   ```

4. 启动FastAPI应用：
   ```bash
   python main.py
   ```

### 配置说明

可以在`config.py`中修改以下配置：

- `ASR_MODEL`: ASR模型名称（默认：paraformer-zh）
- `VAD_MODEL`: VAD模型名称（默认：fsmn-vad）
- `PUNC_MODEL`: 标点模型名称（默认：ct-punc）
- `CELERY_BROKER_URL`: Celery消息代理URL
- `CELERY_RESULT_BACKEND`: Celery结果后端URL
- `API_HOST`: API服务监听地址
- `API_PORT`: API服务端口
- `UPLOAD_FOLDER`: 上传文件存储目录
- `RESULT_FOLDER`: 结果文件存储目录

## Docker部署

### 构建镜像

```bash
docker build -t funasr-api .
```

### 运行容器

```bash
docker run -d -p 8000:8000 --name funasr-api funasr-api
```

注意：单独运行容器时需要链接到Redis服务。

## 许可证

本项目基于FunASR，遵循相应的开源许可证。
