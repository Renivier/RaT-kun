import json
import random
import discord
from num2words import num2words
import asyncio
import time

DATA_FILE = 'data.json'
item_data = 'item_data.json'
JOB_DATA = 'work_list.json'


class Shop():
    def execute(self, user_id, data, user_name, pfp=None, amount=None, **kwargs):
        title = f"All Items In The Bot"
        description = "\n\n".join(
        f"{item} ---> {info['Value']} Coins" 
        for item, info in data.items()
        )
        color = discord.Color.purple()
        return embed_maker(title, description, color, pfp)
    
class Item():
    def execute(self, user_id, data, user_name, item_data, itemname, **kwargs):
        item_use = item_data.get(itemname)["use"]
        price = item_data.get(itemname)["Value"]
        item_description = item_data.get(itemname)["description"]
        use_effects = "\n".join(f"{k}:{v}" for k, v in item_use.items()) if item_use else "None" 
        title = itemname
        description = f"You can buy this item for {price} coins, \n\nItem description: {item_description}. \n\n(JK)\n{use_effects}"
        color = discord.Color.purple()
        return(embed_maker(title, description, color))


class Duel():
    def execute(self, user_id1, data, user_name1, pfp1=None, amount=None, user_id2=None, user_name2=None, pfp2=None):
        pass


class Gamble():
    def execute(self, user_id, data, user_name, pfp=None, amount=None, **kwargs):
        if amount <= data[user_id]['pocket']:
            if random.random() < 0.5:
                data[user_id]['pocket'] += amount * get_multiplier(user_id, data, 'coin')
                title = f"{user_name} won the gamble!"
                description = f"You won {amount * get_multiplier(user_id, data, 'coin')} coins!\n\nYour pocket balance is now {data[user_id]['pocket']} coins."
                color = discord.Color.green()
            else:
                data[user_id]['pocket'] -= amount
                title = f"{user_name} lost the gamble!"
                description = f"You lost {amount} coins!\n\nYour pocket balance is now {data[user_id]['pocket']} coins."
                color = discord.Color.red()
        else:
            title = "Gamble Failed"
            description = "You don't have enough coins to gamble that amount!"
            color = discord.Color.red()
            
        return embed_maker(title, description, color, pfp)


class Beg():
    def execute(self, user_id, data, user_name, pfp=None, amount=None, **kwargs):
        if random.random() < 0.65:
            amount = random.randint(11, 874)
            data[user_id]['pocket'] += amount * get_multiplier(user_id, data, 'coin')
            lines = read_file_lines('win_beg.txt')
            title = f"{user_name} begged like an Indian!"
            description = (f'{random.choice(lines).format(x=amount)} You won {amount*get_multiplier(user_id, data, "coin")} coins.\n\nYour pocket balance is now {data[user_id]["pocket"]} coins.')
            color = discord.Color.green()
        else:
            title =f"{user_name} couldn't even beg properly!"
            lines = read_file_lines('lose_beg.txt')
            description = (f"{random.choice(lines)}\n\nYour balance is now {data[user_id]['pocket']} coins.")
            color = discord.Color.red()
        return embed_maker(title, description, color, pfp)
    

class Balance():
    def execute(self, user_id, data, user_name, pfp=None, **kwargs):
        title = f"{user_name.capitalize()}'s Balance"
        description = f"You have {data[user_id]['pocket']} coins.\n\nBank: {data[user_id]['bank']}/{data[user_id]['bank_limit']}"
        color = discord.Color.blue()
        return embed_maker(title, description, color, pfp)
    

