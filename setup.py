from setuptools import setup, find_packages

# Add these lines to read the version from __init__.py
import re
import os

def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='ConstitutionalAiTuning',
    version=get_version('ConstitutionalAiTuning'),  # Use the function to get the version
    author='Steffen Brandt',
    author_email='steffen@opencampus.sh',
    description='A Python library for fine-tuning LLMs using constitutional AI principles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/steffen74/ConstitutionalAiTuning',
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
