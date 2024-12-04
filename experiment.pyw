#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

#from quest import QuestInstructions
from intros import Initial, Intro, Ending
from demo import Demographics
#from lottery import Lottery, LotteryWin
#from dicelottery import LotteryInstructions, DiceLottery
from trustgame import WaitTrust, Trust, TrustResult, InstructionsTrust
#from questionnaire import PoliticalSkill, TDMS, HEXACOinfo
from comments import Comments
from cheating import Login
from sameness import InstructionsSameness, Sameness
from liking import InstructionsLiking, Liking
from articles import InstructionsArticlesOthers, ChoiceOthers, InstructionsArticlesMyself, ChoiceMyself, InstructionsReading
from articles import ArticlesMyself, InstructionsReadingOthers, ArticlesOthers  
from groups import Groups
from favoritism import Favoritism, InstructionsFavoritism



frames = [Initial,
          Intro,
          Login,    
          InstructionsLiking,
          Liking,
          Groups,
          InstructionsSameness, 
          Sameness,
          InstructionsFavoritism,
          Favoritism,
          InstructionsTrust,
          Trust,
          WaitTrust,
          Trust,
          WaitTrust,
          InstructionsArticlesOthers, 
          ChoiceOthers,      
          InstructionsArticlesMyself,
          ChoiceMyself,
          InstructionsReading,
          ArticlesMyself,
          InstructionsReadingOthers,
          ArticlesOthers,
        #   Instructions3, # selection
        #   Cheating,
        #   Info3,
        #   InstructionsTrust,
        #   Trust, # trust instructions + decision
        #   WaitTrust,
        #   TrustResult,
        #   Instructions4Check, # selection + info about trust
        #   Cheating,
        #   OutcomeWait,          
        #   Trust,
        #   WaitTrust,
        #   TrustResult,
        #   TrustResult,
        #   EndCheating,
        #   Lottery,
        #   LotteryWin,
        #   LotteryInstructions,
        #   DiceLottery,
        #   QuestInstructions,
        #   PoliticalSkill,
        #   TDMS,
        #   HEXACOinfo,
          Demographics,
          Comments#,
          #Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))