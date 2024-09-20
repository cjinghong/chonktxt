from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chonktxt",
    version="0.1.2",
    author="Jing Hong",
    author_email="jinghongchan@gmail.com",
    description="An SDK that makes it easy to do contextual chunking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjinghong/chonktxt",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "pdfminer.six",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)