from setuptools import setup, find_packages

setup(
    name="adpl",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A systematic framework for detecting and mitigating algorithmic discrimination.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/knkntt/Algorithmic-Discrimination-Proof-Ladder",
    packages=find_packages(), 
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.4.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.8',
)