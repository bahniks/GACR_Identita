#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

#from quest import QuestInstructions
from intros import Initial, Intro, Ending
from demo import Demographics
#from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
from trustgame import WaitResults, Trust, TrustResult, InstructionsTrust, IntroTrust
#from questionnaire import PoliticalSkill, TDMS, HEXACOinfo
from comments import Comments
from login import Login
from sameness import InstructionsSameness, Sameness
from liking import InstructionsLiking, Liking
from articles import InstructionsArticlesOthers, ChoiceOthers, InstructionsArticlesMyself, ChoiceMyself, InstructionsReading
from articles import ArticlesMyself, InstructionsReadingOthers, ArticlesOthers  
from groups import InstructionsGroups, Groups
from favoritism import Favoritism, InstructionsFavoritism
from products import ProductsIntro, Choices


frames = [Initial,
          Intro,
          Login,    
          InstructionsGroups,
          Groups,
          InstructionsLiking,
          Liking,          
          InstructionsArticlesOthers,
          ChoiceOthers,     
          InstructionsArticlesMyself,
          ChoiceMyself,     
          #WaitGroups, # cekani na vyplneni skupin
          IntroTrust,
          InstructionsTrust,
          #WaitTrust, 
          Trust,
          #WaitTrust,
          Trust, # bude se jeste opakovat vicekrat (+ synteticke osoby) - predelat s uvadenim trialu, jako jinde    
          # cekani na vyplneni skupin      
          InstructionsFavoritism,
          Favoritism,
          InstructionsSameness, 
          Sameness,              
          InstructionsReading,
          ArticlesMyself,
          InstructionsReadingOthers,
          # cekani na vyber clanku
          ArticlesOthers,
        #   Lottery,  ?
        #   LotteryWin,  ?
          ProductsIntro,
          Choices,
          LotteryInstructions,
          DiceLottery,   
          Demographics,
          Comments,
          # pridat cekani na vysledky
          WaitResults,
          TrustResult,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))