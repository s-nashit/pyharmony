from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='ProjectName',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        
    ],  
    author='Nashit Humam',
    author_email='s_nashit@hotmail.com',
    description='This is the short description',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/s-nashit/pyharmony' #replace with your github source
    }
)