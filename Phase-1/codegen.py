from symbol_table import SymbolTable

from stack import Stack


class CodeGenerator:
    program_block = []
    program_counter = 0
    semantic_stack = Stack()
    scope_stack = Stack()
    scope_counter = 0
    symbol_table = SymbolTable()
    temp_addr = 500

    arith_operators = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '/': 'DIV', '<': 'LT', '==': 'EQ'}

    def call_action_routine(self, action_symbol: str, lookahead: str):
        self.__getattribute__(action_symbol)(lookahead)

    def get_temp_addr(self, size=1):
        prev_addr = self.temp_addr
        self.temp_addr += 4 * size
        return prev_addr

    def save(self, lookahead: str = None):
        self.label()
        self.program_counter += 1

    def label(self, lookahead: str = None):
        self.semantic_stack.push(self.program_counter)

    def save_const(self, lookahead: str = None):
        self.semantic_stack.push(f'#{lookahead}')

    def push_op(self, lookahead: str = None):
        self.semantic_stack.push(lookahead)

    def arith(self, operator: str):
        temp = self.get_temp_addr()
        operand1 = self.semantic_stack[0]
        operand2 = self.semantic_stack[-1]
        self.add_code((self.arith_operators[operator], operand1, operand2, temp))
        self.semantic_stack.multipop(2)
        self.semantic_stack.push(temp)
        self.program_counter += 1

    def add(self, lookahead: str = None):
        self.arith('+')

    def sub(self, lookahead: str = None):
        self.arith('-')

    def mult(self, lookahead: str = None):
        self.arith('*')

    def div(self, lookahead: str = None):
        self.arith('/')

    def lt(self, lookahead: str = None):
        self.arith('<')

    def eq(self, lookahead: str = None):
        self.arith('==')

    def push_id(self, lookahead: str = None):
        self.semantic_stack.push(self.symbol_table.index_of(lookahead, self.scope_stack.top()))

    def index_addr(self, lookahead: str = None):
        addr = self.semantic_stack.pop() + self.semantic_stack.pop()
        self.semantic_stack.push(addr)

    def assign(self, lookahead: str = None):
        self.add_code(('ASSIGN', self.semantic_stack[-1], self.semantic_stack.top()))

    def output(self, lookahead: str = None):
        self.add_code(('PRINT', lookahead))

    def start_scope(self, lookahead: str = None):
        self.scope_stack.push(self.scope_counter)
        self.scope_counter += 1

    def end_scope(self, lookahead: str = None):
        self.scope_stack.pop()

    def ifelse(self, lookahead: str = None):
        # todo
        pass

    def while_loop(self, lookahead: str = None):
        # todo
        pass

    def add_code(self, code, index: int = program_counter):
        if index > len(self.program_block):
            add_count = index + 1 - len(self.program_block)
            self.program_block.extend([None] * (add_count - 1))

        if index == len(self.program_block):
            self.program_block.append(code)
        elif index < len(self.program_block):
            self.program_block[index] = code

    def write_program_block(self):
        with open('output.txt', 'w') as file:
            for code in self.program_block:
                file.write(
                    f'({code[0]}, {code[1]}, {code[2] if len(code) > 2 else ""}, {code[3] if len(code) > 3 else ""})\n'
                )
