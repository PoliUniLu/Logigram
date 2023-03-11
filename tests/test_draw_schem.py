import sys

import logigram.visualisation as visualisation
from parameterized import parameterized
import matplotlib.pyplot as plt

import unittest
import tempfile
import os
from PIL import Image,ImageChops, ImageOps

plt.ioff()

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
GOLDEN_PATH = os.path.join(TEST_PATH, 'images')
TMP_PATH = tempfile.gettempdir()

TEST_PARAMS = [
    ("pic1", "F=A"),
    ("pic2","F=a"),
    ("pic3", "A*b+a*c*D+E<=>F"),
    ("pic4", "A*b+B*c*D<=>F"),
    ("pic5", "A{1}+B{2}<=>F"),
    ("pic6", "A{1}*B{2}*C{2}+A{1}*D{1}+C{0}<=>F"),
    ("pic7", ["A*b*C+C*D<=>F1", "A*b*C+d*a<=>F2"]),
    ("pic8", ["A+b<=>F1", "b<=>F2"]),
    ("pic9", ["A{1}*B{2}<=>F1", "A{1}*B{2}+A{2}<=>F2"]),
    ("pic10", ["A{1}*B{2}*C{0}+B{1}*C{1}+D{1}<=>F1", "A{1}*B{2}*C{0}+D{1}<=>F2"])
]

def golden_path(name):
    return os.path.join(GOLDEN_PATH, '{}.png'.format(name))

def make_tmp_path(name):
    return os.path.join(TMP_PATH, '{}.png'.format(name))


def trim(im):
    return im.crop(ImageOps.invert(im).getbbox())

def func_image(func, p):
    visualisation.draw_schem(func, color_or='white',
                             color_and='white', showplot=False).savefig(p,
                                                                        bbox_inches='tight')
    im = Image.open(p).convert('RGB')
    return trim(im)

def generate_goldens():
    for name, func in  TEST_PARAMS:
        p = golden_path(name)
        print('Generating {}'.format(p))
        func_image(func, p).save(p)

class KnownFigures(unittest.TestCase):
    @parameterized.expand(TEST_PARAMS)
    def test_sequence(self, name, func):
        fgolden = golden_path(name)
        ftest = make_tmp_path(name)
        visualisation.draw_schem(func, color_or='white',
                                 color_and='white', showplot=False).savefig(ftest,
                                                                            bbox_inches='tight')

        img_test = func_image(func, ftest)
        img_golden = Image.open(fgolden).convert('RGB')
        equal_content = not ImageChops.difference(img_test, img_golden).getbbox()
        if not equal_content:
            ImageChops.difference(img_test, img_golden).save('diff_' + name + '.png')
        img_test.save('test_' + name + '.png')
        self.assertTrue(equal_content)


if __name__ == '__main__':
    if '--generate-goldens' in sys.argv:
        generate_goldens()
    else:
        unittest.main()