class Deposit():
    def execute(self, user_id, data, user_name, pfp=None, amount=None, **kwargs):
        max_deposit = (data[user_id]['bank_limit']) - (data[user_id]['bank'])
        if data[user_id]['pocket'] <= 0 or data[user_id]['bank'] >= data[user_id]['bank_limit']:
            title = "Deposit Failed"
            description = "Check your balance lil' bro"
            color = discord.Color.red()
            return embed_maker(title, description, color, pfp)
        else:
            if max_deposit < amount:
                title = "Deposit Failed"
                description = "You can't deposit that much!"
                color = discord.Color.red()
                return embed_maker(title, description, color, pfp)
            elif max_deposit >= amount and data[user_id]['pocket'] >= amount:
                data[user_id]['pocket'] -= amount
                data[user_id]['bank'] += amount
                title = "Deposit Successful"
                description = f"You have deposited {amount} coins.\n\nNew Pocket Balance: {data[user_id]['pocket']} coins.\nNew Bank Balance: {data[user_id]['bank']}/{data[user_id]['bank_limit']} coins."
                color = discord.Color.green()
            return embed_maker(title, description, color, pfp)
    

class Withdraw():
    def execute(self, user_id, data, pfp=None, amount=None):
        max_withdraw = data[user_id]['bank']
        if data[user_id]['bank'] <= 0:
            title = "Withdraw Failed"
            description = "Check your balance lil' bro"
            color = discord.Color.red()
        else:
            if max_withdraw < amount:
                title = "Withdraw Failed"
                description = "You can't withdraw that much!"
                color = discord.Color.red()
            elif max_withdraw >= amount:
                data[user_id]['bank'] -= amount
                data[user_id]['pocket'] += amount
                title = "Withdraw Successful"
                description = f"You have withdrawn {amount} coins.\n\nNew Pocket Balance: {data[user_id]['pocket']} coins.\nNew Bank Balance: {data[user_id]['bank']}/{data[user_id]['bank_limit']} coins."
                color = discord.Color.green()
        return embed_maker(title, description, color, pfp)
        

class Rob():
    def execute(self, user_id, data, user_name, pfp=None, amount=None, user_id2=None, user_name2=None, **kwargs):
        success_chance = 0.4
        if data[user_id2]['pocket'] < 1000:
            title = "Robbery Failed"
            description = "The target is poor af, look for someone richer!"
            color = discord.Color.red()
        if random.random() < success_chance:
            steal_amount = random.randint(100, data[user_id2]['pocket'])
            title = f"Robbery Successful!"
            description = f"You successfully robbed {steal_amount} coins from {user_name2}!\n\nYour new pocket balance is {data[user_id]['pocket'] + steal_amount} coins."
            color = discord.Color.green()
            data[user_id]['pocket'] += steal_amount
            data[user_id2]['pocket'] -= steal_amount
        else:
            title = "Robbery Failed!"
            lines = read_file_lines('lose_rob.txt')
            description = f"{random.choice(lines)}\n\nYou got caught trying to rob {user_name2} and lost {int(data[user_id]['pocket'] * 0.15)} coins as a fine!\n\nYour new pocket balance is {data[user_id]['pocket']} coins."
            color = discord.Color.red()
            data[user_id]['pocket'] = int(data[user_id]['pocket'] * 0.85)
        return embed_maker(title, description, color, pfp)


class Buy():
    def execute(self, user_id, data, user_name, pfp=None, item_data=None, itemname=None, amount=1, **kwargs):
            if amount <= 0 or itemname not in item_data:
                title = "Buying was not successful"
                description = "Make sure the amount is above 0 and item_name is spelled correctly; example; uwu buy 1 apple"
                color = discord.Color.red()
            elif (item_data[itemname]['Value']*amount) > data[user_id]['pocket']:
                title = "Buying was not successful"
                description = "You're poor af, go beg or something..."
                color = discord.Color.red()
            else:
                data[user_id]['pocket'] -= (item_data[itemname]['Value'] * amount)
                if itemname in data[user_id]['inventory']:
                    data[user_id]['inventory'][itemname] += amount
                else:
                    data[user_id]['inventory'][itemname] = amount
                title  = f"Buying Successful!"
                description = f"You have successfully bought {amount} {itemname}s!"
                color = discord.Color.green()
            return embed_maker(title, description, color)
    

