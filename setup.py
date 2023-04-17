from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="openclimatedata",
    description="Library to help downloading climate data",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Robert Gieseke",
    url="https://github.com/openclimatedata/openclimatedata",
    project_urls={
        "Issues": "https://github.com/openclimatedata/openclimatedata/issues",
        "CI": "https://github.com/openclimatedata/openclimatedata/actions",
        "Changelog": "https://github.com/openclimatedata/openclimatedata/releases",
    },
    license="BSD-2-Clause",
    version=VERSION,
    packages=["openclimatedata"],
    package_dir={"openclimatedata": "src/openclimatedata"},
    install_requires=["openpyxl", "pandas", "pooch", "tqdm"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
