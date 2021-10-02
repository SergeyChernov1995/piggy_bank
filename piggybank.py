# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------------
# PiggyBank
# Based on the game show project by Vladimir Khil aka Ur-Quan
# Copyright © 2021 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

import codecs
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
import configparser
from enum import Enum
from random import randrange, randint, choice
root = tk.Tk()
root.geometry("800x600")
root.title("Копилка")
root.resizable(width=False, height=False)
class pressed(Enum):
    no = 0
    yes = 1
    disable = 2

class canpressenter(Enum):
    no = 0
    yes = 1

#active = [1, 3, 6]
vvod = canpressenter.no
_button = pressed.disable
current_round = 0 #Должен быть 0
config = configparser.ConfigParser()
start_names = []
player = []
aux_list = []
baza = []
otvechaet = None
answerstring=""
time_up = False
money_final = []
with codecs.open('base.txt', "r", "utf_8_sig") as f:
    s = list(f)
for a in range(len(s)):
    s[a]=s[a].rstrip("\n")
for a in range(len(s)//2):
    b = {}
    b["Q"] = s[a*2]
    b["A"] = list(map(str, s[a*2+1].split(", ")))
    baza.append(b)
pole_voprosa = tk.Label(root,  width=55, height=5)
config.read('config.ini')
MAX_QUESTIONS_IN_ROUND = int(config['OPTIONS']['MAX_QUESTIONS_IN_ROUND'])
TIME_ROUND_IN_SECONDS = int(config['OPTIONS']['TIME_ROUND_IN_SECONDS'])
JACKPOT = int(config['OPTIONS']['JACKPOT'])
paliktas_laikas = TIME_ROUND_IN_SECONDS
paliktas_laikas_klausimui = 0
questions_asked_in_round = 0
questions_available_in_round = 0
pl_info = []
timer = tk.Label(root, justify = tkinter.CENTER, bg="#007fff", fg="#ffffff", wraplength = 40)
timer_1q = tk.Label(root, justify = tkinter.CENTER, bg="#ff7f7f", fg="#ffffff", wraplength = 40)
q_number_baza = 0
current_question_final = 0
winner = None
winner_sgor = 0
winner_nesgor = 0
def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()

def parse():
    config['OPTIONS'] = {'MAX_QUESTIONS_IN_ROUND': str(MAX_QUESTIONS_IN_ROUND),
                          'TIME_ROUND_IN_SECONDS': str(TIME_ROUND_IN_SECONDS),
                          'JACKPOT': str(JACKPOT)}
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)


def onKeyPress(event):
    global active, _button, aux_list, pl_info, test, otvechaet, vvod
    #print(event.char+": "+str(event.char.isalpha()))
    if (_button != pressed.no):
        pass
    elif (event.char not in set ('123456')):
        pass
    elif (aux_list[int(event.char)-1]['blocked_left']==0) and (aux_list[int(event.char)-1]['in_game']):
        #print(event.char)
        root.after_cancel(root.timer_question)
        guess.set("")
        _button = pressed.yes
        pl_info[int(event.char)-1]["bg"] = "#ffff8f"
        test.place(x=110, y=300)
        otvechaet = int(event.char)-1
        root.title(aux_list[int(event.char)-1]['name']+', дайте ответ')
        log.write("Отвечает "+aux_list[int(event.char)-1]['name']+'.\n')
        vvod = canpressenter.yes



def choose_a_question():
    global q_number_baza, baza, pole_voprosa, current_round
    q_number_baza = randint(0, len(baza)-1)
    pole_voprosa["text"] = baza[q_number_baza]["Q"]
    if (current_round<=5):
        for z in range(6):
            if (aux_list[z]["blocked_left"]>0):
                aux_list[z]["blocked_left"] -=1


def endgame():
    global vvod
    kopilka.place_forget()
    test.place_forget()
    pole_voprosa.place_forget()
    timer_1q.place_forget()
    vvod = canpressenter.no



def runda():
    global paliktas_laikas, time_up
    root.after_cancel(root.timer_round)
    paliktas_laikas -=1
    timer["text"] = time.strftime('%M:%S', time.gmtime(paliktas_laikas))
    if (paliktas_laikas==0):
        time_up = True
    else:
        root.timer_round = root.after(1000, runda)
    pass #napisat'

