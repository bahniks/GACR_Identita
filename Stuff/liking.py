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

introLiking = """Nyní vám budeme ukazovat různé dvojice. Vaším úkolem bude určit, která možnost z každé dvojice se Vám líbí více. Tento úkol bude mít 30 kol."""

likingQuestion = "Klikněte na možnost, která se Vám více líbí z této dvojice."


################################################################################


class Liking(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = likingQuestion, height = 2, font = 15, width = 80, proceed = False)

        self.totalTrials = 30
        self.trial = 0

        self.maximum = 30

        #self.pairs = [["Něco {}".format(i), "Něco {}".format(i + self.totalTrials)] for i in range(self.totalTrials)] # TODO
        with open(os.path.join(os.getcwd(), "Stuff", "pairs.txt"), "r", encoding="utf-8") as file:
            self.pairs = [line.strip().split(" ") for line in file]
        random.shuffle(self.pairs)
   
        self.trialText = ttk.Label(self, text = "", font = "helvetica 15", background = "white", justify = "right")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.left = ttk.Button(self, text = "", command = self.leftClicked, width = 15)
        self.right = ttk.Button(self, text = "", command = self.rightClicked, width = 15)

        self.left.grid(column = 1, row = 2, padx = 60, sticky = E) 
        self.right.grid(column = 2, row = 2, padx = 60, sticky = W)        
        

        self.trialText.grid(column = 2, columnspan = 2, row = 0, pady = 30, padx = 30, sticky = NE)
        
        self.text.grid(row = 1, column = 1, columnspan = 2)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(3, weight = 2)    

        self.file.write("Liking\n")
        
        self.nextTrial("")


    def leftClicked(self):
        self.nextTrial("left")

    def rightClicked(self):
        self.nextTrial("right")

    def nextTrial(self, answer):
        if self.trial == self.totalTrials:
            self.nextFun()
        else:
            self.trial += 1
            self.left["text"] = self.pairs[self.trial - 1][0]
            self.right["text"] = self.pairs[self.trial - 1][1]
            self.trialText["text"] = f"Dvojice: {self.trial}/{self.totalTrials}"






InstructionsLiking = (InstructionsFrame, {"text": introLiking, "height": 5})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#InstructionsLiking, 
         Liking
         ])
