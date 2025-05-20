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
from constants import TESTING, URL, FAVORITISM
from sameness import createSyntetic


################################################################################
# TEXTS


introFavoritism = f"""V rámci této úlohy dostanete Vy i všichni ostatní účastníci studie počáteční bonus {FAVORITISM*3} Kč.

V této úloze dostanete popis pěti trojic osob (tj. informaci o tom, jaké skupiny jsou jim blízké). U každé trojice vyberete jednu osobu, které přidělíte {FAVORITISM} Kč, a jednu, které {FAVORITISM} Kč odeberete. Z pěti trojic bude jedna trojice odpovídat skutečné trojici dalších účastníků výzkumu a zbývající čtyři trojice budou uměle vytvořené. Pouze u trojice skutečných účastníků studie budou peníze na základě Vašich voleb skutečně přiděleny či odebrány.

Váš popis bude podobně zobrazen u třech dalších účastníků studie. Na základě jejich voleb tedy za tuto úlohu dostanete celkem 0-{FAVORITISM*6} Kč k odměně. Výši této odměny se dozvíte na konci studie."""

qFavoritism= f"Pomocí tlačítek vyberte, které osobě přidělíte a které odeberete {FAVORITISM} Kč.\nKaždá možnost musí být zvolena právě jednou."

descriptionLabelText = "<center>Hodnocené osoby vybraly, že jsou jim blízké tyto skupiny:</center>"


################################################################################


class FavoritismFrame(Canvas):
    def __init__(self, root, label):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root
        self.name = label        

        self.label = ttk.Label(self, text = label, font = "helvetica 15 bold", background = "white", justify = "center")

        self.closeText = Text(self, wrap=WORD, font="helvetica 15", height=7, width=33, background="white", relief="flat")
        self.closeText.grid(row = 1, column = 0, pady = 10)
        self.closeText.tag_configure("bold", font = "helvetica 15 bold", foreground = "blue")

        self.distantText = Text(self, wrap=WORD, font="helvetica 15", height=7, width=33, background="white", relief="flat")
        self.distantText.grid(row = 1, column = 1, pady = 10)
        self.distantText.tag_configure("bold", font = "helvetica 15 bold", foreground = "red")

        self.choice = StringVar()
        self.choice.set("ignore")

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        self.add = ttk.Radiobutton(self, text = f"Přidělit {FAVORITISM} Kč", variable = self.choice, value = "add", command = self.clicked)
        self.ignore = ttk.Radiobutton(self, text = "", variable = self.choice, value = "ignore", command = self.clicked)
        self.remove = ttk.Radiobutton(self, text = f"Odebrat {FAVORITISM} Kč", variable = self.choice, value = "remove", command = self.clicked)

        self.label.grid(column = 0, row = 0, pady = 10)
        self.closeText.grid(column = 0, row = 1)
        self.distantText.grid(column = 0, row = 2)
        self.add.grid(column = 0, row = 3, sticky = W)
        self.ignore.grid(column = 0, row = 4, sticky = W)
        self.remove.grid(column = 0, row = 5, sticky = W)

    def clicked(self):
        self.root.changedValue(self.name, self.choice.get())

    def addText(self, value):
        if self.root.trial - 1 == self.root.realTrial:
            close, distant = value.split("|")
            self.close = close.split("_")
            self.distant = distant.split("_")
            self.value = "R"
        else:
            self.close, self.distant = createSyntetic(value)
            self.value = value        
        self.closeText.config(state=NORMAL)
        self.closeText.delete("1.0", END)
        self.closeText.insert("1.0", "\n".join(["Blízké skupiny:"] + self.close))
        self.closeText.tag_add("bold", "1.0", "2.0")
        self.closeText.config(state=DISABLED)
        self.distantText.config(state=NORMAL)
        self.distantText.delete("1.0", END)
        self.distantText.insert("1.0", "\n".join(["Vzdálené skupiny:"] + self.distant))
        self.distantText.tag_add("bold", "1.0", "2.0")
        self.distantText.config(state=DISABLED)

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

        self.realOrder = [1, 2, 3]
        random.shuffle(self.realOrder)
        realPeople = [self.root.status["groups"][self.realOrder[0]], self.root.status["groups"][self.realOrder[1]], self.root.status["groups"][self.realOrder[2]]]        
        self.people = []
        self.realTrial = random.randint(0, self.totalTrials - 1)
        for i in range(self.totalTrials):           
            if i == self.realTrial:
                self.people.append(realPeople)
            else:
                proenvi = random.randint(-8,-4)
                neutral = random.choice([-2, -1, 1, 2])
                antienvi = random.randint(4,8)
                persons = [proenvi, neutral, antienvi]
                random.shuffle(persons)
                self.people.append(persons)                
  
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
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 0)
        self.columnconfigure(4, weight = 1)
        
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)    

        self.file.write("Favoritism\n")
        
        self.nextTrial()


    def nextTrial(self):
        if self.trial != 0:
            if self.trial == self.realTrial:
                data = "_".join([self.first.choice.get(), self.second.choice.get(), self.third.choice.get()])
                data += "|" + "_".join(self.root.status["paired_ids"][i] for i in self.realOrder)
                data = {'id': self.id, 'round': "favoritism", 'offer': data}
                self.sendData(data)
            self.write()

        if self.trial == self.totalTrials:
            self.file.write("\n")
            self.nextFun()
        else:
            self.trial += 1
            self.first.addText(self.people[self.trial - 1][0])
            self.second.addText(self.people[self.trial - 1][1])
            self.third.addText(self.people[self.trial - 1][2])
            self.first.choice.set("ignore")
            self.second.choice.set("ignore")
            self.third.choice.set("ignore")
            self.choices = {}
            self.choices[self.first.name] = "ignore"
            self.choices[self.second.name] = "ignore"
            self.choices[self.third.name] = "ignore"
            self.next["state"] = "disabled"
            self.trialText["text"] = f"Trojice: {self.trial}/{self.totalTrials}"


    def write(self):
        leftText = "\t".join(["|".join(self.first.close), "|".join(self.first.distant), str(self.first.value)])
        middleText = "\t".join(["|".join(self.second.close), "|".join(self.second.distant), str(self.second.value)])
        rightText = "\t".join(["|".join(self.third.close), "|".join(self.third.distant), str(self.third.value)])
        left = self.first.choice.get()
        middle = self.second.choice.get()
        right = self.third.choice.get()
        real = self.trial - 1 == self.realTrial
        self.file.write(f"{self.id}\t{self.trial}\t{leftText}\t{left}\t{middleText}\t{middle}\t{rightText}\t{right}\t{real}\n")


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
    from trustgame import WaitGroups
    GUI([#InstructionsFavoritism, 
        WaitGroups,
         Favoritism
         ])
