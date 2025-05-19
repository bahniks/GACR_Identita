#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from intros import Initial, Intro, Ending
from demo import Demographics
from dicelottery import LotteryInstructions, DiceLottery
from trustgame import WaitResults, Trust, TrustResult, InstructionsTrust, IntroTrust, WaitGroups, WaitArticles
from comments import Comments
from login import Login
from sameness import InstructionsSameness, Sameness
from liking import InstructionsLiking, Liking
from articles import InstructionsArticlesOthers, ChoiceOthers, InstructionsArticlesMyself, ChoiceMyself, InstructionsReading
from articles import ArticlesMyself, InstructionsReadingOthers, ArticlesOthers  
from groups import InstructionsGroups, Groups
from favoritism import Favoritism, InstructionsFavoritism
from products import ProductsIntro, Choices
from charity import CharityInstructions, Charity


frames = [Initial,
          Login,  
          Intro,  
          InstructionsGroups,
          Groups,
          InstructionsLiking,
          Liking,          
          InstructionsArticlesOthers,
          ChoiceOthers,     
          InstructionsArticlesMyself,
          #ChoiceMyself,     # vratit, az budou pripravene clanky
          WaitGroups, # cekani na vyplneni skupin
          IntroTrust,
          InstructionsTrust,
          Trust,
          Trust, # bude se jeste opakovat vicekrat (+ synteticke osoby) - predelat s uvadenim trialu, jako jinde              
          InstructionsFavoritism,
          Favoritism,
          InstructionsSameness, 
          Sameness,              
          ProductsIntro,
          Choices,
          InstructionsReading,
          #ArticlesMyself,     # vratit, az budou pripravene clanky
          InstructionsReadingOthers,
          WaitArticles,          
          ArticlesOthers,
          CharityInstructions, 
          Charity,
          LotteryInstructions,
          DiceLottery,   
          Demographics,
          Comments,          
          #WaitResults,
          #TrustResult,
          #Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))