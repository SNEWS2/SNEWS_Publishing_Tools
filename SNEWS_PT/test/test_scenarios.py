
import json, click, time, sys
from os import path as osp
from SNEWS_PT.snews_pub import CoincidenceTier, Publisher

with open(osp.join(osp.dirname(__file__), "scenarios.json")) as json_file:
    data = json.load(json_file)

try:
    import inquirer
    from inquirer.themes import GreenPassion
    questions = [
      inquirer.Checkbox('scenarios',
                    message=click.style(" Which scenario(s) would you like to run next?", bg='yellow', bold=True),
                    choices=['reset cache']+list(data.keys()),
                )
    ]

    with Publisher() as pub:
        while True:
            try:
                answers = inquirer.prompt(questions) # , theme=GreenPassion()
                for scenario in answers['scenarios']:
                    if scenario == 'reset cache':
                        pub.send({'_id': 'hard-reset_'})
                        time.sleep(1)
                        print('> Cache cleaned')
                        continue
                    click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
                    messages = data[scenario]
                    for msg in messages:
                        message = CoincidenceTier(**msg).message()
                        pub.send(message)
                        time.sleep(1)
                    print()
            except KeyboardInterrupt:
                sys.exit()
except:
    # with Publisher() as pub:
    #     for i, (scenario, dicts) in enumerate(data.items()):
    #         input('Hit enter to run next scenario')
    #         click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
    #         for msg in dicts:
    #             message = CoincidenceTier(**msg).message()
    #             pub.send(message)
    pass