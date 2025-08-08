from setuptools import setup, find_packages

setup(
    name="pbl_assistant",
    version="0.1.0",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    python_requires=">=3.8",
)
