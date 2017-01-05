# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# requirements
install_requires = [
    "ply>=3.9",
    'protobuf>=3.1.0',
]

dev_requires = [
    "grpcio>=1.0.0",
] + install_requires


setup(name="protoparser",
      description="a simple python compiler for protobuf.",
      keywords="protobuf compiler",
      author="liuRoy",
      author_email="lrysjtu@gail.com",
      packages=find_packages(exclude=['docs', 'example']),
      url="https://github.com/LiuRoy/proto_parser",
      license="GNU",
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          "dev": dev_requires,
      },
      classifiers=[
          "Topic :: Software Development",
          "Intended Audience :: Developers",
          "License :: GNU",
          "Programming Language :: Python :: 2.7",
      ])
