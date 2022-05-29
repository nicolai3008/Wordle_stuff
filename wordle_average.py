import numpy as np 
import itertools
import time
from tqdm import tqdm
import matplotlib.pyplot as plt

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
            sol = sol + 'g'
        elif g_letters[i] in a_letters:
            a_count = answer.count(g_letters[i])
            g_count = answer.count(g_letters[i])
            if g_count > 1:
                green_count = 0
                for j in range(5):
                    if g_letters[j] == a_letters[j] and g_letters[j] == g_letters[i]:
                        green_count = green_count + 1
                if green_count == a_count:
                    sol = sol + 'b'
                else:
                    o += 1
                    if o <= a_count - green_count:
                        sol = sol + 'y'
                    else:
                        sol = sol + 'b'
            else:
                sol = sol + 'y'
        else:
            sol = sol + 'b'
    return sol

f = open('C:/Users/nicol/OneDrive - Danmarks Tekniske Universitet/Skrivebord/DTU - Fysik og Nano/Portfolio/Wordle/wordle-nyt-allowed-guesses.txt')
guesses = f.readlines()
for i in range(len(guesses)):
    guesses[i] = guesses[i].strip('\n')

f = open('C:/Users/nicol/OneDrive - Danmarks Tekniske Universitet/Skrivebord/DTU - Fysik og Nano/Portfolio/Wordle/wordle-nyt-answers-alphabetical.txt')
pa = f.readlines()
answers = []
for i in range(len(pa)):
    pa[i] = pa[i].strip('\n')
pa_copy = np.copy(pa)

sol = [''.join(i) for i in itertools.product('byg',repeat=5)]
y = len(sol)
x = len(guesses)
z = len(pa)


guess_start = input("Your guess: ")
n_total= np.zeros(z)
for q in tqdm(range(z)):
    time.sleep(0.00001)
    guess = guess_start
    pa = pa_copy
    answer = pa[q]
    n = 1
    while True:
        c = check(answer,guess)
        #print(guess,len(pa),c)
        if c == "ggggg":
            break
        else:
            n+=1
        possible_answers = np.array([])
        for k in range(len(pa)):
            c_temp = check(pa[k],guess)
            if c_temp == c:
                possible_answers = np.append(possible_answers,pa[k])
        pa = possible_answers
        E_array = np.zeros((x,y))
        for i in range(len(pa)):
            guess = pa[i]
            for j in range(len(pa)):
                answer = pa[j]
                c = check(answer,guess)
                k = sol.index(c)
                E_array[i,k] += 1
        E_array = E_array/len(pa)
        guess_E = np.zeros(len(pa))
        for i in range(len(pa)):
            E_i = E_array[i,:]
            s = 0
            for j in range(y):
                s += -E_i[j]*safe_log2(E_i[j])
            guess_E[i] += s
        ar = np.argsort(guess_E)
        guess_E = np.flip(np.sort(guess_E))
        guesses = np.flip(np.array(pa)[ar])

        guess = guesses[0]
    n_total[q] = n
plt.hist(n_total)
print(np.average(n_total))
plt.show()