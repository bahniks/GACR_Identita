import os
import itertools


studies = {"Login": ("id", "code","bag", "pairs", "roles"),
           "Groups": ("id", "close", "distant"),           
           "Liking": ("id", "trial", "left", "right", "choice"),
           "Articles": ("id", "for_whom", "trial", "articleA", "articleB", "choice"), 
           "Groups Results": ("id", *[f"paired{i}" for i in range(1, 7)], *itertools.chain.from_iterable([[*[f"close{i}_paired{j}" for i in range(1, 5)], * [f"distant{i}_paired{j}" for i in range(1, 5)]] for j in range(1, 7)])), 
           "Trust Control Questions": ("id", "item", "answer"), 
           "Trust": ("id", "block", "other", "groups", "return0", "return1", "return2", "return3", "return4", "return5", "sent", "prediction"),
           "Favoritism": ("id", "trial", "groups1", "value1", "decision1", "groups2", "value2", "decision2", "groups3", "value3", "decision3", "real"),
           "Sameness": ("id", "trial", "value", "close", "distant", "prediction"),
           "Products": ("id", "trial", "left", "right", "choice", "time"),
           "Reading": ("id", "chooser", "trial", "article", "title", "time", "scrolled", "scrolled_to_end"),
           "Articles Results": ("id", "article1", "article2", "Article3"),
           "Charities": ("id", "charity", "contribution", "won", "chosen_charity"),
           "Dice Lottery": ("id", "rolls", "reward"),
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Comments": ("id", "comment"),
           "Results Results": ("id", "pair", "sentA", "sentB", "favoritism", "sameness"),
           "Ending": ("id", "reward")}

frames = [
    "Initial",
    "Login",
    "Intro",
    "InstructionsGroups",
    "Groups",
    "InstructionsLiking",
    "Liking",
    "InstructionsArticlesOthers",
    "ChoiceOthers",
    "InstructionsArticlesMyself",
    "ChoiceMyself",
    "WaitGroups",
    "IntroTrust",
    "InstructionsTrust",
    "Trust1", "Trust2", "Trust3", "Trust4", "Trust5", "Trust6", "Trust7",
    "InstructionsFavoritism",
    "Favoritism",
    "InstructionsSameness",
    "Sameness",
    "ProductsIntro",
    "Choices",
    "InstructionsReading",
    "ArticlesMyself",
    "WaitArticles",
    "InstructionsReadingOthers",    
    "ArticlesOthers",
    "CharityInstructions",
    "Charity",
    "LotteryInstructions",
    "DiceLottery",
    "Demographics",
    "Comments",
    "WaitResults",
    "Ending",
    "end"]


read = True
compute = False

if read:
    for study in studies:
        with open("{} results.txt".format(study), mode = "w", encoding="utf-8") as f:
            f.write("\t".join(studies[study]))

    with open("Time results.txt", mode = "w", encoding="utf-8") as times:
        times.write("\t".join(["id", "order", "frame", "time"]))

    files = os.listdir()
    for file in files:
        if ".py" in file or "results" in file or "file.txt" in file or ".txt" not in file:
            continue

        with open(file, encoding = "utf-8") as datafile:
            #filecount += 1 #
            count = 1
            for line in datafile:

                study = line.strip()
                if line.startswith("time: "):
                    with open("Time results.txt", mode = "a", encoding="utf-8") as times:
                        times.write("\n" + "\t".join([file, str(count), frames[count-1], line.split()[1]]))
                        count += 1
                        continue
                if study in studies:
                    with open("{} results.txt".format(study), mode = "a", encoding="utf-8") as results:                        
                        for line in datafile:
                            if study == "Groups Results":
                                line.replace("~", "\t").replace("|", "\t") 
                            content = line.strip()
                            if not content or content.startswith("time: "):
                                break
                            else:
                                results.write("\n" + content)

if compute:
    times = {frame: [] for frame in frames}
    with open("Time results.txt", mode = "r") as t:
        t.readline()
        for line in t:
            _, num, frame, time = line.split("\t")    
            if int(num) > 1:            
                times[frame0].append(float(time) - t0)            
            t0 = float(time)
            frame0 = frame

    total = 0
    for frame, ts in times.items():
        if ts:
            if frame != "Ending":
                total += sum(ts)/len(ts)
    print("Total")
    print(round(total / 60, 2))

            
