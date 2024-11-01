'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Version 0.1.6
# by Raymont 'QinCai' Qin. https://qincai.xyz

import time
import random
lives = 12
words = ['apple', 'bicycle', 'cloud', 'dragon', 'elephant', 'forest', 'galaxy', 'honey', 'island', 'jungle',
         'kite', 'lemon', 'mountain', 'notebook', 'ocean', 'panda', 'queen', 'rainbow', 'star', 'tiger',
         'umbrella', 'volcano', 'wizard', 'xylophone', 'yacht', 'zebra', 'avocado', 'balloon', 'cactus', 'dolphin',
         'eagle', 'flower', 'guitar', 'hamster', 'igloo', 'jellyfish', 'kangaroo', 'lantern', 'mushroom', 'narwhal',
         'octopus', 'penguin', 'quokka', 'rocket', 'sunflower', 'turtle', 'unicorn', 'violin', 'waterfall', 'yawn']
HEART_SYMBOL = '\u2764' + ' '
clue = []
secret_word = random.choice(words)
unknown_letters = len(secret_word)
guessed_word_correctly = False
guess = ''

def create_clue():
    index = 0
    while index < len(secret_word):
        clue.append('?')
        index += 1
    
def update_clue(guess, secret_word, clue, unknown_letters):
    index = 0
    while index < len(secret_word):
        if guess.lower() == secret_word[index].lower():
            clue[index] = secret_word[index]
            unknown_letters -= 1
        index += 1
    return unknown_letters

create_clue()

while lives > 0:
    print(clue)
    print('Lives left: ' + HEART_SYMBOL * lives)
    guess = input('Guess a letter or the whole word: ')
    
    if guess.lower() == secret_word.lower():
        guessed_word_correctly = True
    elif guess.lower() in secret_word.lower():
        update_clue(guess, secret_word, clue, unknown_letters)
    else:
        print('Nope. You lost one life. Try again.')
        lives -= 1
        
    if unknown_letters == 0 or guessed_word_correctly:
        guessed_word_correctly = True
        break
    print('\n')
    
if guessed_word_correctly:
    time.sleep(0.5)
    print('Well done, you won! Thanks for playing!')
    time.sleep(2)
    print('Visit https://qincai.xyz/feedback to tell me if you discovered any issues/bugs. ')
else:
    time.sleep(0.5)
    print('You died! Try again next time. The word was: ' + secret_word + '. ')
    time.sleep(2)
    print('Visit https://qincai.xyz/feedback/ to tell me if you discovered any issues/bugs. ')
    
time.sleep(5)
quit()
