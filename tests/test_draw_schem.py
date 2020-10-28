import logigram.visualisation as visualisation
from parameterized import parameterized

import unittest
import  filecmp

class KnownFigures(unittest.TestCase):
    @parameterized.expand([
                    ("pic1","F=A","img1.raw"),
                    ("pic2","F=a","img2.raw"),
                    ("pic3","F=A*b+a*c*D+E","img3.raw"),
                    ("pic4","F=A*b+B*c*D","img4.raw"),
                    ("pic5","F=A{1}+B{2}","img5.raw"),
                    ("pic6","F=A{1}*B{2}*C{2}+A{1}*D{1}+C{0}","img6.raw"),
                    ("pic7",["F1=A*b*C+C*D","F2=A*b*C+d*a"],"img7.raw"),
                    ("pic8",["F1=A+b","F2=b"],"img8.raw"),
                    ("pic9",["F1=A{1}*B{2}","F2=A{1}*B{2}+A{2}"],"img9.raw"),
                    ("pic10",["F1=A{1}*B{2}*C{0}+B{1}*C{1}+D{1}","F2=A{1}*B{2}*C{0}+D{1}"],"img10.raw")

            ])
    def test_sequence(self,name,func,expected_image):
        visualisation.draw_schem(func).savefig("test_{}.raw".format(name),bbox_inches='tight')
        self.assertTrue(filecmp.cmp("test_{}.raw".format(name),"images/{}".format(expected_image)))
        
    

if __name__=='__main__':
    unittest.main()
