 import requests
import os

@bot.command()
async def bufflike(ctx, uid: str):
    api = os.environ.get("BUFF_API") # lấy API từ Render
    # gọi API
    r = requests.get(f"{api}&uid={uid}")
    if r.status_code == 200:
        await ctx.send(f"✅ Đã buff like cho UID {uid} rồi nha!")
    else:
        await ctx.send("❌ API lỗi rồi, báo chủ bot đi!")
        https://api-tenweb.com/bufflike?uid=123456&key=API_CUA_BA