def pytanie():
    global paliktas_laikas_klausimui, timer_1q, current_round, q_number_baza, baza, _button, questions_asked_in_round, questions_available_in_round, current_question_final
    root.after_cancel(root.timer_question)
    paliktas_laikas_klausimui -=1
    timer_1q["text"] = str(paliktas_laikas_klausimui)
    if(current_round<=5):
        if (paliktas_laikas_klausimui==0):
            root.after_cancel(root.timer_question)
            _button = pressed.disable
            #print("Время вышло") #debug
            paliktas_laikas_klausimui = 10 * current_round
            tk.messagebox.showinfo("Никто не ответил", "Правильный ответ - "+baza[q_number_baza]["A"][0])
            log.write(tk.messagebox.showinfo("Никто не ответил. \nПравильный ответ - "+baza[q_number_baza]["A"][0])+'\n')
            questions_asked_in_round+=1
            check_if_endround()
        else:
            root.timer_question = root.after(1000, pytanie)
    else:
        if (paliktas_laikas_klausimui==0):
            root.after_cancel(root.timer_question)
            #print("Ответ принят") #debug
            #paliktas_laikas_klausimui = 10 * current_round
            check()
        else:
            root.timer_question = root.after(1000, pytanie)
    pass #napisat'

def check_if_endround():
    global questions_asked_in_round, questions_available_in_round, time_up, current_round, baza, q_number_baza, _button, JACKPOT
    if (questions_asked_in_round>=questions_available_in_round) or (time_up):
        tk.messagebox.showinfo("Раунд!", "Раунд №"+str(current_round)+' завершён.')
        log.write("Вопросы раунда закончились.\n")
        root.after_cancel(root.timer_round)
        _button = pressed.disable
        for a in range(6):
            aux_list[a]['blocked_left'] = 0
        pl_refresh()
        ka = aux_list.copy()
        log.write("Результаты: \n")
        eliminated = []
        for a in range(len(ka)):
            if (ka[a]['in_game'] is False):
                eliminated.append(a)
            else:
                log.write(ka[a]['name']+': '+str(ka[a]['money']))
        ka[:]= [x for i, x in enumerate(ka) if i not in eliminated]
        ka = sorted(ka, key=lambda qa: (qa['money'], qa['right_in_round'], -qa['wrong_in_round']))
        aux_list[ka[0]['index']]['in_game'] = False
        aux_list[ka[0]['index']]['money'], JACKPOT = 0,  JACKPOT+aux_list[ka[0]['index']]['money']
        tk.messagebox.showinfo("Выбывает: ",aux_list[ka[0]['index']]['name'])
        log.write("Игру покидает "+aux_list[ka[0]['index']]['name']+'\n'+'Теперь в Копилке '+str(JACKPOT)+'\n')
        kopilka["text"] = 'В Копилке:' + '\n' + str(JACKPOT)
        pl_refresh()
        current_round +=1
        start(current_round)
    else:
        baza.pop(q_number_baza)
        choose_a_question()
        log.write(baza[q_number_baza]["Q"] + '\n')
        root.timer_question = root.after(1000, pytanie)
        _button = pressed.no
        pass #dopisat'

