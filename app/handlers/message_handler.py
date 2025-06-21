# 지각 사유 제출 로직

import re
import logging

from datetime import datetime

from app.common.config.connect_database_test import get_database

logger = logging.getLogger(__name__)


async def handle_attendance_message(message):
    """지각/결석 사유 제출 채널에서의 메시지 처리"""
    content = message.content.strip()

    # 패턴 매칭
    patterns = [
        r'^지각\s+(\d+분|\d{1,2}:\d{2})\s+(.+)$',  # "지각 30분 병원진료"
        r'^결석\s+(.+)$',  # "결석 가족행사"
        r'^정시출석?$',  # "정시출석" 또는 "정시"
    ]

    for pattern in patterns:
        match = re.match(pattern, content)
        if match:
            await process_attendance_notification(message, match)
            return

    # 패턴이 안 맞으면 도움말 전송
    await send_help_message(message)


async def process_attendance_notification(message, match):
    """매칭된 패턴에 따라 출석 신고 처리"""
    content = message.content.strip()
    user = message.author

    try:
        if content.startswith('지각'):
            time_info = match.group(1)
            reason = match.group(2)

            await save_attendance_notification(
                user_id=user.id,
                user_name=user.display_name,
                notification_type="late",
                time_info=time_info,
                reason=reason
            )

            await message.reply(f"✅ 지각 신고가 접수되었습니다.\n⏰ 예상시간: {time_info}\n📝 사유: {reason}")

        elif content.startswith('결석'):
            reason = match.group(1)

            await save_attendance_notification(
                user_id=user.id,
                user_name=user.display_name,
                notification_type="absent",
                reason=reason
            )

            await message.reply(f"✅ 결석 신고가 접수되었습니다.\n📝 사유: {reason}")

        elif content.startswith('정시'):
            await save_attendance_notification(
                user_id=user.id,
                user_name=user.display_name,
                notification_type="normal"
            )

            await message.reply("✅ 정시 출석으로 신고되었습니다.")

    except Exception as e:
        logger.error(f"출석 신고 처리 중 오류: {e}")
        await message.reply("❌ 신고 처리 중 오류가 발생했습니다. 다시 시도해주세요.")


async def save_attendance_notification(user_id, user_name, notification_type, time_info=None, reason=None):
    """출석 신고를 DB에 저장"""
    try:
        db = get_database()
        notifications = db.attendance_notifications

        today = datetime.now().strftime("%Y-%m-%d")

        notification_data = {
            "user_id": user_id,
            "user_name": user_name,
            "date": today,
            "type": notification_type,
            "created_at": datetime.utcnow(),
            "is_processed": False
        }

        if time_info:
            notification_data["time_info"] = time_info
        if reason:
            notification_data["reason"] = reason

        notifications.update_one(
            {"user_id": user_id, "date": today},
            {"$set": notification_data},
            upsert=True
        )

        logger.info(f"✅ {user_name}님의 출석 신고 저장 완료: {notification_type}")

    except Exception as e:
        logger.error(f"❌ 출석 신고 저장 실패: {e}")
        raise e


async def send_help_message(message):
    help_text = """
📝 **출석 사전 신고 방법**

✅ **정시 출석**: `정시출석`
🟡 **지각 예정**: `지각 [시간] [사유]`
   예: `지각 30분 병원진료`
   예: `지각 14:30 교통체증`
🔴 **결석 예정**: `결석 [사유]`
   예: `결석 가족행사`

💡 간단하게 입력하시면 자동으로 처리됩니다!
    """
    await message.reply(help_text)