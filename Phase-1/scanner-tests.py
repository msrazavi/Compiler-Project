import unittest
import compiler
import scanner

ntests = 15


class ScannerTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        scanner.input_text = ""
        scanner.text_pointer = 0
        scanner.line_counter = 1
        scanner.tokens = []
        scanner.errors = []
        scanner.symbols = []

    def test_all(self):
        for i in range(ntests + 1)[1:]:
            with self.subTest(f"Testcase[{i:02d}]"):
                print(f"running Testcase[{i:02d}]")
                self.setUp()

                input = ""
                with open(f"testcases/scanner/T{i:02d}/input.txt") as file:
                    input = file.read()
                    print("read input file")

                expected_symbol_table, expected_lexical_errors, expected_tokens = "", "", ""
                with open(f"testcases/scanner/T{i:02d}/symbol_table.txt") as file:
                    expected_symbol_table = file.read()
                    print("read symbol_table file for expected value")
                with open(f"testcases/scanner/T{i:02d}/lexical_errors.txt") as file:
                    expected_lexical_errors = file.read()
                    print("read lexical_errors file for expected value")
                with open(f"testcases/scanner/T{i:02d}/tokens.txt") as file:
                    expected_tokens = file.read()
                    print("read tokens file for expected value")

                with open("input.txt", "w") as file:
                    file.write(input)
                    print("wrote input file")

                print("compiling started")
                compiler.main()
                print("compiling ended")

                if i == 4:  # for debugging
                    print("", end="")

                symbol_table, lexical_errors, tokens = "", "", ""
                with open("symbol_table.txt") as file:
                    symbol_table = file.read()
                    print("read symbol_table file for actual value")

                self.assertSymbolTableEquals(symbol_table, expected_symbol_table, f"symbol_table[{i:02d}]")

                print("symbol_table assertion passed")
                with open("lexical_errors.txt") as file:
                    lexical_errors = file.read()
                    print("read lexical_errors file for actual value")
                self.assertEqualTrimWS(lexical_errors, expected_lexical_errors, f"lexical_errors[{i:02d}]")
                print("lexical_errors assertion passed")
                with open("tokens.txt") as file:
                    tokens = file.read()
                    print("read tokens file for actual value")
                self.assertEqualTrimWS(tokens, expected_tokens, f"tokens[{i:02d}]")
                print("tokens assertion passed")

    def assertSymbolTableEquals(self, symbol_table, expected_symbol_table, title):
        self.assertEqual(len(expected_symbol_table.split("\n")), len(symbol_table.split("\n")), f"{title} line count")

        for symbol in ["".join(s.split(".")[1:]).strip() for s in expected_symbol_table.split("\n")]:
            if symbol == "": continue
            self.assertRegex(symbol_table, f".*\d+\.[( *)|\t]{symbol}\n.*?", f"{title} symbol={symbol} check exists")

    def assertEqualTrimWS(self, actual: str, expected: str, msg):
        self.assertEqual("\n".join([f"{s.split('.')[0]}.\t" + "".join(s.split(".")[1:]).strip() for s in expected.split("\n")]),
                         "\n".join([f"{s.split('.')[0]}.\t" + "".join(s.split(".")[1:]).strip() for s in actual.split("\n")]), msg)


if __name__ == "__main__":
    unittest.main()
