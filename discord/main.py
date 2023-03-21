import os, requests, random
import discord
from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive
from get_joke import get_dad_joke, get_jokes
from basic_functions import *
from country import Country

TOKEN = ""


def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} has logged in.")

    @bot.command(name="random", aliases=["rand"])
    async def rand_func(ctx: commands.Context, limit=100):
        """returns random number within given limit number"""
        await ctx.reply(random.randint(0, int(limit)), mention_author=True)

    @bot.command(name="quote", aliases=["q"])
    async def quote_func(ctx):
        """gives a random quote"""
        quote = get_quote()
        await ctx.reply(quote, mention_author=True)

    @bot.command(name="calc", aliases=["cal"])
    async def calc_func(ctx, expr=str(0)):
        """Gives result after calculating the given mathematical expression"""
        result = calculate(expr)
        await ctx.reply(result, mention_author=True)

    @bot.command(name="cat", aliases=["cutie"])
    async def cat_func(ctx, num=1):
        """Returns required no of cat images"""
        url = "https://api.thecatapi.com/v1/images/search"
        image_list = img(url=url, limit=int(num))
        for _image in image_list:
            await ctx.reply(_image, mention_author=True)

    @bot.command(name="dog", aliases=["doggie"])
    async def dog_func(ctx, num=1):
        """Returns required no of dog images"""
        url = "https://api.thedogapi.com/v1/images/search"
        image_list = img(url=url, limit=int(num))
        for _image in image_list:
            await ctx.reply(_image, mention_author=True)

    @bot.command(name="fox", aliases=["foxie"])
    async def fox_func(ctx):
        """Returns  a random fox image"""
        image = requests.get(url="https://randomfox.ca/floof/").json().get("image")
        await ctx.reply(image, mention_author=True)

    @bot.command(name="qr", aliases=["qrcode"])
    async def qr_func(ctx: commands.Context, data=f"Hello World"):
        """Returns qr image of given query"""
        url = f"https://qrickit.com/api/qr.php?d={data.replace(' ','%20')}"
        await ctx.reply(url, mention_author=True)

    @bot.command(name="meme")
    async def meme_func(ctx, num=1):
        """Returns memes from subreddits"""
        data_dict = meme(num)
        for index in range(len(data_dict)):
            dict = data_dict[index]
            meme_msg = f"Title:  {dict.get('title')} \n Subreddit:  {dict.get('subreddit')}\nPostlink:  {dict.get('link')}\n---MeMe---\n{dict.get('image')}"
            await ctx.reply(meme_msg, mention_author=True)

    @bot.command(name="bored")
    async def bored_func(ctx, type="", num=1):
        """Returns a no of things to do while bored"""
        bored_msg = ""
        type_list = os.getenv("activity_types")
        if type == "":
            type = random.choice(type_list)
        else:
            for _type in type_list:
                if type == _type[0:3]:
                    type = _type
        bored_msg = bored(type=type, num=num)
        await ctx.reply(bored_msg, mention_author=True)

    @bot.command(name="fact")
    async def fact_func(ctx, var=""):
        """Returns a random fact. \nUse tod to get fact of the day"""
        var = "today" if var == "tod" else "random"
        url = f"https://uselessfacts.jsph.pl/{var}.json?language=en"
        fact = requests.get(url).json()
        text = str(fact.get("text"))
        link = shorten_url(fact.get("permalink"))
        await ctx.reply(f"Fact:\n{text}\n {link}")

    @bot.command(name="dadjoke", aliases=["djk"])
    async def dad_joke(ctx):
        """Returns a dad joke"""
        await ctx.reply(get_dad_joke(), mention_author=True)

    async def chuck_func(ctx):
      """Returns chuck norris joke with icon"""
      icon, joke = chuck()
      await ctx.reply(f"{icon}\nJoke:\n{joke}", mention_author=True)

    @bot.command(name="joke", aliases=["jk"])
    async def joke_func(ctx, num=1):
        """Gives a list of jokes including category"""
        jokes_msg = ""
        jokes = get_jokes(num=num)
        for index, joke in enumerate(jokes):
            joke_msg = f"\nCategory:{joke.category}\n{joke.joke}\n"
            jokes_msg += joke_msg
        await ctx.reply(jokes_msg, mention_author=True)

    @bot.command(name="pdf", aliases=["html2pdf"])
    async def pdf_func(ctx, url="google.com"):
        """Returns pdf of given url"""
        await ctx.reply(get_pdf(url), mention_author=True)

    @bot.command(name="shorten")
    async def shorten_func(ctx, url="google.com"):
        """Shortens the given url"""
        await ctx.reply(shorten_url(url), mention_author=True)

    @bot.command(name="poke", aliases=["pk"])
    async def poke_func(ctx, name="pikachu"):
        """Returns image and pic of pokemon"""
        await ctx.reply(pokemon(name), mention_author=True)

    @bot.command(name="country", aliases=["coun"])
    async def country_func(ctx, names="Japan-Korea"):
        """Returns details of countries"""
        names = names.split("-")
        for i, name in enumerate(names):
            await ctx.reply(
                Country(name=name, type="country", url_var="name").message,
                mention_author=True,
            )

    @bot.command(name="cc", aliases=["capcity"])
    async def cap_city_func(
        ctx,
        names="Kathmandu-New Delhi",
    ):
        """Returns details of country with given capital city"""
        names = names.split("-")
        for i, name in enumerate(names):
            await ctx.reply(
                Country(name=name, type="capital city", url_var="capital").message,
                mention_author=True,
            )

    @bot.command(name="news")
    async def news_func(ctx, query="tesla", num=1):
        """Returns news of given query within given limits"""
        news = News(num=int(num), query=query)
        news_messages = news.messages
        for news_msg in news_messages:
            await ctx.reply(news_msg, mention_author=True)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