class Sell():
    def execute(self, user_id, data, user_name, pfp, amount, **kwargs):
        item_data = kwargs.get('item_data', None)
        itemname = kwargs.get('itemname', None)
        if itemname is None:
            title = "Selling failed!"
            description = f"You couldn't sell properly because the item doesnt exist, check your spelling!"
            color = discord.Color.red()
            return(title, description, color, pfp)
        if amount > data[user_id]['inventory'].get(itemname, 0):
            title = "Selling failed!"
            description = f"You couldn't sell properly cause you don't have that many items, you idiot!"
            color = discord.Color.red()
            return(title, description, color, pfp)
        else:
            sell_price = amount * (item_data[itemname].get('Value') * 0.7)
            data[user_id]['pocket'] += sell_price * get_multiplier(user_id, data, 'coin')
            data[user_id]['inventory'][itemname] -= amount
            title = "Sold successfully!"
            description = f"You have successfully sold {amount} {itemname}(s) for{sell_price}!"
            color = discord.Color.green()
            if data[user_id]['inventory'][itemname] <= 0:
                del data[user_id]['inventory'][itemname]
        return embed_maker(title, description, color, pfp)


class Slots():
    def execute(self, user_id, data, user_name, pfp, amount, **kwargs):
            num1, num2, num3 = [random.randint(0, 5) for _ in range(3)]
            num1 = num2words(num1)
            num2 = num2words(num2)
            num3= num2words(num3)
            if amount > data[user_id]['pocket']:
                title = "Slots Failed"
                description = "You don't have enough money to bet that much!"
                color = discord.Color.red()
                return embed_maker(title, description, color, pfp)
            data[user_id]['pocket'] -= amount
            if num1 == num2 == num3:
                title = "You won, somehow..."
                description = f":{num1}: :{num2}: :{num3}: \nHoly shark, you just won {3*amount*get_multiplier(user_id, data, 'coin')} coins!"
                color = discord.Color.green()
                data[user_id]['pocket'] += amount * 3 * get_multiplier(user_id, data, 'coin')
            elif num1 == num2 or num1 == num3 or num2 == num3:
                data[user_id]['pocket'] += int(amount * 1.5 * get_multiplier(user_id, data, 'coin'))
                title = "Not bad? I guess.."
                description = f":{num1}: :{num2}: :{num3}: \nWell, you didn't lose anything, ykw, get a 1.5x. You won {int(1.5*amount*get_multiplier(user_id, data, 'coin'))} coins.\n\nNew Pocket Balance: {data[user_id]['pocket']} coins."
                color = discord.Color.pink()
            else:
                title = "L bro."               
                description = f":{num1}: :{num2}: :{num3}: \nSkil issue tbh, you lost everything, even your children. \n\nNew Pocket Balance: {data[user_id]['pocket']}"
                color = discord.Color.red()
            return embed_maker(title, description, color, pfp)


class Inventory():
    def execute(self, user_id, data, user_name, pfp=None, **kwargs):
        title = f"{user_name}'s inventory"
        description = "\n".join(f"**{item}**-------> **{amount}**" for item, amount in data[user_id]['inventory'].items())
        color = discord.Color.pink()
        return embed_maker(title, description, color, pfp)
    

class Dig():
    def execute(self, user_id, data, user_name, pfp, item_data = item_data, **kwargs):
        amount = random.randint(1, 1793)
        chance = random.random()
        if "Shovel" not in data[user_id]['inventory']:
            title = "Can't even dig..."
            description = "You need to buy a shovel first bro"
            color = discord.Color.red()
            return embed_maker(title, description, color, pfp)
        if chance < 0.5 and chance >= 0.2:
            data[user_id]['pocket'] += amount * get_multiplier(user_id, data, 'coin')
            title = "Successfully Dug."
            description = f"You have successfully dug and found {amount} coins!\nYour new pocket balance is {data[user_id]['pocket']}"
            color = discord.Color.purple()
        elif chance < 0.2 and chance > 0.1:
            item = random.choice(list(item_data))
            item_append(user_id, data, item)
            data[user_id]['pocket'] += amount * get_multiplier(user_id, data, 'coin')
            data[user_id]['inventory'][item] += 1
            title = "Successfully dug!"
            description = f"You have successfully dug and found 1x {item} and {amount} coins!"
            color = discord.Color.pink()
        elif chance < 0.1:
            item = random.choice(list(item_data))
            item_append(user_id, data, item)
            data[user_id]['pocket'] += amount * get_multiplier(user_id, data, 'coin')
            data[user_id]['inventory'][item] += 2
            title = "Successfully dug!"
            description = f"You have successfully dug and found 2x {item} and {amount} coins!"
            color = discord.Color.green()
        else:
            title = "Skill Issues bro"
            description = f"You can't even dig, while cavemen can..."
            color = discord.Color.red()
        return embed_maker(title, description, color, pfp)


