"""Setup script for the PDF Information Extraction package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-info-extraction",
    version="1.0.0",
    author="paopaoxiangg",
    description="Extract text, tables, equations, and other elements from PDF documents using advanced OCR models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paopaoxiangg/pdf-info-extraction",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-extract=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pdf_extractor": ["config/*.json"],
    },
)
