import random
from tkinter import *
from Fil import field
from threading import *
from time import *
class Person:
    def __init__(self,level,money,digging_speed,job,working):
        # self.speed = speed
        self.level = level
        self.money = money
        self.diging = digging_speed
        self.job = job
        self.working = working

root, Can = field(30)
cursor = False
persons = []
persons.append(Person(1,random.randint(1,3),random.randint(1,4),None,False))
persons.append(Person(1, random.randint(1, 3), random.randint(1, 4),None,False))

diging_sp = 0
miniral = 0
gold = 400
gold_maining_speed = 0
persons_exists = 2
persons_working = []
cursors = []

per = Can.create_text(950,30,text = f'Люди свободны: {len(persons)}',anchor = 'nw')
miniral_t = Can.create_text(950,50,text = f'Руда: {miniral}',anchor = 'nw')
gold_t = Can.create_text(950,70,text = f'Золото: {gold}',anchor = 'nw')
speed_miniral_t = Can.create_text(950,90,text = f'Скорость добычи руды: {diging_sp}',anchor = 'nw')
speed_gold_t = Can.create_text(950,110,text = f'Скорость добычи золота: {gold_maining_speed}',anchor = 'nw')
cost = Can.create_text(950,130,text = f'Стомость нового рабочего: {persons_exists**2 * 100}',anchor = 'nw')
Can.create_text(1050,250,text ='Купить рабочего',anchor = 'c')
Can.create_rectangle(900,200,1200,300)
Can.create_text(1050,350,text ='Продать руду',anchor = 'c')
Can.create_rectangle(900,300,1200,400)

def create_map():
    global persons
    y = 0
    x = 0
    pool = {}
    for i in range(0,900):
        num = random.randint(1,100)
        if num <= 10:
            pool[i] = [x,y,'Best for mine',Person(1,0,0,None,False)]
        elif num > 10 and num <= 20:
            pool[i] = [x,y,'Best for gold',Person(1,0,0,None,False)]
        else:
            pool[i] = [x,y,'Simple',Person(1,0,0,None,False)]

    for cell in pool.keys():
        if pool[cell][2] == 'Best for gold':
            Can.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30,fill='yellow')
        elif pool[cell][2] == 'Best for mine':
            Can.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill='grey')
        if x == 29:
            y += 1
            x = 0
        else:
            x += 1
    return pool

def warning(text):
    u = Tk()
    j = Canvas(u)
    j.pack()
    j.create_text(200, 100, text=text, font=35)

def go_mine(event):
    global pool,persons,diging_sp,root_helper,gold_maining_speed,x1,y1,persons_working, cursor_mine, cursors
    t = 0
    if event.y <= 100 and len(persons) != 0: # Проверяет для копания ли
        num = random.randint(0, len(persons) - 1)

        person_working = persons.pop(num)  # переводит его на работу в ячейку
        pool[x1 + y1 * 30][3].job = 'Mining'
        pool[x1 + y1 * 30][3].diging = person_working.diging
        pool[x1 + y1 * 30][3].money = person_working.money
        pool[x1 + y1 * 30][3].working = True

        if pool[x1+y1*30][2] == 'Best for mine':
            diging_sp += pool[x1 + y1 * 30][3].diging*2
        else:
            diging_sp += pool[x1 + y1 * 30][3].diging * 0.7

        cursor_mine = Can.create_rectangle(x1 * 30, y1 * 30, (x1 + 1) * 30, (y1 + 1) * 30, outline='red', fill=None, width=3) #Создает курсор на том участке, где есть уже рабочие
        cursors.append([cursor_mine,x1,y1])

    elif event.y > 100 and event.y <= 200 and len(persons) != 0: # Проверяет для добычи золота или нет
        num = random.randint(0, len(persons) - 1)

        person_working = persons.pop(num)  # переводит его на работу в ячейку
        pool[x1 + y1 * 30][3].job = 'Mining gold'
        pool[x1 + y1 * 30][3].diging = person_working.diging
        pool[x1 + y1 * 30][3].money = person_working.money
        pool[x1 + y1 * 30][3].working = True

        if pool[x1 + y1 * 30][2] == 'Best for gold':
            gold_maining_speed += pool[x1 + y1 * 30][3].money * 2
        else:
            gold_maining_speed += pool[x1 + y1 * 30][3].money * 0.7
        cursor_mine = Can.create_rectangle(x1 * 30, y1 * 30, (x1 + 1) * 30, (y1 + 1) * 30, outline='red', fill=None,width=3)#Создает курсор на том участке, где есть уже рабочие
        cursors.append([cursor_mine, x1, y1])

    elif event.y > 200 and pool[x1 + y1 * 30][3].working:
        p = pool[x1 + y1 * 30][3]
        if p.job == 'Mining gold':
            if pool[x1 + y1 * 30][2] == 'Best for gold':
                gold_maining_speed -= p.money * 2
            else:
                gold_maining_speed -= pool[x1 + y1 * 30][3].money * 0.7
        elif p.job == 'Mining':
            if pool[x1 + y1 * 30][2] == 'Best for mine':
                diging_sp -= pool[x1 + y1 * 30][3].diging * 2
            else:
                diging_sp -= pool[x1 + y1 * 30][3].diging * 0.7

        persons.append(Person(1, p.money, p.diging, None, False)) # Переводит его с участка работы
        pool[x1 + y1 * 30][3].money = 0
        pool[x1 + y1 * 30][3].diging = 0
        pool[x1 + y1 * 30][3].job = None
        pool[x1 + y1 * 30][3].working = False

        c = cursors.index([cursor_mine,x1,y1])
        Can.delete(c)
    else:
        warning('Что-то не так')

    root_helper.destroy()

