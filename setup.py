"""
Setup for indico apis
"""
from setuptools import setup, find_packages

setup(
    name="poc-toolkit",
    version="0.0.1",
    packages=find_packages(),
    description="""Assortment of funtions for poc work""",
    license="MIT License (See LICENSE)",
    long_description=open("README.md").read(),
    url="https://github.com/fitzworkhub/toolkit",
    author="indico",
    author_email="field.engineering@indico.io",
    install_requires=[
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "idna==2.9",
        "indico-client==3.2.2",
        "msgpack==1.0.0",
        "msgpack-numpy==0.4.4.3",
        "numpy==1.18.4",
        "pandas==1.0.3",
        "Pillow==8.1.1",
        "PyPDF2==1.26.0",
        "python-dateutil==2.8.1",
        "pytz==2020.1",
        "requests==2.23.0",
        "sh==1.13.1",
        "six==1.15.0",
        "urllib3==1.25.9",
    ],
)
