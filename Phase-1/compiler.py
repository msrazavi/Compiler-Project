'''
Dorrin Sotoudeh         98170851
Maryam Sadat Razavi     98101639
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
    Parser.create_parse_tree_file()


if __name__ == '__main__':
    main()
