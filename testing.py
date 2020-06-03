"""Test Codegen:
Simple unit tests for parts of our code generator.
More complete tests will require us to go through the
whole cycle of compiling a Mallard program, assembling the
generated assembly code, and executing the resulting
object code on our Duck Machine simulator.  The test
cases here just catch some bugs in the pieces as we
build up the full code generator.
"""

import unittest
from expr import *
from codegen_context import Context, IntConst, Var
from typing import List, Union


def squish(s: str) -> str:
    """Discard initial and final spaces and compress
    all other runs of whitespace to a single space,
    """
    parts = s.strip().split()
    return " ".join(parts)

def crush(text: Union[str, List[str]]) -> List[str]:
    """Whether given a single multi-line string or a
    list of strings (each being one line of text),
    'crush' returns a list of squished lines.
    """
    # If it's a single multi-line string, break
    # it into lines
    if isinstance(text, str):
        lines = text.split("\n")
    else:
        # If it's not a string, it better be a list of strings
        assert isinstance(text, list)
        lines = text
    squished = [squish(l) for l in lines]
    crushed = [l for l in squished if len(l) > 0]
    return crushed

class AsmTestCase(unittest.TestCase):

    def codeEqual(self, generated: List[str], expected: str) -> bool:
        gen = crush(generated)
        exp = crush(expected)
        self.assertEqual(len(gen), len(exp))
        for i in range(len(gen)):
            self.assertEqual(gen[i], exp[i])


class Test_IntConst_Gen(AsmTestCase):
    """Generating code for an IntConst"""

    def test_42(self):
        const = IntConst(42)
        context = Context()
        const.gen(context, "r12")
        expected = """
             LOAD  r12,const_42
        const_42:  DATA 42
        """
        generated = context.get_lines()
        self.codeEqual(generated, expected)

    def test_42n(self):
        const = IntConst(-42)
        context = Context()
        const.gen(context, "r12")
        expected = """
             LOAD  r12,const_n_42
        const_n_42:  DATA -42
        """
        generated = context.get_lines()
        self.codeEqual(generated, expected)


class Test_Var_Gen(AsmTestCase):
    "Generating code for Variable reference (rvalue)"

    def test_var(self):
        var = Var("silly")
        context = Context()
        var.gen(context, "r8")
        expected = """
              LOAD  r8,var_silly
         var_silly:  DATA 0
         """
        generated = context.get_lines()
        print(generated)
        self.codeEqual(generated, expected)

class Test_Assign_Gen(AsmTestCase):
    "Generating code for Variable reference (rvalue)"

    def test_assign(self):
        context = Context()
        assignment = Assign( Var("universe"), IntConst(42))
        assignment.gen(context, "r5")
        expected = """
              LOAD  r5,const_42
              STORE r5,var_universe
         const_42: DATA 42
         var_universe: DATA 0
         """
        generated = context.get_lines()
        self.codeEqual(generated, expected)


if __name__ == "__main__":
    unittest.main()
