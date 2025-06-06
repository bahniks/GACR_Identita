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

introArticlesOthers = "Nyní Vám budeme ukazovat titulky článků. Jedná se o krátké články, které vyjadřují různé názory autorů. Vaším úkolem bude vybrat z každé dvojice článek, který by si podle Vás měli ostatní účastníci experimentu přečíst. Vybraní účastníci této studie dostanou některé náhodně vybrané články z těch, které vyberete, a budou mít čas si je přečíst. Tento úkol bude mít 24 kol."

qOthers = "Který z uvedených článků chcete, aby si jiný účastník studie přečetl?"


introArticlesMyself = "Nyní Vám budeme ukazovat titulky jiných článků. Jedná se o naučné encyklopedické články. Vaším úkolem bude vybrat z každé dvojice článek, který byste si raději přečetli. Následně budete mít možnost přečíst si z těchto článků tři náhodně vybrané. Tento úkol bude mít opět 24 kol."

qMyself = "Který článek byste si raději chtěl(a) přečíst?"


introReading = """Nyní máte možnost přečíst si tři náhodně vybrané články z těch, které jste si vybrali dříve.
Na tyto články se již dále nebudeme ptát a na jejich přečtení nijak nezávisí Vaše odměna.
Tlačítko Pokračovat se automaticky aktivuje po 30 vteřinách."""

introReadingOthers = """Nyní máte možnost si přečíst náhodně vybrané články, které vybrali ostatní účastníci studie.
Na tyto články se již dále nebudeme ptát a na jejich přečtení nijak nezávisí Vaše odměna.
Tlačítko Pokračovat se automaticky aktivuje po 2 minutách."""

################################################################################



