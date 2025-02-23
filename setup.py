import os
import re

from setuptools import find_packages, setup

# read in README
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.md'), 'rb') as f:
    long_description = f.read().decode().strip()

# load version
with open("snews_pt/_version.py", "r") as f:
    version_file = f.read()
version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]", version_file, re.M)
version = version_match.group(1)

install_requires = []
with open('requirements.txt', 'r') as f:
    for line in f:
        if line.strip():
            install_requires.append(line.strip())

extras_require = {
    'dev': [
        'pytest~=8.0',
        'pytest-console-scripts~=1.4',
        'pytest-cov~=4.1',
        'pytest-runner~=6.0',
        'virtualenv~=20.13',
    ],
    'docs': [
        'autoapi~=2.0',
        'myst_parser~=2.0',
        'sphinx~=7.2',
        'sphinx-autoapi~=3.0',
        'sphinx-rtd-theme~=2.0',
        'sphinxcontrib-programoutput~=0.17',
    ],
}

setup(
    name='snews_pt',
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
            'snews_pt = snews_pt.__main__:main',
        ],
    },

    python_requires='>=3.11,<3.13',
    install_requires=install_requires,
    extras_require=extras_require,

    classifiers=[
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
