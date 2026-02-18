from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gerrit-checkout",
    version="0.1.0",
    author="Tharindu Piyasekara",
    author_email="tpiyasek@volvocars.com",
    description="Fetch and checkout Gerrit changes by topic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tpiyasek/gerrit-checkout",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "gerrit-checkout=gerrit_checkout.cli:main",
        ],
    },
)
