# SNEWS Publishing Tool
<img src="docs/custom_logo.png" alt="snews_logo" width="200"/> 

[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
![testing](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/ubuntu20-py39.yml/badge.svg)
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


[//]: # (There also exists tools for command line interactions. These are explained in detail [here]&#40;docs/cli_docs.md&#41;)

[//]: # (### Extension for follow-up plugins &#40;only with CLI for now&#41;)

[//]: # (`snews_pt subscribe` also allows for other scripts to be plugged in and act on alerts. The *CLI* command `snews_pt subscribe` takes the custom made script via `--plugin` &#40;`-p`&#41; option.)

[//]: # ()
[//]: # (```bash )

[//]: # (user/home$: snews_pt subscribe -p ./auxiliary/custom_script.py)

[//]: # (```)

[//]: # ()
[//]: # (`snews_pt subscribe` saves the alert messages to a local JSON file with the date stamp of the received time. When a custom plugin is provided, as soon as an alert is received and JSON is created, the name of this unique-JSON file is passed to the script and executed.)

[//]: # ()
[//]: # (Therefore, all custom-made scripts should contain the following two lines;)

[//]: # ()
[//]: # (```python)

[//]: # (# in "custom_made_script.py")

[//]: # (import sys, json)

[//]: # (data = json.load&#40;open&#40;sys.argv[1]&#41;&#41;)

[//]: # (```)

[//]: # (and do the follow-up work using the `data` dictionary as the alert message. See [this dummy example]https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/snews_pt/test/random_plugin.py&#41; which )

[//]: # (only brags about itself and displays you the content of the alert message.)

[//]: # ()
