import numpy as np 
import itertools
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from tkinter import *
import json

sol = [''.join(i) for i in itertools.product('⬛🟨🟩',repeat=5)]
y = len(sol)

def safe_log2(x):
    if x > 0:
        y = np.log2(x)
    else:
        y = 0
    return y

def check(answer,guess):
    a_letters = [i for i in answer]
    g_letters = [i for i in guess]
    sol = ''
    o = 0
    for i in range(len(g_letters)):
        if g_letters[i] == a_letters[i]:
            sol = sol + '🟩'
        elif g_letters[i] in a_letters:
            a_count = answer.count(g_letters[i])
            g_count = guess.count(g_letters[i])
            if g_count > 1:
                green_count = 0
                for j in range(5):
                    if g_letters[j] == a_letters[j] and g_letters[j] == g_letters[i]:
                        green_count = green_count + 1
                if green_count == a_count:
                    sol = sol + '⬛'
                else:
                    o += 1
                    if o <= a_count - green_count:
                        sol = sol + '🟨'
                    else:
                        sol = sol + '⬛'
            else:
                sol = sol + '🟨'
        else:
            sol = sol + '⬛'
    return sol


def entropy(guesses,pa):
    x = len(guesses)
    z = len(pa)
    E_array = np.zeros((x,y))
    for i in tqdm(range(x)):
        guess = guesses[i]
        for j in range(len(pa)):
            answer = pa[j]
            c = check(answer,guess)
            k = sol.index(c)
            E_array[i,k] += 1
        time.sleep(0.001)

    E_array = E_array/z
    guess_E = np.zeros(x)
    for i in range(x):
        E_i = E_array[i,:]
        s = 0
        for j in range(y):
            s += -E_i[j]*safe_log2(E_i[j])
        guess_E[i] += s

    ar = np.argsort(guess_E)
    guess_E = np.flip(np.sort(guess_E))
    guesses = np.flip(np.array(guesses)[ar])
    return guesses, guess_E

def limiting(pa,guess,c):
    print(len(pa))
    possible_answers = np.array([])
    for k in range(len(pa)):
        c_temp = check(pa[k],guess)
        if c_temp == c:
            possible_answers = np.append(possible_answers,pa[k])
    return possible_answers

def hard_mode(guesses,guess,c):
    possible_answers = np.array([])
    for k in range(len(guesses)):
        c_temp = check(guesses[k],guess)
        if c_temp == c:
            possible_answers = np.append(possible_answers,guesses[k])
    return possible_answers

f = open('C:/Users/nicol/OneDrive - Danmarks Tekniske Universitet/Skrivebord/DTU - Fysik og Nano/Portfolio/Wordle/wordle-nyt-allowed-guesses.txt')
guesses = f.readlines()
for i in range(len(guesses)):
    guesses[i] = guesses[i].strip('\n')
guesses = np.array(guesses)

f = open('C:/Users/nicol/OneDrive - Danmarks Tekniske Universitet/Skrivebord/DTU - Fysik og Nano/Portfolio/Wordle/wordle-nyt-answers-alphabetical.txt')
pa = f.readlines()
answers = []
for i in range(len(pa)):
    pa[i] = pa[i].strip('\n')
pa_copy = np.copy(pa)
for i in range(20):
        print('\n')
print("Preferred 1. guess: SOARE \n\n\n")
hard = int(input("Hard mode? (1/0)"))
print('\n\n\n')

freq_map = json.load(open('C:/Users/nicol/OneDrive - Danmarks Tekniske Universitet/Skrivebord/DTU - Fysik og Nano/Portfolio/Wordle/frequency.json'))
words = np.array(list(freq_map.keys()))
freqs = np.array([freq_map[w] for w in words])

guessed = []
possibilities = []
information = []
results = []
n = 0


while True:
    guess = input("{}. Guess: ".format(n+1))
    result = ((input("Result (b - black, y - yellow, g - green): ").replace('b', '⬛')).replace('y','🟨')).replace('g','🟩')
    guessed = np.append(guessed,guess)
    possibilities = np.append(possibilities,len(pa))
    information = np.append(information,np.log2(len(pa)))
    results = np.append(results,result)
    if result == '🟩🟩🟩🟩🟩' or len(pa) == 0:
        break
    for i in range(20):
        print('\n')
    np.delete(guesses,np.where(guesses == guess)[0])
    if hard == 1:
        guesses = hard_mode(guesses,guess,result)
    pa = limiting(pa,guess,result)
    print(pa)
    for i in range(3):
        print('\n')
    if len(pa) > 50:
        guesses, E = entropy(guesses,pa)
    else:
        guesses, E = entropy(pa,pa)
    for i in range(3):
        print('\n')
    print("Possibilities \t Information \t\t Guess -> Result")
    for i in range(len(guessed)):
        print(str(int(possibilities[i])) + '\t\t ' + str(np.round(information[i],3)) + '\t\t\t ' + str(guessed[i]) + ' -> '+str(results[i]))
    for i in range(1):
        print('\n')
    print("Guess \t Entropy \t Frequency")
    for i in range(7):
        try:
            print(str(guesses[i]) + '\t '+ str(E[i]) + '\t' + str(freqs[np.where(words == guesses[i])]))
        except IndexError:
            continue
    
    n += 1


for i in range(3):
    print('\n')
print("Final Results:")
print("Possibilites \t Information \t\t Guess -> Result")
for i in range(len(guessed)):
    print(str(int(possibilities[i])) + '\t\t ' + str(np.round(information[i],3)) + '\t\t\t ' + str(guessed[i]) + ' -> '+str(results[i]))
for i in range(2):
    print('\n')