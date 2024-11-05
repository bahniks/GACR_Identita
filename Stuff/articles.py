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


introArticlesOthers = "Nyní vám vám budeme ukazovat nadpisy článků. Jedná se o krátké články, které vyjadřují různé názory autorů. Vaším úkolem bude vybrat z každé dvojice článek, který by si podle vás měli ostatní účastníci experimentu přečíst. Některé z článků, které vyberete, dostanou náhodně vybraní účastníci experimentu a budou mít čas si je přečíst. Tento úkol bude mít 30 kol."

qOthers = "Který článek chcete, aby si jiný účastník studie přečetl?"


introArticlesMyself = "Nyní vám budeme ukazovat nadpisy jiných článků. Jedná se o naučné encyklopedické články. Vaším úkolem bude vybrat z každé dvojice článek, který byste si raději přečetli. Po vybrání článků budete mít možnost si přečíst náhodně vybrané tři články z vámi vybraných článků. Tento úkol bude mít opět 30 kol."

qMyself = "Který článek byste si raději chtěl(a) přečíst?"

################################################################################


class Choice(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.total = 9
        self.who = who
        
        pairs = [["envi", "anti"], ["envi", "filler"], ["anti", "filler"]]
        pairs *= int(self.total / 3)        
        envi = [i for i in range(1, 21)]
        anti = [i for i in range(1, 21)]
        filler = [i for i in range(1, 21)]
        random.shuffle(pairs)
        random.shuffle(envi)
        random.shuffle(anti)
        random.shuffle(filler)        
        self.items = []        
        for i in range(self.total):
            pair = pairs.pop()
            random.shuffle(pair)     
            left = "{}_{}".format(eval(pair[0]).pop(), pair[0])
            right = "{}_{}".format(eval(pair[1]).pop(), pair[1])
            self.items.append([left, right])

        self.trial = 1

        self.trialText = ttk.Label(self, text = f"Volba: 1/{self.total}", font = "helvetica 15 bold", background = "white", justify = "right")

        leftLabel = ttk.Label(self, text = "Článek A", font = "helvetica 15 bold", background = "white", justify = "center")
        rightLabel = ttk.Label(self, text = "Článek B", font = "helvetica 15 bold", background = "white", justify = "center")

        self.left = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 50, height = 10, wrap = "word", highlightbackground = "white")
        self.right = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 50, height = 10, wrap = "word", highlightbackground = "white")

        questionText = qOthers if who == "others" else qMyself
        question = ttk.Label(self, text = questionText, font = "helvetica 15 bold", background = "white", justify = "center")

        ttk.Style().configure("TButton", font = "helvetica 15")
        leftChoice = ttk.Button(self, text = "Článek A", command = lambda: self.chosen("A"))
        rightChoice = ttk.Button(self, text = "Článek B", command = lambda: self.chosen("B"))

        self.trialText.grid(column = 3, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)

        leftLabel.grid(column = 1, row = 1, pady = 10)
        rightLabel.grid(column = 3, row = 1, pady = 10)

        self.left.grid(column = 1, row = 2)
        self.right.grid(column = 3, row = 2)
        question.grid(column = 1, row = 3, columnspan = 3, pady = 30)
        leftChoice.grid(column = 1, row = 4, pady = 20)
        rightChoice.grid(column = 3, row = 4, pady = 20)

        self.columnconfigure(0, weight = 3)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 3)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(5, weight = 1)    

        self.file.write("Articles\n")
        self.createText()
        

    def chosen(self, choice):
        self.file.write("\t".join([self.id, self.who, str(self.trial), *self.items[self.trial - 1][0].split("_"), *self.items[self.trial - 1][1].split("_"), choice]) + "\n")
        self.trial += 1
        self.trialText["text"] = f"Volba: {self.trial}/{self.total}"
        if self.trial > self.total:
            self.nextFun()
        else:
            self.createText()
        

    def createText(self):
        self.left.delete("1.0", "end")
        self.right.delete("1.0", "end")
        with open(os.path.join(os.getcwd(), "Stuff", "Texts", "text{}_{}.txt".format(*self.items[self.trial - 1][0].split("_")))) as f:
            text = f.read()
            self.left.insert("1.0", text) 
        with open(os.path.join(os.getcwd(), "Stuff", "Texts", "text{}_{}.txt".format(*self.items[self.trial - 1][1].split("_")))) as f:
            text = f.read()
            self.right.insert("1.0", text) 

    

InstructionsArticlesOthers = (InstructionsFrame, {"text": introArticlesOthers, "height": 5})
InstructionsArticlesMyself = (InstructionsFrame, {"text": introArticlesMyself, "height": 5})
ChoiceOthers = (Choice, {"who": "others"})
ChoiceMyself = (Choice, {"who": "myself"})



# for i in range(20):
#     with open(os.path.join(os.getcwd(), "Texts", f"text{i + 1}_filler.txt"), mode = "w") as f:
#         f.write(f"TEXT FILLER {i + 1}\n")
#         repeats = random.randint(1,6)
#         for j in range(repeats):
#             f.write(f"Toto je filler text {i + 1}\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([ChoiceOthers,
         InstructionsArticlesOthers, 
         ChoiceOthers,        
         InstructionsArticlesMyself,
         ChoiceMyself
         ])