#! python3
# -*- coding: utf-8 -*- 

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep
from collections import Counter

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding, OneFrame, Question, TextArea
from gui import GUI
from constants import TESTING, URL


################################################################################
# TEXTS


introFavoritism = """Před následující úlohou dostanete Vy i všichni ostatní účastníci studie bonus 30 Kč.

V této úloze dostanete popis pěti trojic osob (tj. informaci o tom, jaké skupiny jsou jim blízké). U každé trojice vyberete jednu osobu, které přidělíte 10 Kč, a jednu, které 10 Kč vezmete. Z pěti trojic bude jedna trojice odpovídat skutečné trojici dalších účastníků výzkumu a zbývající čtyři trojice budou uměle vytvořené. Pouze u trojice skutečných účastníků studie budou peníze na základě Vašich voleb skutečně přiděleny či odebrány.

Váš popis bude podobně u třech dalších účastníků studie. Na základě jejich voleb tedy za tuto úlohu dostanete 0-60 Kč k odměně."""



qFavoritism= "Pomocí tlačítek vyberte, které osobě přidělíte a které odeberete 10 Kč.\nKaždá možnost musí být zvolena právě jednou."

descriptionLabelText = "Hodnocené osoby vybraly, že jsou jim blízké tyto skupiny:"


################################################################################


class FavoritismFrame(Canvas):
    def __init__(self, root, label):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root
        self.name = label

        self.label = ttk.Label(self, text = label, font = "helvetica 15 bold", background = "white", justify = "center")

        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 30, height = 7, wrap = "word",
                         highlightbackground = "white")

        self.choice = StringVar()
        self.choice.set("ignore")

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        self.add = ttk.Radiobutton(self, text = "Přidělit 10 Kč", variable = self.choice, value = "add", command = self.clicked)
        self.ignore = ttk.Radiobutton(self, text = "", variable = self.choice, value = "ignore", command = self.clicked)
        self.remove = ttk.Radiobutton(self, text = "Odebrat 10 Kč", variable = self.choice, value = "remove", command = self.clicked)

        self.label.grid(column = 0, row = 0, pady = 10)
        self.text.grid(column = 0, row = 1)
        self.add.grid(column = 0, row = 2, sticky = W)
        self.ignore.grid(column = 0, row = 3, sticky = W)
        self.remove.grid(column = 0, row = 4, sticky = W)

    def clicked(self):
        self.root.changedValue(self.name, self.choice.get())

    def addText(self, text):
        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
        self.text["state"] = "disabled"

    def indicate(self, what):
        ttk.Style().configure("Indicated.TRadiobutton", background = "pink")
        if what == "add":
            self.add.config(style = "Indicated.TRadiobutton")
            self.remove.config(style = "TRadiobutton")
        elif what == "remove":
            self.remove.config(style = "Indicated.TRadiobutton")
            self.add.config(style = "TRadiobutton")

    def removeIndications(self):
        self.add.config(style = "TRadiobutton")
        self.remove.config(style = "TRadiobutton")


class Favoritism(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = descriptionLabelText, height = 1, font = 15, width = 80)

        self.totalTrials = 5
        self.trial = 0

        self.descriptions = [[["Skupina {}".format(random.randint(0,30)) for i in range(4)] for g in range(3)] for j in range(self.totalTrials)] # TODO
  
        self.trialText = ttk.Label(self, text = "", font = "helvetica 15", background = "white", justify = "right")
        self.question = ttk.Label(self, text = qFavoritism, font = "helvetica 15", background = "white", justify = "center")

        self.first = FavoritismFrame(self, "Osoba A")
        self.second = FavoritismFrame(self, "Osoba B")
        self.third = FavoritismFrame(self, "Osoba C")

        self.next["command"] = self.nextTrial
        
        self.text.grid(column = 1, row = 1, columnspan = 3)
        self.trialText.grid(column = 3, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        self.question.grid(column = 1, row = 3, columnspan = 3)
        self.first.grid(column = 1, row = 2)
        self.second.grid(column = 2, row = 2)
        self.third.grid(column = 3, row = 2)
        self.next.grid(row = 4, column = 1, columnspan = 3)        

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(4, weight = 1)
        
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)    

        self.file.write("Favoritism\n")
        
        self.nextTrial()


    def nextTrial(self):
        if self.trial == self.totalTrials:
            self.nextFun()
        else:
            self.trial += 1
            self.first.addText("\n".join(self.descriptions[self.trial - 1][0]))
            self.second.addText("\n".join(self.descriptions[self.trial - 1][1]))
            self.third.addText("\n".join(self.descriptions[self.trial - 1][2]))
            self.first.choice.set("ignore")
            self.second.choice.set("ignore")
            self.third.choice.set("ignore")
            self.choices = {}
            self.choices[self.first.name] = "ignore"
            self.choices[self.second.name] = "ignore"
            self.choices[self.third.name] = "ignore"
            self.next["state"] = "disabled"
            self.trialText["text"] = f"Trojice: {self.trial}/{self.totalTrials}"


    def changedValue(self, name, value):                  
        self.choices[name] = value
        if len({choice for choice in self.choices.values()}) == 3:
            self.next["state"] = "normal"
            for frame in [self.first, self.second, self.third]:
                frame.removeIndications()
        else:            
            self.next["state"] = "disabled"
            counts = Counter([choice for choice in self.choices.values()])
            mostCommon, maximum = counts.most_common(1)[0]
            if maximum > 1:
                for frame in [self.first, self.second, self.third]:
                    if frame.choice.get() == mostCommon and mostCommon != "ignore":
                        frame.indicate(mostCommon)
                    else:
                        frame.removeIndications()



InstructionsFavoritism = (InstructionsFrame, {"text": introFavoritism, "height": 11})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#InstructionsFavoritism, 
         Favoritism
         ])
