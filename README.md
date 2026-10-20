# Word-Scramble-Hangman-Arena
 A text-based word guessing challenge leveraging String manipulation, Dictionaries, and File parsing.
Game Mechanics:The program randomly chooses a category (e.g., Cities, Sports, Tech) and presents a scrambled word or hidden underscores.
The player has a limited number of incorrect guesses before losing.
Concepts Used: Dictionaries & Sets (P3): Storing categories and word banks in a nested dictionary; tracking guessed letters in a set and using set difference (first_string - second_string logic) to reveal remaining alphabet choices.
String Slicing & Rotation (P2): Using custom list rotations or slicing to scramble word characters.   
File Handling (Lab NB): Reading words line-by-line from a dictionary file (words.txt) using readlines() and stripping newlines.
