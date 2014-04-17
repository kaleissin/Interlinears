#!/usr/bin/env python

from distutils.core import setup

README_FILE = open('README.rst', 'rt')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(name='Interlinears',
        version='0.2',
        packages=('interlinears',),
        platforms=['any'],
        description='Pretty-printing of linguistic interlinears',
        author_email='kaleissin@gmail.com',
        author='kaleissin',
        long_description=long_description,
        url='https://github.com/kaleissin/Interlinears',
        classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Intended Audience :: Developers',
                'Intended Audience :: Education',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Topic :: Text Processing',
                'Topic :: Text Processing :: General',
                'Topic :: Text Processing :: Linguistic',
                'Topic :: Software Development :: Libraries :: Application Frameworks',
                'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