class Dice():
    def execute(self, user_id, data, user_name, pfp, amount, **kwargs):
        if amount > data[user_id]['pocket']:
            title = 'Command failed'
            description = "You're too poor to bet that much..."
            color = discord.Color.red()
            return embed_maker(title, description, color, pfp)
        else:
            roll = random.randint(1,6)
            data[user_id]['pocket'] -= amount

            multiplier = max(0, (roll - 1) * 0.5)
            coin_multiplier = get_multiplier(user_id, data, 'coin')
            data[user_id]['pocket'] += int(amount * multiplier * coin_multiplier)
            if multiplier == 3:
                title = "Jackpot!!!"
                description = f"You rolled the dice :game_die: {roll} and won {(amount * multiplier) - amount} coins, Lucky tbh.\nYour new balace is {data[user_id]['pocket']}coins"
                color = discord.Color.green()
            elif multiplier == 1:
                title = "Really?"
                description = f"You rolled the dice :game_die: {roll} ... For absolutely nothing, your bal didnt change,\nYour balance is {data[user_id]['pocket']} coins..."
                color = discord.Color.purple()
            elif multiplier > 1:
                title = "Not bad!"
                description= f"You rolled the dice :game_die: {roll} and won {(amount * multiplier) - amount} coins! \nYour new balace is {data[user_id]['pocket']}coins"
                color = discord.Color.green()
            else:
                title = "L"
                description = f"You rolled :game_die: {roll} and lost {amount - (amount * multiplier)} coins"
                color = discord.Color.red()
            return embed_maker(title, description, color, pfp)


class Profile():
    def execute(self, user_id, data, user_name, pfp, **kwargs):
        user_data = data[user_id]
        title = f"# {user_name}'s Profile"
        description = f"* **Pocket Balance**: `{user_data['pocket']}`\n* **Bank:** `{user_data['bank']}/{user_data['bank_limit']}`\n* **Level:** `{user_data['level']}`\n* **Xp:** `{user_data['xp']}`\n * **Job:** `{user_data['job']}`"
        color = discord.Color.green()
        return embed_maker(title, description, color, pfp)
    

class Jobs():
    def execute(self, JOB_DATA, pfp):
        title = "Job List"
        description = "\n\n".join(
            f"**{job}** — Pay: `{JOB_DATA[job]['pay']}`, Required Level: `{JOB_DATA[job]['req_level']}`"
            for job in JOB_DATA)
        color = discord.Color.pink()
        return embed_maker(title, description, color)


class Job_Pick():
    def execute(self, user_id, job_name, data, pfp):
        pay, required_level = job_data(job_name)
        if data[user_id]['level'] < required_level:
            title= "Job Picking Failed"
            description = "You couldn't pick this job due to your level not being enough."
            color = discord.Color.red()
        else:
            data[user_id]['job'] = job_name
            title = "Job Picking Successful"
            description = f"You have successfully picked the {job_name} job!\n\nYour payment is now {pay} coins per work!"
            color = discord.Color.green()
        return embed_maker(title, description, color, pfp)
        

