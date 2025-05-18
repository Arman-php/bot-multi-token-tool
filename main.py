import asyncio
import discord
import httpx
import base64

allowed_user_command = {"youruserid"}

with open("tokens.txt") as f:
    tokens = [line.strip() for line in f if line.strip()]

async def spam_dm(token, user_id, message, times):
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    url = "https://discord.com/api/v10/users/@me/channels"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json={"recipient_id": user_id})
        if resp.status_code == 200:
            channel_id = resp.json()["id"]
            message_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            for _ in range(times):
                try:
                    await client.post(
                        message_url,
                        headers=headers,
                        json={"content": message}
                    )
                    await asyncio.sleep(1)
                except Exception:
                    await asyncio.sleep(10)

async def spam_tag(token, channel_id, user_id, times):
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    message_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    mention = f"<@{user_id}>"
    async with httpx.AsyncClient() as client:
        for _ in range(times):
            try:
                await client.post(
                    message_url,
                    headers=headers,
                    json={"content": mention}
                )
                await asyncio.sleep(1)
            except Exception:
                await asyncio.sleep(10)

def black_embed(guild, description, title=None):
    embed = discord.Embed(
        title=title if title else (guild.name if guild else "Bot"),
        description=description,
        color=discord.Color.from_rgb(0, 0, 0)
    )
    return embed

def is_command(msg):
    cmds = ("a!help", "a!commands", "a!spamdm", "a!spamtag", "a!gettoken")
    return any(msg.content.strip().lower().startswith(cmd) for cmd in cmds)

async def start(token, is_help_token=False):
    intents = discord.Intents.default()
    intents.message_content = True
    arman = discord.Client(intents=intents)

    @arman.event
    async def on_ready():
        print(f"Bot {token[:8]}... is online.")

    @arman.event
    async def on_message(message):
        if message.author.bot:
            return

        if not is_command(message):
            return

        if str(message.author.id) not in allowed_user_command:
            return

        if is_help_token and message.content.strip().lower() in ["a!help", "a!commands"]:
            help_text = (
                "**a!help** — Displays this help message\n"
                "**a!spamdm @user [times] [message]** — DM spam a user a number of times (default 10, default message is 'Hello')\n"
                "**a!spamtag @user [times]** — Mention spam a user in current channel (default 10)\n"
                "**a!gettoken @user** — Shows the user's base64 user ID plus stars to mimic a token\n\n"
                "*All commands are available only to authorized users.*"
            )
            embed = black_embed(message.guild, help_text, title=(message.guild.name if message.guild else "Bot"))
            reply = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()
            await reply.delete()
            return

        if message.content.startswith("a!spamdm") and message.mentions:
            args = message.content.split()
            target = message.mentions[0].id
            times = 10
            content = "Hello"
            if len(args) >= 3:
                try:
                    times = int(args[2])
                except ValueError:
                    times = 10
            if len(args) >= 4:
                content = " ".join(args[3:])
            for t in tokens:
                asyncio.create_task(spam_dm(t, target, content, times))
            embed = black_embed(message.guild, f"Started DM spam of <@{target}> for {times} times by all bots.")
            confirm = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            await confirm.delete()
            return

        if message.content.startswith("a!spamtag") and message.mentions:
            args = message.content.split()
            target = message.mentions[0].id
            times = 10
            if len(args) >= 3:
                try:
                    times = int(args[2])
                except ValueError:
                    times = 10
            for t in tokens:
                asyncio.create_task(
                    spam_tag(
                        t,
                        message.channel.id,
                        target,
                        times
                    )
                )
            embed = black_embed(message.guild, f"Started mention spam of <@{target}> for {times} times by all bots.")
            confirm = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            await confirm.delete()
            return

        if message.content.startswith("a!gettoken") and message.mentions:
            target = message.mentions[0].id
            user_b64 = base64.b64encode(str(target).encode()).decode()
            token_length = len(tokens[0]) if tokens else 60
            stub = user_b64 + ('*' * max(token_length - len(user_b64), 0))
            embed = black_embed(
                message.guild,
                f"Token for <@{target}> (base64 user id + stars):\n`{stub}`"
            )
            result = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            await result.delete()
            return

    await arman.start(token)

async def main():
    tasks = []
    for i, token in enumerate(tokens):
        tasks.append(start(token, is_help_token=(i == 0)))
    await asyncio.gather(*tasks)

asyncio.run(main())
