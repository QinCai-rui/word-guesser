'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Version 1.0.1
# by Raymont 'QinCai' Qin. https://qincai.lovestoblog.com
# Visit https://qincai.lovestoblog.com/feedback/ to provide feedback


import curses
import time
import random

lives = 12
words = ['apple', 'bicycle', 'cloud', 'dragon', 'elephant', 'forest', 'galaxy', 'honey', 'island', 'jungle',
         'kite', 'lemon', 'mountain', 'notebook', 'ocean', 'panda', 'queen', 'rainbow', 'star', 'tiger',
         'umbrella', 'volcano', 'wizard', 'xylophone', 'yacht', 'zebra', 'avocado', 'balloon', 'cactus', 'dolphin',
         'eagle', 'flower', 'guitar', 'hamster', 'igloo', 'jellyfish', 'kangaroo', 'lantern', 'mushroom', 'narwhal',
         'octopus', 'penguin', 'quokka', 'rocket', 'sunflower', 'turtle', 'unicorn', 'violin', 'waterfall', 'yawn',
         'astronaut', 'butterfly', 'chocolate', 'dinosaur', 'envelope', 'fireworks', 'gorilla', 'helicopter', 'iguana',
         'jellybean', 'lighthouse', 'mermaid', 'necklace', 'octagon', 'pineapple', 'quasar', 'rhinoceros', 'spaceship', 'telescope',
         'antelope', 'bison', 'caterpillar', 'dandelion', 'echidna', 'flamingo', 'gazelle', 'hedgehog', 'ibis', 'jackal',
         'koala', 'lemur', 'mongoose', 'newt', 'ostrich', 'platypus', 'quail', 'raccoon', 'salamander', 'tapir',
         'urchin', 'vulture', 'walrus', 'xerus', 'yak', 'zebu']
HEART_SYMBOL = '\u2764' + ' '
clue = []
secret_word = random.choice(words)
unknown_letters = len(secret_word)
guessed_word_correctly = False
guess = ''

def create_clue():
    for _ in range(len(secret_word)):
        clue.append('?')

def update_clue(guess, secret_word, clue, unknown_letters):
    index = 0
    while index < len(secret_word):
        if guess.lower() == secret_word[index].lower():
            clue[index] = secret_word[index]
            unknown_letters -= 1
        index += 1
    return unknown_letters

def main_loop(stdscr):
    global lives, guessed_word_correctly, guess, unknown_letters

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    create_clue()

    while lives > 0:
        stdscr.clear()
        stdscr.addstr(0, 0, ' '.join(clue))
        stdscr.addstr(1, 0, 'Lives left: ' + HEART_SYMBOL * lives)
        stdscr.addstr(2, 0, 'Guess a single letter (DO NOT PRESS SEVERAL TIMES): ')

        key = stdscr.getch()
        if key != -1:
            guess = chr(key)
            if guess.lower() in secret_word.lower():
                unknown_letters = update_clue(guess, secret_word, clue, unknown_letters)
            else:
                stdscr.addstr(3, 0, 'Nope. You lost one life. Try again.')
                stdscr.refresh()
                time.sleep(0.75)
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
    stdscr.addstr(1, 0, 'Visit https://qincai.lovestoblog.com/feedback/ to tell me if you discovered any issues/bugs.')
    stdscr.refresh()
    time.sleep(10)

curses.wrapper(main_loop)

