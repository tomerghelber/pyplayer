from setuptools import setup, find_packages
from pip.req import parse_requirements

import playlist as package


def get_requirements(path):
    # parse_requirements() returns generator of pip.req.InstallRequirement objects
    return map(lambda ir: str(ir.req), parse_requirements(path, session=False))


def main():
    setup(
        name=package.__name__,
        version=package.__version__,
        packages=find_packages(),

        # Project uses reStructuredText, so ensure that the docutils get
        # installed or upgraded on the target machine

        install_requires=get_requirements("requirements.txt"),
        setup_requires=get_requirements("setup_requirements.txt"),

        # metadata for upload to PyPI
        author=package.__author__,
        author_email=package.__email__,
        description=package.__doc__,
        license=package.__license__,
        classifiers=[]
    )


if __name__ == '__main__':
    main()
