"""
Description:
You must create a Guess the Word game that allows the user to play and guess a
secret word. See the assignment description for details.

@author: Ciaran Burr
cjb139
11/4/2023
"""


import random


def handleUserInputDifficulty():
    """
    This function asks the user if they would like to play the game in (h)ard or
    (e)asy mode, then returns the corresponding number of misses allowed for
    the game. Note that the input is assumed to be either h or e, laid out in
    the assignment details. This creates the number of misses.
    """
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    x = input("(h)ard or (e)asy> ")
    if x=="h":
        print("You have 8 misses to guess the word")
        return 8
    elif x=="e":
        print("You have 12 misses to guess the word")
        return 12
    #possible to revisit if need to do while loop, input __


def getWord(words, length):
    """
    Selects the secret word that the user must guess. This is done by randomly
    selecting a word from words that is of a specific length from the text
    file. Through reading the file in the run function, then passing the list of
    words, this chooses a random word of length (length) for the game.
    """
    wordbank = []
    for each in words:
        if len(each) == length:
            wordbank.append(each)
    randomword = wordbank[random.randint(0, len(wordbank))]
    return randomword.lower()
    # use the .lower to ensure no complications since caps in txt


def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    """
    Creates the string that will be displayed to the user, using the information
    in the parameters. Uses \n for new lines. Initializes display for letters to
    guess, misses remaining, and current word progress
    """
    guessedletters = ""
    for letters in sorted(lettersGuessed):
        guessedletters += " " + letters
    result = "letters you've guessed:" + guessedletters + ("\n misses remaining"
             " = ") + str(missesLeft) + "\n" + ' '.join(guessedWordAsList)
    return result


def handleUserInputLetterGuess(lettersGuessed, displayString):
    """
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if
    it is a repeated letter. Note that another assumption that a letter is
    inputted.
    """
    print("\n" + displayString)
    x = input("letter> ")
    while x in lettersGuessed:
        print("you already guessed that")
        x = input("letter> ")
    return x


def updateGuessedWordAsList(guessedLetter, secretWord, guessedWordAsList):
    """
    Updates guessedWordAsList according to whether guessedLetter is in
    secretWord and where in secretWord guessedLetter is in. Forced to remove
    the letter for that turn in case it is in the word multiple times,
    before adding it back in later. Index changes with.
    """
    for i in range(secretWord.count(guessedLetter)):
        if guessedLetter in list(secretWord):
            location = secretWord.index(guessedLetter)
            guessedWordAsList[location+i] = guessedLetter
            secretWord = secretWord.replace(guessedLetter, "", 1)
    return guessedWordAsList



def processUserGuess(guessedLetter, secretWord, guessedWordAsList, missesLeft):
    """
    Uses the information in the parameters to update the user's progress in
    the Guess the Word game. Tells if you correctly guessed, return list of
    new word, misses left and guess accuracy.
    """
    if guessedLetter in list(secretWord):
        guess = bool(True)
    else:
        missesLeft -= 1
        guess = bool(False)
    word = updateGuessedWordAsList(guessedLetter, secretWord, guessedWordAsList)
    return [word, missesLeft, guess]


def runGame(filename):
    """
    This function sets up the game, runs each round, and prints a final message
    on whether the user won. True is returned if the user won the game. If
    the user lost the game, False is returned. Many variables initialized to
    keep track of answers from functions(not all necessary but easier to
    read). List comprehension creates a list of all the times an underscore
    is within the word, that way if finish guessing easly it exits early.
    """
    file = open(filename)
    content = file.readlines()
    missesStart = handleUserInputDifficulty()
    guessWord = getWord(content, random.randint(6, 11))
    guessWordList = []
    lettersGuessed = []
    missesLeft = missesStart
    guesses = 0
    for _ in range(0, len(guessWord)-1): #note the minus one bc \n included
        guessWordList.append('_')
    while missesLeft > 0 and ([item for item in guessWordList if
                               item=='_']) != []:
        display = createDisplayString(lettersGuessed, missesLeft, guessWordList)
        letterGuess = handleUserInputLetterGuess(lettersGuessed, display)
        lettersGuessed.append(letterGuess)
        processed = processUserGuess(letterGuess, guessWord, guessWordList,
                                     missesLeft)
        guessWordList = processed[0]
        missesLeft = processed[1]
        if processed[2] == False:
            print("you missed: " + letterGuess + " not in word")
        guesses += 1
    if ([item for item in guessWordList if item=='_']) == []:
        print("you guessed the word: " + guessWord + "you made " + str(
            guesses)+ " guesses with " +str(missesStart-missesLeft) + " misses")
        return True
    else:
        print("you're hung!!"  "\nword is " + guessWord)
        return False


if __name__ == "__main__":
    """
    Running GuessWord.py should start the game, which is done by calling runGame
    , therefore, we have provided you this code below. Forced to repeat code to 
    ensure the game runes at least once. Assumes only y and n will be 
    inputted. Will repeat until user wants to stop.
    """
    wins = 0
    losses = 0
    result = runGame('lowerwords.txt')
    if result == True:
        wins += 1
    else:
        losses += 1
    again = input("Do you want to play again? y or n> ")
    # Likely not necessary, but included twice to ensure the function runs at
    # least once
    while again == 'y':
        result = runGame('lowerwords.txt')
        if result == True:
            wins += 1
        else:
            losses += 1
        again = input("Do you want to play again? y or n> ")
    print("You won " + str(wins) + " game(s) and lost " + str(losses))

