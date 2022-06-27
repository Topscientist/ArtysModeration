from configParser import ConfigParser
from discord.ext import commands
from json import load as json_load
from requests import get
import random
from discord import (
    Interaction,
    app_commands,
    Object,
    Message,
    Embed
)

config: ConfigParser = ConfigParser().read("PATH-TO-CONFIG.conf")


class CommandsCog(commands.Cog):
    def __init__(self: "CommandsCog", bot: commands.Bot) -> None:
        self.bot: commands.bot = bot
        self.guild_settings = {}

        with open("lists.json", "r") as f:
            self.lists = json_load(f)


    @commands.Cog.listener()
    async def on_message(self: "CommandsCog", msg: Message) -> None:
        """
         | params
         | ======
         |
         | :self: this parameter is passed by defult by the python programing language.
         | :msg:  this paramiter is `Message` object passed by the discord.py libruary.
         | 
         | point of listener
         | =================
         |
         | This listener will listen for posotive and negitive words and respond with
         | an apropriate action.
        """

        # we don't need the bot to analyse the bot for it's own use of language unless the bot is having a bad day
        if msg.author.bot: return

        # this is effectively the same as the previous implimentation
        if self.guild_settings[msg.guild.id]["profan"] and sum(word.lower() in msg.content.lower() for word in self.lists["profanity-words"]):
            await msg.delete() # better to remove the message directely instead of removing the latest one

            await msg.channel.send(
                embed=Embed(
                    title="Mmmmm, automod",
                    description=f"The word that you have used in your message has been dissalowed in the server you are in,\njust make shure not to say that again {message.author.mention}"
                )
            )

        elif self.guild_settings[msg.guild.id]["quote"] and sum(word.lower() in msg.content.lower() for word in self.lists["sad-words"]):
            q = get_quote()
            await msg.chanel.send(
                embed=Embed(
                    title=q["q"],
                    description=q["a"]
                )
            )


    @app_commands.command()
    async def topic(self: "CommandsCog", ctx: Interaction) -> None:
        await ctx.response.send_message(
            embed=Embed(
                tite=f"{ctx.user.mention} requested a topic",
                description="you can also request a topic with `/topic`"
            ).add_filed(
                name="topic",
                value=random.choice(self.lists["topics"])
            )
        )


    @app_commands.command()
    async def github(self: "CommandsCog", ctx: Interaction) -> None:
        await ctx.response.send_message(
            embed=Embed(
                title="github",
                description="run this with `/github`"
            ).add_field(
                name="the link"
                value="https://github.com/Topscientist/ArtysModeration"
            )
        )
        print(f"[*] {ctx.user} has used the /github command")


    @app_commands.command()
    async def togle(self: "CommandCog", ctx: Interaction, setting: str) -> None:
        """
         | paramiters
         | ==========
         |
         | :self: < These paramiters have already been explained
         | :ctx:  <
         |
         | :setting: is one of the events that will triger on a message
        """

        if not setting in ["profan", "quote"]:
            return await ctx.response.send_message(
                embed=Embed(
                    title="invalid setting",
                    description=f"{setting} is not a valid setting sorry"
                ).add_field(
                    name="profan",
                    value="togle automatic profanity detection on and off"
                ).add_field(
                    name="quote",
                    value="togle automatic quote sending"
                )
            )

        self.guild_settings[ctx.guild.id][setting] = not self.guild_settings[ctx.guild.id][setting]

        await ctx.response.send_message(
            embed=Embed(
                title="togled settings",
                description="changed settings"
            ).add_field(
                name="profanity detection",
                value="yes" if self.guild_settings[ctx.guild.id] else "no"
            ).add_field(
                name="quote sending",
                value="yes" if self.guild_settings[ctx.guild.id] else "no"
            )
        )


    # python des not need to give the below function `self` paramiter because it is not needed
    @staticmethod
    async def get_quote():
        return get("https://zenquotes.io/api/random").json()[0]


def setup(bot: commands.Bot) -> None:
    bot.add_cog(
        CommandsCog(bot),
        guilds=[Object(id=config["bot"]["guildId"])]
    )

