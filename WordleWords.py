import requests as res
import bs4 as bs

URL =  "https://www.wordmom.com/5-letter-birds"
PAGE = res.get(URL)
HTML = PAGE.content
SOUP = bs.BeautifulSoup(HTML, 'html.parser')
WORDS = [word.text.upper() for word in SOUP.find_all('li') if len(word.text.strip()) == 5]
print(WORDS)

def checkWord(word : str):
    if word in WORDS:
        return True
    return False

def enterWord(word : str, lst: list):
    lst.append([char for char in word])
    return lst