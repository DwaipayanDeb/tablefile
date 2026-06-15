import os
import setuptools

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tablefile", # Package Name
    version="1.0.0",
    author="Dwaipayan Deb",
    author_email="dwaipayandeb@yahoo.co.in",
    description="A package for reading and processing tabular data files for analytical applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DwaipayanDeb/tablefile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)