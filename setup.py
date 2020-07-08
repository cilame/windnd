import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
 
setup(
    name = "windnd",
    version = "1.0.6",
    description = "windows drag icon & drop load.",
    long_description = "import windnd;help(windnd)",
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
