#! python3
# -*- coding: utf-8 -*- 

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep
from collections import defaultdict

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding, OneFrame, Question, TextArea
from gui import GUI
from constants import TESTING, URL, SAMENESS


################################################################################
# TEXTS


introSameness = f"""Nyní vám ukážeme odpovědi jedenácti osob, z nichž jedna je od dalších účastníků této studie a zbývajících deset je uměle vytvořených. Uvidíte, které skupiny těmto osobám byly blízké a které vzdálené. 

Vaším úkolem bude odhadnout, do jaké míry se s těmito lidmi shodujete v tom, co se vám líbí. Pokud bude Váš odhad správný u dalšího účastníka studie, dostanete bonus {SAMENESS} Kč. Za odhady u uměle vytvořených osob žádný bonus nedostáváte. 

Shoda je určována podle odpovědí v úloze, kde jste uváděli své preference z nabízených dvojic možností. Jako shoda jsou počítány dvojice, kde jste s daným účastníkem studie určili preferenci stejné možnosti z nabídnuté dvojice. 
Celkem jste oba obdrželi 30 stejných dvojic. Pokud byste oba odpovídali náhodně, lze očekávat, že se budete shodovat u 15 položek. Pokud si myslíte, že jste si spíše podobní a máte stejné preference, měl(a) byste uvádět odhad vyšší než 15. Pokud si naopak myslíte, že jste odlišní a máte tedy různé preference, měl(a) byste uvádět odhad nižší než 15.

Zda jste správně shodu odhadl(a), a jakou jste tedy za úlohu obdržel(a) odměnu, se dozvíte na konci studie."""

qSameness = """Pomocí modrého ukazatele níže uveďte odhad, kolik máte shodných preferencí s tímto účastníkem studie.
(Preference označují volby z dvojic možností v dřívější fázi studie.)"""

descriptionLabelText = "Hodnocená osoba vybrala, že jsou jí blízké a vzdálené následující skupiny:"

leftLabelText = "Nejvíce\nodlišný"
rightLabelText = "Nejvíce\npodobný"

infoValueLabelText = "Očekávám shodu v počtu položek: "
################################################################################



def createSyntetic(value, output = "lists"):    
    #with open(os.path.join(os.getcwd(), "groups.txt"), "r", encoding="utf-8") as file:
    with open(os.path.join(os.getcwd(), "Stuff", "groups.txt"), "r", encoding="utf-8") as file:
        groups = [line.strip() for line in file if line.strip()]
    proenvironmental = groups[:10]
    neutral = groups[10: 23]
    antienvironmental = groups[23:]
    values = [(i + 1, abs(value) - i - 1) for i in range(-1, abs(value)) if i <= 4 and abs(value) - i <= 6]

    close = []
    distant = []

    v = random.choice(values)

    if value >= 0:
        close = random.sample(proenvironmental, v[0]) + random.sample(neutral, 5 - v[0])
        neutral = [group for group in neutral if group not in close]
        distant = random.sample(neutral, 5 - v[1]) + random.sample(antienvironmental, v[1])
    elif value < 0:
        close = random.sample(neutral, 5 - v[0]) + random.sample(antienvironmental, v[0])
        neutral = [group for group in neutral if group not in close]
        distant = random.sample(proenvironmental, 5 - v[1]) + random.sample(neutral, v[1])

    if output == "lists":
        return(close, distant)
    elif output == "string":
        return "_".join(close) + "|" + "_".join(distant)



