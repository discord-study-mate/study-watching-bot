# 출석 관련 로직

import logging

from datetime import datetime, time
from typing import Optional

from app.common.config.config import USER_STUDY_SCHEDULES
from app.common.config.connect_database_test import get_database

# 로깅 설정
logger = logging.getLogger(__name__)

class AttendanceStatus:
    PRESENT = "정시출석"
    LATE = "지각"
    ABSENT = "결석"
    TRUANCY = "출튀"

def get_user_schedule(user_name: str, weekday: int) -> Optional[dict]:
    """사용자별 오늘의 스터디 스케쥴 반환"""
    user_schedule = USER_STUDY_SCHEDULES.get(user_name.lower())
    if not user_schedule:
        return None

    return user_schedule.get(weekday)


def is_attendance_time(join_time: datetime, schedule: dict) -> bool:
    """출석 체크 가능한 시간인지 확인"""
    join_time_str = join_time.strftime("%H:%M")
    attendance_start = schedule["attendance_start"]
    attendance_end = schedule["attendance_end"]

    return attendance_start <= join_time_str <= attendance_end


def determine_attendance_status(join_time: datetime, user_name: str) -> Optional[str]:
    """사용자별 출석 상태 판정"""
    current_weekday = join_time.weekday()
    schedule = get_user_schedule(user_name, current_weekday)

    if not schedule:
        return None  # 오늘은 해당 사용자의 스터디 날이 아님

    if not is_attendance_time(join_time, schedule):
        return None  # 출석 체크 시간이 아님

    join_time_str = join_time.strftime("%H:%M")
    standard_end = schedule["standard_end"]

    if join_time_str <= standard_end:
        return AttendanceStatus.PRESENT
    else:  # standard_end < join_time <= attendance_end
        return AttendanceStatus.PRESENT  # 지각허용 시간대도 정시출석으로 처리


async def is_already_recorded_today(user_id: int, date: str) -> bool:
    """오늘 이미 출석 기록이 있는지 확인"""
    db = get_database()
    attendance_records = db.attendance_records

    existing_record = attendance_records.find_one({
        "user_id": user_id,
        "date": date
    })

    return existing_record is not None


async def record_attendance(user_id: int, user_name: str, status: str, join_time: datetime):
    """출석 기록 저장"""
    db = get_database()
    attendance_records = db.attendance_records

    today = join_time.strftime("%Y-%m-%d")

    # 이미 기록된 경우 스킵
    if await is_already_recorded_today(user_id, today):
        logger.info(f"📝 {user_name}님은 오늘 이미 출석 기록이 있습니다.")
        return

    attendance_record = {
        "user_id": user_id,
        "user_name": user_name,
        "date": today,
        "status": status,
        "join_time": join_time,
        "is_pre_notified": False,
        "created_at": datetime.utcnow()
    }

    try:
        attendance_records.insert_one(attendance_record)
        logger.info(f"✅ {user_name}님 출석 기록 저장 완료: {status}")
    except Exception as e:
        logger.error(f"❌ {user_name}님 출석 기록 저장 실패: {e}")