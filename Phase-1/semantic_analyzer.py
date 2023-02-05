class SemanticAnalyzer:
    def __init__(self):
        self.errors = []

    def add_error(self, error, line_num):
        self.errors.append('#' + str(line_num) + ' : Semantic Error! ' + error)

    @staticmethod
    def generate_error_a(id_name):  # lineno: Semantic Error! 'ID' is not defined.
        return id_name + ' is not defined.'

    @staticmethod
    def generate_error_b(id_name):  # lineno: Semantic Error! Illegal type of void for 'ID'.
        return 'Illegal type of void for ' + id_name

    @staticmethod
    def generate_error_c(id_name):  # lineno: Semantic error! Mismatch in numbers of arguments of 'ID'.
        return 'Mismatch in numbers of arguments of ' + id_name

    @staticmethod
    def generate_error_d(id_name):  # lineno: Semantic Error! No 'while' or 'switch case' found for 'break'.
        return 'No \'while\' or \'switch case\' found for \'break\'.'

    @staticmethod
    def generate_error_e(given_type, expected_type):  # lineno: Semantic Error! Type mismatch in operands, Got 'Y' instead of 'X'.
        return 'Type mismatch in operands, Got \'' + given_type + '\' instead of \'' + expected_type + '\'.'

    @staticmethod
    def generate_error_f(id_name, arg_num, given_type, expected_type):  # lineno: Semantic Error! Mismatch in type of argument N for 'ID'. Expected 'X' but got 'Y' instead.
        return 'Mismatch in type of argument ' + arg_num + ' for \'' + id_name + '\'. Expected \'' + expected_type + '\' but got \'' + given_type + '\' instead.'

    def has_errors(self):
        return len(self.errors) > 0

    def write_errors(self):
        with open('semantic_errors.txt', 'w') as file:
            if self.has_errors():
                errors_str = ''
                for err in self.errors:
                    errors_str += err + '\n'
                file.write(errors_str)
            else:
                file.write('The input program is semantically correct.\n')

