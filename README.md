# SNEWS Publishing Tool
<img src="docs/_static/images/snews_logo_bkg_light.png" alt="snews_logo" width="200"/> 

[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
[![tests](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/snews_pt)](https://pypi.org/project/snews_pt/)
[![arXiv](https://img.shields.io/badge/arXiv-2406.17743-b31b1b.svg)](https://arxiv.org/abs/2406.17743)

This package provides users with a Python API and CLI to **publish observation messages** to SNEWS and **subscribe to receive alerts** from the SNEWS servers.

The SNEWS Publishing Tools are fully documented at [snews-publishing-tools.readthedocs.io](https://snews-publishing-tools.readthedocs.io/en/latest/).

Before you begin:
* Ensure your hop credentials are set up!
* Follow the instructions in the [**Quick Start**](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html) guide.                                                                                                                                                                                                                                                                                                             
## Fire Drills

We carry out regular multi-experiment fire drills to test the publishing tools. Fire drills are documented on [this page](https://snews-publishing-tools.readthedocs.io/en/latest/user/firedrills.html).

The `snews_pt` library uses fire-drill mode as its default option. If not desired, it can be disabled using the `firedrill_mode=True/False` arguments in the subscription and publication functions, or through the `--firedrill/--no-firedrill` flags within the CLI tools.

To publish and/or subscribe to the fire drill channels, please ensure you have the correct [hop permissions](https://my.hop.scimma.org/hopauth/).

## How to Install the SNEWS Publishing Tools

Detailed installation instructions are provided in our [Installation Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/installation.html).

We recommend that you install SNEWS the publishing tools PyPI package (`snews_pt`) using pip:
```
pip install snews_pt
```
To minimize conflicts with other Python packages, we suggest you set up a dedicated environment using [virtualenv](https://virtualenv.pypa.io/en/latest/), [conda](https://anaconda.org/anaconda/conda), or another tool used to create isolated Python environments.  Also, note that the SNEWS software requires Python v3.11 or higher at the moment, so be sure to set up your enviornment with a new enough version.

## How to Publish and Subscribe

### Publishing

A main purpose of this software is to publish messages to the SNEWS server for the formation of coincident alerts. The exact protocols and interface are described in our [Publishing Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/publishing_protocols.html). Please also see our paper on the publishing tools: [M. Kara et al., JINST 19:P10017, 2024](https://arxiv.org/abs/2406.17743).

### Subscribing

The `snews_pt` package provides easy "read-only" subscriptions to alert topics, and allows subscribers to receive alerts in real time. See the [Subscription Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/subscribing.html) for detailed instructions.

## Command Line Interface (CLI)

Tools for command line interactions with the `snews_pt` library are available, and are explained in our guide to the [CLI Tools](https://snews-publishing-tools.readthedocs.io/en/latest/user/command_line_interface.html).

## Remote Commands and More

The SNEWS server allows for several remote commands. Some of them are meant only for the developers of `snews_pt` and are not intended for regular users. However, there are a few useful functionalities that the user can exploit to test their connections to the SNEWS 2.0 coincidence server.

The available functions are detailed in our [Remote commands](https://snews-publishing-tools.readthedocs.io/en/latest/user/remote_commands.html) guide.

