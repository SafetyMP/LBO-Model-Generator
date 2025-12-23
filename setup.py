"""
Setup script for LBO Model Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lbo-model-generator",
    version="1.0.0",
    author="LBO Model Generator Team",
    description="A comprehensive tool for generating Leveraged Buyout (LBO) financial models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SafetyMP/LBO-Model-Generator",
    license="Apache-2.0",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lbo-generate=src.lbo_input_generator:main",
        ],
    },
    keywords="lbo leveraged-buyout financial-modeling excel investment-banking private-equity",
    project_urls={
        "Bug Reports": "https://github.com/SafetyMP/LBO-Model-Generator/issues",
        "Source": "https://github.com/SafetyMP/LBO-Model-Generator",
        "Documentation": "https://github.com/SafetyMP/LBO-Model-Generator/tree/main/docs",
    },
)

