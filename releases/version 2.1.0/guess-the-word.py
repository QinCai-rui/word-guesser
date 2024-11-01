"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Version 2.1.0
# by Raymont 'QinCai' Qin. https://qincai.xyz
# Visit https://qincai.xyz/feedback/ to provide feedback
# Lisenced under the GNU General Public License v3.0.
# For more infomation, visit https://github.com/QinCai-rui/word-guesser/blob/main/LICENSE

import curses
import time
import random
import sys

# Constants
HEART_SYMBOL = '\u2764' + ' '

FIVE_LETTER_WORDS = [
    'Apple', 'Bread', 'Chair', 'Dance', 'Eagle', 'Fruit', 'Grape', 'House', 'Ivory', 'Jelly', 
    'Knife', 'Lemon', 'Mango', 'Night', 'Ocean', 'Peach', 'Queen', 'River', 'Stone', 'Tiger', 
    'Union', 'Vivid', 'Whale', 'Xenon', 'Yield', 'Zebra', 'Blaze', 'Crane', 'Dream', 'Flame', 
    'Globe', 'Haven', 'Jolly', 'Kneel', 'Lunar', 'Mirth', 'Noble', 'Orbit', 'Piano', 'Quilt', 
    'Raven', 'Shine', 'Thorn', 'Unity', 'Valor', 'Waltz', 'Xylog', 'Yacht', 'Zealot'
]

SIX_SEVEN_LETTER_WORDS = [
    'Animal', 'Banana', 'Castle', 'Dragon', 'Energy', 'Flower', 'Garden', 'Heaven', 'Island', 
    'Jungle', 'Kitten', 'Laptop', 'Monkey', 'Nature', 'Orange', 'Planet', 'Quiver', 'Rocket', 
    'Sunset', 'Tunnel', 'Umbrella', 'Victory', 'Whisper', 'Xylophone', 'Yellow', 'Zephyr', 
    'Beacon', 'Canyon', 'Desert', 'Empire', 'Forest', 'Galaxy', 'Harbor', 'Insect', 'Jigsaw', 
    'Knight', 'Lantern', 'Mystic', 'Nectar', 'Oracle', 'Pirate', 'Quasar', 'Rescue', 'Savage', 
    'Trophy', 'Utopia', 'Voyage', 'Wander', 'Xenial', 'Yonder', 'Zephyr'
]

EIGHT_PLUS_LETTER_WORDS = [
    'Adventure', 'Butterfly', 'Chocolate', 'Dinosaur', 'Elephant', 'Fireworks', 'Grapefruit', 
    'Happiness', 'Important', 'Jasmine', 'Kangaroo', 'Lighthouse', 'Mountain', 'Notebook', 
    'Orchestra', 'Pineapple', 'Question', 'Rainbow', 'Sunshine', 'Universe', 'Vacation', 
    'Wonderful', 'Xenophobia', 'Youthful', 'Zoologist', 'Beautiful', 'Champion', 'Delicious', 
    'Enchanted', 'Fantastic', 'Glamorous', 'Harmonize', 'Incredible', 'Joyfulness', 'Knowledge', 
    'Legendary', 'Magnificent', 'Nostalgia', 'Optimistic', 'Phenomenal', 'Quintuple', 'Radiation', 
    'Spectacle', 'Triumphant', 'Unstoppable', 'Vibrantly', 'Whimsical', 'Xenophile', 'Yearning', 
    'Zealously'
]

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
    difficulties = {
        '1': ('easy', 10, FIVE_LETTER_WORDS),
        '2': ('medium', 12, FIVE_LETTER_WORDS + SIX_SEVEN_LETTER_WORDS),
        '3': ('hard', 13, SIX_SEVEN_LETTER_WORDS + EIGHT_PLUS_LETTER_WORDS),
        '4': ('extreme', 15, EIGHT_PLUS_LETTER_WORDS)
    }

    print("Choose difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Extreme")

    choice = input("Enter the number of your choice: ").strip()
    difficulty, lives, word_list = difficulties.get(choice, ('medium', 12, FIVE_LETTER_WORDS + SIX_SEVEN_LETTER_WORDS))

    if choice not in difficulties:
        print("Invalid choice. Defaulting to medium difficulty.")

    secret_word = random.choice(word_list)
    print(f'Selected difficulty: {difficulty.capitalize()}. A new window will load in 3 seconds. Please wait...')
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

def main():
    try:
        set_difficulty()
        curses.wrapper(main_loop)
    except curses.error:
        print("Error: This game requires a terminal to run. Please run it in a terminal environment.")
        time.sleep(5)
        sys.exit(1)


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
        stdscr.addstr(3, 0, 'Guess a single letter: ')

        key = stdscr.getch()
        if key != -1:
            if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                continue  # Ignore arrow keys
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
        time.sleep(0.25)
        stdscr.addstr(0, 0, 'Well done, you won! Thanks for playing!')
    else:
        stdscr.addstr(0, 0, f'You died! Try again next time. The word was: {secret_word}.')
    stdscr.addstr(1, 0, 'Visit https://qincai.xyz/feedback/ to tell me if you discovered any issues/bugs.')
    stdscr.refresh()
    time.sleep(10)

if __name__ == "__main__":
    print('Hello. Welcome to Guess the Word by Raymont \'QinCai\' Qin.')
    time.sleep(2.5)
    print('My website is at https://qincai.xyz. Feel free to take a look at it! ')
    time.sleep(2.5)
    print('IMPORTANT: Please make sure to have Python 3 installed and to run this inside a terminal.')
    time.sleep(3)
    print(r'For example, if this code is located at C:\Users\QinCai\Desktop\file.py')
    time.sleep(2.5)
    print('You need to open your terminal and type: ')
    time.sleep(1.5)
    print(r'python3 C:\Users\QinCai\Desktop\file.py')
    time.sleep(3)
    print('One last thing: have fun!\n')
    time.sleep(2.5)
    main()

