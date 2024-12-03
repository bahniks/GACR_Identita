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
NUMGROUPS = 6

closeText = f"""Ze skupin níže vyberte kliknutím na tlačítko {NUMGROUPS} skupin, které jsou Vám nejblíže."""

distantText = f"""Nyní skupin níže vyberte kliknutím na tlačítko {NUMGROUPS} skupin, které jsou Vám nejvzdálenější."""

remainingText = "Zbývá vybrat skupin: {}"

################################################################################



class Groups(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = closeText, height = 2, font = 15, width = 80, proceed = True)

        self.groups = [f"Skupina {i+1}" for i in range(30)]

        columns = 6
        rows = 5

        self.chosen = set()

        ttk.Style().configure("Padded.TButton", padding = (2,2))
        

        self.groupFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.buttons = {}
        for i, group in enumerate(self.groups):
            self.buttons[group] = ttk.Button(self.groupFrame, text = group, command = lambda g = group: self.clicked(g))
            self.buttons[group].config(style="Padded.TButton")    
            self.buttons[group].grid(row = i // columns, column = i % columns, padx = 10, pady = 10)

        self.remaining = ttk.Label(self, text = remainingText.format(NUMGROUPS), font = "helvetica 15", background = "white")

        self.groupFrame.grid(row = 2, column = 1)
        self.remaining.grid(row = 3, column = 1, sticky = N)
        self.next.grid(row = 4, column = 1)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)

        self.next["state"] = "disabled"


    def clicked(self, group):
        if group in self.chosen:
            self.buttons[group].config(style="Padded.TButton")        
            self.chosen.remove(group)
        else:
            ttk.Style().configure("Clicked.TButton", background="lightgreen", foreground="green", font=("Helvetica", 15, "underline", "bold"), padding = (2, 1))
            self.buttons[group].config(style="Clicked.TButton")
            self.chosen.add(group)
        self.remaining["text"] = remainingText.format(NUMGROUPS - len(self.chosen))
        



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Groups
         ])
