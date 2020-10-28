from setuptools import setup

setup(name='logigram',
      version='0.0.1',
      description='Logic diagram drawer',
      url='https://github.com/ZuzanaSebb/Logigram',
      author='Zuzana Sebechlebska',
      author_email='zuzanasebechlebska@gmail.com',
      license='GPL',
      keywords='logic diagram circuit CNF',
      packages=['Logigram'],
      install_requires=[
        'SchemDraw==0.6.0'
          ],
      python_requires='>=3',
      zip_safe=False)

