"""
This script is to demonstrate how a custom made script
can be plugged into the alert subscription
"""

# must have arguments
import json
import sys
import click

data = json.load(open(sys.argv[1]))

print("\n\n")
click.secho(
    (
        r"  _________ _______  _____________      __  _________ .__            _____        "
        r"                                     "
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        r" /   _____/ \      \ \_   _____/  \    /  \/   _____/ |__| ______   /  _  \__ "
        r" _  __ ____   __________   _____   ____  "
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        r" \_____  \  /   |   \ |    __)_\   \/\/   /\_____  \  |  |/  ___/  /  /_\  \ \/"
        r" \/ // __ \ /  ___/  _ \ /     \_/ __ \ "
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        r" /        \/    |    \|        \\        / /        \ |  |\___ \  /    |    "
        r"\     /\  ___/ \___ (  <_> )  Y Y  \  ___/ "
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        r" _______  /\____|__  /_______  / \__/\  / /_______  / |__/____  > \____|__  "
        r"/\/\_/  \___  >____  >____/|__|_|  /\___  >"
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        r"        \/         \/        \/       \/          \/          \/          \/   "
        r"         \/     \/            \/     \/ "
    ),
    fg="black",
    bg="white",
    bold=True,
)
click.secho(
    (
        "\n\n Taking the alert data and doing some important follow-up work "
        "in a custom script\n I am also awesome!\n"
    ),
    bold=True,
)
click.echo("Here is the alert dictionary I received")
for k, v in data.items():
    print(f"{k:20s} : {v}")
