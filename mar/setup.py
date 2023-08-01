import setuptools
from setuptools import setup, find_packages, Extension


# with open("README.md", "r") as fh:

#     long_description = fh.read()



setuptools.setup(
    name="mar", 
    version="0.1",
    author="schwarzam",
    author_email="gustavo.b.schwarz@gmail.com",
    description="reduction",
    url="https://github.com/schwarzam",
    packages= setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    include_package_data=True
)

# python3 setup.py bdist_wheel
# pip3 install dist/mar-0.1-py3-none-any.whl --force-reinstall

# python3 mar/reduction/LacosmicsBuild setup.py build
# sudo pip3 install Cython
# sudo python3 mar/reduction/LacosmicsBuild setup.py install