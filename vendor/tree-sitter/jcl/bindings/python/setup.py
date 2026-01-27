from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

tree_sitter_jcl = Pybind11Extension(
    "tree_sitter_jcl",
    [
        "tree_sitter_jcl/binding.cpp",
        "../../src/parser.c",
    ],
    include_dirs=[
        "../../src",
    ],
    language='c++',
    cxx_std=14,
)

setup(
    name="tree-sitter-jcl",
    version="0.1.0",
    description="JCL grammar for tree-sitter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/yourusername/tree-sitter-jcl",
    license="MIT",
    packages=["tree_sitter_jcl"],
    ext_modules=[tree_sitter_jcl],
    cmdclass={"build_ext": build_ext},
    install_requires=[
        "tree-sitter>=0.20.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
)