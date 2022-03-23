import os
import re
from setuptools import find_packages, setup

# read in README
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.md'), 'rb') as f:
    long_description = f.read().decode().strip()

# load version
with open("SNEWS_PT/_version.py", "r") as f:
    version_file = f.read()
version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]", version_file, re.M)
version = version_match.group(1)

install_requires = []

def read_requirements():
    with open('docs/requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')
    return install_requires.append(requirements)

extras_require = {
    'dev': [
        'autopep8',
        'flake8',
        'mongomock',
        'pytest >= 5.0, < 5.4',
        'pytest-console-scripts',
        'pytest-cov',
        'pytest-mongodb',
        'pytest-runner',
        'twine',
        'schedule',
    ],
    'docs': [
        'sphinx',
        'sphinx_rtd_theme',
        'sphinxcontrib-programoutput'
    ],
}

setup(
    name='SNEWS_PT',
    version=version,
    description='An alert application for observing supernovas.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SNEWS2/SNEWS_Publishing_Tools',
    author='Sebastian Torres-Lara, Melih Kara',
    author_email='sebastiantorreslara17@gmail.com, karamel.itu@gmail.com',
    license='BSD 3-Clause',
    setup_requires=['pbr'],
    pbr=True,
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'snews_pt = SNEWS_PT.__main__:main',
        ],
    },

    python_requires='>=3.6.*',
    install_requires=read_requirements(),
    extras_require=extras_require,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'License :: OSI Approved :: BSD License',
    ],

)
