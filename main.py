import os
import threading
import sqlite3
from flask import Flask
import discord
from discord.ext import commands

# Web giữ bot luôn trực tuyến
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot Buff Like Đang Chạy"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
threading.Thread(target=run_web, daemon=True).start()

# Cấu hình sever
GUILD_ID = 10909397193
GUILD_OBJ = discord.Object(id=GUILD_ID)

# Khởi tạo cơ sở dữ liệu lưu tài khoản
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            ten_tk TEXT,
            so_like INTEGER DEFAULT 0,
            vat_pham TEXT DEFAULT 'Huyết Ma',
            luot_con INTEGER DEFAULT 50
        )
    """)
    conn.commit()
    conn.close()
init_db()

# Hàm tạo bảng thông báo giống mẫu
async def gui_buff_thanh_cong(ctx, ten_tk, uid, like_truoc, like_sau, so_like_gui, vat_pham, luot_con):
    embed = discord.Embed(title="Gửi Likes Thành Công", color=discord.Color.green())
    embed.add_field(name="Xin chào", value=f"Bạn đã buff acc: {ten_tk}", inline=False)
    if so_like_gui < 100:
        embed.add_field(name="Thông báo", value=f"Likes gửi chỉ có {so_like_gui} dưới 100 likes, nên bạn không bị trừ vật phẩm.", inline=False)
    embed.add_field(name="Thông Tin Tài Khoản", value=f"Tên: {ten_tk}\nUID: {uid}", inline=False)
    embed.add_field(name="Thông Tin Likes", value=f"{like_truoc} : {like_sau}\nSố likes gửi: {so_like_gui}", inline=False)
    embed.add_field(name="Vật Phẩm Đang Trang Bị", f"{vat_pham}\nLượt còn lại: {luot_con}", inline=False)
    await ctx.send(embed=embed)

# Hàm cấp thêm lượt Huyết Ma
async def cap_luot_huyet_ma(ctx, uid: str, so_luot: int):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    # Kiểm tra tài khoản đã tồn tại chưa
    cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()
    if not user:
        await ctx.send("❌ Không tìm thấy tài khoản này, hãy tạo tài khoản trước!")
        conn.close()
        return
    # Cập nhật số lượt Huyết Ma
    cursor.execute("UPDATE users SET luot_con = luot_con + ? WHERE uid = ?", (so_luot, uid))
    conn.commit()
    cursor.execute("SELECT luot_con FROM users WHERE uid = ?", (uid,))
    luot_moi = cursor.fetchone()[0]
    conn.close()
    await ctx.send(f"✅ Đã cấp thêm {so_luot} lượt Huyết Ma cho UID: {uid}\nTổng lượt hiện tại: {luot_moi}")

# Khởi tạo bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Lệnh buff like
@bot.hybrid_command(name="buff", description="Buff like cho tài khoản game")
async def buff(ctx, uid: str, so_like_gui: int):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    # Kiểm tra tài khoản đã tồn tại chưa
    cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()
    if not user:
        # Tạo tài khoản mới
        ten_tk = "Vô Danh"
        so_like = so_like_gui
        vat_pham = "Huyết Ma"
        luot_con = 50
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (uid, ten_tk, so_like, vat_pham, luot_con))
    else:
        ten_tk = user[1]
        like_truoc = user[2]
        vat_pham = user[3]
        luot_con = user[4]
        if so_like_gui >= 100:
            luot_con -= 1
        like_sau = like_truoc + so_like_gui
        cursor.execute("UPDATE users SET so_like = ?, luot_con = ? WHERE uid = ?", (like_sau, luot_con, uid))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    user_moi = cursor.fetchone()
    like_truoc = user_moi[2] - so_like_gui
    like_sau = user_moi[2]
    vat_pham = user_moi[3]
    luot_con = user_moi[4]
    conn.close()
    await gui_buff_thanh_cong(ctx, user_moi[1], uid, like_truoc, like_sau, so_like_gui, vat_pham, luot_con)

# Lệnh kiểm tra tài khoản
@bot.hybrid_command(name="kiemtra", description="Kiểm tra thông tin tài khoản")
async def kiemtra(ctx, uid: str):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()
    if not user:
        await ctx.send("❌ Không tìm thấy tài khoản này!")
        return
    embed = discord.Embed(title="Thông Tin Tài Khoản", color=discord.Color.blue())
    embed.add_field(name="Tên tài khoản", value=user[1], inline=False)
    embed.add_field(name="UID", value=user[0], inline=False)
    embed.add_field(name="Tổng likes", value=str(user[2]), inline=False)
    embed.add_field(name="Vật phẩm", value=user[3], inline=False)
    embed.add_field(name="Lượt còn lại", value=str(user[4]), inline=False)
    await ctx.send(embed=embed)
    conn.close()

# Lệnh cấp Huyết Ma
@bot.hybrid_command(name="cap_huyet_ma", description="Cấp thêm lượt Huyết Ma cho tài khoản")
async def cap_huyet_ma(ctx, uid: str, so_luot: int):
    await cap_luot_huyet_ma(ctx, uid, so_luot)

# Đồng bộ lệnh slash
@bot.event
async def on_ready():
    print(f"✅ Đã đăng nhập với tài khoản: {bot.user}")
    bot.tree.copy_global_to(guild=GUILD_OBJ)
    await bot.tree.sync(guild=GUILD_OBJ)
    print("✅ Đồng bộ lệnh slash thành công")

# Chạy bot
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
