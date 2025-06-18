# 채널 유틸리티 함수들

import logging

logger = logging.getLogger(__name__)

def get_user_log_channel(guild, member):
    """사용자의 개인 로그 채널을 자동으로 찾기"""
    possible_names = [
        f"{member.name}-출석-로그",
        f"{member.display_name}-출석-로그",
        f"{member.name.lower()}-출석-로그",
        f"{member.display_name.lower()}-출석-로그"
    ]

    for channel in guild.text_channels:
        if channel.name in possible_names:
            return channel
    return None

def get_movement_message(before_channel, after_channel, member, move_time):
    """채널 이동에 따른 메시지 생성"""

    # 1. 메인 공부방 -> 생각의 방 (출튀)
    if before_channel.name == "메인 공부방" and after_channel.name == "생각의 방":
        return f"[{move_time}] : {member.display_name}님이 '{before_channel.name}'에서 '{after_channel.name}' 채널로 이동했습니다. (🚨출튀 감지🚨)"

    # 2. 생각의 방 -> 메인 공부방 (복귀)
    elif before_channel.name == "생각의 방" and after_channel.name == "메인 공부방":
        return f"[{move_time}] : {member.display_name}님이 '{before_channel.name}'에서 '{after_channel.name}' 채널로 복귀했습니다. (✅복귀 완료✅)"

    # 3. 기타 이동
    else:
        return f"[{move_time}] : {member.display_name}님이 '{before_channel.name}'에서 '{after_channel.name}' 채널로 이동했습니다."