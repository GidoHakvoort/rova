import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rova",
    version="0.0.2",
    author="Gido Hakvoort",
    author_email="gido@hakvoort.it",
    description="API wrapper for ROVA calendar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GidoHakvoort/rova",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)