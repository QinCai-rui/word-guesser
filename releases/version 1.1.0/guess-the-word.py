"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Version 1.1.1 beta
# by Raymont 'QinCai' Qin. https://qincai.xyz
# Visit https://qincai.xyz/feedback/ to provide feedback

import curses
import time
import random

# Constants
HEART_SYMBOL = '\u2764' + ' '

FIVE_LETTER_WORDS = ['Apple', 'Bread', 'Chair', 'Dance', 'Eagle', 'Fruit', 'Grape', 'House', 'Ivory', 'Jelly', 'Knife', 'Lemon', 'Mango', 'Night', 'Ocean', 'Peach', 'Queen', 'River', 'Stone', 'Tiger', 'Union', 'Vivid', 'Whale', 'Xenon', 'Yield', 'Zebra']
SIX_SEVEN_LETTER_WORDS = ['Animal', 'Banana', 'Castle', 'Dragon', 'Energy', 'Flower', 'Garden', 'Heaven', 'Island', 'Jungle', 'Kitten', 'Laptop', 'Monkey', 'Nature', 'Orange', 'Planet', 'Quiver', 'Rocket', 'Sunset', 'Tunnel', 'Umbrella', 'Victory', 'Whisper', 'Xylophone', 'Yellow', 'Zephyr']
EIGHT_PLUS_LETTER_WORDS = ['Adventure', 'Butterfly', 'Chocolate', 'Dinosaur', 'Elephant', 'Fireworks', 'Grapefruit', 'Happiness', 'Important', 'Jasmine', 'Kangaroo', 'Lighthouse', 'Mountain', 'Notebook', 'Orchestra', 'Pineapple', 'Question', 'Rainbow', 'Sunshine', 'Universe', 'Vacation', 'Wonderful', 'Xenophobia', 'Youthful', 'Zoologist']

# Initialize game variables
lives = 0
clue = []
secret_word = ''
unknown_letters = 0
guessed_word_correctly = False
guess = ''
guessed_letters = set()

def set_difficulty():
    """Set the difficulty level and initialize game variables accordingly."""
    global lives, secret_word, unknown_letters
    difficulty = input("Choose difficulty level (easy, medium, hard): ").strip().lower()
    if difficulty == 'easy':
        lives = 10
        secret_word = random.choice(FIVE_LETTER_WORDS)
        print('A new window will load in 3 seconds. Please wait...')
        time.sleep(3)
    elif difficulty == 'medium':
        lives = 12
        secret_word = random.choice(FIVE_LETTER_WORDS + SIX_SEVEN_LETTER_WORDS)
        print('A new window will load in 3 seconds. Please wait...')
        time.sleep(3)
    elif difficulty == 'hard':
        lives = 15
        secret_word = random.choice(SIX_SEVEN_LETTER_WORDS + EIGHT_PLUS_LETTER_WORDS)
        print('A new window will load in 3 seconds. Please wait...')
        time.sleep(3)
    else:
        print("Invalid choice. Defaulting to medium difficulty.")
        lives = 12
        secret_word = random.choice(FIVE_LETTER_WORDS + SIX_SEVEN_LETTER_WORDS)
        time.sleep(2)
        print('A new window will load in 3 seconds. Please wait...')
        time.sleep(3)
    unknown_letters = len(secret_word)

def create_clue():
    """Initialize the clue with '?' for each letter in the secret word."""
    global clue
    clue = ['?' for _ in range(len(secret_word))]

def update_clue(guess, secret_word, clue):
    """Update the clue with the guessed letter if it is in the secret word."""
    unknown_letters = 0
    for index, letter in enumerate(secret_word):
        if guess.lower() == letter.lower():
            clue[index] = letter
        if clue[index] == '?':
            unknown_letters += 1
    return unknown_letters

def main_loop(stdscr):
    """Main game loop."""
    global lives, guessed_word_correctly, guess, unknown_letters, guessed_letters

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    create_clue()

    while lives > 0:
        stdscr.clear()
        stdscr.addstr(0, 0, ' '.join(clue))
        stdscr.addstr(1, 0, 'Lives left: ' + HEART_SYMBOL * lives)
        stdscr.addstr(2, 0, 'Guessed letters: ' + ', '.join(sorted(guessed_letters)))
        stdscr.addstr(3, 0, 'Guess a single letter (DO NOT PRESS SEVERAL TIMES): ')

        key = stdscr.getch()
        if key != -1:
            guess = chr(key).lower()
            if not guess.isalpha() or len(guess) != 1:
                stdscr.addstr(4, 0, 'Invalid input. Please enter a single letter.')
                stdscr.refresh()
                time.sleep(1)
            elif guess in guessed_letters:
                stdscr.addstr(4, 0, 'You already guessed that letter. Try a different one.')
                stdscr.refresh()
                time.sleep(1)
            else:
                guessed_letters.add(guess)
                if guess in secret_word.lower():
                    unknown_letters = update_clue(guess, secret_word, clue)
                else:
                    stdscr.addstr(4, 0, 'Nope. You lost one life. Try again.')
                    stdscr.refresh()
                    time.sleep(1)
                    lives -= 1

                if unknown_letters == 0: 
                    guessed_word_correctly = True
                    break

        stdscr.refresh()
        time.sleep(0.1)

    stdscr.clear()
    if guessed_word_correctly:
        time.sleep(1)
        stdscr.addstr(0, 0, 'Well done, you won! Thanks for playing!')
    else:
        stdscr.addstr(0, 0, f'You died! Try again next time. The word was: {secret_word}.')
    stdscr.addstr(1, 0, 'Visit https://qincai.xyz/feedback/ to tell me if you discovered any issues/bugs.')
    stdscr.refresh()
    time.sleep(10)

if __name__ == "__main__":
    set_difficulty()
    curses.wrapper(main_loop)

