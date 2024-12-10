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

introArticlesOthers = "Nyní Vám vám budeme ukazovat titulky článků. Jedná se o krátké články, které vyjadřují různé názory autorů. Vaším úkolem bude vybrat z každé dvojice článek, který by si podle Vás měli ostatní účastníci experimentu přečíst. Některé z článků, které vyberete, dostanou náhodně vybraní účastníci experimentu a budou mít čas si je přečíst. Tento úkol bude mít 30 kol."

qOthers = "Který z uvedených článků chcete, aby si jiný účastník studie přečetl?"


introArticlesMyself = "Nyní Vám budeme ukazovat titulky jiných článků. Jedná se o naučné encyklopedické články. Vaším úkolem bude vybrat z každé dvojice článek, který byste si raději přečetli. Po vybrání článků budete mít možnost si přečíst náhodně vybrané tři články z Vámi vybraných článků. Tento úkol bude mít opět 30 kol."

qMyself = "Který článek byste si raději chtěl(a) přečíst?"


introReading = "Nyní máte možnost si přečíst náhodně vybrané články, které jste si vybrali v dřívější části studie."

introReadingOthers = "Nyní máte možnost si přečíst náhodně vybrané články, které vybrali ostatní účastníci studie."

################################################################################


class Choice(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.total = 3
        self.who = who
        self.root.status["articles"] = []
        
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
        self.rowconfigure(5, weight = 2)    

        self.file.write("Articles\n")
        self.createText()
        

    def chosen(self, choice):
        chosen = 0 if choice == "A" else 1
        self.root.status["articles"].append(self.items[self.trial - 1][chosen])
        self.file.write("\t".join([self.id, self.who, str(self.trial), *self.items[self.trial - 1][0].split("_"), *self.items[self.trial - 1][1].split("_"), choice]) + "\n")
        self.trial += 1
        self.trialText["text"] = f"Volba: {self.trial}/{self.total}"
        if self.trial > self.total:
            if self.who == "myself":
                random.shuffle(self.root.status["articles"])
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



    

InstructionsArticlesOthers = (InstructionsFrame, {"text": introArticlesOthers, "height": 5})
InstructionsArticlesMyself = (InstructionsFrame, {"text": introArticlesMyself, "height": 5})
InstructionsReading = (InstructionsFrame, {"text": introReading, "height": 5})
InstructionsReadingOthers = (InstructionsFrame, {"text": introReadingOthers, "height": 5})
ChoiceOthers = (Choice, {"who": "others"})
ChoiceMyself = (Choice, {"who": "myself"})
ArticlesOthers = (Articles, {"who": "others"})
ArticlesMyself = (Articles, {"who": "myself"})


# for i in range(20):
#     with open(os.path.join(os.getcwd(), "Texts", f"text{i + 1}_envi.txt"), mode = "w") as f:
#         f.write(f"TEXT ENVI {i + 1}\n")
#         repeats = random.randint(1,6)
#         for j in range(repeats):
#             f.write(f"Toto je envi text {i + 1}\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([InstructionsArticlesOthers, 
         ChoiceOthers,      
         InstructionsArticlesMyself,
         ChoiceMyself,
         InstructionsReading,
         ArticlesMyself,
         InstructionsReadingOthers,
         ArticlesOthers  
         ])