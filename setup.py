from setuptools import setup, find_packages

setup(
    name="yinstruments",
    packages=find_packages(),
    version="1.3.2",
    description="Experiment device control scripts for BYU's Configurable Computing Lab (https://ccl.byu.edu/)",
    author="Jeff Goeders",
    author_email="jeff.goeders@gmail.com",
    url="https://github.com/byuccl/yinstruments",
    install_requires=["pyudev", "pyserial", "pysnmp", "python-vxi11", "pyhubctl"],
    entry_points={"console_scripts": ["pdu = yinstruments.pdu.cli:main"]},
)
