# config.py 파일 내에서 .env 파일의 내용 로드 및 환경 변수 관리

import os

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# TARGET_TEXT_CHANNEL_ID = int(os.getenv("TARGET_TEXT_CHANNEL_ID"))

# 음성채널 입장/퇴장 로그 -> 채팅에 남길 로그 기록
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", 0))  # 추가

# 지각/결석 사유 제출 방
REASON_SUBMIT_CHANNEL_ID = int(os.getenv("REASON_SUBMIT_CHANNEL_ID", 0))  # 추가

# 출석 설정
USER_STUDY_SCHEDULES = {
    "juni": {
        5: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 토요일
        6: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 일요일
    },
    "앵웅": {
        0: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 월요일
        1: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 화요일
        2: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 수요일
        3: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 목요일
    },
    "가가원": {
        5: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 토요일
        6: {"attendance_start": "12:00", "attendance_end": "14:15", "standard_end": "14:00"},  # 일요일
    }
}