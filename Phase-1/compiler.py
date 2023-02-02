'''
Dorrin Sotoudeh         98170851
Maryam Sadat Razavi     98101639
'''

import Scanner
import Parser
import codegen


def main():
    Scanner.read_input('input.txt')
    Scanner.create_symbol_table()
    Parser.read_parse_table()

    Parser.start_parsing()

    Parser.codegen.write_program_block()


if __name__ == '__main__':
    main()
