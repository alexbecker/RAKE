from setuptools import setup

VERSION = '0.0.0'

setup(
    name='pyrake',
    packages='rake',
    version=VERSION,
    description='A Python implementation of the RAKE keyword extraction algorithm',
    author='aneesha',
    author_email='TODO',  # TODO
    url='https://github.com/aneesha/rake',
    download_url='https://github.com/aneesha/rake/tarball/{}'.format(VERSION),
    install_requires=[],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
