from typing import Dict

from symbol_table import SymbolTable

from stack import Stack


# noinspection PyUnusedLocal
class CodeGenerator:
    program_block = {}
    pc = 0
    semantic_stack = Stack()
    break_stack = Stack()
    scope_stack = Stack()
    scope_counter = 0
    call_args_count = Stack()
    symbol_table = SymbolTable()
    assign_chain_len = 0
    temp_addr = 500

    errors = []

    arith_operators = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '/': 'DIV', '<': 'LT', '==': 'EQ'}

    def call_action_routine(self, action_symbol: str, lookahead: str):
        self.__getattribute__(action_symbol)(lookahead)

    def get_temp_addr(self, size=1):
        prev_addr = self.temp_addr
        self.temp_addr += 4 * size
        return prev_addr

    def save(self, lookahead: str = None):
        self.label()
        self.pc += 1

    def label(self, lookahead: str = None):
        self.semantic_stack.push(self.pc)

    def save_const(self, lookahead: str = None):
        self.semantic_stack.push(f'#{lookahead}')

    def push_op(self, lookahead: str = None):
        self.semantic_stack.push(lookahead)

    def arith(self, operator: str):
        temp = self.get_temp_addr()
        operand1 = self.semantic_stack[-1]
        operand2 = self.semantic_stack[0]
        self.add_code((self.arith_operators[operator], operand1, operand2, temp), index=self.pc)
        self.semantic_stack.multipop(2)
        self.semantic_stack.push(temp)
        self.pc += 1

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
        for scope in self.scope_stack.elements[::-1]:
            id = self.symbol_table.get_addr(lookahead, scope)
            if id is not None:
                self.semantic_stack.push(id)

    def index_addr(self, lookahead: str = None):
        index = str(self.semantic_stack.pop()).replace('#', '')
        start_addr = str(self.semantic_stack.pop()).replace('#', '')
        addr = int(index) + int(start_addr)
        self.semantic_stack.push(addr)

    def assign(self, lookahead: str = None):
        self.add_code(('ASSIGN', self.semantic_stack.top(), self.semantic_stack[-1]), index=self.pc)
        self.semantic_stack.pop()
        self.assign_chain_len -= 1
        self.pc += 1

    def assign_chain_inc(self, lookahead: str = None):
        self.assign_chain_len += 1

    def end_expression_stmt(self, lookahead: str = None):
        if self.assign_chain_len == 1: self.semantic_stack.pop()
        self.assign_chain_len = 0

    def output(self, lookahead: str = None):
        self.add_code(('PRINT', self.semantic_stack.pop()), index=self.pc)
        self.pc += 1

    def start_scope(self, lookahead: str = None):
        self.scope_stack.push(self.scope_counter)
        self.scope_counter += 1

    def end_scope(self, lookahead: str = None):
        self.scope_stack.pop()

    def declare_type(self, lookahead: str = None):
        self.symbol_table.declare(lookahead, self.scope_stack.top())

    def declare_arr(self, lookahead: str = None):
        self.symbol_table.declare_arr()

    def declare_func(self, lookahead: str = None):
        self.symbol_table.declare_func()

    def declare_id(self, lookahead: str = None):
        self.symbol_table.declare_name(lookahead)

    def declare_size(self, lookahead: str = None):
        self.symbol_table.declare_size(int(lookahead))

    def declare_address(self, lookahead: str = None):
        self.symbol_table.declare_address(self.pc)

    def if_block(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-1], self.pc), index=self.semantic_stack.top())
        self.semantic_stack.multipop(2)

    def ifelse(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-3], self.semantic_stack.top()), index=self.semantic_stack[-2])
        self.add_code(('JP', self.pc), index=self.semantic_stack[-1])
        self.semantic_stack.multipop(4)

    def while_loop(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-1], self.pc), index=self.semantic_stack.top())
        self.semantic_stack.multipop(2)

    def break_stmt(self, lookahead: str = None):
        self.break_stack.push(self.scope_stack.top())
        self.save()

    def break_accept(self, lookahead: str = None):
        for scope in self.break_stack.elements[::-1]:
            if scope != self.scope_stack.top(): break
            self.add_code(('JP', self.pc), index=self.semantic_stack.pop())

    def break_error(self, lookahead: str = None):
        for scope in self.break_stack.elements[::-1]:
            if scope != self.scope_stack.top(): break
            # todo error: "invalid break in {semantic_stack.top()}"
            self.semantic_stack.pop()

    def call_args_start(self, lookahead: str = None):
        self.call_args_count.push(0)
        self.semantic_stack.push(None)  # to be set later

    def new_call_arg(self, lookahead: str = None):
        self.call_args_count.elements[-1] += 1

    def call_fun(self, lookahead: str = None):
        self.semantic_stack.push(self.call_args_count.top())
        self.semantic_stack[-self.call_args_count.pop() - 1] = self.pc + 1
        self.add_code(('JP', -self.semantic_stack.pop() - 2), index=self.pc)
        self.add_code(('JP', -self.semantic_stack.pop() - 2), index=self.pc)
        self.pc += 1

        # todo add arguments

    def add_code(self, code, index: int):
        # print([f'PB[{i}] = {c}' for i, c in self.program_block.items()])
        if index in sorted(self.program_block.keys()):
            print(f'prev code[{index}] = {code}')
        self.program_block[index] = code

    def write_program_block(self):
        with open('output.txt', 'w') as file:
            for i, code in sorted(self.program_block.items()):
                if code is None: raise NameError
                file.write(
                    f'{i}.\t({code[0]}, {code[1]}, {code[2] if len(code) > 2 else ""}, {code[3] if len(code) > 3 else ""})\n'
                )

    def write_errors(self):
        with open('semanatic_errors.txt', 'w') as file:
            if len(self.errors) == 0: file.write('The input program is semantically correct.\n')
            for err in self.errors:
                # todo write errors
                pass
