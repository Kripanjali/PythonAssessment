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
dictionary = ["dictionary.txt"]
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
letters = {"b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"}
vowels = {"a", "e", "i", "o", "u"}
vowel_cost = 250
roundstatus = ""
finalroundtext = ""

 
def readDictionaryFile():
    global dictionary
    dict = open(dictionaryloc,'r') # Read dictionary file in from dictionary file location
    wordlist = dict.read().splitlines() # Store each word in a list.
    for k in range(len(wordlist)):
        wordlist[k] = str(wordlist[k]).strip().lower()

    
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
    wheel = open(wheeltextloc, 'r') # read the Wheel name from input using the Config wheelloc file location 
    wheellist = wheel.readlines()
    for k in range(len(wheellist)):
        wheellist[k] = str(wheellist[k]).strip().lower()
    
def getPlayerInfo():
    players[0]["name"] = input("Hello Player 1! What is your name?: ")
    players[1]["name"] = input("Hello Player 2! What is your name?: ")
    players[2]["name"] = input("Hello Player 3! What is your name?: ") # read in player names from command prompt input **DONE**
    print(players)

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
    players[0]['roundtotal'] = 0
    players[1]['roundtotal'] = 0
    players[2]['roundtotal'] = 0 # Set round total for each player = 0
    initPlayer = random.randint(0,2) # Return the starting player number (random)
    roundWord, blankWord = getWord() # Use getWord function to retrieve the word and the underscore word (blankWord)

    return initPlayer

 
def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global goodGuess
    stillinTurn = True
    randomSpin = random.choice(wheellist) # Get random value for wheellist
    if randomSpin == 'Lose a turn': # Check for loose turn
        print('Uh oh, you lost a turn!')
        stillinTurn = False
    elif randomSpin == 'Bankruptcy': # Check for bankrupcy, and take action.
        print('Oh no! You went bankrupt so your bank resets to 0!')
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
    else:
        randomSpin.isdigit() == True
        
        print('Time for you to guess a letter. ')
        letterGuess = str(input(f'Time for you to guess a letter.')).lower() # Ask user for letter guess
        if letterGuess in vowels:
            print("Please try a consonant letter.")
        elif (len(letterGuess) != 1):
            print("Please enter a single letter.")
        elif (not letterGuess.isalpha()):
            print('Input a letter.')
        else:
            goodGuess, playerNum = guessletter(letterGuess, playerNum)
            
            stillinTurn, count = guessletter(letterGuess) # Use guessletter function to see if guess is in word, and return count
        
        if goodGuess == True: # Change player round total if they guess right.   
            players[playerNum]['roundtotal'] += randomSpin * count
            print(f"The amount of {randomSpin} has been added to your bank.")
            print(blankWord)
            stillinTurn = True
        else:
            stillinTurn = False
            print(f"The letter {letterGuess} you guessed doesn not exist in the word.")
            
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundWord
    global goodGuess
    goodGuess = False # parameters:  take in a letter guess and player number
    a = True
    count = 0             
    while a == True:
        if letter in vowels: # ensure letter is a consonate.
            print("You cannot guess a vowel! Please try another letter.")
            letter = str(input('Enter a letter: '))
        else: 
            if letter in roundWord:
                for k in range(0,len(roundWord)): # Change position of found letter in blankWord to the letter instead of underscore 
                    if roundWord[k] == letter:
                        blankWord[k] = letter
                        goodGuess = True # return goodGuess= true if it was a correct guess
                        count = roundWord.count(letter) # return count of letters in word.
                        print(f"The {letter} is in the word!")
                    else:
                        goodGuess = False
                        print(f"The {letter} is not in the word.")
                    a = False
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
        
    playerNum = int(input('Enter player number: ')) # Take in a player number
    if players[playerNum]['roundtotal'] >= vowelcost: # Ensure player has 250 for buying a vowelcost
        print('You have enough money to buy a vowel.')
        enterVowel = str(input('Please enter the vowel: '))
        if enterVowel in vowels: # Ensure letter is a vowel
            guessletter(enterVowel, playerNum) # Use guessLetter function to see if the letter is in the file
            goodGuess = True # If letter is in the file let goodGuess = True
            players[playerNum]['roundtotal'] -=250
                
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    playerNum = int(input('Enter player number: ')) # Take in player number
    wordGuess = str(input("Enter the word you want to guess: ")) # Ask for input of the word and check if it is the same as wordguess
    if roundWord == wordGuess:
        for letter in roundWord:
            blankWord.append(letter)  # Fill in blankList with all letters, instead of underscores if correct
            print(f'Congratulations! {blankWord} is the correct word!')
        else:
            print('That word is incorrect.') # return False ( to indicate the turn will finish)
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    print(turntext.format(name = players[playerNum]['name'], word = roundUnderscoreWord))
    stillinTurn = True
    while stillinTurn:
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        choice = str(input(f"[players][playerNum]['name'], what do you want to do? (S)pin the Wheel, (B)uy a Vowel or (G)uess the word."))        
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    roundContinued = True
    while roundContinued:
        roundContinued = wofTurn(initPlayer)
        if roundContinued == False:
            break
        if initPlayer == 3: # update for the next player's turn
            initPlayer = 1
        else:
            initPlayer += 1
    print(roundstatus.format(word = roundWord)) # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

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
    
    
