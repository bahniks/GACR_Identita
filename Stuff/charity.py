from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import os
import random

from common import InstructionsFrame, read_all
from gui import GUI
from constants import TESTING, URL, CHARITY




################################################################################
# TEXTS

charityInstructions = f"""Jako dodatečnou odměnu dáme jednomu z deseti náhodně vybraných účastníků {CHARITY} Kč. Losování proběhne na konci studie.

Částku {CHARITY} Kč si budete moct nechat, anebo jí celou anebo její část věnovat nějaké neziskové organizaci. 

Nyní Vám úkažeme postupně 20 neziskových organizací s krátkým popiskem, čím se zabývají. Vy můžete určit, kolik peněz byste každé z těchto organizací chtěli dát a kolik si nechat pro sebe v případě, že budete vylosováni. 

Pokud budete vylosováni, tak náhodně vybereme jednu z těchto organizací a rozdělíme peníze mezi Vás a danou organizaci podle rozhodnutí, které učiníte nyní. <b>Jinými slovy, rozhodnutí pro jednotlivé organizace jsou nezávislá. Bude vybrána pouze jedna z těchto organizací a jen podle Vašeho rozhodnutí u dané organizace se budou peníze rozdělovat mezi ní a Vás.</b> Neziskové organizaci pošleme peníze po skončení studie."""


charityInstructions2 = f"""<b>Pokud budete vylosováni, tak náhodně vybereme jednu z organizací zobrazených na této nebo další obrazovce a rozdělíme {CHARITY} Kč mezi Vás a danou organizaci podle rozhodnutí, které učiníte nyní.</b> Pomocí posuvníků níže určete, kolik peněz byste dané organizaci chtěli dát a kolik si nechat pro sebe v případě, že bude náhodně vybrána daná organizace."""

charityNotChosenText = f"""V úloze s výběrem neziskové organizace jste nebyl(a) vylosován(a)."""
charityChosenText = """V úloze s výběrem neziskové organizace jste byl(a) vylosován(a). Z neziskových organizací byla náhodně vybrána {}. Dle Vaší volby obdržíte {} Kč a organizaci {} po skončení studie pošleme {} Kč."""


################################################################################



class ScaleFrame(Canvas):
    def __init__(self, root, maximum, charity, description):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.charity = charity
        self.description = description
        self.parent = root
        self.root = root.root
        self.rounding = 10
        self.maximum = maximum 

        self.valueVar = StringVar()
        self.valueVar.set("0")

        ttk.Style().configure("TScale", background = "white")

        self.value = ttk.Scale(self, orient = HORIZONTAL, from_ = 0, to = maximum, length = 400,
                            variable = self.valueVar, command = self.changedValue)
        self.value.bind("<Button-1>", self.onClick)

        self.playerText2 = f"{self.charity}"
        self.playerText1 = "Já"
        self.totalText1 = "{0:3d} Kč"
        self.totalText2 = "{0:3d} Kč"

        self.descriptionLab = ttk.Label(self, text = self.description, font = "helvetica 13", background = "white")
        self.descriptionLab.grid(column = 0, row = 1, columnspan = 6, pady = 5, sticky = "w")

        self.value.grid(column = 3, row = 0, padx = 10)

        self.playerLab1 = ttk.Label(self, text = self.playerText1, font = "helvetica 15", background = "white", width = 3, anchor = "w") 
        self.playerLab2 = ttk.Label(self, text = self.playerText2, font = "helvetica 15 bold", background = "white", width = 40, anchor = "w") 
        self.totalLab1 = ttk.Label(self, text = self.totalText1.format(0), font = "helvetica 15", background = "white", width = 6, anchor = "w")
        self.totalLab2 = ttk.Label(self, text = self.totalText2.format(0), font = "helvetica 15", background = "white", width = 6, anchor = "w")

        self.playerLab1.grid(column = 1, row = 0, padx = 3, sticky = W)
        self.totalLab1.grid(column = 2, row = 0, padx = 3, sticky = "ew")

        self.playerLab2.grid(column = 5, row = 0, padx = 3, sticky = W)        
        self.totalLab2.grid(column = 4, row = 0, padx = 3, sticky = "ew")

        self.columnconfigure(5, weight = 1)
  
        
        self.changedValue(0)


    def onClick(self, event):       
        if self.value.instate(["disabled"]):
            return
        click_position = event.x
        newValue = int((click_position / self.value.winfo_width()) * self.value['to'])
        self.changedValue(newValue)
        self.update()

    def changedValue(self, value):           
        value = str(min([max([eval(str(value)), 0]), self.maximum]))
        self.valueVar.set(value)
        newval = int(round(eval(self.valueVar.get())/self.rounding, 0)*self.rounding)
        self.valueVar.set("{0:3d}".format(newval))
        self.totalLab1["text"] = self.totalText1.format(self.maximum - newval)
        self.totalLab2["text"] = self.totalText2.format(newval)




class Charity(InstructionsFrame):
    def __init__(self, root):

        super().__init__(root, text = charityInstructions2, height = 3.5, font = 15, width = 100)        

        charities = read_all("charities.txt").splitlines()
        randomizer = [i for i in range(len(charities)//3 + 1)]
        random.shuffle(randomizer)
        self.charities = [charities[0 + i*3] for i in randomizer]
        self.descriptions = [charities[1 + i*3] for i in randomizer]
        self.win = random.random() < 0.1     
        self.chosenCharity = random.choice(self.charities)

        self.frames = {}
        for i in range(len(self.charities)//2):          
            self.frames[i] = ScaleFrame(self, maximum = CHARITY, charity = self.charities[i], description = self.descriptions[i])            
            self.frames[i].grid(column = 1, row = i + 2, pady = 1, sticky = W)
            self.rowconfigure(i + 2, weight = 1)
            
        self.next.grid(column = 0, row = 20, columnspan = 3, pady = 10, sticky = N)            
        
        self.text.grid(row = 1, column = 0, columnspan = 3)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(20, weight = 2)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 2)

        self.first = True

    def nextFun(self):
        self.write()
        if self.first:
            self.first = False
            add = len(self.charities)//2
            for i in range(len(self.charities)//2):          
                self.frames[i] = ScaleFrame(self, maximum = CHARITY, charity = self.charities[i+add], description = self.descriptions[i+add])            
                self.frames[i].grid(column = 1, row = i + 2, pady = 1, sticky = W)            
        else:
            if not self.win:
                self.root.status["results"] += [charityNotChosenText]
            super().nextFun()

    def write(self):
        if self.first:
            self.file.write("Charities\n")   
            add = 0
        else:
            self.file.write("\n")
            add = len(self.charities)//2
        for i in range(len(self.charities)//2):
            chosen = 1 if self.charities[i + add] == self.chosenCharity else 0
            if chosen and self.win:
                self.root.status["results"] += [charityChosenText.format(self.chosenCharity, int(self.frames[i].valueVar.get()), self.chosenCharity, CHARITY - int(self.frames[i].valueVar.get()))]
                self.root.status["reward"] += int(self.frames[i].valueVar.get())                
            self.file.write(f"{self.id}\t{self.charities[i+add]}\t{self.frames[i].valueVar.get()}\t{self.win}\t{chosen}\n")        


CharityInstructions = (InstructionsFrame, {"text": charityInstructions, "height": 8, "width": 80, "font": 15})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    from intros import Ending
    GUI([#CharityInstructions,
         Charity,
         Ending
         ])
    