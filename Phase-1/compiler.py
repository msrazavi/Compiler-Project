'''
Dorrin Sotoudeh         98170851
Maryam Sadat Razavi     98101639
'''

import parser
import scanner


def main():
    scanner.read_input('input.txt')
    scanner.create_symbol_table()
    parser.read_parse_table()

    parser.start_parsing()

    parser.semantic_analyzer.write_errors()
    if parser.semantic_analyzer.has_errors():
        parser.codegen.write_program_block(generates_code=False)
    else:
        parser.codegen.write_program_block()


if __name__ == '__main__':
    main()
