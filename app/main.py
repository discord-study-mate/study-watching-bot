import discord, asyncio, logging

from datetime import datetime, timedelta

from app.common.config.config import DISCORD_TOKEN, LOG_CHANNEL_ID
from app.common.config.connect_database_test import test_connection
from app.models.voice_activity import VoiceActivity

# Gateway Intents 설정
intents = discord.Intents.default()

intents.messages = True  # 메시지 관련 이벤트를 처리하려면 활성화
intents.message_content = True   # 메시지 내용 접근 권한 활성화
intents.voice_states = True  # 음성 상태 변경 이벤트 활성화

client = discord.Client(intents=intents)

# 로거 설정
logger = logging.getLogger(__name__)

# 봇의 상태 메시지
# 봇이 한번 실행되면 계속 실행됨
@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user}")
    asyncio.create_task(client.change_presence(status=discord.Status.online))  # 임시 작성된 코드
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("개발 테스트")
    )

    # DB 연결 테스트
    # DB 는 기존 RDS 에서 MongoDB 활용할 예정
    try:
        test_connection()  # DB 연결 테스트 실행 -> MongoDB Atlas 연결 설정 후 실행할 것
        logger.info("✅ DB에 성공적으로 연결되었습니다.")

    except Exception as e:
        logger.error(f"❌ DB 연결에 실패했습니다. : {e}")

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # 로그 채널 가져오기
    log_channel = client.get_channel(LOG_CHANNEL_ID)

    # 음성 채널 입장
    if before.channel is None and after.channel is not None:
        logger.info(f"{member.name}님이 {after.channel.name} 채널에 입장했습니다.")

        # DB 에 저장
        await VoiceActivity.record_join(
            user_id=member.id,
            user_name=member.display_name,
            guild_id=member.guild.id,
            channel_id=after.channel.id,
            channel_name=after.channel.name  # 추가
        )

        # 채널에 메시지 전송
        if log_channel:
            now = datetime.now()
            join_time = now.strftime("%Y-%m-%d %H:%M:%S")
            message = f"{member.display_name}님이 '{after.channel.name}' 채널에 {join_time}에 입장했습니다."
            await log_channel.send(message)

    # 음성 채널 퇴장
    elif before.channel is not None and after.channel is None:
        logger.info(f"{member.name}님이 {before.channel.name} 채널에서 퇴장했습니다.")

        # DB 업데이트
        await VoiceActivity.record_leave(
            user_id=member.id,
            guild_id=member.guild.id,
            channel_id=before.channel.id
        )

        # 채널에 메시지 전송
        if log_channel:
            leave_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 밀리초 포함
            message = f"{member.display_name}님이 '{before.channel.name}' 채널에서 나갔습니다. (퇴장 시간: {leave_time})"
            await log_channel.send(message)

# 봇 종료 처리
@client.event
async def on_disconnect():
    logger.info("디스코드 봇 연결이 종료되었습니다.")

@client.event
async def on_resumed():
    logger.info("디스코드 연결이 성공적으로 복구되었습니다.")

# 봇 실행
if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info("⚙️ 봇 실행 준비 중...")
    
    client.run(DISCORD_TOKEN)