import requests
JOKE_API = "https://v2.jokeapi.dev/joke/Any"

class Joke():
    def __init__(self,category,type,**kwargs) -> None:
        self.category=category
        self.joke_type=type
        if self.joke_type=="single":
            self.joke=kwargs["joke"]
        elif self.joke_type=="twopart":
            new_line="\n"
            joke=f"Q. {kwargs['setup']} \n  A: {kwargs['delivery']}"
            self.joke=joke


def get_dad_joke():
  headers={
    "Accept":"text/plain"
  }
  url="https://icanhazdadjoke.com/"
  joke=requests.get(url=url,headers=headers).text
  return f"Joke:\n{joke}"

def get_jokes(num):
    param={"amount":num}
    joke_objects=[]
    if num!=1:
        jokes = requests.get(url=JOKE_API,params=param).json().get("jokes")
    else:
      jokes = [requests.get(url=JOKE_API,params=param).json()]
    for joke in jokes:
        category=joke["category"]
        type=joke["type"]
        setup=joke.get("setup")
        delivery=joke.get("delivery")
        joke=joke.get("joke")
        joke_obj=Joke(category=category,type=type,setup=setup,delivery=delivery,joke=joke)
        joke_objects.append(joke_obj)
    return joke_objects