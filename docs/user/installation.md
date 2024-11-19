[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/snews_pt)](https://pypi.org/project/snews_pt/)
![testing](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/ubuntu22-py311-312.yml/badge.svg)
[![arXiv](https://img.shields.io/badge/arXiv-1234.56789-b31b1b.svg)](https://arxiv.org/abs/2406.17743)

# Installation

You can install SNEWS publishing tools (snews_pt) from [PyPi](https://pypi.org/project/snews-pt/) via pip.  We recommend doing things in a clean virtualenv to minimize conflicts with the rest of your python world.  In the example below, using the environment named "snews2", you can call it whatever.

Be sure you've [added your hop credentials](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html) first.

```bash
# Install in a virtual environment
virtualenv snews2
source snews2/bin/activate
python -m pip install snews_pt

# Test the install
snews_pt set-name -n [detector]
snews_pt test-connection --no-firedrill
```
 
or from the source using ssh-key,
```bash
git clone git@github.com:SNEWS2/SNEWS_Publishing_Tools.git
cd SNEWS_Publishing_Tools
pip install ./ --user
```

or using https
```bash
git clone https://github.com/SNEWS2/SNEWS_Publishing_Tools.git
cd SNEWS_Publishing_Tools
pip install ./ --user
```
.
