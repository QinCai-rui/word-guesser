"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Version 2.3.3 beta 
# by Raymont 'QinCai' Qin. https://qincai.xyz
# Visit https://qincai.xyz/feedback/ to provide feedback
# Licensed under the GNU General Public License v3.0.
# For more information, visit https://github.com/QinCai-rui/word-guesser/blob/main/LICENSE

import curses
import time
import random
import sys
import json

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


def create_clue(secret_word):
    """Initialize the clue with '?' for each letter in the secret word."""
    return ['?' for _ in range(len(secret_word))]

def update_clue(guess, secret_word, clue):
    """Update the clue with the guessed letter if it is in the secret word."""
    unknown_letters = 0
    for index, letter in enumerate(secret_word):
        if guess.lower() == letter.lower():
            clue[index] = letter
        if clue[index] == '?':
            unknown_letters += 1
    return unknown_letters

def is_valid_guess(guess):
    """Check if the guess is a single alphabetic character."""
    return guess.isalpha() and len(guess) == 1

def display_message(stdscr, message):
    """Display a message and wait for the user to press Enter."""
    stdscr.addstr(4, 0, message)
    stdscr.addstr(5, 0, "Press Enter to continue...")
    stdscr.refresh()
    stdscr.nodelay(0)  # Wait for user input
    while True:
        key = stdscr.getch()
        if key == ord('\n'):  # Check for Enter key
            break
    stdscr.nodelay(1)  # Restore the original non-blocking behavior

def set_difficulty():
    """Set the difficulty level and initialize game variables."""
    difficulties = {
        '1': ('easy', 10, FIVE_LETTER_WORDS, 1),
        '2': ('medium', 12, FIVE_LETTER_WORDS + SIX_SEVEN_LETTER_WORDS, 1),
        '3': ('hard', 13, SIX_SEVEN_LETTER_WORDS + EIGHT_PLUS_LETTER_WORDS, 2),
        '4': ('extreme', 15, EIGHT_PLUS_LETTER_WORDS, 3)
    }

    while True:
        print("Choose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Extreme")

        choice = input("Enter the number of your choice: ").strip()
        if choice in difficulties:
            difficulty, lives, word_list, hints = difficulties[choice]
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

    secret_word = random.choice(word_list)
    print(f'Selected difficulty: {difficulty.capitalize()}. A new window will load in 3 seconds. Please wait...')
    time.sleep(3)
    return lives, secret_word, hints

#def provide_hint(secret_word, clue):
#    """Provide a hint by revealing one of the hidden letters."""
#    hidden_indices = [i for i, letter in enumerate(clue) if letter == '?']
#    if hidden_indices:
#        hint_index = random.choice(hidden_indices)
#        clue[hint_index] = secret_word[hint_index]
#    return clue

def provide_hint(secret_word, clue):
    """Provide a hint by revealing one of the hidden letters."""
    hidden_indices = [i for i, letter in enumerate(clue) if letter == '?']
    
    # Check if there is only one unguessed letter left
    if len(hidden_indices) <= 1:
        print("No hint available: Only one unguessed letter remains.")
        return clue
    
    if hidden_indices:
        hint_index = random.choice(hidden_indices)
        clue[hint_index] = secret_word[hint_index]
    
    return clue

def save_game(lives, secret_word, hints, guessed_letters, clue):
    """Save the current game state to a file."""
    game_state = {
        'lives': lives,
        'secret_word': secret_word,
        'hints': hints,
        'guessed_letters': list(guessed_letters),
        'clue': clue
    }
    with open('game_save.json', 'w') as save_file:
        json.dump(game_state, save_file)

def load_game():
    """Load the game state from a file."""
    try:
        with open('game_save.json', 'r') as save_file:
            game_state = json.load(save_file)
            return (game_state['lives'], game_state['secret_word'], game_state['hints'], 
                    set(game_state['guessed_letters']), game_state['clue'])
    except FileNotFoundError:
        return None

def main():
    try:
        saved_game = load_game()
        if saved_game:
            lives, secret_word, hints, guessed_letters, clue = saved_game
        else:
            lives, secret_word, hints = set_difficulty()
            guessed_letters = set()
            clue = create_clue(secret_word)
        curses.wrapper(main_loop, lives, secret_word, hints, guessed_letters, clue)
    except curses.error:
        sys.exit('Error: This game requires a terminal to run. Please run it in a terminal environment.')

def main_loop(stdscr, lives, secret_word, hints, guessed_letters, clue):
    """Main game loop."""
    guessed_word_correctly = False
    unknown_letters = len(secret_word)
    hints_used = 0
    input_str = ""

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    while lives > 0:
        if curses.is_term_resized(curses.LINES, curses.COLS):
            curses.resize_term(curses.LINES, curses.COLS)
            stdscr.clear()

        stdscr.clear()
        stdscr.addstr(0, 0, ' '.join(clue))
        stdscr.addstr(1, 0, 'Lives left: ' + HEART_SYMBOL * lives)
        stdscr.addstr(2, 0, 'Guessed letters: ' + ', '.join(sorted(guessed_letters)))
        stdscr.addstr(3, 0, 'Guess a single letter or type "hint" for a hint: ')
        stdscr.addstr(4, 0, input_str)
        stdscr.refresh()

        key = stdscr.getch()
        if key != -1:
            if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                continue  # Ignore arrow keys
            elif key == 10:  # Enter key
                if input_str == 'hint':
                    if hints_used < hints:
                        clue = provide_hint(secret_word, clue)
                        hints_used += 1
                        display_message(stdscr, f'Hint used! You have {hints - hints_used} hints left.')
                    else:
                        display_message(stdscr, 'No hints left!')
                elif not is_valid_guess(input_str):
                    display_message(stdscr, 'Invalid input. Please enter a single letter.')
                elif input_str in guessed_letters:
                    display_message(stdscr, 'You already guessed that letter. Try a different one.')
                else:
                    guessed_letters.add(input_str)
                    if input_str in secret_word.lower():
                        unknown_letters = update_clue(input_str, secret_word, clue)
                    else:
                        display_message(stdscr, 'Nope. You lost one life. Try again.')
                        lives -= 1

                    # Save the game state after each guess
                    save_game(lives, secret_word, hints, guessed_letters, clue)

                    if unknown_letters == 0: 
                        guessed_word_correctly = True
                        break
                input_str = ""
            elif key == 27:  # Escape key
                input_str = ""
            elif key == curses.KEY_BACKSPACE or key == 127:  # Handle Backspace key
                input_str = input_str[:-1]
            elif key == curses.KEY_DC:  # Handle Delete key
                input_str = input_str[:-1]
            else:
                input_str += chr(key).lower()

        time.sleep(0.025)

    stdscr.clear()
    if guessed_word_correctly:
        time.sleep(0.25)
        stdscr.addstr(0, 0, 'Well done, you won! Thanks for playing!')
    else:
        stdscr.addstr(0, 0, f'You died! Try again next time. The word was: {secret_word}.')
    stdscr.addstr(1, 0, 'Visit https://qincai.obl.ong/feedback/ to tell me if you discovered any issues/bugs.')
    stdscr.refresh()
    time.sleep(10)

if __name__ == "__main__":
  try:  
    main()
  except KeyboardInterrupt: 
    print('Opps... Looks like you just pressed Ctrl+C. Doing so would quit the running program, but don\'t worry, your progress is saved!')
  except Exception: 
    print('Hmm... Looks like something weird happened... Try again.')
