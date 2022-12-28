##This program (Artys Moderation) is liscenced under the GNU Affero General Public License v3.0 and all re-distributions or modifictaions of this code must be done under the terms set out in the liscence otherwise they are in violation of the liscence agreement and are subject to copyright law enforcement.

import discord
import discord.ext.commands
import os
import sys
import random
import requests
import json
from replit import db
from time import sleep
import subprocess

# Import the uptime check
from uptime import uptime_check

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


discordnames = ("a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F",
                "g", "G", "h", "H", "i", "I", "j", "J", "k", "K", "l", "L",
                "m", "M", "n", "N", "o", "O", "p", "P", "q", "Q", "r", "R",
                "s", "S", "t", "T", "u", "U", "v", "V", "w", "W", "x", "X",
                "y", "Y", "z", "z")

whitelist = ("competition", "Competition", "passed", "Passed", "glass",
             "Glass", "GLASS", "Assign", "assign", "ASSIGN", "passport",
             "Passport", "passive", "Passive", "pass", "Pass", "Mass", "mass",
             "Assets", "assets", "Wassup", "wassup")

report_required = ["@"]

banned_words = [
    "ahole", "Ahole", "AHOLE", "anus", "ANUS", "Anus", "ass", "ASS", "Ass",
    "Ass Monkey", "ASS MONKEY", "ass monkey", "f.uck", "Assface", "assface",
    "ASSFACE", "assh0le", "ASSH0LE", "Assh0le", "asshole", "Asshole",
    "ASSHOLE", "assholes", "Assholes", "ASSHOLES", "bassterds", "Bassterds",
    "BASSTERDS", "bastard", "Bastard"
    "BASTARD", "bastards", "Bastards", "BASTARDS", "basterds", "Basterds",
    "BASTERDS", "bitch", "BITCH", "Bitch", "bitches", "BITCHES", "Bitches",
    "Blow Job", "blow job", "BLOW JOB", "c0ck", "C0ck", "C0CK", "c0cks",
    "C0CKS", "C0cks", "c0k", "C0K", "C0k", "cock", "COCK", "Cock", "cockhead",
    "COCKHEAD", "Cockhead", "cock-head", "COCK-HEAD", "Cock-head", "Cock-Head",
    "cocks", "COCKS", "Cocks", "CockSucker", "cocksucker", "COCKSUCKER",
    "Cocksucker", "cock-sucker", "COCK-SUCKER", "Cock-Sucker", "Cock-sucker",
    "crap", "Crap", "CRAP", "cum", "Cum", "CUM", "dick", "DICK", "Dick",
    "f u c k", "F U C K", "F u c k", "f u c k e r", "F U C K E R",
    "F u c k e r", "fuck", "FUCK", "Fuck", "fucker", "Fucker", "FUCKER",
    "fuckin", "Fuckin", "FUCKIN", "fucking", "Fucking", "FUCKING", "fucks",
    "Fucks", "FUCKS", "fuk", "Fuk", "FUK", "Fukah", "fukah", "FUKAH", "fuker",
    "Fuker", "FUKER", "Fukin", "FUKIN", "Fukk", "fukk", "FUKK", "Fukkah",
    "fukkah", "FUKKAH", "Fukken", "fukken", "FUKKEN", "Fukker", "fukker",
    "FUKKER", "Fukkin", "kukkin", "FUKKIN", "h0ar", "H0ar", "H0AR", "h0re",
    "H0re", "H0RE", "Lipshits", "lipshits", "LIPSHITSS", "Lipshitz",
    "lipshitz", "LIPSHITZ", "massterbait", "Massterbait", "MASSTERBAITER",
    "masstrbate", "Masstrbate", "MASSTRBATE", "masterbaiter", "Masterbaiter",
    "MASTERBAITER", "masterbate", "Masterbate", "MASTERBATE", "masterbates",
    "Masterbates", "MASTERBATES", "Motha Fucker", "MOTHA FUCKER",
    "motha fucker", "Motha Fuker", "motha fuker", "Motha Fukkah",
    "motha fukkah", "Motha Fukker", "motha fukker", "Mother Fukah",
    "mother fukah", "Mother Fuker", "mother fuker", "Mother Fukkah",
    "mother fukkah", "Mother Fukker", "mother fukker", "mother-fucker",
    "Mother-Fucker", "Mutha Fucker", "mutha fucker", "Mutha Fukah",
    "mutha fukah", "Mutha Fuker", "mutha fuker", "Mutha Fukkah",
    "mutha fukkah", "Mutha Fukker", "mutha fukker", "n1gr"
    "N1GR", "N1gr", "nigger", "Nigger", "NIGGER", "nigur", "Nigur", "NIGUR",
    "niiger", "Niiger", "NIIGER", "niigr", "Niigr", "peeenus", "Peeenus",
    "PEEENUS", "peeenusss", "Peeenusss", "PEEENUSSS", "peenus", "Peenus",
    "PEENUS", "peinus", "Peinus", "PEINUS", "pen1s", "Pen1s", "PEN1S", "penas",
    "Penas", "PENAS", "penis", "Penis", "PENIS", "penus", "Penus", "PENUS",
    "penuus", "Penuus", "PENUUS", "Phuc", "phuc", "PHUC", "Phuck", "phuck",
    "PHUCK", "Phuk", "phuk", "PHUK", "Phuker", "phuker", "PHUKER", "Phukker",
    "phukker", "PHUKKER", "pusse", "Pusse", "PUSSE", "pussee", "Pussee",
    "pussy", "Pussy", "PUSSY", "recktum", "Recktum", "RECKTUM", "rectum",
    "Rectum", "RECTUM", "retard", "Retard", "RETARD", "semen", "Semen",
    "SEMEN", "sex", "Sex", "SEX", "sexy", "Sexy", "SEXY", "sh1ter", "Sh1ter",
    "SH1TER", "sh1ts", "Sh1ts", "SH1TS", "sh1tter", "Sh1tter", "SH1TTER",
    "shit", "Shit", "SHIT", "shits", "Shits", "SHITS", "shitter", "Shitter",
    "SHITTER", "Shitty", "shitty", "SHITTY", "Shity", "shity", "SHITY",
    "son-of-a-bitch", "SON-OF-A-BITCH", "Son of a bitch", "Son Of A Bitch",
    "SON OF A BITCH", "son of a bitch", "Son-of-a-bitch", "Son-Of-A-Bitch",
    "tit", "Tit", "TIT", "turd", "Turd", "TURD", "vag1na", "Vag1na", "VAG1NA",
    "vagiina", "Vagiina", "VAGIINA", "vagina", "Vagina", "VAGINA", "vaj1na",
    "Vag1na", "VAG1NA", "vajina", "Vajina", "VAJINA", "vullva", "Vullva",
    "VALLVA", "vulva", "Vulva", "VULVA", "wh00r", "Wh00r", "WH00R", "wh0re",
    "Wh0re", "WGO0RE", "whore", "Whore", "WHORE", "b!+ch", "B!+ch", "B!+CH",
    "bitch", "Bitch", "BITCH", "fuck", "Fuck", "FUCK", "shit", "Shit", "SHIT",
    "ass", "Ass", "ASS", "asshole", "Asshole", "ASSHOLE", "b1tch", "B1tch",
    "B1TCH", "bastard", "Bastard", "BASTARD", "bi+ch", "Bi+ch", "BI+CH",
    "c0ck", "C0ck", "C0CK", "cawk", "Cawk", "CAWK", "cock", "Cock", "COCK",
    "cum", "Cum", "CUM", "cunt", "Cunt", "CUNT", "ejakulate", "Ejakulate",
    "EJAKULATE", "fatass", "Fatass", "FATASS", "fcuk", "Fcuk", "FCUK", "fuk",
    "Fuk", "FUK", "kawk", "Kawk", "KAWK", "masturbate", "Masturbate",
    "MASTURBATE", "masterbat*", "Masterbat*", "MASTERBAT*", "masterbat3",
    "Masterbat3", "MASTERBAT3", "motherfucker", "Motherfucker", "MOTHERFUCKER",
    "nigga", "Nigga", "NIGGA", "nigger", "Nigger", "NIGGER", "nutsack",
    "Nutscack", "MUTSACK", "pusse", "Pusse", "PUSSE", "pussy", "Pussy",
    "PUSSY", "scrotum", "Scrotum", "SCROTUM", "sh!t", "Sh!t", "SH!T", "shi+",
    "Shi+", "SHI+", "sh!+", "Sh!+", "SH1+", "tits", "Tits", "TITS", "boobs",
    "Boobs", "BOOBS", "b00bs", "B00bs", "B00BS", "testical", "Testical",
    "TESTICAL", "testicle", "Testicle", "titt", "Titt", "TITT", "w00se",
    "W00se", "W00SE", "jackoff", "Jackoff", "JACKOFF,"
    "*fuck*", "*Fuck*", "*FUCK*", "*shit*", "*Shit*", "*SHIT*", "faggot",
    "Faggot", "f@gg0t", "F@gg0t", "fag", "Fag", "f@G", "F@G", "f@g", "FAG",
    "@$$", "arse*", "ARSE*", "Arse*", "assrammer", "Assrammer", "ASSRAMMER",
    "bi7ch", "Bi7ch", "BI7CH", "bitch*", "Bitch*", "BITCH*", "bollock*",
    "Bollock*", "BOLLOCK*", "breasts", "Breasts", "BREASTS", "Cock*", "Cock*",
    "COCK*", "dick*", "DICK*", "ejackulate", "Ejackulate", "EJACKULATE",
    "foreskin", "Foreskin", "FORESKIN", "fuk*", "Fuk*", "FUK*", "h0r", "H0r",
    "H0R", "kanker*", "KANKER*"
    "Janker*", "JANKER*", "nigger*", "NIGGER*"
    "Niggr*", "NIGGR*", "paska*", "Paska*", "PASKA*", "perse", "Perse",
    "PERSE", "picka"
    "PICKA", "Picka", "piss*", "PISS*"
    "Piss*", "poontsee", "Poontsee", "POONTSEE", "porn", "Porn", "PORN",
    "p0rn", "P0rn", "P0RN", "pr0n", "PR0N", "Pr0n", "schaffer", "Schaffer",
    "SCHAFFER", "sh!t*", "Sh!t*", "SH!T*", "sharmuta", "Sharmuta", "SHARMUTA",
    "sharmute", "Sharmute", "SHARMUTE", "shipal", "Shipal", "SHIPAL", "suka",
    "Suka", "SUKA", "b00b*", "B00b*", "B00B*", "testicle*", "Testicle*",
    "TESTICLE*", "titt*", "Titt*", "TITT*", "twat", "Twat", "TWAT", "wank*",
    "Wank*", "WANK*", "wichser", "Wichser", "WINCHER", "wop*", "Wop*", "WOP*",
    "p3n1s", "P3n1s", "p3n1S", "P3N1S", "p3N1s", "p3N1S", "fagg", "faggot",
    "Fagg", "fag", "Fag", "FaG", "FAG", "FAG", "f@g", "F@g", "F@G", "f@G",
    "Faggot", "FAGGOT", "f@gg0t", "F@GG0T", "f@GG0t", "Fagg", "FAGG", "F@gg",
    "f@GG", "FaGG", "fAGG", "F@gG", "f@gg", "F@GG"
]

