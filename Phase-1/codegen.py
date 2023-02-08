from typing import List

from semantic_analyzer import SemanticAnalyzer
from stack import Stack
from symbol_table import SymbolTable, FunArg


# noinspection PyUnusedLocal
class CodeGenerator:
    arith_operators = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '/': 'DIV', '<': 'LT', '==': 'EQ'}

    def __init__(self, semantic_analyzer):
        self.program_block = {}
        self.pc = 0
        self.semantic_stack = Stack()
        self.break_stack = Stack()
        self.scope_stack = Stack()
        self.scope_counter = 0
        self.call_args_count = 0
        self.return_stack = Stack()
        self.return_addr_stack = Stack()
        self.symbol_table = SymbolTable()
        self.temp_types = {}
        self.assign_chain_len = 0
        self.temp_addr = 500
        self.switch_case_count = 0
        self.semantic_analyzer = semantic_analyzer
        self.line_counter = -1

    def call_action_routine(self, action_symbol: str, lookahead: str, line_counter):
        self.line_counter = line_counter
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

        operand1_type = self.get_mem_type(operand1)
        operand2_type = self.get_mem_type(operand2)

        if operand2_type == 'any':
            temp_type = operand1_type
        elif operand1_type == 'any':
            temp_type = operand2_type
        elif operand1_type != operand2_type:
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_e(operand2_type, operand1_type),
                                             self.line_counter)
            temp_type = 'undefined'
        elif operand1_type != 'undefined':
            # fixme maybe needs an error?
            temp_type = operand1_type
        else:
            temp_type = 'undefined'
        self.temp_types[temp] = temp_type

    def get_mem_type(self, address: str) -> str:
        if str(address).startswith('#') or str(address).startswith('@'):
            return 'int'
        elif int(address) < 500:
            return self.symbol_table.get_type(address)
        else:
            try:
                return self.temp_types[address]
            except KeyError:
                return 'any'

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
            addr = self.symbol_table.get_addr(lookahead, scope)
            if addr is not None:
                if self.symbol_table.get_is_arr(addr):
                    print(end='')
                self.semantic_stack.push(addr)
                found = True
                break
        if not found:
            self.semantic_analyzer.add_error(error=SemanticAnalyzer.generate_error_a(lookahead),
                                             line_num=self.line_counter)
            self.semantic_stack.push('#0');

    def index_addr(self, lookahead: str = None):
        self.semantic_stack.elements[-2] = f'#{self.semantic_stack.elements[-2]}'
        self.add(lookahead)
        self.semantic_stack.push(f'@{self.semantic_stack.pop()}')

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
            scope = f'fun#{self.symbol_table.elements[-1].address}'
        elif lookahead == '{':
            scope = ''
        else:
            raise NameError()
        scope += f' {self.scope_counter}'
        self.scope_stack.push(scope)
        self.scope_counter += 1

    def end_scope(self, lookahead: str = None):
        while len(self.break_stack.elements) > 0:
            break_pc = self.break_stack.top().split(' ')[2]
            if self.break_stack.top().split(' ')[:2] != self.scope_stack.top().split(' '): break
            self.add_code(('JP', self.pc), index=break_pc)
            self.break_stack.pop()

        self.scope_stack.pop()

    def declare_type(self, lookahead: str = None):
        self.symbol_table.declare(lookahead, self.scope_stack.top())

    def declare_arr_init(self, lookahead: str = None):
        self.symbol_table.declare_arr()
        if self.symbol_table.elements[-1].type == 'void':
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_b(self.symbol_table.elements[-1].name),
                                             line_num=self.line_counter - 1)
        else:
            var = self.symbol_table.elements[-1]
            for i in range(var.size):
                self.add_code(('ASSIGN', '#0', var.address + i), index=self.pc)
                self.pc += 1

    def declare_var_init(self, lookahead: str = None):
        if self.symbol_table.elements[-1].type == 'void':
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_b(self.symbol_table.elements[-1].name),
                                             line_num=self.line_counter - 1)
        else:
            var = self.symbol_table.elements[-1]
            self.add_code(('ASSIGN', '#0', var.address), index=self.pc)
            self.pc += 1

    def declare_arr(self, lookahead: str = None):
        self.symbol_table.declare_arr()
        if self.symbol_table.elements[-1].type == 'void':
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_b(self.symbol_table.elements[-1].name),
                                             line_num=self.line_counter)

    def declare_var(self, lookahead: str = None):
        if self.symbol_table.elements[-1].type == 'void':
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_b(self.symbol_table.elements[-1].name),
                                             line_num=self.line_counter)

    def declare_func(self, lookahead: str = None):
        self.symbol_table.declare_func()

    def declare_id(self, lookahead: str = None):
        self.symbol_table.declare_name(lookahead)

    def declare_size(self, lookahead: str = None):
        self.symbol_table.declare_size(int(lookahead))

    def declare_address(self, lookahead: str = None):
        self.symbol_table.declare_address(self.pc)
        if self.symbol_table.elements[-1].name == 'main':
            self.add_code(('ASSIGN', '#2000', '2000'), index=0)
            self.add_code(('JP', self.pc), index=1)

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
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_d(), line_num=self.line_counter - 1)

    def new_fun_arg(self, lookahead: str = None):
        for i in range(len(self.symbol_table.elements))[::-1]:
            elem = self.symbol_table.elements[i]
            if elem.is_func:
                arg = self.symbol_table.elements[-1]
                elem.arguments.append(FunArg(arg.name, arg.type, arg.is_arr, arg.address))
                break

    def new_call_arg(self, lookahead: str = None):
        func_args: List[FunArg] = self.symbol_table.get_arguments(
            self.semantic_stack.elements[-1 - self.call_args_count])
        func_arg = func_args[min(self.call_args_count - 1, len(func_args) - 1)]
        if self.call_args_count <= len(func_args) and \
                self.get_mem_type(self.semantic_stack[0]) != func_arg.get_type():
            self.semantic_analyzer.add_error(
                SemanticAnalyzer.generate_error_f(
                    id_name=self.symbol_table.get_name(self.semantic_stack.elements[-1 - self.call_args_count]),
                    arg_num=self.call_args_count,
                    given_type=self.get_mem_type(self.semantic_stack[0]),
                    expected_type='array' if func_arg.is_arr else func_arg.get_type()),
                self.line_counter)
        self.call_args_count += 1

    def call_args_start(self, lookahead: str = None):
        self.call_args_count = 1

    def call_fun(self, lookahead: str = None):
        self.call_args_count -= 1
        func_addr = self.semantic_stack[-self.call_args_count]
        func_args = self.symbol_table.get_arguments(func_addr)
        func_return = self.symbol_table.get_type(func_addr)
        if self.call_args_count != len(func_args):
            self.semantic_analyzer.add_error(SemanticAnalyzer.generate_error_c(self.symbol_table.get_name(func_addr)),
                                             self.line_counter)
            self.semantic_stack.multipop(self.call_args_count + 1)
            if func_return == 'int':
                self.semantic_stack.push('#0')
        else:
            ra_reg = '2000'
            self.add_code(('ASSIGN', f'#{self.pc + self.call_args_count + 2}', ra_reg), index=self.pc)
            for i in range(self.call_args_count)[::-1]:
                self.add_code(('ASSIGN', self.semantic_stack.pop(), func_args[i].address), index=self.pc + i + 1)
            self.add_code(('JP', func_addr), index=self.pc + self.call_args_count + 1)
            self.semantic_stack.pop()
            if func_return != 'void':
                temp = self.get_temp_addr()
                self.add_code(('ASSIGN', '3000', temp), index=self.pc + self.call_args_count + 2)
                self.semantic_stack.push(temp)
            self.pc += self.call_args_count + 3

    def return_void(self, lookahead: str = None):
        self.return_stmt()

    def return_expr(self, lookahead: str = None):
        ret_val = str(self.semantic_stack.pop())
        is_num = ret_val.startswith('#')
        self.add_code(('ASSIGN', ret_val, '3000'), index=self.pc)
        self.pc += 1
        self.return_stmt()

    def return_stmt(self):
        self.return_stack.push(self.pc)
        self.pc += 1

    def end_func(self, lookahead: str = None):
        while len(self.return_stack.elements) != 0:
            ret_pc = self.return_stack.pop()
            self.add_code(('JP', self.pc), index=ret_pc)
        if self.symbol_table.get_name(int(self.scope_stack.top().split('#')[-1].split()[0])) != 'main':
            self.add_code(('JP', '@2000'), index=self.pc)
            self.pc += 1

    def add_code(self, code, index):
        index = int(index)
        if index in sorted(self.program_block.keys()):
            print(f'prev code[{index}] = {code}')
        self.program_block[index] = code

    def write_program_block(self, generates_code=True):
        with open('output.txt', 'w') as file:
            if not generates_code:
                file.write('The code has not been generated.')
            else:
                max_line = max([int(k) for k in self.program_block.keys()])
                for i in range(max_line):
                    try:
                        self.program_block[i]
                    except KeyError:
                        self.program_block[i] = ('JP', i + 1)
                for i in sorted(self.program_block.keys()):
                    code = self.program_block[i]
                    if code is None: raise NameError
                    file.write(
                        f'{i}\t({code[0]}, {code[1]}, {code[2] if len(code) > 2 else ""}, {code[3] if len(code) > 3 else ""})\n'
                    )
