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

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding, OneFrame, Question, TextArea, read_all
from gui import GUI
from constants import TESTING, URL


################################################################################
# TEXTS

introArticlesOthers = "Nyní Vám budeme ukazovat titulky článků. Jedná se o krátké články, které vyjadřují různé názory autorů. Vaším úkolem bude vybrat z každé dvojice článek, který by si podle Vás měli ostatní účastníci experimentu přečíst. Některé z článků, které vyberete, dostanou náhodně vybraní účastníci této studie a budou mít čas si je přečíst. Tento úkol bude mít 24 kol."

qOthers = "Který z uvedených článků chcete, aby si jiný účastník studie přečetl?"


introArticlesMyself = "Nyní Vám budeme ukazovat titulky jiných článků. Jedná se o naučné encyklopedické články. Vaším úkolem bude vybrat z každé dvojice článek, který byste si raději přečetli. Následně budete mít možnost přečíst si z těchto článků tři náhodně vybrané. Tento úkol bude mít opět 30 kol."

qMyself = "Který článek byste si raději chtěl(a) přečíst?"


introReading = "Nyní máte možnost přečíst si tři náhodně vybrané články z těch, které jste si vybrali dříve."

introReadingOthers = "Nyní máte možnost si přečíst náhodně vybrané články, které vybrali ostatní účastníci studie."

################################################################################



class Choice(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.total = 24
        self.who = who
        self.root.status["articles"] = []
        
        self.titles = {}
        types = ["envi", "filler", "anti"]
        if who == "others":
            t = read_all("articles_others_titles.txt")                        
            for count, title in enumerate(t.split("\n")):      
                n = count % 16    
                self.titles[types[count // 16] + str(n + 1)] = title                                

        pairs = [["envi", "anti"], ["envi", "filler"], ["anti", "filler"]]
        pairs *= int(self.total / 3)        
        envi = [i for i in range(1, self.total*2 // 3 + 1)]
        anti = [i for i in range(1, self.total*2 // 3 + 1)] 
        filler = [i for i in range(1, self.total*2 // 3 + 1)]
        random.shuffle(pairs)
        random.shuffle(envi)
        random.shuffle(anti)
        random.shuffle(filler)        
        self.items = []        
        for i in range(self.total):
            pair = pairs.pop()
            random.shuffle(pair)     
            left = "{}{}".format(pair[0], eval(pair[0]).pop())
            right = "{}{}".format(pair[1], eval(pair[1]).pop())            
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
        limit = 0.2 if TESTING else 0.5
        if perf_counter() - self.t0 < limit:
            return
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
        self.t0 = perf_counter()
        self.left["state"] = "normal"
        self.right["state"] = "normal"
        self.left.delete("1.0", "end")
        self.right.delete("1.0", "end")
        self.left.insert("1.0", self.titles[self.items[self.trial - 1][0]]) 
        self.right.insert("1.0", self.titles[self.items[self.trial - 1][1]])
        self.left["state"] = "disabled" 
        self.right["state"] = "disabled"
        # with open(os.path.join(os.getcwd(), "Stuff", "Texts", "text{}_{}.txt".format(*self.items[self.trial - 1][0].split("_")))) as f:
        #     text = f.read()
        #     self.left.insert("1.0", text) 
        # with open(os.path.join(os.getcwd(), "Stuff", "Texts", "text{}_{}.txt".format(*self.items[self.trial - 1][1].split("_")))) as f:
        #     text = f.read()
        #     self.right.insert("1.0", text) 



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

        self.trialText = ttk.Label(self, text=f"Článek: 1/{self.total}", font="helvetica 15 bold", background="white", justify="right")

        self.text = Text(self, font="helvetica 15", relief="flat", background="white", width=80, height=15, wrap="word", highlightbackground="white")

        self.scrollbar = ttk.Scrollbar(self, command=self.on_scroll)  # Bind to custom scroll function
        self.text.config(yscrollcommand=self.scrollbar.set)

        ttk.Style().configure("TButton", font="helvetica 15")
        self.next = ttk.Button(self, text="Pokračovat", command=self.proceed)

        self.trialText.grid(column=1, columnspan=2, row=0, pady=30, padx=30, sticky=NE)
        self.text.grid(column=1, row=2)
        self.scrollbar.grid(column=2, row=2, sticky="NSW")
        self.next.grid(column=1, row=4, pady=30)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(2, weight=1)   
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=3)    

        self.next["state"] = "disabled"

        self.file.write("Articles\n")

        self.createText()
        
    def on_scroll(self, *args):
        """Custom scroll function to track scrollbar usage and end position."""
        self.scrolled = True  # Mark that the scrollbar was used
        self.text.yview(*args)  # Perform the actual scrolling

        # Check if the scrollbar is at the bottom
        if float(self.text.yview()[1]) == 1.0:
            self.end = True
        else:
            self.end = False

    def createText(self):
        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        source = self.root.status["articles"] if self.who == "myself" else self.root.status["othersArticles"]
        self.filename = "text{}_{}.txt".format(*source[self.trial - 1].split("_"))
        with open(os.path.join(os.getcwd(), "Stuff", "Texts", self.filename)) as f:
            self.text.insert("1.0", f.read() * 3)
        self.text["state"] = "disabled"
        self.t0 = perf_counter()
        self.disable()
        self.scrolled = False  # Tracks if the scrollbar was used
        self.end = False       # Tracks if the text was scrolled to the end
        
    def disable(self):
        self.next["state"] = "disabled"
        limit = 0.1 if TESTING else 3
        self.after(int(limit * 6000), self.enable)   
        
    def proceed(self):
        self.file.write("\t".join([self.id, self.who, str(self.trial), self.filename, str(perf_counter() - self.t0), str(self.scrolled), str(self.end)]) + "\n")
        self.trial += 1
        if self.trial > self.total:
            self.nextFun()
        else:
            self.trialText["text"] = f"Článek: {self.trial}/{self.total}"
            self.createText()  
        
    def enable(self):
        self.next["state"] = "normal"
        


    

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
    GUI([#InstructionsArticlesOthers, 
         ChoiceOthers,      
         #InstructionsArticlesMyself,
         #ChoiceMyself,
         #InstructionsReading,
         ArticlesMyself,
         InstructionsReadingOthers,
         ArticlesOthers  
         ])