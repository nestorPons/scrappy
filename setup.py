from setuptools import setup

setup(name='scrappy',
      version='0.1.0',
      description='Scrapeo de paginas web',
      long_description=open('README.md').read(),
      url='https://github.com/nestorPons/scrappy',
      author='Néstor Pons',
      author_email='nestorpons@gmail.com',
      license='MIT',
      packages=[],
      install_requires=[
          'pyexiv2', 
          'tabulate', 
          'requests',
          'wget',
          'PyExifTool',
          'mechanize >= 0.4.4',
          'progress == 1.5',
          'geocoder'
      ],
      zip_safe=False)