from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""

 
def readDictionaryFile():
    global dictionary
    dict = open(dictionaryloc,'r') # Read dictionary file in from dictionary file location
    readdict = dict.read().splitlines() # Store each word in a list.
    dict.close()
    for k in readdict:
        dictionary.append(k)

    
def readTurnTxtFile():
    global turntext
    ttext = open(turntextloc,'r') #read in turn intial turn status "message" from file
    turntext = ttext.read()

        
def readFinalRoundTxtFile():
    global finalroundtext
    finalround = open(finalRoundTextLoc, 'r') #read in turn intial turn status "message" from file
    finalroundtext = finalround.read().splitlines()

def readRoundStatusTxtFile():
    global roundstatus
    roundstat = open(roundstatusloc, 'r') # read the round status  the Config roundstatusloc file location
    roundstatus = roundstat.read()


def readWheelTxtFile():
    global wheellist
    openwheel = open(wheeltextloc, 'r') # read the Wheel name from input using the Config wheelloc file location 
    readwheel = openwheel.read().splitlines()
    for category in readwheel:
        wheellist.append(category)
    
def getPlayerInfo():
    global players
    for i in range(0,len(players)):
        players[i]["name"] = str(input(f"Enter the name of player {i+1}: "))

def gameSetup():
    global turntext
    global dictionary
    
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global roundUnderscoreWord
    global roundWord
    roundWord = random.choice(dictionary).lower() #choose random word from dictionary
    roundUnderscoreWord = ['_'] * len(roundWord) #make a list of the word with underscores instead of letters.
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    for i in range(0,len(players)):
        players[i]["roundtotal"] = 0
    # Return the starting player number (random)
    initPlayer = random.choice([0,1,2])
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundWord, blankWord = getWord()
    return initPlayer

 
def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    print(roundWord)
    
    randomSpin = random.choice(wheellist) # Get random value for wheellist
    print(f"Your Spin: {randomSpin}")
    stillinTurn = True
    if randomSpin == 'Lose a turn': # Check for loose turn
        print('Uh oh, you lost a turn!')
        stillinTurn = False
    elif randomSpin == 'Bankruptcy': # Check for bankrupcy, and take action.
        print('Oh no! You went bankrupt so your bank resets to 0!')
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
    elif randomSpin[0] == "$":
        letterguess = str(input("Guess a letter!: ")).lower()

        if letterguess not in vowels:
            validGuess = guessletter(letterguess)
            if validGuess:
                players[playerNum]["roundtotal"] += int(randomSpin[1:])
                print(blankWord)
            else:
                stillinTurn = False
                print("This letter is not in the word.")
        else:
            stillinTurn = False
            print("Please enter a consonant.")
    else:
        print("Error")
        
    return stillinTurn


