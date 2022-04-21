
import json, click, time, sys
from os import path as osp
from SNEWS_PT.snews_pub import SNEWSTiersPublisher, Publisher
fd_mode = bool(sys.argv[1])

with open(osp.join(osp.dirname(__file__), "scenarios.json")) as json_file:
    data = json.load(json_file)

try:
    import inquirer
    # from inquirer.themes import GreenPassion
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
                    SNEWSTiersPublisher(**msg, firedrill_mode=fd_mode).send_to_snews()
                    time.sleep(1)
                    # clear cache after each scenario
                with Publisher() as pub:
                    pub.send([{'_id': 'hard-reset_', 'pass':'very1secret2password', 'detector_name':'TEST'}])
                    print('> Cache cleaned\n')

        except KeyboardInterrupt:
            sys.exit()
except Exception as e:
    print("Something went wrong\n", e, "\nTry manually submitting messages :/")
#