import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.messages = True

# Define your list of bad words and spam threshold
bad_words = ['fuck', 'nigga']  # List of bad words
spam_threshold = 5  # Number of messages in a short period considered as spam

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to track user message counts for spam detection
user_message_count = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    reset_message_count.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for bad words
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        await message.channel.send(f'{message.author.mention}, that word is not allowed!')

    # Check for links
    elif "http://" in message.content or "https://" in message.content:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, links are not allowed!')

    # Spam detection
    user_id = message.author.id
    if user_id in user_message_count:
        user_message_count[user_id] += 1
    else:
        user_message_count[user_id] = 1

    if user_message_count[user_id] > spam_threshold:
        await message.channel.send(f'{message.author.mention}, please stop spamming!')
        user_message_count[user_id] = 0  # Reset the count after warning

    await bot.process_commands(message)

@tasks.loop(minutes=1)
async def reset_message_count():
    user_message_count.clear()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')