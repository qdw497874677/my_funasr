from celery import Celery
from asr_service import asr_service
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import logging
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Celery实例
celery_app = Celery(
    "asr_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# 配置Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

@celery_app.task(bind=True)
def transcribe_audio_task(self, audio_file_path: str, task_id: str) -> dict:
    """
    异步转录音频文件的Celery任务
    :param self: Celery任务实例
    :param audio_file_path: 音频文件路径
    :param task_id: 任务ID
    :return: 转录结果
    """
    try:
        logger.info(f"Starting transcription task {task_id} for file: {audio_file_path}")
        
        # 更新任务状态
        self.update_state(state="PROGRESS", meta={"status": "Transcribing audio..."})
        
        # 执行转录
        result = asr_service.transcribe(audio_file_path)
        
        # 保存结果
        result_file_path = asr_service.save_result(task_id, result)
        result["result_file_path"] = result_file_path
        
        logger.info(f"Transcription task {task_id} completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in transcription task {task_id}: {e}")
        return {"error": str(e)}
