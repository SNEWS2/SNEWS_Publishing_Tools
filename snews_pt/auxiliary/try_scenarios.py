
import json, click, time, sys
from os import path as osp
from snews_pt.messages import SNEWSMessageBuilder, Publisher
from snews_pt.remote_commands import reset_cache

fd_mode = True if sys.argv[1].lower() == "true" else False
is_test = True if sys.argv[2].lower() == "true" else False

with open(osp.join(osp.dirname(__file__), "scenarios.json")) as json_file:
    data = json.load(json_file)

try:
    import inquirer
    questions = [
    inquirer.Checkbox('scenarios',
                    message=click.style(" Which scenario(s) would you like to run next?", bg='yellow', bold=True),
                    choices=list(data.keys())+list(["finish & exit", "restart cache"]),
                )
    ]

    while True:
        try:
            answers = inquirer.prompt(questions)
            for scenario in answers['scenarios']:
                if scenario=="finish & exit":
                    click.secho("Terminating.")
                    sys.exit()
                elif scenario=="restart cache":
                    reset_cache(firedrill=fd_mode, is_test=is_test)
                    print('> Cache cleaned\n')
                else:
                    click.secho(f"\n>>> Testing {scenario}", fg='yellow', bold=True)
                    messages = data[scenario]
                    for msg in messages: # send one by one and sleep in between
                        msg['is_test'] = is_test
                        print(msg, "\n\n")
                        SNEWSMessageBuilder(**msg).send_messages(firedrill_mode=fd_mode)
                        time.sleep(1)
                        # clear cache after each scenario
                    with Publisher(firedrill_mode=fd_mode, verbose=False) as pub:
                        reset_cache(firedrill=fd_mode, is_test=is_test)
                        print('> Cache cleaned\n')
        except KeyboardInterrupt:
            break
except Exception as e:
    print("Something went wrong\n", e, "\nTry manually submitting messages :/")
#