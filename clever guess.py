"""
Created on 12/28/23
@author: ciaranburr
"""
"""
Description:
You must create a Clever Guess the Word game that allows the user to play and
guess a secret word. See the assignment description for details.

@author: Ciaran Burr
cjb139
11/28/2023
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


def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    """
    Creates the string that will be displayed to the user, using the information
    in the parameters. Uses \n for new lines. Initializes display for letters to
    guess, misses remaining, and current word progress
    """
    guessedletters = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letters in sorted(lettersGuessed):
        letters = letters.lower()
        alphabet = alphabet.replace(letters, " ")
    result = "letters not yet guessed: " + alphabet + ("\n misses "
        "remaining = ") + str(missesLeft) + "\n" + ' '.join(guessedWordAsList)
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


def handleUserInputDebugMode():
    """
    Determines whether the player is going to play on debug or play mode.
    Debug provides more information to ensure the game is working properly
    """
    mode = input("Which mode do you want: (d)ebug or (p)lay:")
    if mode=='d':
        return True
    if mode=='p':
        return False


def handleUserInputWordLength():
    """
    returns an integer after prompting the user how long the word they want
    to guess should be
    """
    num = input("How many letters are in the word you will guess? Enter an "
                "integer from 5 to 10: ")
    return int(num)


def createTemplate(currTemplate, letterGuess, word):
    """
    This takes the current template being used, the letterGuess from the
    user, amd the current word that the game has selected. It then updates
    the template based on that word, with the word representing the first word
    from the template with the most possibilities.
    """
    z = 0
    currTemplate = [x for x in currTemplate]
    for let in word:
        if let == letterGuess:
            currTemplate[z] = letterGuess
        z += 1
    return "".join(currTemplate)


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    """
    This function creates a new possible word list using dictionaries by
    running every word in the wordlist through the createTemplate. Then it
    selects the template with the most possible words to make it much more
    difficult for the user, with a for loop then iterating through the
    dictionary to determine which template has the maximum possibilities.
    Additional debug information as in example
    """
    dict = {}
    for word in wordList:
        if createTemplate(currTemplate,letterGuess, word) not in dict:
            dict[createTemplate(currTemplate, letterGuess, word)] = [word]
        else:
            dict[createTemplate(currTemplate,letterGuess, word)] += [word]
    max = []
    template = ""
    for each in dict:
        if len(dict[each]) > len(max):
            max = dict[each]
            template = each
        elif len(dict[each]) == len(max):
            x = template.count("_")
            y = each.count("_")
            if y > x:
                max = dict[each]
                template = each
    if debug:
        i = 0
        for each in sorted(dict):
            print(each + " : " + str(len(dict[each])))
            i += 1
        print("# keys = " + str(i))
    return template, max


def processUserGuessClever(guessedLetter, guessedWordAsList, missesLeft):
    """
    Function returns whether the guess was in the word, as well as
    increases the counter variable of misses left
    """
    if guessedLetter not in guessedWordAsList:
        missesLeft -= 1
        result = False
    else:
        result = True
    return [missesLeft, result]


def runGame(filename):
    """
    This function sets up the game, runs each round, and prints a final message
    on whether the user won. True is returned if the user won the game. If
    the user lost the game, False is returned. Many variables initialized to
    keep track of answers from functions(not all necessary but easier to
    read). List comprehension creates a list of all the times an underscore
    is within the word, that way if finish guessing easily it exits early.
    I added new stuff for clever guess word. Strip each line, constantly have to
    keep a current template, a list of possible words, and a new debug
    variable. Prompts player, debug allows more to be seen. Constantly
    changing guess word/possible answer, changes list and the guesswordlist
    and word according to changes. Ends when user runs out of misses or the
    guesswordlist is full, meaning no more not known words
    """
    content = []
    file = open(filename)
    for each in file:
        each = each.strip()
        content.append(each)
    debug = handleUserInputDebugMode()
    guessWord = handleUserInputWordLength()
    missesStart = handleUserInputDifficulty()
    guessWordList = []
    lettersGuessed = []
    missesLeft = missesStart
    guesses = 0
    currenttemp = ""
    wordList = []
    for _ in range(0, guessWord): #note the minus one bc \n included
        guessWordList.append('_')
    currenttemp = "".join(guessWordList)
    for each in content:
        if len(each) == guessWord:
            wordList.append(each)
    guessWord = wordList[0]
    while missesLeft > 0 and ([item for item in guessWordList if
                               item=='_']) != []:
        guessWord = wordList[0]
        display = createDisplayString(lettersGuessed, missesLeft, guessWordList)
        letterGuess = handleUserInputLetterGuess(lettersGuessed, display)
        lettersGuessed.append(letterGuess)
        if debug:
            print("(word is " + guessWord + ")")
            print('# possible words:', len(wordList))
        NewWordList = getNewWordList(currenttemp, letterGuess, wordList,
                                  debug)
        currenttemp = NewWordList[0]
        guessWordList = [x for x in currenttemp]
        wordList = NewWordList[1]
        processed = processUserGuessClever(letterGuess, guessWordList,
                                           missesLeft)
        missesLeft = processed[0]
        if processed[1] == False:
            print("you missed: " + letterGuess + " not in word")
        guesses += 1
    if ([item for item in guessWordList if item=='_']) == []:
        print("you guessed the word: " + guessWord + " you made " + str(
            guesses)+ " guesses with " +str(missesStart-missesLeft) + " misses")
        return True
    else:
        print("you're hung!!"  "\nword is " + guessWord + "\nyou made " +
        str(guesses)+ " guesses with " +str(missesStart-missesLeft) + " misses")
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


