import re
import os
import random
import itertools

os.system('cls')

def printColor(printArray):
    for i in printArray:
        pattern = ""
        for color in i:
            match color:
                case "R":
                    pattern += "🔴 "
                case "Y":
                    pattern += "🟡 "
                case "G":
                    pattern += "🟢 "
                case "C":
                    pattern += "🔵 "
                case "W":
                    pattern += "⚪ "
                case "B":
                    pattern += "⚫ "
        print(pattern)

def calculatePins(userGuess, solution):
    blackCount = 0
    whiteCount = 0
    userGuess = userGuess[:]
    solution = solution[:]
    for j in range(4):
        if userGuess[j] == solution[j]:
            blackCount += 1
            userGuess[j] = "X"
            solution[j] = "X"
    for l in range(4):
        for m in range(4):
            if solution[l] == userGuess[m] and solution[l] != "X":
                whiteCount += 1
                userGuess[m] = "X"
                solution[l] = "X"
    return [blackCount, whiteCount]

def narrowList(possibles, solution, blackCount, whiteCount):
    matches = []
    for possible in possibles:
        bCount, wCount = calculatePins(solution[:], possible[:])
        if bCount == blackCount and wCount == whiteCount:
            matches.append(possible)
    return matches

def bestNextGuess(possibleGuesses, allPatterns):
    bestGuess = None
    minMaxRemaining = float('inf')
    for guess in allPatterns:
        maxRemaining = 0
        for black in range(5):
            for white in range(5 - black):
                remaining = narrowList(possibleGuesses, guess, black, white)
                if len(remaining) > maxRemaining:
                    maxRemaining = len(remaining)
        if maxRemaining < minMaxRemaining:
            minMaxRemaining = maxRemaining
            bestGuess = guess
    return bestGuess

def getPlayerPins():
    b = ""
    w = ""
    while True:
        b = input("Enter the black pins returned: ")
        w = input("Enter the white pins returned: ")
        try:
            w = int(w)
            b = int(b)
        except:
            os.system('cls')
            print("Must enter numbers!")
        else:
            if w + b <= 4 and w + b >= 0:
                break
            else:
                os.system('cls')
                print("Pins must add up between 0 and 4!")
    return [b, w]

def getUserGuess():
    g = ""
    userArray = False
    while True:
        g = input("Enter a guess: ")
        userArray = stringGuessToArray(g, k)
        if userArray:
            break
    return userArray

def getComputerGuess(currentLoop):
    g = ""
    color = []
    if currentLoop == 0:
        # for i in range(4):
        #     g += colors[random.randint(0,5)]
        for i in range(2):
            while True:
                temp = colors[random.randint(0,5)]
                if temp in color:
                    continue
                else:
                    color.append(temp)
                    break
            for i in range(2):
                g += temp
        print(g)
    value = stringGuessToArray(g, k)
    return value

def stringGuessToArray(stringGuess, currentLoop):
    arrayGuess = []
    color = []
    pattern = re.search(regexColors,stringGuess)
    try:
        if stringGuess == "":
            if currentLoop == 0:
                # for i in range(4):
                #     g += colors[random.randint(0,5)]
                for i in range(2):
                    while True:
                        temp = colors[random.randint(0,5)]
                        if temp in color:
                            continue
                        else:
                            color.append(temp)
                            break
                    for i in range(2):
                        arrayGuess.append(temp)
            else:
                arrayGuess = nextGuess
            os.system('cls')
            printColor([arrayGuess])
        elif "?" in stringGuess:
            os.system('cls')
            printColor(possibleGuesses)
            return
        elif pattern.group(1) and pattern.group(2) and pattern.group(3) and pattern.group(4):
            os.system('cls')
            arrayGuess = [pattern.group(1).upper(), pattern.group(2).upper(), pattern.group(3).upper(), pattern.group(4).upper()]
            printColor([arrayGuess])
        else:
            return
    except:
        os.system('cls')
        print("Must match Valid 4-Pin Format. R Y G C")
        print("(Red Yellow Green Cyan White Black)")
        return
    return arrayGuess

