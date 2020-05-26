import codecs
import re
from collections import Counter


def get_words_from_file(file_path):
    file = codecs.open(file_path, 'r', 'utf8')
    words = file.read().lower()
    file.close()
    return words.split()


def create_base(pattern, old_base):
    result_base = []
    for word in old_base:
        word += ' '
        if re.match(pattern, word):
            result_base.append(word.rstrip())
    return result_base


def the_most_common(word_base, hidden=[]):
    symbols = ''
    for words in word_base:
        symbols += words
    symbol_list = symbols.replace(' ', '')
    for i in hidden:
        symbol_list = symbol_list.replace(i, '')
    cnt = Counter(symbol_list)
    return cnt.most_common()[0][0]


def main(count=0):
    """
    It is a hangman game.
    Choose word from text file words.txt and
    write down it like ------.
    For example, if you choose 'Gucci'
    you should input a '-----'.
    Then, computer will start to guess symbols
    which exist in words.txt. ' - is also a symbol.
    You should answer by 'YES' or 'NO'.
    If computer guess symbol, you should input a
    number(s) of it(s) index(es) by whitespaces.
    """
    secret_word = input('Input your word: ')
    used_symbols = []

    def pattern(hidden_symbols):
        return secret_word.replace('-', '[^' + str(hidden_symbols) + ']') + r'\s'

    p = [secret_word.replace('-', '[^ ]') + r'\s']
    hidden_sb = ''
    base = create_base(p[-1], get_words_from_file('words.txt'))
    while secret_word.count('-') > 0:
        count += 1
        base = create_base(p[-1], base)
        if len(base) == 0:
            return 'Check your word and play again!'
        elif len(base) == 1:
            if count/len(secret_word) < 2:
                print("Yes, it was easy for me.({} tries)".format(count))
            else:
                print('It was a difficult game for me. ({} tries)'.format(count))
            return 'I can tell a whole word! It is {}'.format(base[0])
        else:
            x = the_most_common(base, used_symbols)
            print('My symbol is :', x)
            used_symbols.append(x)
            for symbol in used_symbols:
                if symbol not in hidden_sb:
                    hidden_sb += symbol
            answer = input().lower()
            if answer == 'no':
                p[-1]= pattern(hidden_sb)
            elif answer == 'yes':
                print(f'Tell a position of letter {x}')
                position = input().split()
                s = list(secret_word)
                for i in position:
                    pos = int(i)-1
                    try:
                        s[pos] = x
                    except IndexError:
                        return f'This word has not {pos+1} number!'
                secret_word = ''.join(s)
                if re.match(p[-1], secret_word + ' '):
                    p.append(pattern(hidden_sb))
                    print(secret_word)
                else:
                    return 'This word form is not suitable for previous condition'
            else:
                return 'Answer should be YES or NO!'
    if count/len(secret_word) < 2:
        return "Yes, it was easy for me.({} tries)".format(count)
    else:
        return 'It was a difficult game for me. ({} tries)'.format(count)


if __name__ == '__main__':
    print(main.__doc__)
    print(main())

