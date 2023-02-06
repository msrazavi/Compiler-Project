import unittest
import compiler
import scanner
import parser
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
        scanner.input_text = ""
        scanner.text_pointer = 0
        scanner.line_counter = 1
        scanner.tokens = []
        scanner.errors = []
        scanner.symbols = []

        parser.stack = Stack()
        parser.next_token_type, next_token, next_token_nt = '', '', ''
        parser.terminals = []
        parser.non_terminals = []
        parser.follow = {}
        parser.grammar = {}
        parser.parse_table = {}
        parser.syntax_errors = []  # (message, args as tuple)
        parser.action_nt_start_index = -2
        parser.semantic_analyzer = SemanticAnalyzer()
        parser.semantic_analyzer.errors = []
        parser.codegen = CodeGenerator(parser.semantic_analyzer)

    def test_all(self):
        # remaining tests: T15 o3-function o1-semantic o2-semantic o3-semantic
        for folder_name in ['T15']:  # os.listdir('testcases/code-generator'):
        # for folder_name in ['o3-semantic'.upper()]:  # os.listdir('testcases/code-generator'):
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
                compiler.main()
                print("compiling ended")

                with open(f"testcases/code-generator/{folder_name}/semantic_errors.txt") as f:
                    expected_semantic_errors = f.read()

                with open(f"semantic_errors.txt") as f:
                    semantic_errors = f.read()
                self.assertEqualTrimWS(semantic_errors, expected_semantic_errors, f"semantic_errors[{folder_name}]")

                has_error = expected_semantic_errors.strip() != 'The input program is semantically correct.'
                if not has_error:
                    os.system('rm interpreter/output.txt')
                    os.system('cp output.txt interpreter/output.txt')

                    if platform.system() == 'Darwin':
                        tester = 'tester_mac_non_m1'
                    else:
                        tester = 'tester_linux.out'
                    os.system(f'./interpreter/{tester} > interpreter/actual.txt')

                with open('interpreter/actual.txt') as f:
                    actual = f.read()
                    actual = ''.join([s + '\n' for s in re.findall(r'PRINT +[\-+]?\d+', actual)])
                    if folder_name == 'T15':
                        print(end='')
                    self.assertEqualTrimWS(actual, expected, f"output[{folder_name}]")

        os.system('cd ..; zip -vr -q Phase-1.zip Phase-1 -i "*.py" "*.json" Phase-1/input.txt; cd Phase-1;')

    def assertEqualTrimWS(self, actual: str, expected: str, msg):
        self.assertEqual(
            " ".join([s.replace('PRINT ', '').strip() for s in expected.split('\n')]),
            " ".join([s.replace('PRINT ', '').strip() for s in actual.split('\n')])
        )

    if __name__ == "__main__":
        unittest.main()
