import logging

from datetime import datetime
from typing import Optional
from pymongo import MongoClient
from app.common.config.connect_database_test import get_database

# 로거 설정
logger = logging.getLogger(__name__)

class VoiceActivity:
    def __init__(self, user_id: int, guild_id: int, channel_id: int, join_time: datetime, leave_time: Optional[datetime] = None):
        self.user_id = user_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.join_time = join_time
        self.leave_time = leave_time

    @staticmethod
    async def record_join(user_id: int, user_name: str, guild_id: int, channel_id: int, channel_name: str):
        db = get_database()
        voice_activities = db.study_sessions  # 컬렉션 이름 맞추기
        
        activity = {
            "user_id": user_id,
            "user_name" : user_name,
            "guild_id": guild_id,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "join_time": datetime.utcnow(),
            "leave_time": None
        }
        try:
            voice_activities.insert_one(activity)
            logger.info("✅ MongoDB insert 성공")
        except Exception as e:
            logger.error(f"❌ MongoDB insert 실패 : {e}")


    @staticmethod
    async def record_leave(user_id: int, guild_id: int, channel_id: int):
        db = get_database()
        voice_activities = db.study_sessions  # 컬렉션 이름을 맞춰줌
        
        # 가장 최근의 입장 기록을 찾아서 퇴장 시간 업데이트
        voice_activities.update_one(
            {
                "user_id": user_id,
                "guild_id": guild_id,
                "channel_id": channel_id,
                "leave_time": None
            },
            {
                "$set": {
                    "leave_time": datetime.utcnow()
                }
            }
        ) 