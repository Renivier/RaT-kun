import discord
from discord.ext import commands
import logging
import calculator
import unrelated
import random
import requests
import asyncio


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='uwu ', intents = intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("The bot's done, working gud")




@bot.command(name="calculate", help= "This is a recursive calculator, it can calculate equations based on PEMDAS.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def calculate(ctx, *, expression: str):
    try:
        result = calculator.calculate_expression(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"Error in calculation: {e}")


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="", help= "Shows balance of the wanted user.")
async def bal(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    data = unrelated.load_data()[0]
    user_id = str(user.id)
    user_name = str(user.name)
    user_pfp = str(user.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "bal", data, user_name, pfp = user_pfp)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="beg", help= "Beg for some coins, best command for starters!")
@commands.cooldown(1, 5, commands.BucketType.user)
async def beg(ctx):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "beg", data, user_name=ctx.author.name, pfp = user_pfp, amount=None)
    unrelated.save_data(data)
    await ctx.send(embed=embed)



@bot.command(name="deposit", help= "Deposit a specific amount of coins to your bank account.")
async def deposit(ctx, amount: int= None):
    if amount != None and amount <= 0:
        await ctx.send("Amount must be a positive integer.")
        return
    if amount == None:
        await ctx.send("Please specify an amount to deposit.")
        return
    data = unrelated.load_data()[0]
    user_id, user_pfp = str(ctx.author.id), str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "deposit", data, user_name=ctx.author.name, pfp = user_pfp, amount=amount)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="withdraw", help="Withdraw a specific amount of coins from your bank account.")
async def withdraw(ctx, amount: int= None):
    if amount != None and amount <= 0:
        await ctx.send("Amount must be a positive integer.")
        return
    if amount == None:
        await ctx.send("Please specify an amount to withdraw.")
        return
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "withdraw", data, user_name=ctx.author.name, pfp = user_pfp, amount=amount)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="shop", help="Displays the shop!")
async def shop(ctx):
    _, item_data = unrelated.load_data()
    user_id = str(ctx.author.id)
    user_pfp = str(ctx.author.display_avatar.url)
    embed = unrelated.perform_action(user_id, "shop", item_data, user_name=ctx.author.name, pfp = user_pfp, amount=None)
    await ctx.send(embed=embed)



@bot.command(name="slap", help= "What's better than slapping someone, eh?")
async def slap(ctx, user: discord.User):
    await ctx.send(f"{ctx.author.mention} slapped {user.mention} 💥")



@bot.command(name="gamble", help="You wanna win some money? we'll see....")
async def gamble(ctx, amount: int = None):
    if amount is None or amount <= 0:
        await ctx.send("Please specify a positive amount to gamble.")
    else:
        data = unrelated.load_data()[0]
        user_id = str(ctx.author.id)
        user_name = str(ctx.author.name)
        user_pfp = str(ctx.author.display_avatar.url)
        get_user_data(user_id, data)
        embed = unrelated.perform_action(user_id, "gamble", data, user_name=user_name, pfp=user_pfp, amount=amount)
        unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="Waifu", help= "Down. Fucking. Bad.")
async def Waifu(ctx, type:str, category:str):
    
    base_url = f"https://api.waifu.pics/{type}/{category}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        image_url = data.get("url")
        embed = discord.Embed(title=f"{type.capitalize()} - {category.capitalize()}")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Failed to fetch image. Please check the type and category.\n\nValid types: sfw, nsfw\nValid categories for sfw: waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, happy, wink, poke, dance, cringe\nValid categories for nsfw: waifu, neko, trap, blowjob")



@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Wait {error.retry_after:.1f}s before using this again!")

@bot.command(name="rob", help= "Rob someone!(Don't get caught tho!)")
@commands.cooldown(1, 5, commands.BucketType.user)
async def rob(ctx, user: discord.User):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    user_id2 = str(user.id)
    user_name2 = str(user.name)
    get_user_data(user_id, data)
    if user_id2 not in data:
        await ctx.send("The target user didnt even play yet!")
    else:

        embed = unrelated.perform_action(user_id, "rob", data, user_name=user_name, pfp=str(ctx.author.display_avatar.url), amount=None, user_id2=user_id2, user_name2=user_name2, pfp2=str(user.display_avatar.url))
        await ctx.send(embed=embed)
        unrelated.save_data(data)


@bot.command(name="item", help="Full information on an item!")
async def item(ctx,  *, item_name:str):
    user_id = str(ctx.author.id)
    data, item_data = unrelated.load_data()
    user_name = str(ctx.author.name)
    if item_name not in item_data:
        await ctx.send("This item does not exist, not a great keyboard user?")
    else:
        embed = unrelated.perform_action(user_id, "item", data, user_name, item_data=item_data, itemname=item_name)
        await ctx.send(embed=embed)



@bot.command(name="buy", help="Buy something from the shop!")
async def buy(ctx, amount:int = 1, *, itemname):
    user_id = str(ctx.author.id)
    data, item_data = unrelated.load_data()
    get_user_data(user_id, data)
    embed = unrelated.perform_action(
    user_id, 
    "buy", 
    data, 
    user_name=ctx.author.name, 
    item_data=item_data, 
    itemname=itemname,
    amount=amount
)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="sell", help="Sell something to shop!")
async def sell(ctx, amount = 1, *, itemname):
    data, item_data = unrelated.load_data()
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "sell", data, user_name, pfp, amount, item_data = item_data, itemname = itemname)
    unrelated.save_data(data)

    
    await ctx.send(embed=embed)