class Work():
    def execute(self, user_id, data, user_name, pfp, **kwargs):
        now = time.time()
        job_name = data[user_id]['job']
        pay = job_data(job_name)[0]
        if now - data[user_id]['last_worked'] >= 3600:
            data[user_id]['last_worked'] = now
            data[user_id]['pocket'] += (pay * get_multiplier(user_id, data, 'coin'))
            title = f"{user_name} successfully worked!"
            description = f"You worked and got {pay} coins!\n\nYou can work again in 1 hour!"
            color = discord.Color.green()
        else:
            remaining = 3600- (now-data[user_id]['last_worked'])
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            title = f"Whoa, chill out!"
            description = f"Chill out bro! You can work again in {minutes} minutes and {seconds} seconds!"
            color = discord.Color.red()
        return embed_maker(title, description, color, pfp)


class Study():
    def execute(self, user_id, data, user_name, pfp, **kwargs):
        if data[user_id]['pocket'] < 4000:
            title = "Failed to study"
            description = "Study is like a converter, you pay money for teachers to gain EXP. 4000 is needed."
            color = discord.Color.red()
        else:
            req_exp = level_up(user_id, data)
            amount = round(req_exp * 0.3)
            data[user_id]['pocket'] -= 4000
            data[user_id]['xp'] += amount
            level_up(user_id, data)
            title = "Studied Successfully!"
            description = f"You have successfully studied, gained {amount} xp!"
            color = discord.Color.green()
        return embed_maker(title, description, color, pfp)


class Use():
    def execute(self, user_id, data, user_name, pfp, amount, item_data, itemname, **kwargs):
        now = time.time()
        item_info = item_data.get(itemname, {})
        use_info = item_info.get("use", {})

        if itemname not in data[user_id]['inventory'] or data[user_id]['inventory'][itemname] < amount:
            return embed_maker("Failed to Use", f"You don't have that many {itemname}s!", discord.Color.red(), pfp=pfp)
        
        if itemname == "Bank Note":
            e = 2000 * amount 
            data[user_id]['bank_limit'] += e
            data[user_id]['inventory'][itemname] -= amount
            if data[user_id]['inventory'][itemname] <=  0:
                del data[user_id]['inventory'][itemname]
            return embed_maker("Successfully used!", f"You successfully used {amount} Bank Notes to improve your storage by {e}", discord.Color.green(), pfp=pfp)

        

        if not use_info:
            return embed_maker("Item Not Used!", "That item is not usable bro...", discord.Color.red(), pfp=pfp)

        data[user_id]['inventory'][itemname] -= amount
        if data[user_id]['inventory'][itemname] <= 0:
            del data[user_id]['inventory'][itemname]

        xp_buff = use_info.get('xp_buff', 0)
        coin_buff = use_info.get('amount_buff', 0)
        duration = use_info.get("duration", 0)
        


        if xp_buff:
            matched = False
            for index, (buff, start_time, buff_duration) in enumerate(data[user_id]['buffs']['xp']):
                if buff == xp_buff:
                    data[user_id]['buffs']['xp'][index][2] += duration
                    matched = True
                    break
            if not matched:
                data[user_id]['buffs']['xp'].append([xp_buff, now, duration])

        if coin_buff:
            matched = False
            for index, (buff, start_time, buff_duration) in enumerate(data[user_id]['buffs']['coin']):
                if buff == coin_buff:
                    data[user_id]['buffs']['coin'][index][2] += duration
                    matched = True
                    break
            if not matched:
                data[user_id]['buffs']['coin'].append([coin_buff, now, duration])

        return embed_maker(
            "Successfully Used!", 
            f"{user_name} has successfully used {amount} {itemname}(s)!", 
            discord.Color.green(), 
            pfp
        )
    
class Daily():
    def execute(self, user_id, data, user_name, pfp, **kwargs):
        now = time.time()
        if now - data[user_id]['last_daily'] >= 3600*24:
            data[user_id]['last_daily'] = now
            data[user_id]['pocket'] += 10000
            title, description, color = f"Successfully used daily.", f"You used daily and got 10000 coins!", discord.Color.green()
        else:
            remaining = 3600*24 - (now - data[user_id]['last_daily'])
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            seconds = int(remaining % 60)
            title, description, color = f"Failed to use daily", f"You couldn't use daily because of the cooldown,\nTime left: {hours} hours, {minutes} minutes and {seconds} seconds!", discord.Color.red()
        return embed_maker(title, description, color, pfp)
    
        