def guessletter(letter): 
    global players
    global blankWord
    global roundWord
    global goodGuess
    
    goodGuess = False # parameters:  take in a letter guess and player number
    count = 0             

    for letternum in range(0,len(roundWord)):
            if roundWord[letternum] == letter:
                blankWord[letternum] = letter
                goodGuess = True
                count += 1

    return goodGuess

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    
    # Ensure player has 250 for buying a vowel
    if players[playerNum]["roundtotal"] >= 250:
        while True:
            print("You have enough money to buy a vowel!")
            vowelGuess = input("Please enter a vowel: ")
            # Ensure letter is a vowel
            if vowelGuess in vowels:
                # Use guessLetter function to see if the letter is in the file
                guessletter(vowelGuess, playerNum)
                players[playerNum]['roundtotal'] -=250
            goodGuess = True
            break
    else:
        print("You don't have enough money to buy a vowel!")
        goodGuess = True
        
    
    return goodGuess  
                
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    #print(roundWord)
    guessWord = input("Please enter the word you would like to guess: ")
    if guessWord == roundWord:
    # Fill in blankList with all letters, instead of underscores if correct 
        for i in range (len(roundWord)):
            if roundWord == guessWord:
                roundUnderscoreWord[i] = guessWord
            #print(roundUnderscoreWord)
            print(f"Congratulations! You guessed the word! The word was {roundWord}")
    # return False ( to indicate the turn will finish) 
    else:
        print("That word was not correct!")
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    readRoundStatusTxtFile()# use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    print(turntext.format(name = players[playerNum]['name'], word = roundUnderscoreWord))
    stillinTurn = True
    while stillinTurn:
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        if '_' not in roundUnderscoreWord:
            stillinTurn = False
            break
        choice = input(f"Hello {players[playerNum]['name']}, would you like to (S)pin, (B)uy Vowel, or (G)uess the word?: ")
        
        # use the string.format method to output your status for the round
        readRoundStatusTxtFile()
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")         


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundNum

    roundNum = roundNum +1
    print(f"This is round {roundNum}")

    initPlayer = wofRoundSetup()
    roundInProgress = True
    while roundInProgress:
        print(roundUnderscoreWord)
        if '_' not in roundUnderscoreWord:

            for i in players.keys():
                newGameTotal = players[i]["gametotal"] + players[i]["roundtotal"]
                players[i].update({"gametotal": newGameTotal})

            roundInProgress = False
            break

        # Begin the current players turn
        wofTurn(initPlayer)

        # Update so the next person gets to go
        initPlayer += 1
        if (initPlayer > 2):
            initPlayer = 0
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round
    print(roundstatus.format(word=roundWord))

    
def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    knownLetters = {"R", "S", "T", "L", "N", "E"}
    
    # Find highest gametotal player.  They are playing.
    for k in players.keys():
        if players[k]['gametotal'] > players[winplayer]['gametotal']:
            k = winplayer
    amount = players[winplayer]['gametotal']
    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(name=players[winplayer]['name'], total = amount))
    print(f"""Welcome to the final round, congratulations {players[winplayer]['name']}.
    You will be given the letters R,S,T,L,N,E and you can pick 3 consonants and 1 more vowel.
    If you guess them correctly, your letters will be revealed. If you guess the final answer
    you will win a grand cash prize of {finalprize} dollars. However, if you guess the wrong word,
    you will lose all the money and go home. are you ready?""")

    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    for k in ("R","S","T","L","N","E"):
        guessletter(k)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print("Your word is: [blankWord]")
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    for k in range(3):
        guessedConsonant = []
        while True:
            consonant = str(input(f'Enter your first number {k+1} consonant you want to guess: ')).lower()
            if consonant.isalpha  == False or len(consonant) != 1:
                print('You did not enter a letter, please try again.')
            elif consonant in vowels:
                print('You are not allowed to guess a vowel, please try again.')
            elif consonant in guessedConsonant:
                print('The letter you guessed is already available, please try again.')
            else:
                guessletter(consonant)
                guessedConsonant.append(consonant)
                break
        
        while True:
            vowel = str(input('What is your vowel guess? ')).lower()
            if vowel.isaplha == False or len(vowel) != 1:
                print('You did not enter a letter, please try again.')
            elif vowel not in vowels:
                print('You are only allowed to guess a vowel, please try again.')
            elif vowel in blankWord:
                print('The vowel you guessed is already available, please try again.')
            else:
                guessletter(vowel)
                break


    # Print out the current blankWord again
    print([blankWord])

    # Remember guessletter should fill in the letters with the positions in blankWord
    print(f'The word currently looks like this: {" ".join(blankWord)}')
    
    # Get user to guess word
    finalGuess = input("It's time to guess the word, are you ready? ")

    # If they do, add finalprize and gametotal and print out that the player won 
    if finalGuess == roundWord:
       grandPrize = finalprize + amount
       print(f"Hooray! You have guessed the correct word and your total prize is {grandPrize}")
    else:
        print(f" Uh oh! That is not the correct word, the correct word is {roundWord}. You have lost, better luck next time!") 

def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
