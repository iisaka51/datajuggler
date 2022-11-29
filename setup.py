from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def get_version(rel_path):
    for line in (this_directory / rel_path).read_text().splitlines():
        if line.startswith('__VERSION__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

LONG_DESCRIPTION = (this_directory / "README.md").read_text()
SHORT_DESCRIPTION = "Utility for data juggling."

def requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="datajuggler",
    version=get_version('datajuggler/versions.py'),
    license="MIT",
    install_requires=requires_from_file('requirements.txt'),
    extras_require={
        'xml': ["xmltodict>=0.13.0"],
        'yaml': ["PyYAML>=6.0"],
        'toml': ["toml>=0.10.2"],
        'bson': ["bson>=0.3.5.1"],
        'phpserialize': [ "phpserialize>=1.3"],
        'dill': ["dill>=0.5.10"],
        'serpent': [ "serpent>=1.4.1"],
        'requests': ["requests>=2.27.0"],
        'emoji': ["emoji==2.1.0"],
        'pandas': ["pandas>=1.4.0"],
        'database': ["dataset>=1.5.0"],
        'msgpack': ["msgpack>=1.0.4"],
        'cloudpack': ["cloudpickle>=2.2.0"],
        'serializer': ["bson>=0.3.5.1",
                       "dill>=6.0",
                       "PyYAML>=6.0",
                       "msgpack>-1.0.4",
                       "phpserialize>=1.3",
                       "serpent>=1.4.1",
                       "toml>=0.10.2",
                       "xmltodict>=0.13.0",
                       "cloudpickle>=2.2.0",
                       ],
    },
    author="Goichi (Iisaka) Yukawa",
    author_email="iisaka51@gmail.com",
    url="https://github.com/iisaka51/datajuggler",
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'': []},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
