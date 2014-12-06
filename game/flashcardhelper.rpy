#depends on wtf_iorpy_magic
init:
    image holder = "#f00"

init 1 python:
    import os
    from os import listdir
    from os.path import isfile, join
    import random
    from itertools import izip
    import re
    
    largeDir = os.path.abspath(get_user_dir() + "/Packs")
    
    def pairwise(iterable):
        list = iter(iterable)
        return izip(list, list)
    
    def setup():
        if not os.path.exists(largeDir):
            os.makedirs(largeDir)
    
    def parseAllPacks(parseList):
        theseLines = []
        for singlePack in parseList:
            grabbedPack = listPack("/" + singlePack)
            theseLines.extend(unifyList(grabbedPack))
        return theseLines
    
    def getCards():
        cardDir = os.path.abspath(largeDir)
        return [ f for f in listdir(cardDir) if (isfile(join(cardDir,f)) and (f.endswith('.rsv')))]
        
    def listPack(fileName):
        cardDir = os.path.abspath(largeDir + fileName)
        rawData = file(cardDir).read().decode("utf-8")
        return rawData.split("\n")
    
    def dpRight(packs):
        for pack in packs:
            if("GAT110" in pack):
                return " All GAT110 Flashcards are © Copyright 2014 DigiPen Institute of Technology."
        return ""
        
    def askPack(packs):
        menu_answers = []
        for pack in packs:
            menu_answers.append((pack, "/" + pack))
        if (menu_answers == []):
            renpy.say(None, "No packs detected. Install packs.")
            renpy.full_restart()
        else:
            renpy.say(None, "Click to continue and pick a pack." + dpRight(packs))
            q = []
            q.extend(menu_answers)
            return menu(q)
            
    def unifyList(pack):
        newPack = []
        for line1, line2 in pairwise(pack):
            newLine = (line1, line2)
            newPack.append(newLine)
        return newPack
        
    def shufflePack(pack):
        random.shuffle(pack)
        
    def getMode(answer):
        if "[any_of]" in answer:
            return "any_of"
        elif "[image]" in answer:
            return "image"
        elif "[combo]" in answer:
            return "combo"
        elif "[at_least]" in answer:
            return "at_least"
        elif "[any_of+formula]" in answer:
            return "any_of+formula"
        else:
            return None
        
    def modeCheck(answer, mode):
        fullAnswers = []
        if(mode == "any_of"):
            fullAnswers = answer.split('/')
            fullAnswers.remove("[any_of]")
            return decomp(fullAnswers)
        if(mode == "any_of+formula"):
            fullAnswers = answer.split("BREAK")
            fullAnswers.remove("[any_of+formula]")
            return decomp(fullAnswers)
        if(mode == "image"):
            newAnswer = answer.replace("[image]/", "")#remove image tag
            imageWithAnswer = newAnswer.split(']')#[image location, answers
            imageLoc = imageWithAnswer[0].replace("[", "")#remove left bracket
            onlyAnswers = imageWithAnswer[1].split('/')#just the answers
            fullAnswers.append(imageLoc)
            fullAnswers.extend(onlyAnswers)
            return fullAnswers
        if(mode == "combo"):
            fullAnswers = answer.split('/')
            fullAnswers.remove("[combo]")
            return decomp(fullAnswers)
        if(mode == "at_least"):
            newAnswer = answer.replace("[at_least]/", "")#remove at_least tag
            numberWithAnswers = newAnswer.split(']')#[number, answers
            number = numberWithAnswers[0].replace("[", "")#remove left bracket
            onlyAnswers = numberWithAnswers[1].split('/')#just the answers
            fullAnswers.append(number)
            fullAnswers.extend(onlyAnswers)
            return fullAnswers
        else:
            return answer
        
    def decomp(list):
        newList = []
        for item in list:
            newList.append((str(item).translate(None, ',. ')).lower())
        return newList
    
    def halfcomp(list):
        newList = []
        for item in list:
            newList.append((str(item)) + " ")
        return newList
    
    def removeMode(answer, mode):
        fullAnswers = []
        if(mode == "any_of"):
            fullAnswers = answer.split('/')
            fullAnswers.remove("[any_of]")
            return halfcomp(fullAnswers)
        if(mode == "any_of+formula"):
            fullAnswers = answer.split("BREAK")
            fullAnswers.remove("[any_of+formula]")
            return halfcomp(fullAnswers)
        if(mode == "image"):
            newAnswer = answer.replace("[image]/", "")#remove image tag
            imageWithAnswer = newAnswer.split(']')#[image location, answers
            imageLoc = imageWithAnswer[0].replace("[", "")#remove left bracket
            onlyAnswers = imageWithAnswer[1].split('/')#just the answers
            fullAnswers.extend(onlyAnswers)
            return halfcomp(fullAnswers)
        if(mode == "combo"):
            fullAnswers = answer.split('/')
            fullAnswers.remove("[combo]")
            return halfcomp(fullAnswers)
        if(mode == "at_least"):
            newAnswer = answer.replace("[at_least]/", "")#remove at_least tag
            numberWithAnswers = newAnswer.split(']')#[number, answers
            number = numberWithAnswers[0].replace("[", "")#remove left bracket
            onlyAnswers = numberWithAnswers[1].split('/')#just the answers
            fullAnswers.extend(onlyAnswers)
            return halfcomp(fullAnswers)
        else:
            return answer
        
    def answerCheck(answer, listRight, mode):
        poolSimp = []
        answerSimp = (str(answer).translate(None, ',. ')).lower()
        if(mode == "any_of" or mode == "image" or mode == "any_of+formula"):
            poolSimp = decomp(listRight)
            if answerSimp in poolSimp:
                return True
            else:
                return False
        elif(mode == "combo"):
            poolSimp = decomp(listRight)
            for neededAnswer in poolSimp:
                if(not(neededAnswer in answerSimp)):
                    return False
            return True
        elif(mode == "at_least"):#the number is 0
            numberHave = 0
            numberNeeded = int(listRight.pop(0))
            poolSimp = decomp(listRight)
            for neededAnswer in poolSimp:
                if((neededAnswer in answerSimp)):
                    numberHave += 1
            return (numberHave >= numberNeeded)
        else:
            listRight = (str(listRight).translate(None, ',. ')).lower()
            if(answerSimp == listRight):
                return True
            else:
                return False
            
        
    def quizMe(packLines):
        leftoverPack = []
        for line in packLines:
            #packLines.remove(line)
            answerMode = getMode(line[1])
            rightAnswer = modeCheck(line[1], answerMode)
            if(answerMode == "image"):
                renpy.show("modal", at_list=[truecenter], what=Image((os.path.abspath(largeDir+rightAnswer[0])).replace('\\', '/')), tag="modal")
                rightAnswer.pop(0)#take out the image
            userAnswer = renpy.input(line[0])
            if(answerCheck(userAnswer, rightAnswer, answerMode)):
                renpy.say(None, "That was right! \"" + userAnswer + "\" was close enough.")
                renpy.hide("modal")
            else:
                if(answerMode == "any_of" or answerMode == "image" or answerMode == "combo" or answerMode == "at_least"):
                    unformatAnswer = ', '.join(removeMode(line[1], answerMode))
                else:
                    unformatAnswer = rightAnswer
                renpy.say(None, "That was wrong... the right answer was along the lines of " + "\"" + unformatAnswer + "\".")
                renpy.hide("modal")
                leftoverPack.append(line)
        return leftoverPack
        
    def arrayMerge(arr1, arr2):
        for line in arr2:
            if((line is not None) and (arr1 is not None) and (line not in arr1)):
                arr1.append(line[0])
        return arr1
        
    def arraySplit(arr):
        split = ""
        for question in arr:
            split = split + question + "\n"
        return split