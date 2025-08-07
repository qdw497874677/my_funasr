import os
import uuid
from funasr import AutoModel
from config import ASR_MODEL, VAD_MODEL, PUNC_MODEL, RESULT_FOLDER
import logging

# 创建结果文件夹
os.makedirs(RESULT_FOLDER, exist_ok=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ASRService:
    def __init__(self):
        """
        初始化ASR服务
        """
        logger.info("Initializing ASR model...")
        try:
            self.model = AutoModel(
                model=ASR_MODEL,
                vad_model=VAD_MODEL,
                punc_model=PUNC_MODEL
            )
            logger.info("ASR model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ASR model: {e}")
            raise

    def transcribe(self, audio_file_path: str) -> dict:
        """
        转录音频文件
        :param audio_file_path: 音频文件路径
        :return: 转录结果
        """
        try:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            # 执行语音识别
            result = self.model.generate(
                input=audio_file_path,
                batch_size_s=300,
                hotword='魔搭'
            )
            
            # 处理结果
            if isinstance(result, list) and len(result) > 0:
                transcription = result[0] if isinstance(result[0], dict) else {"text": str(result[0])}
            else:
                transcription = {"text": str(result)}
                
            logger.info("Transcription completed successfully")
            return transcription
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return {"error": str(e)}

    def save_result(self, task_id: str, result: dict) -> str:
        """
        保存转录结果到文件
        :param task_id: 任务ID
        :param result: 转录结果
        :return: 结果文件路径
        """
        try:
            result_file_path = os.path.join(RESULT_FOLDER, f"{task_id}.json")
            import json
            with open(result_file_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result_file_path
        except Exception as e:
            logger.error(f"Error saving result: {e}")
            raise

# 全局ASR服务实例
asr_service = ASRService()
