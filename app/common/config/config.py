# config.py 파일 내에서 .env 파일의 내용 로드 및 환경 변수 관리

import os

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_TEXT_CHANNEL_ID = int(os.getenv("TARGET_TEXT_CHANNEL_ID"))

# 지각사유 채팅채널
LATE_REASON_CHANEL_ID = int(os.getenv("LATE_REASON_CHANEL_ID"))