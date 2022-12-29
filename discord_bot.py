# MTA1NjI0ODIwNjQxMDkwNzcyMQ.G3mgTl.epX_vCcHS5J77_B1ptwx-DosdTbdnJy5wx2vfA

import discord
from discord.ext import commands
from dotenv import load_dotenv
from torch import tensor
from chat_model_generator import generate_GPT2, chat_history_ids
from config_operations import read_config, update_config


load_dotenv()

config = read_config()

def remove_prefix_word(message, remove_num_words=1):
    return " ".join(message.split()[remove_num_words:])


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(intents=intents, command_prefix=config["prefix"])


# --------------------------------------------------------------------
@bot.command()
async def bebra(ctx, member):
    if member == discord.Member:
        await ctx.reply(f"{member} Нюхает Бебру")
    else:
        await ctx.reply("Нюхай бебру")

# --------------------------------------------------------------------
@bot.command()
async def text(ctx):
    if ctx.author == bot.user:
        return

    await ctx.reply(f"{remove_prefix_word(ctx.message.content)}")

# --------------------------------------------------------------------
@bot.command()
async def generate_translate(ctx, message):
    if message.lower() == "off":
        update_config("TRANSLATE_FLAG", "False")
        await ctx.reply("Перевод генерации выключен (ввод только на английском)")
    elif message.lower() == "on":
        update_config("TRANSLATE_FLAG", "True")
        await ctx.reply("Перевод генерации включен")
    else:
        await ctx.reply("Неверный аргумент (off/on)")

# --------------------------------------------------------------------
@bot.command()
async def say(ctx, message):
    await ctx.send(r"/tts Нюхай бебру")
# --------------------------------------------------------------------
@bot.command()
async def generate(ctx):
    if ctx.author == bot.user:
        return

    print(remove_prefix_word(ctx.message.content))
    await ctx.reply(generate_GPT2(remove_prefix_word(ctx.message.content)))

bot.run(config['token'])