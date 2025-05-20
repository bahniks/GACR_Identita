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

likingQuestion = "<center>Klikněte na možnost, která se Vám více líbí z této dvojice.</center>"


################################################################################


class Liking(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = likingQuestion, height = 2, font = 15, width = 80, proceed = False)

        self.totalTrials = 30
        self.trial = 0

        self.maximum = 30

        with open(os.path.join(os.getcwd(), "Stuff", "pairs.txt"), "r", encoding="utf-8") as file:
            self.pairs = [line.strip().split(" ") for line in file]
        self.originalPairs = self.pairs.copy()
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

        self.t0 = perf_counter()


    def send(self):                
        data = {'id': self.id, 'round': "liking", 'offer': "".join(self.originalPairs)}
        if URL != "TEST":
            self.sendData(data)

    def leftClicked(self):
        self.nextTrial("left")

    def rightClicked(self):
        self.nextTrial("right")

    def nextTrial(self, answer):        
        if self.trial != 0:
            limit = 0.1 if TESTING else 0.5
            if perf_counter() - self.t0 < limit:            
                return
            
            left = self.currentPair[0]
            right = self.currentPair[1]            
            self.file.write(f"{self.id}\t{self.trial}\t{left}\t{right}\t{answer}\n")

            for i in range(len(self.originalPairs)):
                search = left if answer == "left" else right
                if len(self.originalPairs[i]) == 1:
                    continue
                if self.originalPairs[i][0] == search:
                    self.originalPairs[i] = "0"
                    break
                elif self.originalPairs[i][1] == search:
                    self.originalPairs[i] = "1"
                    break

        if self.trial == self.totalTrials:
            self.file.write("\n")
            self.send()
            self.nextFun()
        else:            
            self.trial += 1
            self.currentPair = self.pairs[self.trial - 1]
            random.shuffle(self.currentPair)
            self.left["text"] = self.currentPair[0]
            self.right["text"] = self.currentPair[1]            
            self.trialText["text"] = f"Dvojice: {self.trial}/{self.totalTrials}"
            self.t0 = perf_counter()






InstructionsLiking = (InstructionsFrame, {"text": introLiking, "height": 5})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#InstructionsLiking, 
         Liking
         ])
