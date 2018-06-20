from setuptools import setup

setup(
    name="GLRM",
    version="0.0.1",
    author="Corinne Horn",
    author_email="cehorn@stanford.edu",
    packages=["glrm"],
    package_dir={"glrm": "glrm"},
    url="http://github.com/cehorn/GLRM/",
    license="MIT",
    install_requires=["numpy >= 1.8",
                      "scipy >= 0.13",
                      "cvxpy >= 0.4.11",
                      "matplotlib >= 2.1.2"]
)
