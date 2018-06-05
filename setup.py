import os
import sys
import codecs
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
 
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),
                encoding="utf-8").read()
 
LONG_DESCRIPTION = read("README.md")
 
setup(
    name = "windnd",
    version = "1.0.2",
    description = "windows drag icon & drop load.",
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    keywords = "windnd",
    author = "vilame",
    author_email = "opaquism@hotmail.com",
    url = "https://pypi.org/project/windnd/",
    license = "MIT",
    packages = ["windnd"],
    include_package_data=True,
    zip_safe=True,
)
