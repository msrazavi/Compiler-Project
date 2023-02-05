'''
Dorrin Sotoudeh         98170851
Maryam Sadat Razavi     98101639
'''

import Parser
import Scanner


def main():
    Scanner.read_input('input.txt')
    Scanner.create_symbol_table()
    Parser.read_parse_table()

    Parser.start_parsing()

    Parser.semantic_analyzer.write_errors()
    if Parser.semantic_analyzer.has_errors():
        Parser.codegen.write_program_block(generates_code=False)
    else:
        Parser.codegen.write_program_block()


if __name__ == '__main__':
    main()