@bot.command(name="inventory", help= "Shows a user's inventory!")
async def inventory(ctx, user:discord.User = None):
    if user is None:
        user_id = str(ctx.author.id)
        user_name = str(ctx.author.name)
        pfp = str(ctx.author.display_avatar.url)
    else:
        user_id = str(user.id)
        user_name = str(user.name)
        pfp = str(user.display_avatar.url)
    data= unrelated.load_data()[0]
    user_name = str(ctx.author.name) if user is None else user.name
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "inventory", data, user_name, pfp)
    await ctx.send(embed=embed)


@bot.command(name="slots", help="You wanna earn MORE, money? eh..")
async def slots(ctx, amount:int):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "slots", data, user_name, pfp, amount)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="dig", help= "Dig to find some coins, and maybe items!")
async def dig(ctx):
    data, item_data = unrelated.load_data()
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "dig", data, user_name, pfp, item_data=item_data)
    unrelated.save_data(data)
    await ctx.send(embed=embed)

@bot.command(name="dice", help="Roll a dice and gamble your money!")
async def dice(ctx, amount:int):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    msg = await ctx.send("Rolling the dice...")
    for delay in [0.2, 0.25, 0.35, 0.5]:
        fake_roll = random.randint(1,6)
        new_embed = discord.Embed(
        title="Rolling the dice...",
        description=f"Rolling... :game_die: **{fake_roll}**"
    )
        await msg.edit(embed=new_embed)
        await asyncio.sleep(delay)

    final_embed = unrelated.perform_action(user_id, "dice", data, user_name, pfp, amount)
    unrelated.save_data(data)
    await msg.edit(embed=final_embed)


@bot.command(name="profile", help="Displays a user's profile!")
async def profile(ctx, user:discord.User=None):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id) if user is None else str(user.id)
    user_name = str(ctx.author.name) if user is None else str(user.name)
    pfp = str(ctx.author.display_avatar.url) if user is None else str(user.display_avatar.url)
    embed = unrelated.perform_action(user_id, "profile", data, user_name, pfp)
    await ctx.send(embed=embed)



@bot.command(name="jobs", help="Displays all the available jobs!")
async def jobs(ctx):
    jobs_data = unrelated.job_list()
    pfp = str(ctx.author.display_avatar.url)
    job_class = unrelated.Jobs() 
    embed = job_class.execute(jobs_data, pfp)
    await ctx.send(embed=embed)





@bot.command("pick_job", help="Pick a job!")
async def pick_job(ctx, *, job_name):
    jobs = unrelated.job_list()
    data = unrelated.load_data()[0]
    if job_name not in jobs:
        await ctx.send("That job does not exist, use the keyboard more often lil' bro!")
    user_id = str(ctx.author.id)
    get_user_data(user_id, data)
    pfp = str(ctx.author.display_avatar.url)
    pick_job_class = unrelated.Job_Pick()
    embed = pick_job_class.execute(user_id, job_name, data, pfp)
    unrelated.save_data(data)
    await ctx.send(embed=embed)





@bot.command(name="work", help="Work! Work! Work!")
async def work(ctx):
    user_id = str(ctx.author.id)
    data = unrelated.load_data()[0]
    user_data = get_user_data(user_id, data)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    if user_data['job'] == 'None':
        await ctx.send("You're fucken jobless, get a job!")
    embed = unrelated.perform_action(user_id, "work", data, user_name, pfp)
    unrelated.save_data(data)
    await ctx.send(embed=embed)





@bot.command(name="study", help= "Study, convert your money to EXP.")
async def study(ctx):
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    data = unrelated.load_data()[0]
    user_data = get_user_data(user_id, data)
    pfp = str(ctx.author.display_avatar.url)
    embed = unrelated.perform_action(user_id, "study", data, user_name, pfp)
    unrelated.save_data(data)
    await ctx.send(embed=embed)


@bot.command(name="use", help = "Use an item to get a coin or XP boost.")
async def use(ctx, amount:int, *, itemname: str):
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    data, item_data = unrelated.load_data()
    user_data = get_user_data(user_id, data)
    pfp = str(ctx.author.display_avatar.url)
    embed = unrelated.perform_action(user_id, "use", data, user_name, pfp, amount, item_data=item_data, itemname=itemname)
    unrelated.save_data(data)
    await ctx.send(embed=embed)

bot.remove_command("help")

@bot.command(name="help", description="Help? Help? Help!")
async def custom_help(ctx):
    embed = discord.Embed(
        title="📘 Help Menu",
        description="Here’s everything your fragile human brain can run:",
        color=discord.Color.blurple()
    )

    for command in bot.commands:
        embed.add_field(name=f"`{command.name}`", value=command.help or "No description.", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="daily", description= "Get your daily reward!")
async def daily(ctx):
    data = unrelated.load_data()[0]
    user_id = str(ctx.author.id)
    user_name = str(ctx.author.name)
    pfp = str(ctx.author.display_avatar.url)
    get_user_data(user_id, data)
    embed = unrelated.perform_action(user_id, "daily", data, user_name, pfp)
    unrelated.save_data(data)
    await ctx.send(embed=embed)








def get_user_data(user_id, data):
    if user_id not in data:
        data[user_id] = {
            'pocket': 1000,
            'level': 1,
            'xp': 0,
            'inventory': {"Apple": 3},
            'bank': 0,
            'bank_limit': 2000,
            'job': 'None',
            'last_worked': 0,
            'last_daily': 0,
            'buffs': {'xp': [], 'coin': []}


        }
    return data[user_id]


        
        











''' Daily, TTT, fortune, transform, quote, leaderboard, duel, heist, jail function, make better embeds, add shovel durability'''



    







with open('token.txt', 'r') as f:
    token = f.read().strip()

bot.run(token)










