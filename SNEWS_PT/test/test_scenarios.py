
import json, click, time, sys
from os import path as osp
from SNEWS_PT.snews_pub import SNEWSTiersPublisher, Publisher

with open(osp.join(osp.dirname(__file__), "scenarios.json")) as json_file:
    data = json.load(json_file)

# try:
import inquirer
from inquirer.themes import GreenPassion
questions = [
  inquirer.Checkbox('scenarios',
                message=click.style(" Which scenario(s) would you like to run next?", bg='yellow', bold=True),
                choices=list(data.keys()),
            )
]

while True:
    try:
        answers = inquirer.prompt(questions) # , theme=GreenPassion()
        for scenario in answers['scenarios']:
            click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
            messages = data[scenario]
            for msg in messages: # send one by one and sleep in between
                SNEWSTiersPublisher(**msg).send_to_snews()
                time.sleep(1)
                # clear cache after each scenario
            with Publisher() as pub:
                pub.send([{'_id': 'hard-reset_'}])
                print('> Cache cleaned\n')

    except KeyboardInterrupt:
        sys.exit()
# except:
#     print('Something went wrong')
    # with Publisher() as pub:
    #     for i, (scenario, dicts) in enumerate(data.items()):
    #         input('Hit enter to run next scenario')
    #         click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
    #         for msg in dicts:
    #             message = CoincidenceTier(**msg).message()
    #             pub.send(message)
    pass