cookie_list = ["Congrats! You have won a cookie! 🍪", "No, No cookie for you!"]

sad_words = [
    "unhappy", "Unhappy", "depressed", "Depressed", "miserable", "Miserable",
    "i feel alone", "I feel alone"
]

starter_encouragements = [
    "Cheer Up! Life will be ok", "Don't Worry, Be happy!",
    "Every little thing is going to be alright!", "Hang In There!",
    "Whatever life throws at you, You will be stonger!"
]

banned_entries = [
    "829680222478925864", "Artys Moderation", "@829680222478925864",
    "artys moderation", "artys Moderation", "Artys moderation"
]

topics = [
    "If you go anywhere or do anything in the world, what would it be?",
    "What is the meaning of life", "What is life's greatest challenge?",
    "Who is one person that would never give you up?",
    "Who is one person that would never let you down?",
    "Is ceral a soup, Why and why not?",
    "What do you think will be the most popular in 3 years time?",
    "What's something that's very popular but in 3-5 years people will look back on and be embarressed by?",
    "How would you describe the human race?",
    "What are 5 things that should be changed about the way we live our lives right now?",
    "If there was one fairytale that you could move to modern times, what would it be and what would it look like?",
    "What things do you wish were easier to say to people?",
    "What makes you stong?",
    "If animals could talk, which one would be the rudest?",
    "Which object do you wish you could eliminate from existnace and why?",
    "If you could rule the world for one day, What would you do?",
    "What Can You Do That No One Else Can?",
    "What Is The Craziest Story You’ve Ever Heard?",
    "If You Could Teleport, Where Would You Go, And Why?",
    "What Is One Of The Things You Have On Your “Bucket” List?",
    "Would You Accept A One-Way Ticket To Mars?",
    "What Is The One Thing You Have Always Wanted To Do?",
    "If You Could Win Any Award What Would It Be, And Why?",
    "What Do You Like More, Being A Leader Or A Follower?",
    "What Character Traits Do You Share With Your Favorite Animal?",
    "If You Were On A Desert Island, But Your Needs For Food And Shelter Were Totally Taken Care Of, What One Luxury Item Would You Wish For?",
    "If You Were A Movie Director, What Genre Of Movie Would You Make?",
    "When You Go To The Zoo, What Animal Would You Most Like To Be? Why?",
    "Would You Make Modern Technology Disappear If You Could?",
    "Has Social Media Had A Positive Influence On Modern  Life, Or Negative?",
    "do you guys know that there was a guy that ran pc on a potato?"
]


