
import json, click, time, sys
from os import path as osp
from snews_pt.messages import Publisher
from snews_pt.remote_commands import reset_cache
from snews.data.mock import coincidence_scenarios
from snews.models.messages import CoincidenceTierMessage

fd_mode = True if sys.argv[1].lower() == "true" else False
is_test = True if sys.argv[2].lower() == "true" else False

if not is_test:
    click.secho("This script is only for testing purposes, and uses past neutrino times.\n"
                "We are running the scenarios in test mode", fg='red', bold=True)
    is_test = True

scenarios_labels = [d['label'] for d in coincidence_scenarios]

try:
    import inquirer
    questions = [
    inquirer.Checkbox('scenarios',
                    message=click.style(
                        " Which scenario(s) would you like to run next?", 
                        bg='yellow', bold=True),
                    choices=scenarios_labels + ["finish & exit", 
                                                "restart cache"],
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
                    
                    # Find the dict for the scenario in coincidence_scenarios
                    scenario_dict = [d for d in coincidence_scenarios if d['label'] == scenario][0]
                    scenario_events = scenario_dict['events']

                    with Publisher(firedrill_mode=fd_mode, verbose=False) as pub:

                        for evt in scenario_events: # send one by one and sleep in between
                            print(evt, "\n\n")
                            msg = CoincidenceTierMessage(detector_name = evt['detector_name'], 
                                neutrino_time_utc = evt['neutrino_time'],
                                is_test = True) # allow future timestamps
                            
                            pub.add_message(msg)
                            time.sleep(1)

                        pub.send()
                        print(f'> {len(scenario_events)} messages sent.')

                    # clear cache after each scenario
                    with Publisher(firedrill_mode=fd_mode, verbose=False) as pub:
                        reset_cache(firedrill=fd_mode, is_test=is_test)
                        print('> Cache cleaned\n')
                        
        except KeyboardInterrupt:
            break
except Exception as e:
    print("Something went wrong\n", e, "\nTry manually submitting messages :/")
#