from setuptools import setup, find_packages

setup(
    name='btcalculator',
    version='1.0.0',
    description='A simple calculator package',
    author='Evlar',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['btcalculator=BTcalculator:main'],
    },
)
