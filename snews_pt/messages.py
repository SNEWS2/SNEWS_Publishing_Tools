import json
import pickle
from datetime import UTC, datetime
from typing import Union

import click
from hop import Stream
from hop.models import Blob
from snews.models import messages
from snews.models.timing import PrecisionTimestamp


class Publisher:
    def __init__(self, kafka_topic, auth=True):
        self.kafka_topic = kafka_topic
        self.auth = auth

        self.message_queue = []

        pass

    def add_message(self, message: Union[dict, messages.MessageBase],
                    verbose: int = 0) -> None:
        """This method will add a message to the message queue.

        Parameters
        ----------
        message: `dict` or snews.messages.MessageBase
            observation message.
        verbose: `int`
            verbosity level. 0: no output, 1: print simple feedback, 2: print message details.
        """

        msg_props = message if type(message) is dict else message.model_dump()

        for snews_message in messages.create_messages(**msg_props):
            self.message_queue.insert(0, snews_message)

            if verbose >= 1:
                click.secho(f"Added message to queue", fg="green", bold=True)
                if verbose >= 2:
                    click.secho('--------------------------------', fg="blue", bold=True)
                    message_data = snews_message.model_dump()
                    for key, value in message_data.items():
                        click.secho(f"  {key}: {value}", fg="cyan")
                    click.secho('--------------------------------', fg="blue", bold=True)

        return

    def send(self, verbose: int = 0) -> None:
        """This method will send the messages to the Kafka topic.

        Parameters
        ----------
        verbose: `int`
            verbosity level. 0: no output, 1: print simple feedback, 2: print message details.
        """
        stream = Stream(until_eos=True, auth=self.auth)
        with stream.open(self.kafka_topic, "w") as conn:
            while len(self.message_queue) > 0:
                message = self.message_queue.pop()
                message.sent_time_utc = str(PrecisionTimestamp())
                conn.write(Blob(pickle.dumps(message)))
                
                if verbose >= 1:
                    click.secho(f"Sent message to {self.kafka_topic}", fg="green", bold=True)
                    if verbose >= 2:
                        message_data = message.model_dump()
                        click.secho('--------------------------------', fg="blue", bold=True)
                        for key, value in message_data.items():
                            click.secho(f"  {key}: {value}", fg="cyan")
                        click.secho('--------------------------------', fg="blue", bold=True)
                


def test():
    # Build the individual message classes.
    sn = messages.CoincidenceTierMessage(
        detector_name="Super-K", neutrino_time_utc=datetime.now(UTC), dude=5
    )
    print(sn.model_dump())

    sn = messages.SignificanceTierMessage(
        detector_name="Super-K", p_values=[1], t_bin_width_sec=1
    )
    print(sn.model_dump())

    sn = messages.TimingTierMessage(
        detector_name="Super-K",
        timing_series=[1, 2, 3],
        neutrino_time_utc=datetime.now(UTC),
        start_time_utc=datetime.now(UTC),
        machine_time_utc=datetime.now(UTC),
    )
    print(sn.model_dump())

    sn = messages.RetractionMessage(detector_name="Super-K", retract_latest_n=1)
    print(sn.model_dump())

    sn = messages.HeartbeatMessage(detector_name="Super-K", detector_status="ON")
    print(sn.model_dump())

    # Use the builder class.
    print("Exercise the SNEWSMessageBuilder:\n")
    sm = messages.create_messages(
        detector_name="Super-K",
        neutrino_time_utc=datetime.now(UTC),
        p_values=[1],
        t_bin_width_sec=1,
        timing_series=[1, 2, 3],
    )

    # Print generated messages in the SNEWSMessageBuilder, save to JSON.
    print("Messages created and saved to JSON:")
    for j, msg in enumerate(sm):
        print(msg)
        jsonfile = f"{msg.__class__.__name__}.json"
        print(j, msg.__class__.__name__, msg.model_dump())
        json.dump(msg.model_dump(), open(jsonfile, "w"))

    # Instantiate messages from JSON.
    from glob import glob

    jsonfiles = sorted(glob("*.json"))
    for jsonfile in jsonfiles:
        print(f"\nMessages from JSON file {jsonfile}:")
        msgs = messages.create_messages(**json.load(open(jsonfile, "r")))
        for j, msg in enumerate(msgs):
            print(j, msg.__class__.__name__, msg.model_dump(), "\n")


if __name__ == "__main__":  # pragma: no cover
    test()
