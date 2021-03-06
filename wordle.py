import argparse
import random

### things to fix
# double letters not working
# better variable manipulation?

INCORRECT = 0
HALF_CORRECT = 1
CORRECT = 2
UNAVAILABLE = 3


# colors
green = '\x1b[6;30;42m'
yellow = '\x1b[6;30;43m'
gray = '\x1b[6;30;47m'
end_color = '\x1b[0m'


def set_possible_words(num_letters, text_file):
    results = []

    with open(text_file) as file:
        lines = file.read().splitlines()
        for word in lines:
            if len(word) == num_letters:
                results.append(word.lower())
    return results


def generate_word_dict(word):
    dictionary = {}
    # bc i forgot the one line way to do this
    for letter in word:
        if letter in dictionary:
            dictionary[letter] += 1
        else:
            dictionary[letter] = 1
    return dictionary


def generate_colored_letter(pos, letter):
    line = ""
    if pos == CORRECT:
        line += "{} {} {}".format(green, letter.upper(), end_color)
    elif pos == HALF_CORRECT:
        line += "{} {} {}".format(yellow, letter.upper(), end_color)
    elif pos == INCORRECT:
        line += "{} {} {}".format(gray, letter.upper(), end_color)
    else:
        line += " {} ".format(letter.upper())
    return line


def print_grid():
    num_letters = len(final_results[0])
    line_break = "-" * (num_letters * 4 + 1)
    for result in final_results:
        print(line_break)

        line = ""
        for letter_result in result:
            # empty state
            if letter_result == " ":
                line += "|   "

            else:
                letter = letter_result[0]
                pos = letter_result[1]
                line += "|{}".format(generate_colored_letter(pos, letter))

        line += "|"
        print(line)

    print(line_break)
    return


def print_keyboard():
    dictionary_results = {}

    first_line = 'qwertyuiop'
    second_line = ' asdfghjkl '
    third_line = '  zxcvbnm  '

    def _flatten_and_filter(t):
        flattened_list = [item for sublist in t for item in sublist]
        return filter(lambda c: c != " ", flattened_list)

    flattened_final_results = _flatten_and_filter(final_results)

    for item in flattened_final_results:
        letter = item[0]
        pos = item[1]
        if letter in dictionary_results:
            dictionary_results[letter] = max(dictionary_results[letter], pos)
        else:
            dictionary_results[letter] = pos

    for keyboard_line in [first_line, second_line, third_line]:
        line = ""
        for letter in keyboard_line:
            if letter != " ":
                line += "|"
                if letter in dictionary_results:
                    line += generate_colored_letter(dictionary_results[letter], letter)
                else:
                    line += generate_colored_letter(UNAVAILABLE, letter)
            else:
                line += " "
        line += "|"
        print(line)


def input_result(word, num):
    # [(h, 0), (e, 1), (l, 2), (l, 0), (o, 1)]
    result = []
    winning_words_dict = generate_word_dict(winning_word)

    for i in range(len(word)):
        inputted_letter = word[i]
        winning_letter = winning_word[i]
        # letter is in the right place
        if inputted_letter == winning_letter:
            result.append((inputted_letter, CORRECT))

        elif inputted_letter in winning_words_dict:
            inputted_word_dict = generate_word_dict(word)
            num_letters_in_inputted_word_dict = inputted_word_dict[inputted_letter]

            # hello -> sails; first l should be gray not yellow
            # letter is in the word, but you've inputted more of that letter than are in the word itself
            # TODO
            if num_letters_in_inputted_word_dict > winning_words_dict[inputted_letter]:
                result.append((inputted_letter, INCORRECT))

            # letter is in the word, but not in the right place
            else:
                result.append((inputted_letter, HALF_CORRECT))

        # letter doesn't exist at all
        else:
            result.append((inputted_letter, INCORRECT))

    # TODO change it so that we don't manipulate this every time yeah
    final_results[num - 1] = result
    return result


def evaluate_word(word, num, possible_words):
    if len(word) != num_letters:
        result = raw_input("word isn't {} letters, type in another guess: ".format(num_letters))
        return evaluate_word(result, num, possible_words)
    
    elif word not in possible_words:
        result = raw_input("word doesn't exist, type in another guess: ")
        return evaluate_word(result, num, possible_words)

    else:
        input_result(word, num)
        return word

def validate_num_letters():
    try:
        num_letters = input("Type in the number of letters you'd like to guess from 3-10: ")
        if type(num_letters) != int:
            print("Please type in a number")
            validate_num_letters()

        elif num_letters < 3 or num_letters > 10:
            print("Please type in a number between 3 and 10")
            validate_num_letters()

        else:
            return num_letters

    except NameError:
        print("Please try again, without quotes if you used them")
        validate_num_letters()
    except SyntaxError:
        print("Please try again, without quotes if you used them")
        validate_num_letters()


def play(num_letters, winning_word, possible_words):
    for cycle in range(1, num_letters + 2):
        word = raw_input("type your guess for word {}: ".format(cycle)).lower()
        word = evaluate_word(word, cycle, possible_words)
        print_grid()
        print_keyboard()

        if word == winning_word:
            print("Congratulations! You've won")
            return

    print("Unfortunately, you've lost. The word was {}.".format(winning_word))
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--num', choices=['3', '4', '5', '6', '7', '8', '9', '10'])
    args = parser.parse_args()
    print("Welcome to Wordle. Let's begin.")

    text_file = '1000.txt'
    if args.all:
        text_file = 'words_alpha.txt'

    if args.num:
        num_letters = int(args.num)
    else:
        num_letters = validate_num_letters()

    possible_words = set_possible_words(num_letters, text_file)
    winning_word = random.choice(possible_words)
    final_results = [[" "] * num_letters] * 6

    print_grid()
    print_keyboard()
    play(num_letters, winning_word, possible_words)
