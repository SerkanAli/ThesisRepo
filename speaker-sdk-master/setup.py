#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="speaker-sdk",  # Replace with your own username
    version="1.0.0",
    author="Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e.V.",
    author_email="speaker@iais.fraunhofer.de",
    description="Speaker SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://speaker.fraunhofer.de",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "grpcio==1.32.0",
        "grpcio-tools==1.32.0",
    ],
    extras_require={
        "tests": [
            "pytest",
            "pytest-grpc",
            "pytest-black",
            "pytest-cov",
        ]
    },
)
