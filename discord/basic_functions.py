import requests,os

def calculate(expression):
  """Most basic algebric calculator"""
  try:
    result = round(eval(expression), 2)
  except SyntaxError:
    result = "Use signs properly"
  except ZeroDivisionError:
    result = "Number can't be divided by zero(0)."
  return result


def bored(type, num):
  """Uses bored API to get no of activities to do while bored"""
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
  """Uses meme API to fetch memes from Reddit"""
  url = f"https://meme-api.com/gimme/{num}"
  memes = requests.get(url=url).json().get("memes", "noooooo")
  images = [meme["url"] for meme in memes]
  links = [shorten_url(meme["postLink"]) for meme in memes]
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
  """Gives a random along with author from zenquotes API"""
  url = "https://zenquotes.io/api/random"
  response = requests.get(url).json()
  quote = response[0]["q"]
  author = response[0]["a"]
  return f"{quote}\n--> {author}"


def img(url, limit: int):
  """Gives back images of dog or cat using similar APIs"""
  param = {"limit": limit}
  response = requests.get(url, params=param).json()
  images_list = []
  for index, image in enumerate(response):
    if index < limit:
      images_list.append(image.get("url"))

  return images_list

def get_pdf(url):
  key=os.getenv("KEY")
  api_url=f"https://api.html2pdf.app/v1/generate?html={url}&apiKey={key}"
  return shorten_url(api_url)
def shorten_url(url):
  api_url="https://api.shrtco.de/v2/shorten"
  param={"url":url}
  response=requests.get(api_url,params=param).json().get("result")
  short_link=response.get("short_link")
  return f"https://{short_link}"

def pokemon(name):
  api_url=f"https://pokeapi.co/api/v2/pokemon/{name}"
  pokemon_data=requests.get(api_url).json()
  image=pokemon_data["sprites"].get("front_default")
  return f"Name:{name.title()}\nImage:\n{image}"

class News():
  def __init__(self,num,query) -> None:
    self.num=num
    self.query=query
    self.messages=self.get_news()
  def get_news(self):
    news_msg_list=[]
    API_KEY=os.getenv("NEWS_KEY")
    param={
      "q": self.query,
      "apiKey":API_KEY
    }
    api_url="https://newsapi.org/v2/everything"
    try:
      articles=requests.get(api_url,params=param).json().get("articles")
    except IndexError:
      news_msg_list.append("Given query is invalid for our bot.")
   
    else:
      try:
        for index,article in enumerate(articles):
          if index < self.num:
            source=article["source"].get("name","N/A")
            title=article.get("title")
            description=article.get("description")
            date=article.get("publishedAt")[:10]
            image=shorten_url(article.get("urlToImage"))
            link=shorten_url(article.get("url"))
            news_msg=f"Index:{index+1}/{self.num}\nTitle: {title}\n Source:{source}\nLink:{link}\nPublished:{date}\nNews:\n{description}\n{image}"
            news_msg_list.append(news_msg)
      except TypeError:
        news_msg_list.append("Something went wrong!")
    return news_msg_list

