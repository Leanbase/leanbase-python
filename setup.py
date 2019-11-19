import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


TEST_REQUIRES = [
    "nose==1.3.7",
    "twine==1.13.0",
]

setuptools.setup(
    name="leanbase",
    version="1.2.0",
    author="Dipanjan Mukherjee",
    author_email="dipanjan@leanbase.io",
    description="A client for the leanbase API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leanbase/leanbase-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "six==1.12.0",
        "sseclient==0.0.24",
    ],
    tests_require=TEST_REQUIRES,
    extras_require={'test': TEST_REQUIRES},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)