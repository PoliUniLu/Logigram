import logigram.visualisation as visualisation
from parameterized import parameterized

import unittest
import  filecmp

class KnownFigures(unittest.TestCase):
    @parameterized.expand([("A{1}<=>F", visualisation.Mode.MULTI_VALUE_MODE),
                           ("A*b=F",visualisation.Mode.BOOLEAN_MODE),
                           ("A{1}B{2}*C{3}<=>F", visualisation.Mode.INVALID),
                           ("A{1}B{2}*C{3}=F", visualisation.Mode.INVALID),
                           ("A{1}*B{2}+C{3}<=>F", visualisation.Mode.MULTI_VALUE_MODE),
                           ("A*B+c<=>f", visualisation.Mode.BOOLEAN_MODE),
                           ("A*B+c=f", visualisation.Mode.BOOLEAN_MODE),
                           ("A*B+c*A<=>f", visualisation.Mode.BOOLEAN_MODE),
                           (["A*b*C+C*D<=>F","A*b*C+d*a<=>Y"],visualisation.Mode.MULTI_OUTPUT),
                           (["A*b*C+C*D=F","A*b*C+d*a=Y"],visualisation.Mode.MULTI_OUTPUT),
                           (["A{1}+C{1}+C*D<=>F","A{1}+C+D<=>Y"],visualisation.Mode.INVALID),
                           (["A{1}+C{1}<=>F","A{1}+B{2}<=>Y"],visualisation.Mode.MUTLI_VALUE_MULTI_OUT),
                           (["A*b"],visualisation.Mode.INVALID)])
    def test_get_mode(self, input, expected_mode):
        self.assertEqual(visualisation._get_mode(input), expected_mode)
