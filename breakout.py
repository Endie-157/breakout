from tkinter import *
from tkinter import ttk
from random import *
import numpy as np
import sounddevice as sd
from time import sleep
from sys import exit

def screen(): #fonction qui initialise la fenêtre et les fonctions du jeux
    global window
    global zone
    global dx, dy, dxb, dyb
    global score
    global setup
    global tone
    global balle2
    global winlose
    balle2 = None
    winlose="perdu"
    tone = (100, 110, 120, 130, 140)
    try:
        fin.destroy()
    except:
        setup.destroy()
    score = 0
    dx=5
    dy=5
    dxb=5
    dyb=5
    window=Tk()
    zone=Canvas(window, width=814, height=680, bg="white")
    zone.pack(padx=10,pady=10)
    elements()
    ballmove()
    raqumove()
    rectremove()
    scores()
    window.mainloop()

def ballmove(): #Fonction qui gère le mouvement de la balle et les collisions
    global dx
    global dy
    global zone
    global balle1
    if zone.coords(balle1)[3]<65:
        dy=-1*dy
    elif zone.coords(balle1)[2]>813 or zone.coords(balle1)[2]<65:
        dx=-1*dx
    elif zone.find_overlapping(zone.coords(raquette)[0],zone.coords(raquette)[1],zone.coords(raquette)[2],zone.coords(raquette)[3])[0]==balle1:
        ballm = zone.coords(balle1)[0]+32
        rectm = zone.coords(raquette)[0]+75
        dx = (ballm-rectm)/7
        dy=-1*dy
    elif zone.coords(balle1)[3]>680:
        window.destroy()
        end()
    zone.move(balle1,dx,dy)
    window.after(20,ballmove)

def gauche(event): #Fonction qui bouge la raquette à gauche quand on appuie sur la flèche gauche
    if zone.coords(raquette)[2]>150:
        zone.move(raquette,-20,0)

def droite(event): #Fonction qui bouge la raquette à droite quand on appuie sur la flèche droite
    if zone.coords(raquette)[2]<810:
        zone.move(raquette,20,0)

def raqumove(): #Fonction qui relie les touches aux fonctions gauche et droite
    zone.bind_all('<Right>', droite)
    zone.bind_all('<Left>', gauche)

def elements(): #Fonction qui crée les éléments du jeu
    global balle1
    global raquette
    global rectdict
    global tex
    balle1 = zone.create_oval(400,300,464,364,fill='purple')
    raquette = zone.create_rectangle(500,580,650,610,fill='black')
    tex = zone.create_text(700, 650, text=score, font='Arial 24')
    x1=1
    y1=0
    x2=100
    y2=30
    id=0
    chance=0
    chance=random()
    rectdict={}
    colours=('red', 'orange', 'yellow', 'green', 'blue')
    for loop in range(5):
        for loooop in range(8):
            if chance > 0.4:
                altid = "*"+str(id)
                rectdict[altid] = zone.create_rectangle(x1,y1,x2,y2, fill='grey')
            else:    
                rectdict[id] = zone.create_rectangle(x1,y1,x2,y2, fill=colours[loop])
            id=id+1
            x1=x1+102
            #y1=y1+32
            x2=x2+102
            #y2=y2+32
            chance=random()
        x1=1
        y1=y1+32
        x2=100
        y2=y2+32

def rectremove(): #Fonction qui casse une brique touchée par la balle et change sa direction
    global dx, dy, dxb, dyb
    global score
    global tex
    global tone
    global balle2, balle1
    global zone
    for id in rectdict:
        if zone.find_overlapping(zone.coords(rectdict[id])[0],zone.coords(rectdict[id])[1],zone.coords(rectdict[id])[2],zone.coords(rectdict[id])[3])[0]==balle1:
            if str(id)[0]=="*" and balle2==None:
                balle2 = zone.create_oval(400,300,464,364,fill='magenta')
                ballbonus()
            zone.delete(rectdict[id])
            del rectdict[id]
            score = score + 1
            if str(id)[0]=="*":
                sd.play(np.sin(2 * np.pi * 125 * np.arange(0, 1, 1/4410)), 44100)
            else:
                sd.play(np.sin(2 * np.pi * tone[-id//8] * np.arange(0, 1, 1/4410)), 44100)
            dy=-1*dy
            break
        elif zone.find_overlapping(zone.coords(rectdict[id])[0],zone.coords(rectdict[id])[1],zone.coords(rectdict[id])[2],zone.coords(rectdict[id])[3])[-1]==balle2:
            zone.delete(rectdict[id])
            del rectdict[id]
            if str(id)[0]=="*":
                sd.play(np.sin(2 * np.pi * 125 * np.arange(0, 1, 1/4410)), 44100)
            else:
                sd.play(np.sin(2 * np.pi * tone[-id//8] * np.arange(0, 1, 1/4410)), 44100)
            score = score + 1
            dyb=-1*dyb
            break
    window.after(20,rectremove)

def scores(): #fonction qui compte et affiche le score, il arrête le jeux quand il n'y a plus de briques
    global score
    global tex
    global rectdict
    zone.itemconfig(tex, text="score: "+str(score))
    if rectdict=={}:
        winlose="gagné"
        window.destroy()
        end()
    window.after(20,scores)

def start(): #Fonction qui donne un écran de démarrage
    global setup
    setup=Tk()
    setup.geometry('200x100')
    title = Label(setup, text="Jeu de casse briques")
    title.pack()
    zone=Canvas(setup, width=200, height=100, bg="white")
    ttk.Button(setup, text = 'Jouer', command=screen).pack()
    ttk.Button(setup, text = 'Arréter', command=exit).pack()
    setup.mainloop()

def end(): #Fonction qui donne un écran de fin avec le score
    global fin
    global score
    global winlose
    fin=Tk()
    fin.geometry('300x100')
    title = Label(fin, text="Vous avez "+winlose+" avec un score de "+str(score))
    title.pack()
    zone=Canvas(fin, width=300, height=100, bg="white")
    ttk.Button(fin, text = 'Rejouer', command=screen).pack()
    ttk.Button(fin, text = 'Arréter', command=exit).pack()
    fin.mainloop()

def ballbonus(): #Fonction qui gère le mouvement de la balle bonus et les collisions
    global dxb
    global dyb
    global zone
    global balle2
    if zone.coords(balle2)[3]<27:
        dyb=-1*dyb
    elif zone.coords(balle2)[2]>813 or zone.coords(balle2)[2]<65:
        dxb=-1*dxb
    elif zone.find_overlapping(zone.coords(raquette)[0],zone.coords(raquette)[1],zone.coords(raquette)[2],zone.coords(raquette)[3])[-1]==balle2:
        ballm = zone.coords(balle2)[0]+32
        rectm = zone.coords(raquette)[0]+75
        dxb = (ballm-rectm)/7
        dyb=-1*dyb
    elif zone.coords(balle2)[3]>680:
        zone.delete(balle2)
        Balle2=None
    zone.move(balle2,dxb,dyb)
    window.after(20,ballbonus)

start()
