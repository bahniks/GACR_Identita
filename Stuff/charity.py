from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep


from common import InstructionsFrame
from gui import GUI
from constants import TESTING, URL, CHARITY




################################################################################
# TEXTS

charityInstructions = f"""Jako dodatečnou odměnu dáme jednomu z deseti náhodně vybraných účastníků {CHARITY} Kč. Losování proběhne na konci studie.

Částku {CHARITY} Kč si budete moct nechat, anebo jí celou anebo její část věnovat nějaké neziskové organizaci. 

Nyní Vám úkažeme 10 neziskových organizací s krátkým popiskem, čím se zabývají. Vy můžete určit, kolik peněz byste kqaždé z těchto organizací chtěli dát a kolik si nechat pro sebe v případě, že budete vylosováni. 

Pokud budete vylosováni, tak náhodně vybereme jednu z těchto organizací a rozdělíme peníze mezi Vás a danou organizaci podle rozhodnutí, které učiníte nyní. Jinými slovy, rozhodnutí pro jednotlivé organizace jsou nezávislá. Bude vybrána pouze jedna z těchto organizací a jen podle Vašeho rozhodnutí u dané organizace se budou peníze rozdělovat mezi ní a Vás."""


#Pokud dostanete 500 Kč, jak tuto částku rozdělíte mezi sebe a tuto organizaci zabývající se ochranou životního prostředí: Greenpeace

################################################################################

class Charity(InstructionsFrame):
    def __init__(self, root):

        if not "trustblock" in root.status:
            root.status["trustblock"] = 1
        else:
            root.status["trustblock"] += 1

        endowment = CHARITY
     
        close, distant = createSyntetic(5) # TODO

        text = instructionsT2.format(endowment, int(endowment/5), endowment)

        height = 13
        width = 102

        super().__init__(root, text = text, height = height, font = 15, width = width)

        self.groupFrame = GroupsFrame(self, close, distant)

        self.labA = ttk.Label(self, text = "Pokud budu hráč A", font = "helvetica 15 bold", background = "white")
        self.labA.grid(column = 0, row = 2, columnspan = 3, pady = 10)        

        # ta x-pozice tady je hnusny hack, idealne by se daly texty odmen vsechny sem ze slideru
        self.labR = ttk.Label(self, text = "Rozdělení odměn po tomto kroku", font = "helvetica 15 bold", background = "white", anchor = "center", width = 30)
        self.labR.grid(column = 1, row = 2, pady = 5, sticky = E)

        self.labX = ttk.Label(self, text = "Finální rozdělení odměn", font = "helvetica 15 bold", background = "white", anchor = "center", width = 28)
        self.labX.grid(column = 1, row = 6, pady = 5, sticky = E)

        self.frames = {}
        for i in range(8):            
            if i < 6:
                text = "Pokud hráč A pošle {} Kč, pošlu hráči A zpět:".format(int(i*endowment/5))
                ttk.Label(self, text = text, font = "helvetica 15", background = "white").grid(column = 0, row = 7 + i, pady = 1, sticky = E)
                player = "B"
            elif i == 6:
                ttk.Label(self, text = "Pošlu hráči B:", font = "helvetica 15", background = "white").grid(column = 0, row = 3, pady = 1, sticky = E)            
                player = "A"
            else:
                ttk.Label(self, text = "Očekávám, že hráč B pošle zpět:", font = "helvetica 15", background = "white").grid(column = 0, row = 4, pady = 1, sticky = E)  
                player = None
            maximum = int(i * 3 * endowment / 5 + endowment) if i < 6 else endowment            
            self.frames[i] = ScaleFrame(self, maximum = maximum, player = player, returned = int(i*endowment/5), endowment = endowment)
            row = 7 + i if i < 6 else i - 3
            self.frames[i].grid(column = 1, row = row, pady = 1)
            if i == 7:
                self.frames[i].value["state"] = "disabled"
        
        self.labB = ttk.Label(self, text = "Pokud budu hráč B", font = "helvetica 15 bold", background = "white")
        self.labB.grid(column = 0, row = 6, columnspan = 3, pady = 10)

        self.checkVar = BooleanVar()
        ttk.Style().configure("TCheckbutton", background = "white", font = "helvetica 15")
        self.checkBut = ttk.Checkbutton(self, text = checkButtonText, command = self.checkbuttoned, variable = self.checkVar, onvalue = True, offvalue = False)
        self.checkBut.grid(row = 19, column = 0, columnspan = 3, pady = 10)

        self.next.grid(column = 0, row = 20, columnspan = 3, pady = 5, sticky = N)            
        self.next["state"] = "disabled"
        
        self.groupFrame.grid(row = 0, column = 0, columnspan = 3, pady = 5, sticky = S)
        self.text.grid(row = 1, column = 0, columnspan = 3)

        self.deciding = True

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(18, weight = 2)
        self.rowconfigure(20, weight = 2)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 2)

    def checkbuttoned(self):
        self.next["state"] = "normal" if self.checkVar.get() else "disabled"
      
    def nextFun(self):
        if self.deciding:
            for i, frame in self.frames.items():
                if i != 7:
                    frame.value["state"] = "normal" if not self.checkVar.get() else "disabled"
                else:
                    frame.value["state"] = "normal" if self.checkVar.get() else "disabled"
                    frame.maximum = TRUST + int(self.frames[6].valueVar.get()) * 3
                    frame.value["to"] = frame.maximum
            self.deciding = False
            self.checkBut["text"] = checkButtonText2
            self.next["state"] = "disabled"
            self.checkVar.set(False)
        else:
            self.send()
            self.write()
            super().nextFun()

    def send(self):        
        self.responses = [self.frames[i].valueVar.get().strip() for i in range(8)]
        data = {'id': self.id, 'round': "trust" + str(self.root.status["trustblock"]), 'offer': "_".join(self.responses)}
        self.sendData(data)

    def write(self):
        block = self.root.status["trustblock"]
        self.file.write("Trust\n")        
        d = [self.id, str(block + 2), self.root.status["trust_pairs"][block-1], list(self.root.status["trust_roles"])[block-1]]
        self.file.write("\t".join(map(str, d + self.responses)))
        if URL == "TEST":
            if self.root.status["trust_roles"][block-1] == "A":                        
                self.root.status["trustTestSentA"] = int(self.frames[6].valueVar.get())
            else:
                self.root.status["trustTestSentB"] = [int(self.frames[i].valueVar.get()) for i in range(6)]       
        self.file.write("\n\n")


CharityInstructions = (InstructionsFrame, {"text": charityInstructions, "height": 8, "width": 80, "font": 15})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([CharityInstructions,
         Charity
         ])