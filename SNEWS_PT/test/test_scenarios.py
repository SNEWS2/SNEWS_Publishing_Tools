
import json, click
from SNEWS_PT.snews_pub import CoincidenceTier, Publisher

with open("scenarios.json") as json_file:
    data = json.load(json_file)

with Publisher() as pub:
    for scenario, dicts in data.items():
        click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
        for msg in dicts:
            message = CoincidenceTier(**msg).message()
            pub.send(message)