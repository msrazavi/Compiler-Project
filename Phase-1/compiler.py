'''
Dorrin Sotoudeh         98170851
Maryam Sadat Ramezani   98101639
'''

import Scanner
import Parser


def main():
    Scanner.read_input('input.txt')
    Scanner.create_symbol_table()
    Parser.read_parse_table()

    Parser.start_parsing()

    Scanner.write_symbol_table()
    Scanner.write_lexical_errors()
    Scanner.write_tokens()


if __name__ == '__main__':
    main()
