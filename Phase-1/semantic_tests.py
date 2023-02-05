import unittest
import compiler
import Scanner
import Parser
from semantic_analyzer import SemanticAnalyzer
from stack import Stack
from codegen import CodeGenerator
import re

import platform
import os

ntests = 15


class SemanticCodegenTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        Scanner.input_text = ""
        Scanner.text_pointer = 0
        Scanner.line_counter = 1
        Scanner.tokens = []
        Scanner.errors = []
        Scanner.symbols = []

        Parser.stack = Stack()
        Parser.next_token_type, next_token, next_token_nt = '', '', ''
        Parser.terminals = []
        Parser.non_terminals = []
        Parser.follow = {}
        Parser.grammar = {}
        Parser.parse_table = {}
        Parser.syntax_errors = []  # (message, args as tuple)
        Parser.action_nt_start_index = -2
        Parser.semantic_analyzer = SemanticAnalyzer()
        Parser.codegen = CodeGenerator(Parser.semantic_analyzer)

    def test_all(self):
        for folder_name in os.listdir('testcases/code-generator'):
            with self.subTest(f"Testcase[{folder_name}]"):
                print(f"running Testcase[{folder_name}]")
                self.setUp()

                with open(f"testcases/code-generator/{folder_name}/input.txt") as file:
                    input = file.read()
                    print("read input file")

                with open(f"testcases/code-generator/{folder_name}/expected.txt") as file:
                    expected = file.read()
                    print("read expected file for expected value")

                with open("input.txt", "w") as file:
                    file.write(input)
                    print("wrote input file")

                print("compiling started")
                if folder_name == 'T9':
                    print(end='')
                compiler.main()
                print("compiling ended")

                with open(f"testcases/code-generator/{folder_name}/semantic_errors.txt") as f:
                    expected_semantic_errors = f.read()

                with open(f"semantic_errors.txt") as f:
                    semantic_errors = f.read()
                self.assertEqualTrimWS(semantic_errors, expected_semantic_errors, f"semantic_errors[{folder_name}]")

                has_error = expected_semantic_errors != 'The input program is semantically correct.\n'
                if not has_error:
                    os.system('cp output.txt interpreter/output.txt')

                    if platform.system() == 'Darwin':
                        tester = 'tester_mac_non_m1'
                    else:
                        tester = 'tester_linux.out'
                    os.system(f'./interpreter/{tester} > interpreter/actual.txt')

                with open('interpreter/actual.txt') as f:
                    actual = f.read()
                    actual = ''.join([s + '\n' for s in re.findall(r'PRINT +\d+', actual)])
                    self.assertEqualTrimWS(actual, expected, f"output[{folder_name}]")

        os.system('cd ..; zip -vr -q Phase-1.zip Phase-1 -i "*.py" "*.json" Phase-1/input.txt; cd Phase-1;')

    def assertEqualTrimWS(self, actual: str, expected: str, msg):
        self.assertEqual(
            "\n".join([s.strip() for s in expected.split()]),
            "\n".join([s.strip() for s in actual.split()])
        )

    if __name__ == "__main__":
        unittest.main()
