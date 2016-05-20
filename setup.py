from setuptools import setup, find_packages

import playlist as package


def main():
    with open("requirements.txt") as f:
        install_requires = f.readlines()
    with open("setup_requirements.txt") as f:
        setup_requires = f.readlines()
    setup(
        name=package.__name__,
        version=package.__version__,
        packages=find_packages(),

        # Project uses reStructuredText, so ensure that the docutils get
        # installed or upgraded on the target machine

        install_requires=install_requires,
        setup_requires=setup_requires,

        # metadata for upload to PyPI
        author=package.__author__,
        author_email=package.__email__,
        description=package.__doc__,
        license=package.__license__,
        classifiers=[]
    )


if __name__ == '__main__':
    main()
