# ID số nguyên của sever (để kiểm tra quyền)
GUILD_ID = 10909397193
# Đối tượng để đồng bộ lệnh slash
GUILD_OBJ = discord.Object(id=GUILD_ID)
# Dùng hybrid để vừa có !bufflike vừa có /bufflike
@bot.hybrid_command(name="bufflike", description="Thêm phản ứng cho tin nhắn")
async def bufflike(ctx, amount: int = 200):
    if not ctx.guild or ctx.guild.id != GUILD_ID:
        await ctx.send("❌ Chỉ dùng trong sever Việt Nam đã cài đặt!")
        return
    for emo in ["❤️", "👍", "🔥"]:
        await ctx.message.add_reaction(emo)
    await ctx.send("✅ Bot đã thêm phản ứng")
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.tree.copy_global_to(guild=GUILD_OBJ)
    await bot.tree.sync(guild=GUILD_OBJ)
    print("✅ Đã đồng bộ lệnh slash cho sever")
