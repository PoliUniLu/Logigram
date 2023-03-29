import logigram.visualisation as visualisation
from parameterized import parameterized

import unittest
import  filecmp

class KnownFigures(unittest.TestCase):
    @parameterized.expand([("A{1}<=>F",False,True,["A"]),
                           ("A{1}*B{2}+A{2}<=>F",False,True,["A","B"]),
                           ("A*b=F",False,False,["A","B"]),
                           ("A=F",False,False,["A"])
    ])
    def test_get_variables(self, input_f,multi_output,multi_value, variables):
        self.assertEqual(visualisation._get_the_variabels(input_f, multi_output,
                                                          multi_value), variables)