Classes = {
    "beg": Beg(),
    "bal": Balance(),
    "dig": Dig(),
    "deposit": Deposit(),
    "withdraw": Withdraw(),
    "shop": Shop(),
    "gamble": Gamble(),
    "rob": Rob(),
    "item":Item(),
    "buy" : Buy(),
    "sell": Sell(),
    "inventory": Inventory(),
    "slots": Slots(),
    "dice": Dice(),
    "profile": Profile(),
    "work": Work(),
    "study": Study(),
    "use": Use(),
    "daily": Daily(),
}
xp_classes = {
    "dig": 40,
    "beg": 30,
    "rob": 60, 
    "buy": 20,
    "sell": 15,
    "gamble": 80,
    "dice": 50,
    "work": 60,
    "slots": 55,
    "daily": 40
}


def perform_action(user_id, func, data, user_name, pfp=None, amount=None, user_id2=None, user_name2=None, pfp2=None, item_data=None, itemname=None):
    if func in xp_classes:
        base_xp = xp_classes[func]
        xp_multi = get_multiplier(user_id, data, 'xp')
        data[user_id]['xp'] += base_xp * xp_multi
        level_up(user_id, data)


    if func in Classes:
        result = Classes[func].execute(
        user_id=user_id,
        data=data,
        user_name=user_name,
        pfp=pfp,
        amount=amount,
        user_id2=user_id2,
        user_name2=user_name2,
        pfp2=pfp2,
        item_data=item_data,
        itemname=itemname
        )

    else:
        result = "Invalid action, perhaps you need some guidance due to your illiteracy?"



    return result


def embed_maker(func_title, func_description, func_color, pfp=None, **kwargs):
    embed = discord.Embed(title=func_title, description=func_description, color=func_color)
    if pfp:
        embed.set_thumbnail(url=pfp)
    return embed


def read_file_lines(file_name):
    try:
        with open(file_name, 'r', encoding = "utf8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        return []


def save_data(dictionary):
    with open(DATA_FILE, 'w', encoding='utf8') as f:
        json.dump(dictionary, f, indent=4)


def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf8') as f:
            dictionary = json.load(f)
            if not dictionary:
                dictionary = {}
        with open(item_data, 'r', encoding='utf8') as f:
            item_dictionary = json.load(f)
            if not item_dictionary:
                item_dictionary = {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, {}
    return dictionary, item_dictionary


def job_list():
    try:
        with open('work_list.json', 'r', encoding='utf8') as f:
            jobs = json.load(f)
            if not jobs:
                jobs = {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return jobs


def job_data(job_name):
    try:
        with open('work_list.json', 'r', encoding='utf8') as f:
            jobs = json.load(f)
            if job_name not in jobs:
                return "Job Not Found, you should use the keyboard more often bro"
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error while fetching the data"
    return jobs[job_name]['pay'], jobs[job_name]['req_level']


def level_up(user_id, data):
    required_xp = int(1000 * (1.1 ** (data[user_id]['level'] - 1)))
    while data[user_id]['xp'] >= required_xp:
        data[user_id]['xp'] -= required_xp
        data[user_id]['level'] += 1
        required_xp = int(1000 * (1.1 ** (data[user_id]['level'] - 1)))
    return required_xp


def item_append(user_id, data, item):
    if item not in data[user_id]['inventory']:
        data[user_id]['inventory'][item] = 0



def get_multiplier(user_id, data, buff_type):
    now = time.time()
    total = 1
    active_buffs = []
    for multi, start, duration in data[user_id]['buffs'].get(buff_type, []):
        if now - start <= duration:
            total *= multi 
            active_buffs.append((multi, start, duration))
    data[user_id]['buffs'][buff_type] = active_buffs
    return total