class Sameness(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "", height = 8, font = 15, width = 35)

        self.totalTrials = 11
        self.trial = 0

        self.maximum = 30

        self.people = [-9, -7, -5, -3, -1, 1, 3, 5, 7, 9]
        if URL == "TEST":
            self.people += [0]
        else:
            self.people += ["REAL"]
        random.shuffle(self.people)

        self.distantText = Text(self, font = "helvetica 15", background = "white", relief = "flat", wrap = "word", height = 8, highlightbackground = "white", width = 35)

        self.valueVar = StringVar()

        self.descriptionText = ttk.Label(self, text = descriptionLabelText, font = "helvetica 15", background = "white", justify = "center")      
        self.trialText = ttk.Label(self, text = "", font = "helvetica 15", background = "white", justify = "right")        

        self.question = ttk.Label(self, text = qSameness, font = "helvetica 15", background = "white", justify = "center")

        self.scaleFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        ttk.Style().configure("TScale", background = "white")
        self.value = ttk.Scale(self.scaleFrame, orient = HORIZONTAL, from_ = 0, to = self.maximum, length = 400,
                            variable = self.valueVar, command = self.changedValue)

        self.leftLabel = ttk.Label(self.scaleFrame, text = leftLabelText, font = "helvetica 15 bold", background = "white", justify = "right")
        self.rightLabel = ttk.Label(self.scaleFrame, text = rightLabelText, font = "helvetica 15 bold", background = "white", justify = "left")
        self.valueLab = ttk.Label(self.scaleFrame, textvariable = self.valueVar, font = "helvetica 15", background = "white", width = 3, anchor = "e")
        self.infoValueLabel = ttk.Label(self.scaleFrame, text = infoValueLabelText, font = "helvetica 15", background = "white")
        self.value.grid(column = 1, columnspan = 2, row = 0)
        self.valueLab.grid(column = 2, row = 1)
        self.leftLabel.grid(column = 0, row = 0, padx = 10) 
        self.rightLabel.grid(column = 3, row = 0, padx = 10)        
        self.infoValueLabel.grid(row = 1, column = 1)

        self.next["command"] = self.nextTrial

        self.scaleFrame.grid(column = 1, columnspan = 2, row = 4)
        self.descriptionText.grid(column = 1, columnspan = 2, row = 1)
        self.trialText.grid(column = 2, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        self.question.grid(column = 1, columnspan = 2, row = 3, pady = 30)
        self.text.grid(row = 2, column = 1, sticky = E, padx = 30, columnspan = 1)
        self.distantText.grid(row = 2, column = 2, sticky = W, padx = 30)
        self.next.grid(row = 5, column = 1, columnspan = 2)        

        self.columnconfigure(0, weight = 3)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 3)
        
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(4, weight = 2)
        self.rowconfigure(5, weight = 2)
        self.rowconfigure(6, weight = 4)    

        self.file.write("Sameness\n")
        
        self.nextTrial()


    def nextTrial(self):
        limit = 0.1 if TESTING else 0.5

        if self.trial != 0:
            if perf_counter() - self.t0 < limit:
                return
            value = self.people[self.trial - 1]
            if value == "REAL":
                self.root.status["sameness_prediction"] = self.valueVar.get()
            self.file.write(f"{self.id}\t{self.trial}\t{value}\t{"|".join(self.close)}\t{"|".join(self.distant)}\t{self.valueVar.get()}\n")        

        if self.trial == self.totalTrials:
            self.file.write("\n")
            self.nextFun()
        else:
            self.trial += 1
            value = self.people[self.trial - 1]
            if value == "REAL":
                self.close, self.distant = self.root.status["groups"][0].split("|")
                self.close = self.close.split("_")
                self.distant = self.distant.split("_")
            else:
                self.close, self.distant = createSyntetic(value)
            self.changeText("\n".join(["<blue><b>Blízké skupiny:</b></blue>",""] + self.close))
            self.distantText["state"] = "normal"
            self.distantText.delete("1.0", "end")            
            self.distantText.tag_configure("bold", font = "helvetica 15 bold", foreground = "red")
            self.distantText.insert("1.0", "\n".join(["Vzdálené skupiny:", ""] + self.distant))
            self.distantText.tag_add("bold", "1.0", "2.0")
            self.distantText["state"] = "disabled"  
            self.trialText["text"] = f"Osoba: {self.trial}/{self.totalTrials}"        
            self.valueVar.set(f"{self.maximum//2}")
            self.t0 = perf_counter()


    def changedValue(self, value):                 
        value = str(min([max([eval(str(value)), 0]), self.maximum]))
        self.valueVar.set(value)        
        newval = int(round(eval(self.valueVar.get())))
        self.valueVar.set("{0:2d}".format(newval))


InstructionsSameness = (InstructionsFrame, {"text": introSameness, "height": 19})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#InstructionsSameness, 
         Sameness
         ])


