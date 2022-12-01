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
    symbols.extend(['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif'])


def write_tokens():
    with open('tokens.txt', 'w') as tokens_file:
        grouped = []
        for token in tokens:
            while len(grouped) < token[0]: grouped.append([])
            grouped[token[0] - 1].append(token[1:])
        for i, tokens_inline in enumerate(grouped):
            if len(tokens_inline) == 0: continue

            line = f"{i+1}.\t"
            line += "".join([f"({token[0]}, {token[1]}) " for token in tokens_inline])
            line += "\n"
            tokens_file.write(line)


def write_lexical_errors():
    with open('lexical_errors.txt', 'w') as error_file:
        if len(errors) == 0:
            error_file.write(error_masseges.no_error)
        else:
            error_file.write(str(errors[0][0]) + ' ')
            for i in range(len(errors)):
                error_file.write('(' + errors[i][1] + ', ' + errors[i][2] + ') ')
                if i + 1 < len(errors) and errors[i + 1][0] > errors[i][0]:
                    error_file.write('\n' + str(errors[i + 1][0]))


def write_symbol_table():
    with open('symbol_table.txt', 'w') as symbol_file:
        counter = 1
        for symbol in symbols:
            symbol_file.write(f"{counter}.\t{symbol}\n")
            counter += 1
        symbol_file.close()


def read_input(input_file_path):
    global input_text
    with open(input_file_path, 'r') as input_file:
        input_text = ''.join([line for line in input_file.readlines()])


def detect_type(read_char):
    if read_char == ' ' or read_char == '\n' or read_char == '\r' or \
            read_char == '\t' or read_char == '\v' or read_char == '\f':
        return 'WHITESPACE'
    if read_char == '/' and text_pointer + 1 < len(input_text) and (input_text[text_pointer + 1] == '*' or input_text[text_pointer + 1] == '/'):
        return 'COMMENT'
    if read_char == ';' or read_char == ':' or read_char == ',' or \
            read_char == '[' or read_char == ']' or read_char == '{' or \
            read_char == '}' or read_char == '(' or read_char == ')' or \
            read_char == '+' or read_char == '-' or read_char == '<' or \
            read_char == '=' or read_char == '*' or read_char == '/':
        return 'SYMBOL'
    if read_char.isdigit():
        return 'NUM'
    if read_char.isalpha():
        return 'ID_or_KEYWORD'


def get_next_token():
    global text_pointer
    global line_counter
    read_char = input_text[text_pointer]
    if read_char == '\n':
        line_counter += 1
    detected_type = detect_type(read_char)
    if detected_type == 'WHITESPACE':
        text_pointer += 1
        return ['WHITESPACE']
    if detected_type == 'SYMBOL':
        if read_char == '=' and text_pointer + 1 < len(input_text) and input_text[text_pointer + 1] == '=':
            text_pointer += 2
            return [line_counter, 'SYMBOL', '==']
        if read_char == '*' and text_pointer + 1 < len(input_text) and input_text[text_pointer + 1] == '=':
            text_pointer += 2
            errors.append([line_counter, '*/', error_masseges.unmatched_comment])
            return ['ERROR']
        text_pointer += 1
        return [line_counter, 'SYMBOL', read_char]
    if detected_type == 'NUM':
        number = read_char
        while text_pointer + 1 < len(input_text):
            text_pointer += 1
            if detect_type(input_text[text_pointer]) == 'NUM':
                number += input_text[text_pointer]
            elif detect_type(input_text[text_pointer]) == 'WHITESPACE' or detect_type(input_text[text_pointer]) == 'SYMBOL':
                return [line_counter, 'NUM', number]
            else:
                errors.append([line_counter, number + input_text[text_pointer], error_masseges.bad_number])
                text_pointer += 1
                return ['ERROR']
        text_pointer += 1
        return [line_counter, 'NUM', number]
    if detected_type == 'ID_or_KEYWORD':
        word = read_char
        while text_pointer + 1 < len(input_text):
            text_pointer += 1
            if detect_type(input_text[text_pointer]) == 'NUM' or detect_type(input_text[text_pointer]) == 'ID_or_KEYWORD':
                word += input_text[text_pointer]
            elif detect_type(input_text[text_pointer]) == 'WHITESPACE' or detect_type(input_text[text_pointer]) == 'SYMBOL':
                if word in symbols[:10]:
                    return [line_counter, 'KEYWORD', word]
                if word not in symbols:
                    symbols.append(word)
                return [line_counter, 'ID', word]
            else:
                errors.append([line_counter, word + input_text[text_pointer], error_masseges.bad_token])
                text_pointer += 1
                return ['ERROR']
        text_pointer += 1
        return [line_counter, 'ID', word]
    if detected_type == 'COMMENT':
        text_pointer+=1
        if input_text[text_pointer] == '*':
            while text_pointer+2<len(input_text):
                text_pointer +=1
                if input_text[text_pointer]=='*' and input_text[text_pointer+1] =='/':
                    return ['COMMENT']
            #has work
        elif input_text[text_pointer] == '/':
            while text_pointer+1<len(input_text):
                text_pointer += 1
                if input_text[text_pointer] == '\n':
                    return ['COMMENT']
        else:
            return [line_counter,'SYMBOL',read_char]
    errors.append([line_counter, read_char, error_masseges.bad_token])
    text_pointer += 1
    return ['ERROR']


def scan_tokens(input_file_path):
    read_input(input_file_path)
    create_symbol_table()
    while text_pointer < len(input_text):
        next_token = get_next_token()
        if next_token[0] != 'ERROR' and next_token[0] != 'WHITESPACE' and next_token[0] != 'COMMENT':
            tokens.append(next_token)
    write_symbol_table()
    write_lexical_errors()
    write_tokens()
