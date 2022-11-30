input_text = ""
text_pointer = 0
line_counter = 1
tokens = []
errors = []
symbols = []


class error_masseges:
    no_error = 'There is no lexical error.'
    bad_token = 'Invalid input'
    unclosed_comment = 'Unclosed comment'
    unmatched_comment = 'Unmatched comment'
    bad_number = 'Invalid number'


def create_symbol_table():
    global symbols
    symbols.extend(['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif'])


def write_tokens():
    pass


def write_lexical_errors():
    pass


def write_symbol_table():
    global symbols
    counter = 1
    symbol_file = open('symbol_table.txt', 'a')
    for symbol in symbols:
        symbol_file.write(str(counter) + ' ' + symbol + '\n')
        counter += 1
    symbol_file.close()


def read_input(input_file_path):
    with open(input_file_path, 'r') as input_file:
        return ''.join([line for line in input_file.readlines()])


def detect_type(read_char):
    if read_char == ' ' or read_char == '\n' or read_char == '\r' or \
            read_char == '\t' or read_char == '\v' or read_char == '\f':
        return 'WHITESPACE'
    if read_char == ';' or read_char == ':' or read_char == ',' or \
            read_char == '[' or read_char == ']' or read_char == '{' or \
            read_char == '}' or read_char == '(' or read_char == ')' or \
            read_char == '+' or read_char == '-' or read_char == '<' or \
            read_char == '=' or read_char == '*':
        return 'SYMBOL'
    if read_char.isdigit():
        return 'NUMBER'
    if read_char.isalpha():
        return 'ID_or_KEYWORD'
    if read_char == '/':
        return 'may_be_COMMENT'
    return 'INVALID'


def get_next_token():
    global input_text
    global text_pointer
    global line_counter
    global tokens
    read_char = input_text[text_pointer]
    if read_char == '\n':
        line_counter += 1


def scan_tokens(input_file_path):
    global input_text
    global text_pointer
    global line_counter
    global tokens
    input_text = read_input(input_file_path)
    text_pointer = 0
    line_counter = 0
    while text_pointer < len(input_text):
        next_token = get_next_token()
        if next_token[0] == "ERROR":
            pass
        else:
            tokens.append(next_token)
    create_symbol_table()
