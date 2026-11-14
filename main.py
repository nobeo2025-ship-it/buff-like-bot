async def bang_nhan_huyet_ma(ctx, uid, tong_luot):
    embed = discord.Embed(
        title = "Đã Nhận Được Huyết Ma 🦋",
        color = discord.Color.purple()
    )
    embed.add_field(name = "UID tài khoản", value = f"`{uid}`", inline = False)
    embed.add_field(name = "Tổng lượt Huyết Ma", value = f"`{tong_luot}`", inline = False)
    embed.set_footer(text = "Hệ thống buff like")
    await ctx.send(embed = embed)
    await bang_nhan_huyet_ma(ctx, "10909397193", "999999")

