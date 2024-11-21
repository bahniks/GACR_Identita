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
from constants import TESTING, URL


################################################################################
# TEXTS


introSameness = "Nyní vám ukážeme, odpovědi čtyř dalších účastníků této studie. Uvidíte, které skupiny jim byly blízké a které jim byly vzdálené. Vaším úkolem bude odhadnout, do jaké míry se s těmito lidmi shodujete v tom, co se vám líbí. Pokud bude váš odhad správný dostanete pokaždé bonus 100 Kč."

qSameness = "Zkuste prosím odhadnout, kolik shodných preferencí s tímto člověkem máte. Pokud se shodnete (+/- 1 shoda), dostanete bonus 100 Kč."



################################################################################


class Sameness(InstructionsFrame):
    def __init__(self, root, who):
        super().__init__(root, text = "", height = 3, font = 15, width = 45)


        self.trial = 1
        self.valueVar = StringVar()
        self.valueVar.set("15")

        
        self.trialText = ttk.Label(self, text = f"Osoba: 1/{self.total}", font = "helvetica 15 bold", background = "white", justify = "right")
        self.question = ttk.Label(self, text = qSameness, font = "helvetica 15 bold", background = "white", justify = "right")

        

        ttk.Style().configure("TScale", background = "white")
        self.value = ttk.Scale(self, orient = HORIZONTAL, from_ = 0, to = maximum, length = 400,
                            variable = self.valueVar, command = self.changedValue)
        self.value.bind("<Button-1>", self.onClick)

        self.valueLab = ttk.Label(self, textvariable = self.valueVar, font = "helvetica {}".format(font), background = "white", width = 3, anchor = "e")


        self.trialText.grid(column = 3, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        self.question.grid(column = 1, row = 3, columnspan = 3, pady = 30)
        self.valueLab.grid()


        self.columnconfigure(0, weight = 3)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 3)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(5, weight = 2)    

        self.file.write("Sameness\n")
        


    def changedValue(self, value):           
        value = str(min([max([eval(str(value)), 0]), self.maximum]))
        self.valueVar.set(value)
        newval = int(round(eval(self.valueVar.get())/self.rounding, 0)*self.rounding)
        self.valueVar.set("{0:3d}".format(newval))
        if self.player == "A":
            self.totalLab1["text"] = self.totalText1.format(self.endowment - newval)
            self.totalLab2["text"] = self.totalText2.format(self.endowment + newval * 3)
            self.totalLab1["font"] = "helvetica {} bold".format(self.font)
            self.playerLab1["font"] = "helvetica {} bold".format(self.font)
        else:
            self.totalLab1["text"] = self.totalText1.format(self.endowment - self.returned + newval)
            self.totalLab2["text"] = self.totalText2.format(self.returned * 3 + self.endowment - newval)
            self.totalLab2["font"] = "helvetica {} bold".format(self.font)
            self.playerLab2["font"] = "helvetica {} bold".format(self.font)

    def onClick(self, event):
        click_position = event.x
        newValue = int((click_position / self.value.winfo_width()) * self.value['to'])
        self.changedValue(newValue)
        self.update()
       





class Articles(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.who = who

        if TESTING and self.who == "myself" and not "articles" in self.root.status:
            self.root.status["articles"] = ["7_anti", "11_filler", "20_envi"]
        if TESTING and self.who == "others" and not "othersArticles" in self.root.status:
            self.root.status["othersArticles"] = ["12_anti", "5_filler", "3_envi"]
            
        self.total = 3
        self.trial = 1

        self.trialText = ttk.Label(self, text = f"Článek: 1/{self.total}", font = "helvetica 15 bold", background = "white", justify = "right")

        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 80, height = 15, wrap = "word", highlightbackground = "white")

        self.scrollbar = ttk.Scrollbar(self, command = self.text.yview)        
        self.text.config(yscrollcommand = self.scrollbar.set)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)

        self.trialText.grid(column = 1, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        self.text.grid(column = 1, row = 2)
        self.scrollbar.grid(column = 2, row = 2, sticky = "NSW")
        self.next.grid(column = 1, row = 4, pady = 30)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.rowconfigure(0, weight = 3)
        self.rowconfigure(2, weight = 1)   
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 3)    

        self.createText()

    def createText(self):
        self.text.delete("1.0", "end")
        source = self.root.status["articles"] if self.who == "myself" else self.root.status["othersArticles"]
        with open(os.path.join(os.getcwd(), "Stuff", "Texts", "text{}_{}.txt".format(*source[self.trial - 1].split("_")))) as f:
            self.text.insert("1.0", f.read()*3)
        
    def proceed(self):
        self.trial += 1
        if self.trial > self.total:
            self.nextFun()
        else:
            self.trialText["text"] = f"Článek: {self.trial}/{self.total}"
            self.createText()



    

InstructionsSameness = (InstructionsFrame, {"text": introSameness, "height": 5})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([InstructionsSameness, 
         Sameness
         ])