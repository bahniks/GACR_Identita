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

from common import InstructionsFrame
from gui import GUI
from constants import TESTING, URL






class Login(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "Počkejte na spuštění experimentu", height = 3, font = 15, width = 45, proceed = False)

        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def login(self):       
        count = 0
        while True:
            self.update()
            if count % 50 == 0:            
                data = urllib.parse.urlencode({'id': self.root.id, 'round': 0, 'offer': "login"})
                data = data.encode('ascii')
                if URL == "TEST":
                    condition = random.choice(["control", "version", "reward", "version_reward"])
                    incentive_order = random.choice(["high-low", "low-high"])
                    tokenCondition = random.choice([True, False])                    
                    winning_block = str(random.randint(1,6))
                    winning_trust = str(random.randint(3,6))
                    trustRoles = "".join([random.choice(["A", "B"]) for i in range(4)])
                    trustPairs = "_".join([str(random.randint(1, 10)) for i in range(4)])                    
                    response = "|".join(["start", condition, incentive_order, str(tokenCondition), winning_block, winning_trust, trustRoles, trustPairs, str(random.randint(1,2000))])
                else:
                    response = ""
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8") 
                    except Exception:
                        self.changeText("Server nedostupný")
                if "start" in response:
                    info, condition, incentive_order, tokenCondition, winning_block, winning_trust, trustRoles, trustPairs, idNumber = response.split("|")              
                    self.root.status["condition"] = condition   
                    self.create_control_question(condition)
                    self.root.status["incentive_order"] = incentive_order                    
                    self.root.status["tokenCondition"] = eval(tokenCondition)
                    self.root.texts["block"] = self.root.status["winning_block"] = winning_block
                    self.root.texts["trustblock"] = self.root.status["winning_trust"] = winning_trust
                    self.root.status["trust_roles"] = list(trustRoles)
                    self.root.status["trust_pairs"] = trustPairs.split("_")                 
                    self.root.texts["idNumber"] = '{:03d}'.format(int(idNumber) % 1000)
                    self.update_intros(condition, incentive_order)
                    self.progressBar.stop()
                    self.write(response)
                    self.nextFun()                      
                    break
                elif response == "login_successful" or response == "already_logged":
                    self.changeText("Přihlášen")
                    self.root.status["logged"] = True
                elif response == "ongoing":
                    self.changeText("Do studie se již nelze připojit")
                elif response == "no_open":
                    self.changeText("Studie není otevřena")
                elif response == "closed":
                    self.changeText("Studie je uzavřena pro přihlašování")
                elif response == "not_grouped":
                    self.changeText("V experimentu nezbylo místo. Zavolejte prosím experimentátora zvednutím ruky.")
            count += 1                  
            sleep(0.1)        

    def run(self):
        self.progressBar.start()
        self.login()

    def update_intros(self, condition, incentive_order):
        pass
        # self.root.texts["incentive_4"] = 50 if incentive_order == "low-high" else 200
        # self.root.texts["incentive_5"] = 200 if incentive_order == "low-high" else 50
        # self.root.texts["add_block_4"] = eval(condition + "Text")
        # self.root.texts["add_block_5"] = eval(condition + "Text")
        # self.root.texts["add_block_6"] = eval(condition + "Text")
        # self.root.texts["add_block_6"] += tokenConditionText if self.root.status["tokenCondition"] else "\n\n" + version_choice

    def create_control_question(self, condition):        
        pass
        # feedbackManipulation = []
        # conditions = ["version_reward", "version", "reward", "control"]
        # cf = correctFeedback if condition != "control" else correctFeedbackControl
        # inf = incorrectFeedback if condition != "control" else incorrectFeedbackControl
        # for i, cond in enumerate(conditions):
        #     f = cf if condition == cond else inf
        #     feedbackManipulation.append(f + answersManipulation[conditions.index(condition)].lower())
        # self.root.texts["controlTexts2"] = [[controlManipulation, answersManipulation, feedbackManipulation]]        

    def write(self, response):
        self.file.write("Login" + "\n")
        self.file.write(self.id + response.replace("|", "\t").lstrip("start") + "\n\n")        

    def gothrough(self):
        self.run()