def start(d):
    global questions_asked_in_round, questions_available_in_round, timer, paliktas_laikas, q_number_baza, baza, pole_voprosa, paliktas_laikas_klausimui, _button, time_up, money_final, current_question_final, config, winner, winner_sgor, winner_nesgor, vvod
    if (d>5):
        _button=pressed.disable
        timer.place_forget()
        spieler.place_forget()
        current_question_final +=1
        if(current_question_final==1):
            parse()
            money_final = [0, JACKPOT//1000, JACKPOT//100, JACKPOT//10, JACKPOT]
            for m in range(len(aux_list)):
                if aux_list[m]['in_game']:
                    tk.messagebox.showinfo("Финал", aux_list[m]['name']+', вы уже выиграли '+str(aux_list[m]['money'])+'!\n')
                    winner = aux_list[m]['name']
                    winner_sgor = 0
                    winner_nesgor = aux_list[m]['money']
                    break
        paliktas_laikas_klausimui = 60
        timer_1q["text"] = str(paliktas_laikas_klausimui)
        root.title("Вопрос на "+str(money_final[current_question_final]))
        log.write("Вопрос "+str(current_question_final)+ (' (')+str(money_final[current_question_final])+') \n')
        choose_a_question()
        log.write(baza[q_number_baza]["Q"] + '\n')
        test.place(x=110, y=300)
        root.timer_question = root.after(2000, pytanie)
        vvod = canpressenter.yes
        pass #дописать
    else:
        log.write("Раунд "+str(d)+'\n')
        questions_asked_in_round = 0
        questions_available_in_round = 6-d
        paliktas_laikas = TIME_ROUND_IN_SECONDS
        paliktas_laikas_klausimui = 10*d
        timer.place(x=10, y=120, width=50, height=30)
        timer["text"] = time.strftime('%M:%S', time.gmtime(paliktas_laikas))
        timer_1q.place(x=10, y=180, width=50, height=30)
        timer_1q["text"] = str(paliktas_laikas_klausimui)
        choose_a_question()
        log.write(baza[q_number_baza]["Q"]+'\n')
        pole_voprosa["justify"] = tkinter.CENTER
        pole_voprosa["bg"] = "#ffff7f"
        pole_voprosa["fg"] = "#000000"
        pole_voprosa["wraplength"] = 280
        pole_voprosa.place(relx=0.15, rely=0.25)
        for m in range(6):
            aux_list[m]['blocked_left'] = 0
            aux_list[m]['right_in_round'] = 0
            aux_list[m]['wrong_in_round'] = 0
        root.timer_round = root.after(2000, runda)
        root.timer_question = root.after(2000, pytanie)
        _button = pressed.no
        time_up = False
        vvod = canpressenter.no


def pl_refresh():
    global pl_info, aux_list
    for a in range(6):
        pl_info[a]["text"]=aux_list[a]['name'] + '(' + str(a + 1) + ')' + '\n' + str(aux_list[a]["money"])
        if (aux_list[a]['in_game']):
            pl_info[a]["bg"] = "#8f8fff"
        else:
            pl_info[a]["bg"] = "#222222"
        if (aux_list[a]['blocked_left'] > 0):
            pl_info[a]["bg"] = "#686868"


def check(*args):
    global answerstring, test, questions_available_in_round, questions_asked_in_round, paliktas_laikas_klausimui, current_round, current_question_final, winner, winner_sgor, winner_nesgor, money_final, baza, q_number_baza, JACKPOT, vvod
    if (vvod==canpressenter.no):
        pass
    else:
        answerstring=guess.get()
        log.write("Ответ игрока: "+answerstring+'\n')
        test.place_forget()
        if (current_round<=5):
            o = []
            for i in range(len(baza[q_number_baza]["A"])):
                o.append(baza[q_number_baza]["A"][i])
                o[i] = o[i].replace(' ', '')
                o[i] = o[i].lower()
            answerstring = answerstring.lower()
            answerstring = answerstring.replace(' ', '')
            if (answerstring in o):
                j = o.index(answerstring)
                aux_list[otvechaet]["money"] += (1000*current_round)
                aux_list[otvechaet]['right_in_round'] +=1
                questions_available_in_round+=(6-current_round)
                if (questions_available_in_round>MAX_QUESTIONS_IN_ROUND):
                    questions_available_in_round = MAX_QUESTIONS_IN_ROUND
                root.title("Верно!")
                log.write("Это правильный ответ "+ '\n')
            else:
                aux_list[otvechaet]['wrong_in_round'] += 1
                aux_list[otvechaet]['blocked_left'] += (7-current_round)#6-current_round
                root.title("Неверно! Правильный ответ - "+baza[q_number_baza]["A"][0])
                log.write("Правильный ответ - "+baza[q_number_baza]["A"][0]+'\n')
            questions_asked_in_round +=1
            paliktas_laikas_klausimui = 10 * current_round
            #print("Осталось вопросов: "+str(questions_available_in_round-questions_asked_in_round))
            timer_1q["text"] = str(paliktas_laikas_klausimui)
            check_if_endround()
            pl_refresh()
            vvod = canpressenter.no
        else:
            root.after_cancel(root.timer_question)
            vvod = canpressenter.no
            log.write("Ответ игрока: " + answerstring + '\n')
            o = []
            for i in range(len(baza[q_number_baza]["A"])):
                o.append(baza[q_number_baza]["A"][i])
                o[i] = o[i].replace(' ', '')
                o[i] = o[i].lower()
            answerstring = answerstring.lower()
            answerstring = answerstring.replace(' ', '')
            if (answerstring in o):
                j = o.index(answerstring)
                winner_sgor = money_final[current_question_final]
                if (current_question_final<4):
                    log.write("Это правильный ответ " + '\n')
                    baza.pop(q_number_baza)
                    if tk.messagebox.askyesno('Верно!', winner+', у вас '+str(winner_sgor+winner_nesgor)+'!\n Будете ли вы играть дальше?'):
                        guess.set("")
                        start(current_round)
                        vvod = canpressenter.yes
                    else:
                        tk.messagebox.showinfo("Конец игры",
                                               winner + ', вы выиграли ' + str(winner_sgor + winner_nesgor) + '.')
                        log.write("Игрок останавливает игру. Выигрыш: "+str(winner_sgor + winner_nesgor) + '.'+'\n')
                        JACKPOT -= winner_sgor
                        kopilka["text"] = 'В Копилке:' + '\n' + str(JACKPOT)
                        log.write("В Копилке осталось: " + str(JACKPOT) + '.\n')
                        parse()
                        endgame()
                else:
                    tk.messagebox.showinfo("Конец игры",
                                           winner + ', вы выиграли ' + str(winner_sgor + winner_nesgor) + '.')
                    JACKPOT -= winner_sgor
                    kopilka["text"] = 'В Копилке:' + '\n' + str(JACKPOT)
                    log.write("Игрок опустошил копилку и выиграл " + str(winner_sgor + winner_nesgor) + '.' + '\n')
                    parse()
                    endgame()
            else:
                winner_sgor=money_final[0]
                root.title("Неверно! Правильный ответ - " + baza[q_number_baza]["A"][0])
                log.write("Правильный ответ - " + baza[q_number_baza]["A"][0] + '\n')
                tk.messagebox.showinfo("Конец игры", winner+', вы выиграли '+str(winner_sgor+winner_nesgor)+'.')
                log.write("Игрок остался с" + str(winner_sgor + winner_nesgor) + '.' + '\n')
                kopilka["text"] = 'В Копилке:' + '\n' + str(JACKPOT)
                log.write("В Копилке осталось: " + str(JACKPOT) + '.\n')
                endgame()



def kwalif():
    global aux_list, current_round, questions_asked_in_round, spieler, player, pl_info, JACKPOT
    for a in range(len(start_names)):
        if start_names[a].get()=="":
            tk.messagebox.showwarning("Имена", "По меньшей мере у одного из игроков пустое имя. Исправьте")
            break
    else:
        rich.place_forget()
        log.write('Игроки: '+'\n')
        aux_list = []
        for b in range (6):
            aux_dict = {}
            aux_dict['name'] = start_names[b].get()
            aux_dict['money'] = 0
            aux_dict['blocked_left'] = 0
            aux_dict['right_in_round'] = 0
            aux_dict['wrong_in_round'] = 0
            aux_dict['in_game'] = True
            aux_dict['index'] = b
            D = aux_dict.copy()
            aux_list.append(aux_dict)
        for b in range(6):
            pass
            log.write(aux_list[b]['name'] + '\n')
        for b in range(6):
            player[b].place_forget()
        tk.messagebox.showinfo("Готово", "Мы начинаем игру")
        #global q_number
        pl_info = []
        current_round+=1
        questions_asked_in_round = 0
        spieler.place(relx=0.03, rely=0.02)
        for a in range(6):
            k = tk.Label(spieler, text=aux_list[a]['name']+'('+str(a+1)+')'+'\n'+str(aux_list[a]["money"]))
            if (aux_list[a]['in_game']):
                k["bg"] = "#8f8fff"
            else:
                k["bg"] = "#222222"
            if (aux_list[a]['blocked_left']>0):
                k["bg"] = "#686868"
            pl_info.append(k)
            pl_info[a].place(relx=0.05+0.15*a, rely=0.14)
        root.qu_sh = root.after(1000, start(current_round))
        kopilka.place(relx=0.08, rely=0.7)
        kopilka["text"] = 'В Копилке:'+'\n'+str(JACKPOT)
        log.write('В Копилке: '+str(JACKPOT)+'\n')














for a in range(6):
    dummy = tk.StringVar()
    dummy.set("Игрок "+str(a+1))
    start_names.append(dummy)

for a in range(6):
    nombre = ttk.Entry(root, textvariable = start_names[a])
    player.append(nombre)
    player[a].place(width=140, relx = 0.03, rely=0.05+a*(0.18))

rich = tk.Button(root, text="Начать игру", command=kwalif, width = 14, height = 30)
rich.place(relx = 0.5, rely=0.05)
guess = tk.StringVar()
test = ttk.Entry(root, width=29, textvariable=guess)
test.bind("<Return>", check)
spieler = ttk.LabelFrame(root, text="Игроки", width=550, height=83)
kopilka = tk.Label(root, width=125, height=2)
log = codecs.open("log.txt", 'a', "utf_8_sig")
kopilka["justify"] = tkinter.CENTER
kopilka["wraplength"]=110
root.protocol('WM_DELETE_WINDOW', doSomething)
root.bind('<KeyPress>', onKeyPress)
root.mainloop()