from symbol_table import SymbolTable

from stack import Stack


class CodeGenerator:
    program_block = []
    program_counter = 0
    semantic_stack = Stack()
    scope_stack = Stack()
    symbol_table = SymbolTable()
    temp_addr = 500

    arith_operators = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '/': 'DIV', '<': 'LT', '==': 'EQ'}

    def call_action_routine(self, action_symbol: str, lookahead: str):
        self.__getattribute__(action_symbol[1:])(lookahead)

    def get_temp_addr(self, size=1):
        prev_addr = self.temp_addr
        self.temp_addr += 4 * size
        return prev_addr

    def save(self):
        self.label()
        self.program_counter += 1

    def label(self):
        self.semantic_stack.push(self.program_counter)

    def save_const(self, lookahead: str):
        self.semantic_stack.push(f'#{lookahead}')

    def push_op(self, lookahead: str):
        self.semantic_stack.push(lookahead)

    def arith(self, operator: str):
        temp = self.get_temp_addr()
        operand1 = self.semantic_stack[0]
        operand2 = self.semantic_stack[-1]
        self.add_code((self.arith_operators[operator], operand1, operand2, temp))
        self.semantic_stack.multipop(2)
        self.semantic_stack.push(temp)
        self.program_counter += 1

    def add(self):
        self.arith('+')

    def sub(self):
        self.arith('-')

    def mult(self):
        self.arith('*')

    def div(self):
        self.arith('/')

    def lt(self):
        self.arith('<')

    def eq(self):
        self.arith('==')

    def push_id(self, lookahead: str):
        self.semantic_stack.push(self.symbol_table.index_of(lookahead, self.scope_stack.top()))

    def index_addr(self, lookahead: str):
        index = int(lookahead)
        addr = self.semantic_stack.pop() + index
        self.semantic_stack.push(addr)

    def add_code(self, code, index: int = program_counter):
        if index > len(self.program_block):
            add_count = index + 1 - len(self.program_block)
            self.program_block.extend([None] * (add_count - 1))

        if index == len(self.program_block):
            self.program_block.append(code)
        elif index < len(self.program_block):
            self.program_block[index] = code
