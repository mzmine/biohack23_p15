import os
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(here, "__version__.py")) as f:
    exec(f.read(), version)

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="library spectra validator",
    version=version["__version__"],
    description="Tool for validation and uploading spectral libraries",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Niek de Jonge, Olena Mokshyna",
    author_email="",
    url="https://github.com/mzmine/biohack23_p15/tree/main/library_spectra_validation",
    packages=find_packages(),
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    test_suite="tests",
    python_requires='>=3.9',
    install_requires=[
        "matchms>=0.23.1"
    ],
    extras_require={"dev": ["bump2version",
                            "isort>=5.1.0",
                            "prospector[with_pyroma]",
                            "pytest",
                            "pytest-cov",
                            ],
    }
)