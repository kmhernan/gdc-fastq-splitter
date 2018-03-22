try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from gdc_fastq_splitter import VERSION

setup(
    name = "gdc_fastq_splitter",
    author = "Kyle Hernandez",
    author_email = "khernandez@bsd.uchicago.edu",
    version = VERSION, 
    description = "CLI for splitting a fastq with multiple readgroups",
    url = "https://github.com/kmhernan/gdc-fastq-splitter",
    license = "Apache 2.0",
    packages = [
        "gdc_fastq_splitter",
        "gdc_fastq_splitter.fastq",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points= {
        'console_scripts': [
            'gdc-fastq-splitter = gdc_fastq_splitter.__main__:main'
        ]
    }
)
