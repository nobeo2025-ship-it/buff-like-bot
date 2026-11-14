@bot.command()
async def bufflike(ctx,amount: int = 200)
    for emo in ["❤️", "👍", "🔥"]:
        await ctx.message.add_reaction(emo)
    await ctx.send("✅ Bot đã thêm phản ứng cho tin nhắn")

