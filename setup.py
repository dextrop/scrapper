import setuptools

__version__ = "0.0.1"
__description__ = 'The package helps developers to scrap html content from a theme file'
__author__ = 'scoder91@gmail.com'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='html-scrapper',
     version=__version__,
     author="Dextrop",
     py_modules=["scrapper"],
     install_requires=['cssutils', 'bs4', 'requests'],
     entry_points={
        'console_scripts': [
            'scrapper=scrapper:run'
        ],
     },
     author_email=__author__,
     description= __description__,
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dextrop/scrapper",
     packages=setuptools.find_packages(),
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
 )