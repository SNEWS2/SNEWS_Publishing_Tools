## This script is to demonstrate how a custom made script
## can be plugged into the alert subscription

# must have arguments
import sys, json
data = json.load(open(sys.argv[1]))

# custom work
import click
print("\n\n")
click.secho(r"  _________ _______  _____________      __  _________ .__            _____                                             " , fg='black', bg='white', bold=True)
click.secho(r" /   _____/ \      \ \_   _____/  \    /  \/   _____/ |__| ______   /  _  \__  _  __ ____   __________   _____   ____  " , fg='black', bg='white', bold=True)
click.secho(r" \_____  \  /   |   \ |    __)_\   \/\/   /\_____  \  |  |/  ___/  /  /_\  \ \/ \/ // __ \ /  ___/  _ \ /     \_/ __ \ " , fg='black', bg='white', bold=True)
click.secho(r" /        \/    |    \|        \\        / /        \ |  |\___ \  /    |    \     /\  ___/ \___ (  <_> )  Y Y  \  ___/ " , fg='black', bg='white', bold=True)
click.secho(r" _______  /\____|__  /_______  / \__/\  / /_______  / |__/____  > \____|__  /\/\_/  \___  >____  >____/|__|_|  /\___  >" , fg='black', bg='white', bold=True)
click.secho(r"        \/         \/        \/       \/          \/          \/          \/            \/     \/            \/     \/ ", fg='black', bg='white', bold=True)
click.secho(f"\n\n Taking the alert data and doing some important follow-up work in a custom script\n I am also awesome!\n", bold=True)
click.echo(f"Here is the alert dictionary I received")
for k,v in data.items():
    print(f"{k:20s} : {v}")