regexColors = re.compile("(R|Y|G|C|W|B)(?: *)(R|Y|G|C|W|B)(?: *)(R|Y|G|C|W|B)(?: *)(R|Y|G|C|W|B)(?: *)", re.IGNORECASE)
colors = ["R", "Y", "G", "C", "W", "B"]
allPatterns = list(itertools.product(colors,repeat=4))
allPatterns = [list(guess) for guess in allPatterns]
possibleGuesses = allPatterns[:]
turnSuccess = [[],[],[],[],[],[],[],[]]
turnSolution = [[],[],[],[],[],[],[],[]]
testSolution = []
allGuesses = []
firstGuess = []
nextGuess = []
testing = False
master = True
curLoop = 0
loops = 0
k = 0

g = input("Would you like to test? ")
os.system('cls')
if "y" in g or "Y" in g and not "n" in g and not "N" in g:
    testing = True
    while True:
        loops = input("How many iterations? ")
        try:
            loops = int(loops)
            break
        except ValueError:
            os.system('cls')
            print("Must be an integer!")
    for i in range(4):
        testSolution.append(colors[random.randint(0,5)])
    
############################### MASTER ###############################

while master:
    curGuess = []
    b = 0
    w = 0
    if testing:
        curGuess = stringGuessToArray("", k)
        print(curGuess, "!!!!")
        b, w = calculatePins(curGuess, testSolution)
        if k == 0:
            firstGuess = curGuess[:]
    else:
        curGuess = getUserGuess()
        b, w = getPlayerPins()
    os.system('cls')
    allGuesses.append(
        {
            "guess": curGuess,
            "result": {"Black": b,
                       "White": w,
            }
        }
    )
    temp = narrowList(possibleGuesses, allGuesses[k]["guess"], allGuesses[k]["result"]["Black"], allGuesses[k]["result"]["White"])

    if len(temp) == 0:
        del allGuesses[k]
        print("Invalid feedback")
        continue
    else:
        possibleGuesses = temp
    if testing:
        print(curLoop + 1, "/", loops, "Guess", k + 1)
        print("Current Guess:", end = " ")
        printColor([curGuess])
        print("Solution:     ", end = " ")
        printColor([testSolution])
        print("")
        for i in range(len(turnSuccess)):
            print("Guess:", i+1, "--", len(turnSuccess[i]))
            # BROKEN
            # for j in range(len(turnSuccess[i])):
                # printColor([turnSuccess[i][j]]), ">>", printColor([turnSolution[i][j]]))
        print("")
    print("Possibilities:", len(possibleGuesses))

    if b == 4:
        if testing:
            turnSuccess[k] += [firstGuess]
            turnSolution[k] += [testSolution[:]]
            curLoop += 1
            k = -1
            possibleGuesses = allPatterns[:]
            allGuesses.clear()
            testSolution.clear()
            for i in range(4):
                testSolution.append(colors[random.randint(0,5)])
        if not testing or curLoop >= loops:
            if testing:
                os.system('cls')
                print("")
                print("")
                for i in range(len(turnSuccess)):
                    print("Guess:", i+1, "--", len(turnSuccess[i]))
                    # BROKEN
                    # for j in range(len(turnSuccess[i])):
                        # printColor([turnSuccess[i][j]]), ">>", printColor([turnSolution[i][j]]))
                print("")
            else:
                print("Guessed in", k + 1, "attempts")
                printColor(possibleGuesses)
            master = False
    else:
        if len(possibleGuesses) > 6:
            nextGuess = bestNextGuess(possibleGuesses, allPatterns)       
        else:
            nextGuess = bestNextGuess(possibleGuesses, possibleGuesses)
            printColor(possibleGuesses)
        for pattern in possibleGuesses:
            if nextGuess == pattern:
                print("Guess is possible!")
        print("Press enter to accept next best guess:")
        printColor([nextGuess])

    k += 1