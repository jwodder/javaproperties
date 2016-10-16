from   os.path    import dirname, join
import re
from   setuptools import setup

with open(join(dirname(__file__), 'javaproperties', '__init__.py')) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError('Unable to find own __version__ string')

with open(join(dirname(__file__), 'README.rst')) as fp:
    long_desc = fp.read()

setup(
    name='javaproperties',
    version=version,
    packages=['javaproperties'],
    license='MIT',
    author='John Thorvald Wodder II',
    author_email='javaproperties@varonathe.org',
    keywords='java properties javaproperties configfile config configuration',
    description='Read & write Java .properties files',
    long_description=long_desc,
    url='https://github.com/jwodder/javaproperties',

    setup_requires=['pytest-runner>=2.0,<3'],
    install_requires=['six>=1.4.0,<2'],
    tests_require=['pytest>=2.8,<3', 'python-dateutil'],

    extras_require={
        ':python_version=="2.6"': ['argparse'],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # Python 3.2 doesn't support \uXXXX escapes in regular expressions, so
        # I'm not supporting it.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Java Libraries',
        'Topic :: Utilities',
    ],

    entry_points={
        "console_scripts": [
            'javapropeties = javaproperties.__main__:main',
            'properties2json = javaproperties.tojson:main',
            'json2properties = javaproperties.fromjson:main',
        ]
    },
)