def click(event): #смотрит, куда ты кликнул
    global pool,cursor,root_helper,x1,y1,gold,persons,cost,persons_exists,miniral
    x1 = event.x//30
    y1 = event.y//30
    if x1 < 30 and y1 < 30:
        if cursor:
            Can.delete(cursor)
            cursor = Can.create_rectangle(x1*30,y1*30,(x1+1)*30,(y1+1)*30,outline='green',fill=None,width=3)
        else:
            cursor = Can.create_rectangle(x1*30,y1*30,(x1+1)*30,(y1+1)*30, outline='green', fill=None,width=3)

        root_helper = Tk()
        root_helper.geometry('500x300')
        C = Canvas(root_helper, width=500, height=300)
        C.pack()
        C.create_line(0, 100, 500, 100)
        C.create_line(0, 200, 500, 200)
        C.create_text(250, 50, text='Послать добывать руду')
        C.create_text(250, 150, text='Послать добывать золото')
        C.create_text(250, 250, text='Забрать рабочего')
        root_helper.bind('<Button-1>', go_mine)
        root_helper.mainloop()

    if event.x > 900 and event.y < 300 and event.y > 200:
        if gold >= persons_exists**2 * 100:
            persons.append(Person(1, random.randint(1, 3), random.randint(1, 4), None, False))
            gold -= persons_exists**2 * 100
            persons_exists += 1
            Can.delete(cost)
            cost = Can.create_text(950, 130, text=f'Стомость нового рабочего: {persons_exists ** 2 * 100}', anchor='nw')
        else:
            warning('Копи деньги')

    if event.x > 900 and event.y < 400 and event.y > 300:
        gold += miniral
        miniral -= miniral

def counter():
    global diging_sp, miniral, gold, gold_maining_speed,speed_miniral_t, miniral_t, gold_t, speed_gold_t,per, persons_working, persons, per
    while True:
        miniral += diging_sp
        gold += gold_maining_speed
        Can.delete(speed_miniral_t, miniral_t, gold_t, speed_gold_t,per)

        per = Can.create_text(950, 30, text=f'Люди свободны: {len(persons)}', anchor='nw')
        miniral_t = Can.create_text(950, 50, text=f'Руда: {round(miniral,2)}', anchor='nw')
        gold_t = Can.create_text(950, 70, text=f'Золото: {round(gold,2)}', anchor='nw')
        speed_miniral_t = Can.create_text(950, 90, text=f'Скорость добычи руды: {diging_sp}', anchor='nw')
        speed_gold_t = Can.create_text(950, 110, text=f'Скорость добычи золота: {gold_maining_speed}', anchor='nw')
        sleep(1)

thread1 = Thread(target = counter)
thread1.start()

pool = create_map()
root.bind('<Button-1>',click)
root.mainloop()