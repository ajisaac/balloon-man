import curses

from graphics import *
from words import *


def main():
    curses.wrapper(curses_main)


def valid_letter_or_none(ch):
    # todo if you resize the screen this blows up
    if 64 > ch > 123:
        return None
    letter = chr(ch)
    if 'a' <= letter <= 'z':
        return letter.upper()
    if 'A' <= letter <= 'Z':
        return letter
    return None


def prompt_for_letter(y, x, w, letters):
    w.addstr(y, x, "please pick a letter:  ")
    w.refresh()
    while True:
        ch = w.getch()
        alpha = valid_letter_or_none(ch)
        if alpha is None:
            w.addstr(y, x, "not a valid letter, try again:    ")
            w.refresh()
            continue
        elif alpha not in letters:
            w.addstr(y, x, "letter already used, try again:  ")
            w.addstr(alpha)
            w.refresh()
            continue
        else:
            return alpha


def print_letters(y, x, w, letters):
    w.addstr(y, x, "letters remaining")
    let_len = len(letters)
    half_let_len = let_len // 2
    # first row
    for i in range(half_let_len):
        w.addch(y + 2, x + (i * 2), letters[i])

    # second row
    for i in range(half_let_len, let_len):
        w.addch(y + 4, x + ((i - half_let_len) * 2), letters[i])


def print_man(y, x, w, man):
    for m in man.split('\n'):
        w.addstr(y, x, m)
        y += 1


def print_blank_word(y, x, w, blank_word):
    # split word 23 characters
    bw = format_blank_word(blank_word)

    w.addstr(y, x, 'Countries and Territories')
    # w.addstr(y + 2, x, blank_word)
    for i, words in enumerate(bw):
        w.addstr(y + 2 + i, x, words)


def print_win_words(y, x, w):
    w.addstr(y, x, 'Congratulations, you have won!')
    w.addstr(y + 1, x, 'Press \'q\' to exit.')
    w.addstr(y + 2, x, 'Press any key to play again.')


def print_loss_words(y, x, w):
    w.addstr(y, x, 'Sorry, you have lost.')
    w.addstr(y + 1, x, 'Press \'q\' to exit.')
    w.addstr(y + 2, x, 'Press any key to play again.')


def print_losing_image(y, x, w):
    img = get_losing_image()
    for m in img.split('\n'):
        w.addstr(y, x, m)
        y += 1


def print_winning_image(y, x, w):
    img = get_winning_image()
    for m in img.split('\n'):
        w.addstr(y, x, m)
        y += 1


def curses_main(w):
    # top left
    b_y = 0
    b_x = 19

    # main menu
    w.addstr(b_y + 2, b_x, 'Baloon Man Takes Geography Exam')
    w.addstr(b_y + 5, b_x, 'Instructions:')
    w.addstr(b_y + 7, b_x, 'Guess letters of the country or territory name.')
    w.addstr(b_y + 8, b_x,
             'Get too many letters wrong and we will unleash the hornets.')
    w.addstr(b_y + 10, b_x, 'Press any key to continue:')
    w.getch()

    # game loop
    while True:
        won = False
        baloons = 5
        curses.curs_set(False)
        letters = get_fresh_letters()
        word = get_country().upper()
        blank_word = make_word_blank(word)

        # a single round of play
        while baloons > 0 and won is False:
            w.clear()
            print_man(b_y + 1 + (5 - baloons), b_x + 30, w, get_man(baloons))
            print_letters(b_y + 2, b_x + 2, w, letters)
            print_blank_word(b_y + 11, b_x + 6, w, blank_word)
            w.refresh()

            letter = prompt_for_letter(b_y + 18, b_x + 2, w, letters)
            remove_letter(letters, letter)

            if letter.upper() in word:
                blank_word = updated_blank_word(word, blank_word, letter)
                if blank_word == word:
                    won = True
            else:
                baloons -= 1

        # round is finished
        if won:
            w.clear()
            print_winning_image(b_y + 3, b_x + 33, w)
            print_letters(b_y + 2, b_x + 2, w, letters)
            print_blank_word(b_y + 11, b_x + 6, w, blank_word)
            print_win_words(b_y + 18, b_x + 2, w)
            w.refresh()
        if not won:
            w.clear()
            print_losing_image(b_y + 3, b_x + 35, w)
            print_letters(b_y + 2, b_x + 2, w, letters)
            print_blank_word(b_y + 11, b_x + 6, w, word)
            print_loss_words(b_y + 18, b_x + 2, w)
            w.refresh()

        # play again
        ch = w.getkey()
        if ch == 'q' or ch == 'Q':
            exit(0)


if __name__ == '__main__':
    main()
