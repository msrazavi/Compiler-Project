from typing import Dict

from symbol_table import SymbolTable

from stack import Stack


# noinspection PyUnusedLocal
class CodeGenerator:
    arith_operators = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '/': 'DIV', '<': 'LT', '==': 'EQ'}

    def __init__(self):
        self.program_block = {}
        self.pc = 0
        self.semantic_stack = Stack()
        self.break_stack = Stack()
        self.scope_stack = Stack()
        self.scope_counter = 0
        self.call_args_count = Stack()
        self.symbol_table = SymbolTable()
        self.assign_chain_len = 0
        self.temp_addr = 500
        self.switch_case_count = 0

        self.errors = []

    def call_action_routine(self, action_symbol: str, lookahead: str):
        self.__getattribute__(action_symbol)(lookahead)

    def get_temp_addr(self, size=1):
        prev_addr = self.temp_addr
        self.temp_addr += size
        return prev_addr

    def save(self, lookahead: str = None):
        self.label()
        self.empty_cell()

    def empty_cell(self, lookahead: str = None):
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
        found = False
        for scope in self.scope_stack.elements[::-1]:
            id = self.symbol_table.get_addr(lookahead, scope)
            if id is not None:
                self.semantic_stack.push(id)
                found = True
                break
        if not found:
            # todo id not found
            pass

    def index_addr(self, lookahead: str = None):
        self.semantic_stack.elements[-2] = f'#{self.semantic_stack.elements[-2]}'
        self.add(lookahead)
        self.semantic_stack[0] = f'@{self.semantic_stack.top()}'

    def assign(self, lookahead: str = None):
        self.add_code(('ASSIGN', self.semantic_stack.top(), self.semantic_stack[-1]), index=self.pc)
        self.semantic_stack.multipop(2 if self.assign_chain_len == 1 and lookahead == ';' else 1)
        self.assign_chain_len -= 1
        self.pc += 1

    def assign_chain_inc(self, lookahead: str = None):
        self.assign_chain_len += 1

    def output(self, lookahead: str = None):
        self.add_code(('PRINT', self.semantic_stack.pop()), index=self.pc)
        self.pc += 1

    def start_scope(self, lookahead: str = None):
        if lookahead in ['if', 'while', 'switch']:
            scope = f'{lookahead}#'
        elif lookahead in ['int', 'void']:
            scope = ''
        elif lookahead == '(':
            scope = f'fun#{len(self.symbol_table.elements) - 1}'
        elif lookahead == '{':
            scope = ''
        else:
            raise NameError()
        scope += f'{self.scope_counter}'
        self.scope_stack.push(scope)
        self.scope_counter += 1

    def end_scope(self, lookahead: str = None):
        while len(self.break_stack.elements) > 0:
            break_scope, break_pc = tuple(self.break_stack.top().split(' '))
            if break_scope != self.scope_stack.top(): break
            self.add_code(('JP', self.pc), index=break_pc)
            self.break_stack.pop()

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
        if self.symbol_table.elements[-1].name == 'main':
            self.add_code(('JP', self.pc), index=self.semantic_stack.elements[0])

    def if_block(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-1], self.pc), index=self.semantic_stack.top())
        self.semantic_stack.multipop(2)

    def ifelse(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-3], self.semantic_stack.top()), index=self.semantic_stack[-2])
        self.add_code(('JP', self.pc), index=self.semantic_stack[-1])
        self.semantic_stack.multipop(4)

    def while_loop(self, lookahead: str = None):
        self.add_code(('JPF', self.semantic_stack[-1], self.pc + 1), index=self.semantic_stack[0])
        self.add_code(('JP', self.semantic_stack[-2]), index=self.pc)
        self.pc += 1
        self.semantic_stack.multipop(3)

    def switch_block(self, lookahead: str = None):
        switch_val = self.semantic_stack[-3 * self.switch_case_count]

        while self.switch_case_count > 0:
            t = self.get_temp_addr()
            self.add_code(('EQ', self.semantic_stack[-2], switch_val, t), index=self.semantic_stack[-1])
            self.add_code(('JPF', t, self.semantic_stack[0]), index=self.semantic_stack[-1] + 1)

            self.semantic_stack.multipop(3)

            self.switch_case_count -= 1
        self.semantic_stack.pop()

    def new_case(self, lookahead: str = None):
        self.switch_case_count += 1

    def break_stmt(self, lookahead: str = None):
        break_accepted = False
        for scope in self.scope_stack.elements[::-1]:
            scope_split = str(scope).split('#')
            if len(scope_split) == 2 and scope_split[0] in ['while', 'switch']:
                break_accepted = True
                self.break_stack.push(f'{scope} {self.pc}')
                self.pc += 1
                break
        if not break_accepted:
            # todo break not accepted
            pass

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

    def add_code(self, code, index):
        index = int(index)
        if index in sorted(self.program_block.keys()):
            print(f'prev code[{index}] = {code}')
        self.program_block[index] = code

    def write_program_block(self):
        with open('output.txt', 'w') as file:
            for i in sorted(self.program_block.keys()):
                code = self.program_block[i]
                if code is None: raise NameError
                file.write(
                    f'{i}.\t({code[0]}, {code[1]}, {code[2] if len(code) > 2 else ""}, {code[3] if len(code) > 3 else ""})\n'
                )

    def write_errors(self):
        with open('semantic_errors.txt', 'w') as file:
            if len(self.errors) == 0: file.write('The input program is semantically correct.\n')
            for err in self.errors:
                # todo write errors
                pass
