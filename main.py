from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from celery import uuid
from tasks import transcribe_audio_task
import os
import uuid as uuid_lib
from config import API_HOST, API_PORT, UPLOAD_FOLDER
import logging

# 创建上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(
    title="FunASR API",
    description="基于FunASR的语音识别API，支持异步处理",
    version="1.0.0"
)

# 读取HTML模板
def get_html_template():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>欢迎使用FunASR语音识别API</h1><p>请使用API接口进行语音识别</p>"

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    根路径，返回HTML页面
    """
    html_content = get_html_template()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    上传音频文件并启动异步转录任务
    :param file: 上传的音频文件
    :return: 任务ID和状态信息
    """
    try:
        logger.info(f"Received transcription request for file: {file.filename}")
        
        # 生成唯一的任务ID
        task_id = uuid()
        
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid_lib.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存上传的文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File saved to: {file_path}")
        
        # 启动异步转录任务
        transcribe_audio_task.delay(file_path, task_id)
        
        return JSONResponse(
            status_code=202,
            content={
                "task_id": task_id,
                "status": "Processing",
                "message": "Transcription task started successfully"
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing transcription request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    获取任务状态和结果
    :param task_id: 任务ID
    :return: 任务状态和结果
    """
    try:
        logger.info(f"Checking status for task: {task_id}")
        
        # 获取任务结果
        task = transcribe_audio_task.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            # 任务还在等待中
            response = {
                "task_id": task_id,
                "status": task.state,
                "message": "Task is waiting to be processed"
            }
        elif task.state == 'PROGRESS':
            # 任务正在进行中
            response = {
                "task_id": task_id,
                "status": task.state,
                "message": task.info.get('status', '')
            }
        elif task.state == 'SUCCESS':
            # 任务成功完成
            response = {
                "task_id": task_id,
                "status": task.state,
                "result": task.result
            }
        else:
            # 任务失败
            response = {
                "task_id": task_id,
                "status": task.state,
                "error": str(task.info)
            }
        
        return JSONResponse(status_code=200, content=response)
        
    except Exception as e:
        logger.error(f"Error checking task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
