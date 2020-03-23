from setuptools import setup


setup(name='blupper',
      version='0.1',
      description='Generate BLUPs',
      long_description='Generates BLUPs implementing algorithms described in Linear models for the prediction of animal breeding values (Mrode RA.) Cabi; 2014 Feb 27.',
      url='http://github.com/biomlds/blupper',
      author='Kirill Krivushin',
      author_email='krivushi@ualberta.ca',
      license='MIT',
      packages=['blupper'],
      install_requires=[
          'pandas', 'numpy', 'click'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
