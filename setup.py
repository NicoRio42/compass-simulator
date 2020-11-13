import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compass-simulator",
    version="0.0.1",
    author="Nicolas Rio",
    author_email="nicolas.rio42@gmail.com",
    description="A package to simulate balance, stability and rapidity tests of an orienteering compass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)