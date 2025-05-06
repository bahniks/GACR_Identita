#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep,  perf_counter
from itertools import chain
from collections import defaultdict

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI



##################################################################################################################
# TEXTS #
#########

questionText = """Který z dvojice výrobků byste si raději odnesl(a) domů?
Vyberte kliknutím na obrázek."""

intro = """Blížíme se ke konci tohoto experimentálního sezení. Jako malé poděkování vylosujeme každého desátého respondenta, který vyhraje nad rámec své odměny několik výrobků podle vlastního výběru. 

Nyní Vám postupně ukážeme 15 párů výrobků. U každého páru klikněte na ten výrobek, který by se Vám líbil více. Máte pravděpodobnost 10%, že vyhrajete náhodně vybraných 5 výrobků z těch, které si vyberete. Vybírejte proto prosím pečlivě, později už není možné volbu změnit. 
"""

##################################################################################################################


ProductsIntro =(InstructionsFrame, {"text": intro, "height": 7})


class Choices(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        with open(os.path.join(os.path.dirname(__file__), "products.txt")) as f:
            self.infos = [line.rstrip().split("\t") for line in f]
        random.shuffle(self.infos)

        self.file.write("Products\n")        

        self.selected = defaultdict(list)

        self.order = -1                      

        self.text = ttk.Label(self, font = "helvetica 15", justify = "center", background = "white", text = questionText)
        self.text.grid(row = 0, column = 0, sticky = S, pady = 35)
             
        self.twoProducts = TwoProducts(self)
        self.twoProducts.grid(row = 1, column = 0)

        self.columnconfigure(0, weight = 1)      
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)

        self.proceed()
        
    def proceed(self):
        self.order += 1
        if self.order == len(self.infos):
            self.root.status["products"] = self.selected
            self.nextFun()
        else:
            self.twoProducts.changeImages(self.infos[self.order][0])
            self.t0 = time()            


class TwoProducts(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white", background = "white")

        self.root = root
        self.selected = self.root.selected
            
        self.leftProduct = OneProduct(self)
        self.leftProduct.grid(column = 1, row = 1, padx = 5)

        self.rightProduct = OneProduct(self)
        self.rightProduct.grid(column = 3, row = 1, padx = 5)
                            
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)

    def proceed(self):
        self.root.proceed()

    def changeImages(self, product):
        self.sides = ["Bio", "Nebio"]
        random.shuffle(self.sides)
        left = os.path.join(os.path.dirname(__file__), "Products", self.sides[0], product)
        right = os.path.join(os.path.dirname(__file__), "Products", self.sides[1], product)
        if self.sides[0] == "Bio":
            leftDescription = self.root.infos[self.root.order][1]
            rightDescription = self.root.infos[self.root.order][2]
        else:   
            leftDescription = self.root.infos[self.root.order][2]
            rightDescription = self.root.infos[self.root.order][1]
        self.leftProduct.changeImage(left, leftDescription)
        self.rightProduct.changeImage(right, rightDescription)


class OneProduct(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white")

        self["background"] = "white"

        self.root = root
        self.selected = self.root.selected

        self.product = Product(self)
        self.product.grid(column = 1, row = 0)

        self.label = ttk.Label(self, text = "", background = "white", font = "helvetica 15", width = 60, anchor = "center")
        self.label.grid(column = 1, row = 1, pady = 8)
        self.bottomLabel = ttk.Label(self, text = "", background = "white", font = "helvetica 15")
        self.bottomLabel.grid(column = 1, row = 2, pady = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def changeImage(self, product, description):        
        self.product.changeImage(product + ".png")        
        self.label["text"] = description
            
    def proceed(self):
        self.root.proceed()

    def highlight(self):
        self.product.highlight()

    def removeHighlight(self):
        self.product.removeHighlight()



class Product(Label):
    def __init__(self, root):
        super().__init__(root, background = "white", foreground = "white", relief = "flat", borderwidth = 10)

        self.root = root
        self.selected = self.root.selected

        self.bind("<Enter>", self.entered)
        self.bind("<Leave>", self.left)
        self.bind("<1>", self.clicked)

    def changeImage(self, file):
        file = os.path.join(os.path.dirname(__file__), "Products", file)        
        self.image = PhotoImage(file = file)
        self["image"] = self.image
        self.file = file

    def entered(self, _):
        self.config(cursor = "hand2")

    def left(self, _):
        self.config(cursor = "arrow")

    def clicked(self, _):
        name = os.path.basename(self.file)
        folder = os.path.basename(os.path.dirname(self.file))
        self.selected[name].append(folder)
        self.root.root.root.file.write("\t".join([self.root.root.root.id,
                                                  str(self.root.root.root.order + 1),
                                                  self.root.label["text"],
                                                  #str(self.root.root.root.current[0]),
                                                  self.root.root.leftProduct.label["text"],
                                                  self.root.root.rightProduct.label["text"],
                                                  str(time() - self.root.root.root.t0)]
                                                 ) + "\n")
        self.root.proceed()

    def highlight(self):
        self["background"] = "red"

    def removeHighlight(self):
        self["background"] = "white"
        





def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#ProductsIntro,
         Choices
         ])


if __name__ == "__main__":
    main()

