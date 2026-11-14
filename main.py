import discord
from discord.ext import commands
# ID server của bạn
GUILD_ID = 10909397193
GUILD_OBJ = discord.Object(id=GUILD_ID)
# Biến đếm tổng phản ứng
tong_like = 0
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.hybrid_command(name="bufflike", description="Thêm phản ứng đếm số lượt")
async def bufflike(ctx):
    global tong_like
    # Kiểm tra đúng server
    if not ctx.guild or ctx.guild.id != GUILD_ID:
        await ctx.send("❌ Chỉ dùng trong sever này thôi!")
        return
    emoji_list = ["❤️", "👍", "🔥", "😂", "🥳"]
    so_luot = len(emoji_list)
    for emo in emoji_list:
        await ctx.message.add_reaction(emo)
    tong_like += so_luot
    await ctx.send(f"✅ Đã buff thêm {so_luot} lượt! Tổng: {tong_like}")

@bot.hybrid_command(name="kiemtra", description="Xem tổng phản ứng đã buff")
async def kiemtra(ctx):
    await ctx.send(f"📊 Tổng số phản ứng: {tong_like}")
# Đồng bộ lệnh slash
@bot.event
sync def on_ready():
     print(f"✅ Đã đăng nhập với tài khoản: {bot.user}")
     bot.tree.copy_global_to(guild=GUILD_OBJ)
     await bot.tree.sync(guild=GUILD_OBJ)
     print("✅ Đồng bộ lệnh slash thành công")
 # Chạy bot
 TOKEN = os.environ.get("DISCORD_TOKEN")
 bot.run(TOKEN)
