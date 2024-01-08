from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='ConstitutionalAiTuning',
    version='0.1.0',
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

