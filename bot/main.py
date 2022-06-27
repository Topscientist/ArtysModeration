from discord.ext import commands
from discord import Object


bot = commands.Bot()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    bot.load_extension('commands')
    await bot.tree.sync(guild=Object(id="test-guild-id-here"))

bot.run()
