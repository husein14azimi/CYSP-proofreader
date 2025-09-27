"""
Setup script for Conference Editing Assistant
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="CYSP-proofreader",
    version="1.0.0",
    author="Hussein Azimi et al.",
    author_email="hossein14azimi@gmail.com",
    description="AI-powered proofreading tool for conference editors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/husein14azimi/CYSP-proofreader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "conference-editor=main:main",
        ],
    },
    package_data={
        "": ["*.md", "LICENSE"],
    },
    include_package_data=True,
)