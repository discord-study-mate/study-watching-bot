# 음성 채널 관련 로직

import logging

from datetime import datetime

from app.models.voice_activity import VoiceActivity
from app.handlers.channel_utils import get_user_log_channel, get_movement_message

logger = logging.getLogger(__name__)

async def handle_voice_join(member, after_channel):
    """음성 채널 입장 처리"""
    logger.info(f"{member.name}님이 {after_channel.name} 채널에 입장했습니다.")

    # DB에 저장
    await VoiceActivity.record_join(
        user_id=member.id,
        user_name=member.display_name,
        guild_id=member.guild.id,
        channel_id=after_channel.id,
        channel_name=after_channel.name
    )

    # 개인 채널에 메시지 전송
    log_channel = get_user_log_channel(member.guild, member)
    if log_channel:
        now = datetime.now()
        join_time = now.strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{join_time}] : {member.display_name}님이 '{after_channel.name}' 채널에 입장했습니다."
        await log_channel.send(message)
        logger.info(f"📥 {member.display_name}님 개인 로그 채널({log_channel.name})에 입장 메시지 전송")
    else:
        logger.warning(f"⚠️ {member.display_name}님의 개인 로그 채널을 찾을 수 없습니다.")


async def handle_voice_leave(member, before_channel):
    """음성 채널 퇴장 처리"""
    logger.info(f"{member.name}님이 {before_channel.name} 채널에서 퇴장했습니다.")

    # DB 업데이트
    await VoiceActivity.record_leave(
        user_id=member.id,
        guild_id=member.guild.id,
        channel_id=before_channel.id
    )

    # 개인 채널에 메시지 전송
    log_channel = get_user_log_channel(member.guild, member)
    if log_channel:
        leave_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        message = f"[{leave_time}] : {member.display_name}님이 '{before_channel.name}' 채널에서 나갔습니다."
        await log_channel.send(message)
        logger.info(f"📤 {member.display_name}님 개인 로그 채널({log_channel.name})에 퇴장 메시지 전송")
    else:
        logger.warning(f"⚠️ {member.display_name}님의 개인 로그 채널을 찾을 수 없습니다.")


async def handle_voice_move(member, before_channel, after_channel):
    """음성 채널 이동 처리"""
    logger.info(f"{member.name}님이 {before_channel.name} → {after_channel.name} 채널로 이동했습니다.")

    # 1. 이전 채널에서 나간 것으로 DB 처리
    await VoiceActivity.record_leave(
        user_id=member.id,
        guild_id=member.guild.id,
        channel_id=before_channel.id
    )

    # 2. 새 채널에 들어간 것으로 DB 처리
    await VoiceActivity.record_join(
        user_id=member.id,
        user_name=member.display_name,
        guild_id=member.guild.id,
        channel_id=after_channel.id,
        channel_name=after_channel.name
    )

    # 3. 개인 채널에 메시지 전송
    log_channel = get_user_log_channel(member.guild, member)
    if log_channel:
        now = datetime.now()
        move_time = now.strftime("%Y-%m-%d %H:%M:%S")
        message = get_movement_message(before_channel, after_channel, member, move_time)
        await log_channel.send(message)
        logger.info(f"🔄 {member.display_name}님 개인 로그 채널({log_channel.name})에 이동 메시지 전송")
    else:
        logger.warning(f"⚠️ {member.display_name}님의 개인 로그 채널을 찾을 수 없습니다.")