class Choice(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.total = 24
        self.who = who
        if who == "myself":
            self.root.status["myselfArticlesChosen"] = []            
            self.titles = {}
            types = ["envi", "filler"]
            t = read_all("articles_myself_titles.txt")
            self.root.status["myselfArticlesTitles"] = t.split("\n")
            for count, title in enumerate(self.root.status["myselfArticlesTitles"]):      
                n = count % self.total
                self.titles[types[count // self.total] + str(n + 1)] = title     
                
            envi = ["envi{}".format(i) for i in range(1, self.total + 1)]
            filler = ["filler{}".format(i) for i in range(1, self.total + 1)]
            random.shuffle(envi)
            random.shuffle(filler)
            self.items = [[i, j] if random.random() < 0.5 else [j, i] for i, j in zip(envi, filler)]      
            
            self.root.status["myselfArticlesTitles"] = self.titles
            
        else:
            self.root.status["othersArticlesChosen"] = []        
            self.titles = {}
            types = ["envi", "filler", "anti"]
            t = read_all("articles_others_titles.txt")                        
            for count, title in enumerate(t.split("\n")):      
                n = count % 16    
                self.titles[types[count // 16] + str(n + 1)] = title  
            self.root.status["othersArticlesTitles"] = self.titles                             

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

        self.left = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 50, height = 6, wrap = "word", highlightbackground = "white")
        self.right = Text(self, font = "helvetica 15", relief = "flat", background = "white", width = 50, height = 6, wrap = "word", highlightbackground = "white")
        self.left.tag_configure("center", justify="center")
        self.right.tag_configure("center", justify="center")

        questionText = qOthers if who == "others" else qMyself
        question = ttk.Label(self, text = questionText, font = "helvetica 15 bold", background = "white", justify = "center")

        ttk.Style().configure("TButton", font = "helvetica 15")
        leftChoice = ttk.Button(self, text = "Článek A", command = lambda: self.chosen("A"))
        rightChoice = ttk.Button(self, text = "Článek B", command = lambda: self.chosen("B"))

        self.trialText.grid(column = 3, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)

        leftLabel.grid(column = 1, row = 2, pady = 10)
        rightLabel.grid(column = 3, row = 2, pady = 10)

        self.left.grid(column = 1, row = 3)
        self.right.grid(column = 3, row = 3)
        question.grid(column = 1, row = 1, columnspan = 3, pady = 30)
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
        limit = 0.1 if TESTING else 0.5
        if perf_counter() - self.t0 < limit:
            return
        chosen = 0 if choice == "A" else 1
        if self.who == "myself":            
            self.root.status["myselfArticlesChosen"].append(self.items[self.trial - 1][chosen])
        else:
            self.root.status["othersArticlesChosen"].append([*self.items[self.trial - 1], self.items[self.trial - 1][chosen]])
        
        self.file.write("\t".join([self.id, self.who, str(self.trial), *self.items[self.trial - 1][0].split("_"), *self.items[self.trial - 1][1].split("_"), choice, str(perf_counter() - self.t0)]) + "\n")
        self.trial += 1
        self.trialText["text"] = f"Volba: {self.trial}/{self.total}"
        if self.trial > self.total:
            if self.who == "myself":
                random.shuffle(self.root.status["myselfArticlesChosen"])
            else:
                triples = "|".join(["_".join(i) for i in self.root.status["othersArticlesChosen"]])
                data = {'id': self.id, 'round': "articles", 'offer': triples}
                if URL != "TEST":
                    self.sendData(data)
            self.nextFun()
        else:            
            self.createText()
        

    def createText(self):
        self.t0 = perf_counter()
        self.left["state"] = "normal"
        self.right["state"] = "normal"
        self.left.delete("1.0", "end")
        self.right.delete("1.0", "end")
        self.left.insert("1.0", self.titles[self.items[self.trial - 1][0]], "center ") 
        self.right.insert("1.0", self.titles[self.items[self.trial - 1][1]], "center ")
        self.left["state"] = "disabled" 
        self.right["state"] = "disabled"



class Articles(ExperimentFrame):
    def __init__(self, root, who):
        super().__init__(root)

        self.who = who

        self.total = 3
        self.trial = 1

        # if TESTING and self.who == "myself" and URL == "TEST":
        #      self.root.status["myselfArticlesChosen"] = [f"envi{i}" for i in range(1, 25)] + [f"filler{i}" for i in range(1, 25)]           
        #      self.total = 48
        # if TESTING and self.who == "others":
        #     if not "othersArticles" in self.root.status:            
        #         self.root.status["othersArticles"] = [f"envi{i}" for i in range(1, 17)] + [f"filler{i}" for i in range(1, 17)] + [f"anti{i}" for i in range(1, 17)]      
        #         self.total = 48            
            #self.root.status["othersArticlesTitles"] = self.root.status["othersArticlesTitles"][self.root.status["othersArticles"]]

        self.trialText = ttk.Label(self, text=f"Článek: 1/{self.total}", font="helvetica 15 bold", background="white", justify="right")

        self.title = Text(self, font="helvetica 15 bold", relief="flat", background="white", width=80, height=2, wrap="word", highlightbackground="white")
        self.title.tag_configure("center", justify="center")  
        height = 10 if self.who == "myself" else 12
        self.text = Text(self, font="helvetica 15", relief="flat", background="white", width=80, height=height, wrap="word", highlightbackground="white", spacing2 = 5, spacing3 = 20)

        self.scrollbar = ttk.Scrollbar(self, command=self.on_scroll)  # Bind to custom scroll function
        self.text.config(yscrollcommand=self.scrollbar.set)

        ttk.Style().configure("TButton", font="helvetica 15")
        self.next = ttk.Button(self, text="Pokračovat", command=self.proceed)

        self.trialText.grid(column=1, columnspan=2, row=0, pady=30, padx=30, sticky=NE)
        self.title.grid(column=1, row=1, pady=10, sticky = S)
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

        self.file.write("Reading\n")

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
        source = self.root.status["myselfArticlesTitles"] if self.who == "myself" else self.root.status["othersArticlesTitles"]

        self.title["state"] = "normal"
        self.title.delete("1.0", "end")
        self.chosen = self.root.status["myselfArticlesChosen"][self.trial - 1] if self.who == "myself" else self.root.status["othersArticles"][self.trial - 1]
        self.title.insert("1.0", source[self.chosen].replace(".", "\n"), "center")
        self.title["state"] = "disabled"

        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.filename = "{}.txt".format(source[self.chosen]).replace(":", "_").replace("?", "_").replace("%", "_").replace("„", "_").replace("“", "_").strip()
        with open(os.path.join(os.getcwd(), "Stuff", "Texts", self.filename), encoding = "utf-8") as f:
            self.text.insert("1.0", f.read().strip("'").strip('"').strip().replace('""', '"'))
        self.text["state"] = "disabled"
        self.t0 = perf_counter()
        self.disable()
        self.scrolled = False  # Tracks if the scrollbar was used
        self.end = False       # Tracks if the text was scrolled to the end
        
    def disable(self):
        self.next["state"] = "disabled"
        limit = 0.5 if self.who == "myself" else 2
        if TESTING:
            limit = 0.001
        self.after(int(limit * 60000), self.enable)   
        
    def proceed(self):
        self.file.write("\t".join([self.id, self.who, str(self.trial), self.chosen, self.filename.rstrip(".txt"), str(perf_counter() - self.t0), str(self.scrolled), str(self.end)]) + "\n")
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



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    from trustgame import WaitArticles
    GUI([InstructionsArticlesOthers, 
         ChoiceOthers,      
         InstructionsArticlesMyself,
         ChoiceMyself,
         InstructionsReading,
         ArticlesMyself,
         WaitArticles,
         InstructionsReadingOthers,
         ArticlesOthers  
         ])