@client.event
async def on_ready():
    uptime_check()
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(
        name=
        f"Never Gonna Give You Up! | Helping Out On {len(client.guilds)} servers | arty help"
    ))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    msg = message.content

    if any(word in msg for word in banned_words):
        if any(word in msg for word in whitelist):
            return
        else:
            abc = message.guild.id
            if str(abc) in db:
                return
            else:
                author = message.author.mention
                await message.delete()
                embed = discord.Embed(
                    title='🛡 Hmmm, AutoMod',
                    description=
                    'That word appears to be banned in this discord server, please watch your language %s. '
                    % author,
                    color=discord.Colour.orange())
                await message.channel.send(embed=embed, delete_after = 10)
                print(
                    'Automoderator> Banned word was deleted in a discord server'
                )

    if any(word in msg for word in sad_words):
        name = message.guild.name
        if name in db:
            return
        else:
            if message.author.bot:
                return
            else:
                await message.channel.send(
                    random.choice(starter_encouragements))

    elif msg.startswith('arty topic'):
        await message.channel.send(random.choice(topics))

    elif msg.startswith('arty github'):
        await message.channel.send(
            'Want To Know How Our Bot Works? Here is the link to our github page! https://github.com/Topscientist/ArtysModeration'
        )
        print('External> GitHub link has been sent')

    elif msg.startswith('arty config'):
        owner = message.guild.owner_id
        author = message.author.id
        writer = message.author.mention
        if author == owner:
            embed = discord.Embed(title="⚙️ Bot Settings! ⚙️",
                                  colour=discord.Colour(0))

            embed.add_field(
                name=f"**arty cheer up true/false**",
                value=
                "_Cheer up is a chat feature which looks for sad words in peoples messages then send them a message of encurouragment. [Enabled By Defult]_",
                inline=False)
            embed.add_field(
                name=f"**arty mod true/false**:",
                value=
                "_ Moderation is a chat feature that identifies and removes all swear and NSWF words. [Enabled By Defult]_",
                inline=False)

            await message.channel.send(embed=embed)
            print(
                'Command> Configuration page for bot viewed in a discord server'
            )

        elif writer == '<@786182411465392128>':
            embed = discord.Embed(title="⚙️ Bot Settings!⚙️ ",
                                  colour=discord.Colour(0))

            embed.add_field(
                name=f"**arty cheer up true/false**",
                value=
                "_Cheer up is a chat feature which looks for sad words in peoples messages then send them a message of encurouragment. [Enabled By Defult]_",
                inline=False)
            embed.add_field(
                name=f"**arty mod true/false**:",
                value=
                "_ Moderation is a chat feature that identifies and removes all swear and NSWF words. [Enabled By Defult]_",
                inline=False)

            await message.channel.send(embed=embed)
            print('Command> config executed')

        else:
            embed = discord.Embed(
                title='💥 Error 401',
                description='Only the guild owner can change this!',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)

    elif msg.startswith('<@829680222478925864>'):
        embed = discord.Embed(
            title='👋 Hello There!',
            description=
            'My name is Artys Moderation, To get a list of my commands type `arty help`',
            color=discord.Colour.green())
        await message.channel.send(embed=embed)

    elif msg.startswith('arty cheer up false'):
        owner = message.guild.owner_id
        author = message.author.id
        if author != owner:
            emoji = '❌'
            await message.add_reaction(emoji)
        else:
            emoji = '🔁'
            await message.add_reaction(emoji)
            guild_id = message.guild.name
            if guild_id in db:
                await message.channel.send(
                    '❌ **Failed To Run Command:** Cheer Up is already disabled in this guild'
                )
            else:
                db[guild_id] = guild_id
                await message.channel.send(
                    '✅ **Succsessfully Disabled Cheer Up In This Guild!**')
    elif msg.startswith('arty cheer up true'):
        owner = message.guild.owner_id
        author = message.author.id
        if author != owner:
            emoji = '❌'
            await message.add_reaction(emoji)
        else:
            guild_id = message.guild.name
            emoji = '🔁'
            await message.add_reaction(emoji)
            if guild_id in db:
                del db[guild_id]
                await message.channel.send(
                    '✅ **Succsessfully Enabled Cheer Up In This Guild!**')
            else:
                await message.channel.send(
                    '❌ **Failed To Run Command:** Cheer Up is alreday enabled in this guild'
                )

    elif msg.startswith('arty mod false'):
        owner = message.guild.owner_id
        author = message.author.id
        if author != owner:
            emoji = '❌'
            await message.add_reaction(emoji)
        else:
            emoji = '🔁'
            await message.add_reaction(emoji)
            name = message.guild.id
            if str(name) in db:
                await message.channel.send(
                    '❌ **Failed To Run Command:** Moderation is already disabled in this guild'
                )
            else:
                db[name] = "True"
                await message.channel.send(
                    '✅ **Succsessfully Disabled Moderation In This Guild!**')
    elif msg.startswith('arty mod true'):
        owner = message.guild.owner_id
        author = message.author.id
        if author != owner:
            emoji = '❌'
            await message.add_reaction(emoji)
        else:
            name = message.guild.id
            emoji = '🔁'
            await message.add_reaction(emoji)
            if str(name) in db:
                del db[str(name)]
                await message.channel.send(
                    '✅ **Succsessfully Enabled Moderation In This Guild!**')
            else:
                await message.channel.send(
                    '❌ **Failed To Run Command:** Moderation is alreday enabled in this guild'
                )

    elif msg.startswith('arty cookie'):
        await message.channel.send(random.choice(cookie_list))
        print('Command> arty cookie has been executed')

    elif msg.startswith('arty labs'):
        embed = discord.Embed(title="🤖 Arty Labs!",
                              colour=discord.Colour(0xe91e63))

        embed.add_field(
            name=f"Hey There!",
            value="My names Arty and I am a discord.py bot developer.",
            inline=False)
        embed.add_field(
            name=
            f"I have recently partnered with a friend to make a bot lab or a family of bots!",
            value=
            " This lab or 'family' will include Artys Moderation, Artys Raid Protection and the 0x102 Discord bot. This lab will contain a lot of different features within the bots and moderation wise will contain all of the same intelligence and is planned to be one of the most intelligent discord moderation bot systems to date! This lab will launch soon so watch this space...",
            inline=False)

        await message.channel.send(embed=embed)

    elif msg.startswith('arty help'):
        name = message.guild.name
        if name == 'EXAMPLE-HERE123':
            await message.channel.send(
                '❌ Failed: **This Discord Server Has Been Blacklisted.** There are many reasons for a blacklist, Please run arty discord to join the discord to appeal ypur balcklist. The bot will not work in this discord until your blacklist is removed. Kicking the bot and then re-adding will not have an effect.'
            )
            return
        else:
            embed = discord.Embed(title="Command List:",
                                  colour=discord.Colour(0x9b59b6))

            embed.add_field(name=f"ℹ️ Bot Info:",
                            value="arty info",
                            inline=False)
            embed.add_field(name=f"✉️ Join Our Discord:",
                            value="arty discord",
                            inline=False)
            embed.add_field(name=f"🚦Bot Status:",
                            value="arty status",
                            inline=False)
            embed.add_field(name=f"🍪 Try to win a cookie:",
                            value="arty cookie",
                            inline=False)
            embed.add_field(name=f"💭 Inspiration and Quotes:",
                            value="arty inspire",
                            inline=False)
            embed.add_field(name=f"🌐 The GitHub page for Artys Moderation:",
                            value="arty github",
                            inline=False)
            embed.add_field(name=f"📮 Report Command Help:",
                            value="arty report help",
                            inline=False)
            embed.add_field(name=f"📋 Suggest a chat topic:",
                            value="arty topic",
                            inline=False)
            embed.add_field(name=f"🤖 Learn about our bot lab:",
                            value="arty labs",
                            inline=False)
            embed.add_field(name=f"⚙️ Bot Settings *(Server Owner Only)*:",
                            value="arty config",
                            inline=False)

            await message.channel.send(embed=embed)
            print('Command> arty help has been executed')

    elif msg.startswith('arty info'):
        embed = discord.Embed(
            title='Bot Info',
            description=
            "**Welcome To Artys Moderation!** A bot that is fully automated with no pior setup! The idea of Artys Moderation is to help your mod bot with moderating and to help cheer people up when they are feeling down. So, you know how nower days a lot of discord servers have widley used mod bots and while this can be good it means that sometimes these bots can be a bit slow at doing their job, And thats where Artys Moderation comes into play! Because of my light code-base and good hosting I can get down on those bad words and keep your chat clean and fresh, I also have a feature called cheer up! The premise of this feature is to detect when a user is feeling sad and send them a message of encourgement! I am always adding new features and listening to feedback so if you have any suggestions then please do leave them in my discord, I would love to hear them!",
            color=discord.Colour.blue())
        await message.channel.send(embed=embed)
        print('Command> arty info has been executed')

    elif msg.startswith('arty status'):
        embed = discord.Embed(
            title='Bot Status',
            description=
            '**Bot Online** Bot is online in all discord servers. To get more info or real-time updates please join pur disvord or check our status page at the following link; https://stats.uptimerobot.com/rVzDJuAZkN/787787175',
            color=discord.Colour.green())
        await message.channel.send(embed=embed)
        print('Command> $status has been executed')

    elif msg.startswith('arty discord'):
        await message.channel.send(
            'Got A Bug To Report? Feature To Suggest? Here is the invite to our discord; https://discord.gg/5y9tDDBkBW'
        )
        print('Command> discord has been executed')

    elif msg.startswith('arty inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        print('Command> arty inspire has been executed')

    elif msg.startswith('arty report help'):
        embed = discord.Embed(title="Arty's Moderation Report Help!",
                              colour=discord.Colour(0x11806a))

        embed.add_field(
            name=f"First",
            value=
            "type arty r and then do the username of the user @mentioned and then the report reason. Format: arty r [@user] [reason]",
            inline=False)
        embed.add_field(
            name=f"Second:",
            value=
            "Submit the report by sending the message, If your report has an @mention and a report reason and doesn't contain any foul language Arty should come back with comfirmation of the report being sent.",
            inline=False)
        embed.add_field(
            name=f"Third:",
            value=
            "Hopefully the mods of the discord should be in contact with you.",
            inline=False)
        embed.add_field(
            name=f"*Notes:*",
            value=
            "*Recations must be enbled for the report to go though. The report must @mention a valid user and not a bot. The report must not contain any foul language. If the report contains fould language, the report will go through even if moderation is disabled.*",
            inline=False)

        await message.channel.send(embed=embed)

    elif msg.startswith('arty r'):
        report = message.content
        author = message.author.mention
        if any(word in msg for word in report_required):
            if any(word in msg for word in banned_words):
                emoji = '❌'
                await message.add_reaction(emoji)
                embed = discord.Embed(
                    title='💥 Error',
                    description=
                    'Reports cannot contain foul language. Please re-submit the re-sibmit the report without the foul language',
                    color=discord.Colour.red())
                await message.channel.send(embed=embed)
                return
            if any(word in msg for word in banned_entries):
                emoji = '❌'
                await message.add_reaction(emoji)
                embed = discord.Embed(
                    title='💥 Error',
                    description=
                    'I cannot report myself, If I am misbehaving please type `arty discord` and contact our staff there, They would love to help out!',
                    color=discord.Colour.red())
                await message.channel.send(embed=embed)
                return
            if len(message.clean_content) < 18:
                emoji = '❌'
                await message.add_reaction(emoji)
                embed = discord.Embed(
                    title='💥 Error',
                    description=
                    'The report must contain at least 18 characters.',
                    color=discord.Colour.red())
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title='Report!',
                                      description=report,
                                      color=discord.Colour.orange())
                await message.channel.send(embed=embed)
                embed = discord.Embed(
                    description=' _Report Submitted By: %s_ ' % author, )
                await message.channel.send(embed=embed)
                emoji = '✅'
                await message.add_reaction(emoji)

        else:
            emoji = '❌'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='💥 Error',
                description='You need to @mention a valid user in your report',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)

    elif msg.startswith('arty sudo bot ban'):
        sudouser = message.author.id
        if sudouser == int("786182411465392128"):
            await message.channel.send(
                '✅ Succsessfully Un-Blacklisted this discord.')
        else:
            emoji = '❌'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='💥 Error 401',
                description=
                '**sudo.adims.db** retured the following error; You are not a sudo-user. Please do not attempt to run this command again.',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            print(
                'Sudo Error> An Unathorised User Attempted To Accses A Sudo Only Area Anf Failed'
            )
            return

    elif msg.startswith('arty sudo restart'):
        sudo = message.author.id
        if sudo == int("786182411465392128"):
            emoji = '🔄'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='🔄 Restarting Artys Moderation...',
                description=
                '**The Artys Moderation Bot is being restarted** Please allow up to 3 seconds for the bot to completly shutdown before restarting in order to finish off any sub-processes. A message will be sent in chat when this process is complete. *Please note: The website will remain operational and will not be restarted*',
                color=discord.Colour.greyple())
            await message.channel.send(embed=embed)
            print('')
            print('Restarting Artys Moderation...')
            print('')
            sleep(3)
            print('')
            print(
                'Sudo Restart> Artymartin3459 or another sudo user has restarted Artys Moderation'
            )
            emoji = '✅'
            await message.add_reaction(emoji)
            await message.channel.send(
                '🎉 Artys Moderation has been successfully restarted!')
            print('Sudo> Bot has been restarted')
            subprocess.call(
                [sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

        else:
            emoji = '❌'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='💥 Error 401',
                description=
                '**sudo.adims.db** retured the following error; You are not a sudo-user. Please do not attempt to run this command again.',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            print(
                'Sudo Error> A User Attempted To Accses A Sudo Only Area And Failed'
            )
            return
    elif msg.startswith('arty sudo shutdown'):
        sudo = message.author.id
        if sudo == int("786182411465392128"):
            emoji = '🔄'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='🪫 Shuttting Down Artys Moderation...',
                description=
                '**The Artys Moderation Bot is being shut down** Please allow up to 3 seconds for the bot to completly shut down and finish off any sub-processes. A message will be sent in chat when this process is complete. *Please note: The website will remain operational*',
                color=discord.Colour.greyple())
            await message.channel.send(embed=embed)
            print('')
            print('Shutting Down Artys Moderation...')
            print('')
            sleep(3)
            emoji = '✅'
            await message.add_reaction(emoji)
            await message.channel.send(
                '💤 Artys Moderation has shutdown sucsessfully and all processes have been terminated at the root, excluding the website.'
            )
            sleep(0.1)
            print('')
            print(
                'Sudo> Artymartin3459 or another sudo user has shutdown Artys Moderation with the reason: null'
            )
            exit()

        else:
            emoji = '❌'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='💥 Error 401',
                description=
                '**sudo.adims.db** retured the following error; You are not a sudo-user. Please do not attempt to run this command again.',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            print(
                'Sudo Error> A User Attempted To Accses A Sudo Only Area And Failed'
            )
            return

    elif msg.startswith('arty sudo'):
      sudouser = message.author.id
      if sudouser == int("786182411465392128"):
            embed = discord.Embed(title="Sudo Command List:",
                                  colour=discord.Colour(000000))

            embed.add_field(name=f"Restart The Bot:",
                            value="arty sudo restart",
                            inline=False)
            embed.add_field(name=f"Shutdown The Bot:",
                            value="arty sudo shutdown",
                            inline=False)
            embed.add_field(name=f"Bot Ban Someone:",
                            value="arty sudo bot ban",
                            inline=False)

            await message.channel.send(embed=embed)
            print('Sudo> Sudo commands list has been accessed')
      else:
            emoji = '❌'
            await message.add_reaction(emoji)
            embed = discord.Embed(
                title='💥 Error 401',
                description=
                '**sudo.adims.db** retured the following error; You are not a sudo-user. Please do not attempt to run this command again.',
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            print(
                'Sudo Error> A User Attempted To Accses The Sudo Command List and Failed'
            )
            return
        
client.run(os.getenv('TOKEN'))
