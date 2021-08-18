from setuptools import setup
from distutils.util import convert_path

version_path = convert_path('paam/__version__.py')
global_vars = {}
exec(open(version_path).read(), global_vars)

setup(
    name='python-attribute-access-modifiers',
    version=global_vars['__version__'],
    packages=['paam'],
    install_requires=[
        'importlib; python_version >= "3.8"',
    ],
    long_description=open('README.md').read(),
    url="https://github.com/2435191/python-attribute-access-modifiers",
    author="Will Bradley",
    author_email="derivativedude123@gmail.com",
    license='License :: OSI Approved :: MIT License',
    long_description_content_type='text/markdown'
)