import os

# ASR模型配置
ASR_MODEL = os.getenv("ASR_MODEL", "paraformer-zh")
VAD_MODEL = os.getenv("VAD_MODEL", "fsmn-vad")
PUNC_MODEL = os.getenv("PUNC_MODEL", "ct-punc")

# Celery配置
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# API配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# 文件存储配置
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
RESULT_FOLDER = os.getenv("RESULT_FOLDER", "results")
