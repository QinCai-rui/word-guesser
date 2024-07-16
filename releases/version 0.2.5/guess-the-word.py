'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Version 0.2.5
# by Raymont 'QinCai' Qin. https://qincai.lovestoblog.com
# Visit https://qincai.lovestoblog.com/feedback/ to provide feedback
# Licensed under the GNU General Public License v3.0.
# See https://github.com/QinCai-rui/word-guesser/blob/main/LICENSE for more info

import time
import random

# Word lists
FIVE_LETTER_WORDS = ['Apple', 'Bread', 'Chair', 'Dance', 'Eagle',
                     'Fruit', 'Grape', 'House', 'Ivory', 'Jelly',
                     'Knife', 'Lemon', 'Mango', 'Night', 'Ocean',
                     'Peach', 'Queen', 'River', 'Stone', 'Tiger',
                     'Union', 'Vivid', 'Whale', 'Xenon', 'Yield',
                     'Zebra']
SIX_SEVEN_LETTER_WORDS = ['Animal', 'Banana', 'Castle', 'Dragon', 'Energy',
                          'Flower', 'Garden', 'Heaven', 'Island', 'Jungle',
                          'Kitten', 'Laptop', 'Monkey', 'Nature', 'Orange',
                          'Planet', 'Quiver', 'Rocket', 'Sunset', 'Tunnel',
                          'Umbrella', 'Victory', 'Whisper', 'Xylophone',
                          'Yellow', 'Zephyr']
EIGHT_PLUS_LETTER_WORDS = ['Adventure', 'Butterfly', 'Chocolate', 'Dinosaur', 'Elephant',
                           'Fireworks', 'Grapefruit', 'Happiness', 'Important', 'Jasmine',
                           'Kangaroo', 'Lighthouse', 'Mountain', 'Notebook', 'Orchestra',
                           'Pineapple', 'Question', 'Rainbow', 'Sunshine', 'Universe',
                           'Vacation', 'Wonderful', 'Xenophobia', 'Youthful', 'Zoologist']

# Function to create a clue
def create_clue(secret_word):
    return ['?' for _ in range(len(secret_word))]

# Function to update the clue based on the user's guess
def update_clue(guess, secret_word, clue):
    for index, letter in enumerate(secret_word):
        if guess.lower() == letter.lower():
            clue[index] = letter
    return clue.count('?')

# Function to check the user's guess
def check_letter(input_value, secret_word, clue, lives, guessed_letters):
    if not input_value.isalpha() or len(input_value) != 1:
        raise ValueError("Input must be a single letter.")
    if input_value.lower() in guessed_letters:
        print("You've already guessed that letter. Try a different one.")
        return clue.count('?'), lives
    guessed_letters.add(input_value.lower())
    if input_value.lower() in secret_word.lower():
        unknown_letters = update_clue(input_value, secret_word, clue)
    else:
        print('Nope. You lost one life. Try again.')
        lives -= 1
        unknown_letters = clue.count('?')
    return unknown_letters, lives

# Main game function
def main():
    ans = input('Choose a difficulty level. 1 for easy, 2 for medium, 3 for hard. NOTE: anything else means level hard: ')

    if ans == '1':
        lives = 10
        words = FIVE_LETTER_WORDS
        level = 'Easy'
    elif ans == '2':
        lives = 12
        words = SIX_SEVEN_LETTER_WORDS
        level = 'Medium'
    else:
        lives = 15
        words = EIGHT_PLUS_LETTER_WORDS
        level = 'Hard'
    print(f'The level you chose is: {level}')
    time.sleep(1)
    print(f'Therefore, you have {lives} lives. Have fun!')
    
    secret_word = random.choice(words)
    clue = create_clue(secret_word)
    guessed_word_correctly = False
    guessed_letters = set()

    while lives > 0 and not guessed_word_correctly:
        try:
            print('\n')
            guess = input("Enter a letter: ")
            unknown_letters, lives = check_letter(guess, secret_word, clue, lives, guessed_letters)
            print(' '.join(clue))
            print(f'Lives remaining: {lives}')
            if unknown_letters == 0:
                guessed_word_correctly = True
        except ValueError as e:
            print(e)

    if guessed_word_correctly:
        time.sleep(0.5)
        print('Well done, you won! Thanks for playing!')
    else:
        time.sleep(0.5)
        print(f'You died! Try again next time. The word was: {secret_word}.')
    
    time.sleep(2)
    print('Visit https://qincai.lovestoblog.com/feedback to tell me if you discovered any issues/bugs.')
    time.sleep(5)

if __name__ == "__main__":
    main()

