from setuptools import setup, find_packages

setup(
    name="network-pong",
    version="0.0.1",
    author="Ada Piekarska",
    author_email="adapiekarska97@gmail.com",
    description="Network Pong Client Server Package",
    url="",
    packages=find_packages(exclude=['tests']),
    install_requires=['pygame'],
    entry_points={
        "console_scripts": [
            "play=pong_client:main",
            "pong_server=pong_server:main",
        ],
    },
    licence="MIT",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT Licence",
        "Operating System :: OS Independent",
    ),
)