from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="student-grade-manager",
    version="2.0.0",
    author="Maruf Shawkat Hossain, Hasan Md Mahadi",
    author_email="shawkath646@gmail.com",
    description="A comprehensive Student Grade Management System with MySQL database and GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shawkath646/student-grade-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "student-grade-manager=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": ["*.py"],
        "data": ["*.sample.json", "*.sample.csv"],
    },
)
