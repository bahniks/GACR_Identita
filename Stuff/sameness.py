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


introSameness = f"""Nyní vám ukážeme odpovědi deseti osob, z nichž čtyři jsou od dalších účastníků této studie a zbývajících šest je uměle vytvořených. Uvidíte, které skupiny těmto osobám byly blízké a které vzdálené. 

Vaším úkolem bude odhadnout, do jaké míry se s těmito lidmi shodujete v tom, co se vám líbí. Za každého účastníka studie, kde bude váš odhad správný dostanete bonus {SAMENESS} Kč. Za odhady u uměle vytvořených osob žádný bonus nedostáváte. 

Shoda je určována podle odpovědí v úloze, kde jste uváděli své preference z nabízených dvojic možností. Jako shoda jsou počítány dvojice, kde jste s daným účastníkem studie určili preferenci stejné možnosti z nabídnuté dvojice. 
Celkem jste oba obdrželi 30 stejných dvojic. Pokud byste oba odpovídali náhodně, lze očekávat, že se budete shodovat u 15 položek. Pokud si myslíte, že jste si spíše podobní a máte stejné preference, měl(a) byste uvádět odhad vyšší než 15. Pokud si naopak myslíte, že jste odlišní a máte tedy různé preference, měl(a) byste uvádět odhad nižší než 15.

Kolikrát jste správně shodu odhadl(a), a jakou jste tedy za úlohu obdržel(a) odměnu, se dozvíte na konci studie."""

qSameness = "Pomocí modrého ukazatele níže zkuste odhadnout kolik shodných preferencí s tímto účastníkem studie máte."

descriptionLabelText = "Hodnocená osoba vybrala, že je členem těchto skupin:"

leftLabelText = "Nejvíce\nodlišný"
rightLabelText = "Nejvíce\npodobný"

infoValueLabelText = "Očekávám shodu v počtu položek: "
################################################################################


class Sameness(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "", height = 6, font = 15, width = 45)

        self.totalTrials = 10
        self.trial = 0

        self.maximum = 30

        self.descriptions = [["Kategorie {}".format(random.randint(0,50)) for i in range(4)] for j in range(self.totalTrials)] # TODO

        self.valueVar = StringVar()

        self.descriptionText = ttk.Label(self, text = descriptionLabelText, font = "helvetica 15", background = "white", justify = "center")      
        self.trialText = ttk.Label(self, text = "", font = "helvetica 15", background = "white", justify = "right")

        self.question = ttk.Label(self, text = qSameness, font = "helvetica 15", background = "white", justify = "right")

        self.scaleFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        ttk.Style().configure("TScale", background = "white")
        self.value = ttk.Scale(self.scaleFrame, orient = HORIZONTAL, from_ = 0, to = self.maximum, length = 400,
                            variable = self.valueVar, command = self.changedValue)
        # self.value.bind("<Button-1>", self.onClick)
        # self.value.bind("<ButtonRelease-1>", self.onRelease)
        # self.clicked = False
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

        self.scaleFrame.grid(column = 1, row = 3)
        self.descriptionText.grid(column = 1, row = 0)
        self.trialText.grid(column = 1, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        self.question.grid(column = 1, row = 2, pady = 30)
        self.text.grid(row = 1, column = 1)
        self.next.grid(row = 4, column = 1)        

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(5, weight = 2)    

        self.file.write("Sameness\n")
        
        self.nextTrial()


    def nextTrial(self):
        if self.trial == self.totalTrials:
            self.nextFun()
        else:
            self.trial += 1
            self.changeText("\n".join(self.descriptions[self.trial - 1]))
            self.trialText["text"] = f"Osoba: {self.trial}/{self.totalTrials}"
            self.valueVar.set(f"{self.maximum//2}")


    def changedValue(self, value):          
        # if self.clicked:
        #     return
        #self.value.configure(command=None)               
        value = str(min([max([eval(str(value)), 0]), self.maximum]))
        self.valueVar.set(value)        
        newval = int(round(eval(self.valueVar.get())))
        self.valueVar.set("{0:2d}".format(newval))
        #self.value.configure(command=self.changedValue)


    # def onClick(self, event):
    #     #self.value.configure(command=None)
    #     if not self.clicked:
    #         self.clicked = True
    #         newValue = int((event.x / self.value.winfo_width()) * self.value['to'])
    #         value = str(min([max([eval(str(newValue)), 0]), self.maximum]))
    #         self.valueVar.set(value)        
    #         newval = int(round(eval(self.valueVar.get())))
    #         self.valueVar.set("{0:2d}".format(newval))        
    #         #self.changedValue(newValue)
    #         #self.update()

    #     #self.value.configure(command=self.changedValue)
       
    # def onRelease(self, event):
    #     self.clicked = False




InstructionsSameness = (InstructionsFrame, {"text": introSameness, "height": 15})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([InstructionsSameness, 
         Sameness
         ])
