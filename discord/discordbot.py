import os, requests, random
import discord

TOKEN = "MTA2OTQ0NjcxODMwOTAxOTY2OQ.GLp-Gl.syrgfNcggzZa5MTVaf5RODLG6CxE8nw-k8bRu0"

sad_words = [
    "Down",
    "Somber",
    "Despondent",
    "Downcast",
    "Heartsick",
    "Dejected",
    "Glum",
    "Pensive",
    "Blue",
    "Pessimistic",
    "Wretched",
    "Miserable",
    "Hurting",
    "Heartbroken",
    "Dismal",
    "Grieved",
    "Forlorn",
    "Distraught",
    "Distressed",
    "On edge",
    "Sorry",
    "Morose",
    "Out of sorts",
    "Melancholy",
    "Doleful",
    "Sorrowful",
    "Tearful",
    "Morbid",
    "Languishing",
    "Troubled",
    "Unhappy",
    "Upset",
    "Wistful",
    "Weeping",
    "Depressed",
    "Gloomy",
    "Cheerless",
    "Frustrated",
    "In grief",
    "Disheartened",
    "Bitter",
    "Mournful",
]
encourage = [
    "You're never far from my thoughts.",
    "Know how often I think of you? Always.",
    "You're on my mind and in my heart.",
    "Keeping you close in my thoughts.",
    "Lifting you up in prayer and hoping you have a better day today.",
    "I can't wait to catch up with you soon.",
    "Just wanted you to know you're on my mind and in my prayers.",
    "I'm thinking of you. And I'm just a text or phone call away.",
    "It's okay not to be okay.",
    "Your pain is valid. I'm here if you need someone to listen.",
    "No wise words or advice here. Just me. Thinking of you. Hoping for you. Wishing you better days ahead.",
    "I don't know what depression feels like, and wish with all my heart that you didn't have to know, either.",
    "I'm so sorry you're experiencing a setback. I don't know what to say, except that care about you, and I'm here for you.",
    "We've got friends for our happiest days and saddest moments. I hope you know I'm your friend now just as much as ever.",
    "If you ever need to talk, or just cry, I'm your gal.",
    "I'm not sure what's most helpful right now, but I figure a card with a cute kitten on it couldn't hurt, right? ☺ Thinking of you…",
    "Just wanted to say we miss you at work. Looking forward to a time when you're feeling much better.",
]


def calculate(expression):
    try:
        result = round(eval(expression), 2)
    except SyntaxError:
        result = f"Use signs properly"
    except ZeroDivisionError:
        result = f"Number can't be divided by zero(0)."
    return result


def bored(type, num):
    url = "https://www.boredapi.com/api/activity"
    not_available = "N/A"
    if type:
        url += f"?type={type}"
    bored_msg = ""
    for i in range(num):
        bored_activity = requests.get(url=url).json()
        type = bored_activity.get("type", not_available).title()
        activity = bored_activity.get("activity", not_available)
        people = bored_activity.get("participants", not_available)
        _message = f"\nIndex:{i+1}\nType: {type}\n Work: {activity}\nNo of people required: {people}\n"
        bored_msg += _message
    return bored_msg


def meme(num: int) -> list:
    url = f"https://meme-api.com/gimme/{num}"
    memes = requests.get(url=url).json().get("memes", "noooooo")
    images = [meme["url"] for meme in memes]
    links = [meme["postLink"] for meme in memes]
    subreddits = [meme["subreddit"] for meme in memes]
    titles = [meme["title"] for meme in memes]
    data_dict = {}
    for i in range(len(images)):
        dict = {
            "image": images[i],
            "link": links[i],
            "subreddit": subreddits[i],
            "title": titles[i],
        }
        data_dict[i] = dict
    return data_dict


def get_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url).json()
    quote = response[0]["q"]
    author = response[0]["a"]
    return f"{quote}\n--> {author}"


def image_func(url, limit: int):
    param = {"limit": limit}
    response = requests.get(url, params=param).json()
    images_list=[]
    for image in response:
        images_list.append(image.get("url"))
    return images_list



class MyClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        print(f"Your id is {self.user.id}")

    async def on_message(self, message):
        msg = message.content.lower().strip()
        if message.author.id == self.user.id:
            return
        if any(word.lower() in message.content for word in sad_words):
            print(True)
            await message.reply(random.choice(encourage), mention_author=True)
        if msg.startswith("$hello"):
            commands = """

    Checkout given commands!
    Note:Cases of commands doesnot matter!
        $hello: gives a list of comands with greeting!
        $calc : does basic calculations
        $meme <num>: gives <num> no of memes with extra details.
        $quote: gives random quote along with author name
        $bored <type> <num>: gives no of activites when you feel bored.
            """
            await message.reply(
                f"Hello {message.author}.\n How is it going?{commands}",
                mention_author=True,
            )
        if msg.startswith("$quote"):
            quote = get_quote()
            await message.reply(quote, mention_author=True)
        if msg.startswith("$calc"):
            expr = msg.split("$calc")[1].strip()
            result = calculate(expr)
            await message.reply(result, mention_author=True)
        if msg.startswith("$meme"):
            if msg != "$meme":
                num = msg.split("$meme")[1]
            else:
                num = 1
            data_dict = meme(int(num))
            for index in range(len(data_dict)):
                dict = data_dict[index]
                meme_msg = f"Title:  {dict.get('title')} \n Subreddit:  {dict.get('subreddit')}\nPostlink:  {dict.get('link')}\n---MeMe---\n{dict.get('image')}"
                await message.reply(meme_msg, mention_author=True)
        if msg.startswith("$cat"):
            url="https://api.thecatapi.com/v1/images/search"
            data=msg.strip().split()
            try:
                num=data[1]
            except IndexError:
                num=1
            image_list=image_func(url=url,limit=num)
            for image in image_list:
                await message.reply(image,mention_author=True)
        if msg.startswith("$dog"):
            url="https://api.thedogapi.com/v1/images/search"
            data=msg.split()
            try:
                num=data[1]
            except IndexError:
                num=1
            image_list=image(url=url,limit=num)
            for image in image_list:
                await message.reply(image,mention_author=True)
        if msg.startswith("$bored"):
            bored_msg = ""
            type_list = [
                "education",
                "recreational",
                "social",
                "diy",
                "charity",
                "cooking",
                "relaxation",
                "music",
                "busywork",
            ]
            data = msg.strip().split()
            if len(data) == 3 and data[2].isnumeric():
                type = data[1]
                for _type in type_list:
                    if type == _type[0:3]:
                        type = _type
                num = int(data[2])
                bored_msg = bored(type=type, num=num)

            elif len(data) <= 2:
                try:
                    num = data[1]
                except IndexError:
                    num = 1

                bored_msg = bored(type=False, num=int(num))

            await message.reply(bored_msg, mention_author=True)


intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)
