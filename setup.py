from setuptools import setup, find_packages

setup(
    name="yinstruments",
    packages=find_packages(),
    version="1.10.1",
    description="Experiment device control scripts for BYU's Configurable Computing Lab (https://ccl.byu.edu/)",
    author="Jeff Goeders",
    author_email="jeff.goeders@gmail.com",
    url="https://github.com/byuccl/yinstruments",
    install_requires=[
        "pyudev",
        "pyserial",
        "pysnmp",
        "secbench-vxi11==0.10.1",
        "pyhubctl",
        "standard-telnetlib; python_version >= '3.13'",
    ],
    entry_points={
        "console_scripts": [
            "pdu = yinstruments.pdu.cli:main",
            "usb_power = yinstruments.usb_power:cli",
        ]
    },
)
