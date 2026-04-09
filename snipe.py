import discord
from discord.ext import commands
from collections import defaultdict, deque
from datetime import timezone, timedelta

MAX_SNIPES = 10
ICT = timezone(timedelta(hours=7))


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cache = defaultdict(lambda: deque(maxlen=MAX_SNIPES))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return

        self._cache[message.channel.id].append({
            "author": message.author,
            "content": message.content,
            "attachments": message.attachments,
            "deleted_at": discord.utils.utcnow(),
        })

    @commands.command()
    async def snipe(self, ctx):
        cache = self._cache.get(ctx.channel.id)
        if not cache:
            await ctx.reply("Không có tin nhắn bị xoá gần đây.", mention_author=False)
            return

        record = cache[-1]
        time = record["deleted_at"].astimezone(ICT).strftime("%H:%M:%S %d/%m/%Y")
        content = record["content"] or "*Không có nội dung văn bản*"

        msg = f"<a:mfz_here1:1421442489960894475> Tin nhắn bị xóa bởi **{record['author']}** vào lúc *{time}*\n───────────────────────\n{content}"
        if record["attachments"]:
            msg += "\n" + "\n".join(a.url for a in record["attachments"])

        await ctx.reply(msg, mention_author=False)


async def setup(bot):
    await bot.add_cog(Snipe(bot))