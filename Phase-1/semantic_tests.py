import unittest
import compiler
import Scanner
import parser
from stack import Stack
from codegen import CodeGenerator
import re

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

        parser.stack = Stack()
        parser.next_token_type, next_token, next_token_nt = '', '', ''
        parser.terminals = []
        parser.non_terminals = []
        parser.follow = {}
        parser.grammar = {}
        parser.parse_table = {}
        parser.syntax_errors = []  # (message, args as tuple)
        parser.action_nt_start_index = -2
        parser.codegen = CodeGenerator()

    def test_all(self):
        for i in [4]:#range(ntests + 1)[1:]:
            with self.subTest(f"Testcase[{i}]"):
                print(f"running Testcase[{i}]")
                self.setUp()

                with open(f"testcases/code-generator/T{i}/input.txt") as file:
                    input = file.read()
                    print("read input file")

                with open(f"testcases/code-generator/T{i}/expected.txt") as file:
                    expected = file.read()
                    print("read expected file for expected value")

                with open("input.txt", "w") as file:
                    file.write(input)
                    print("wrote input file")

                print("compiling started")
                compiler.main()
                print("compiling ended")

                with open(f"testcases/code-generator/T{i}/semantic_errors.txt") as f:
                    expected_semantic_errors = f.read()

                with open(f"semantic_errors.txt") as f:
                    semantic_errors = f.read()
                self.assertEqualTrimWS(semantic_errors, expected_semantic_errors, f"semantic_errors[{i}]")

                has_error = expected_semantic_errors != 'The input program is semantically correct.\n'
                if not has_error:
                    os.system('cp output.txt interpreter/output.txt')
                    os.system('./interpreter/tester_mac_non_m1 > interpreter/actual.txt')

                with open('interpreter/actual.txt') as f:
                    actual = f.read()
                    actual = ''.join([s + '\n' for s in re.findall(r'PRINT +\d+', actual)])
                    self.assertEqualTrimWS(actual, expected, f"output[{i}]")

        os.system('cd ..; zip -vr Phase-1.zip Phase-1/ -x "*.DS_Store"; cd Phase-1')

    def assertEqualTrimWS(self, actual: str, expected: str, msg):
        self.assertEqual(
            "\n".join([f"{s.split('.')[0]}.\t" + "".join(s.split(".")[1:]).strip() for s in expected.split("\n")]),
            "\n".join([f"{s.split('.')[0]}.\t" + "".join(s.split(".")[1:]).strip() for s in actual.split("\n")]), msg)


if __name__ == "__main__":
    unittest.main()
