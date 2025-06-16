# SNEWS Publishing Tool
<img src="docs/_static/images/custom_logo.png" alt="snews_logo" width="200"/> 

[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
[![tests](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/snews_pt)](https://pypi.org/project/snews_pt/)
[![arXiv](https://img.shields.io/badge/arXiv-2406.17743-b31b1b.svg)](https://arxiv.org/abs/2406.17743)

<br>See the docs at

|              |        |
| ------------ | ------ |
| **Docs:**    | https://snews-publishing-tools.readthedocs.io/en/latest/  |

This packages provides users with a Python API and CLI to **publish observation messages** to SNEWS and **subscribe to receive alerts** from the SNEWS servers.

> Note: Make sure your hop credentials are set up !!<br>
> Follow the instructions in [**Quick Start**](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html)


|                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| **Fire-Drills**                                                                                                                                                                                                                                                                                                                                                                                                       |
| Also see [this page](https://snews-publishing-tools.readthedocs.io/en/latest/user/firedrills.html)                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                            |
| `snews_pt` allows for fire-drill mode, currently this is the default option. <br/><br/> Later, it can be adjusted through `firedrill_mode=True/False` arguments in subcription and publication functions, and through `--firedrill/--no-firedrill` flags within the CLI tools. <br/>Make sure you have the correct [permissions](https://my.hop.scimma.org/hopauth/) to publish and subscribe to these firedrill channels. |

## How to Install

### [Installation Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/installation.html)

## How to Publish and Subscribe

### [Publishing Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/publishing_protocols.html)
### [Subscribe Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/subscribing.html)


## Command Line Interface (CLI)
There also exists tools for command line interactions. These are explained in detail here;
### [CLI Tools](https://snews-publishing-tools.readthedocs.io/en/latest/user/command_line_interface.html)

## Remote Commands and More

### [Remote commands](https://snews-publishing-tools.readthedocs.io/en/latest/user/remote_commands.html)

