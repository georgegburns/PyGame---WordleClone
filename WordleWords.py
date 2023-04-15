
f = open('5letterwords.txt', 'r')
WORDS = []
CONTENT = f.readlines()
for word in CONTENT:
    word = word.strip('\n')
    word = word.upper()
    WORDS.append(word)

def checkWord(word : str):
    if word in WORDS:
        return True
    return False

def enterWord(word : str, lst: list):
    lst.append([char for char in word])
    return lst