import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def retrieve_version():
    with open("pychkari/__init__.py", "r") as f:
        content = f.read()

    v = content.split("\"")[1]
    return v


version = retrieve_version()

setuptools.setup(
    name="pychkari",
    version=version,
    author="Akshay Zade",
    author_email="akshay2000@hotmail.com",
    description="A Very Simple Python Dependency Injector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akshay2000/Pychkari",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
