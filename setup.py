from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='restrant',
    version='0.0.1',
    url='https://github.com/lambdaofgod/restrant',
    author='Jakub Bartczuk',
    packages=find_packages(),
    install_requires=requirements
)
