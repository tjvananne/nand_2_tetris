from assembler import Assembler
from unittest import TestCase



def test_to_bin():
    a = Assembler()
    assert(a._int_to_bin("7") == "0000000000000111")


def test_parse_line_01():
    a = Assembler()
    result = a.parse_line("@100")
    answer = {"type": "A-instruction-literal", "a_numliteral": "100"}
    TestCase().assertDictEqual(result, answer)


def test_parse_line_02():
    a = Assembler()
    result = a.parse_line("@mysymbol")
    answer = {"type": "A-instruction-symbol", "a_symbol": "mysymbol"}
    TestCase().assertDictEqual(result, answer)


def test_parse_line_03():
    a = Assembler()
    result = a.parse_line("0;JMP")
    answer = {"type": "C-instruction", "dest": "null", "comp": "0", "jump": "JMP"}
    TestCase().assertDictEqual(result, answer)


def test_parse_line_04():
    a = Assembler()
    result = a.parse_line("A=D-1")
    answer = {"type": "C-instruction", "dest": "A", "comp": "D-1", "jump": "null"}
    TestCase().assertDictEqual(result, answer)


def test_parse_line_05():
    a = Assembler()
    result = a.parse_line("A=0;JEQ")
    answer = {"type": "C-instruction", "dest": "A", "comp": "0", "jump": "JEQ"}
    TestCase().assertDictEqual(result, answer)


def test_parse_line_06():
    a = Assembler()
    a.instruction_number = 7
    result = a.parse_line("(END)")
    answer = {"type": "label", "label": "END", "value": 7}
    TestCase().assertDictEqual(result, answer)


# for debugging... if necessary
if __name__ == "__main__":
    test_parse_line_02()


