import random

jokefile = open('./quantumjokes.txt', 'r')
jokes = [joke for joke in jokefile.readlines() if joke.strip()]

print(random.choice(jokes).strip())