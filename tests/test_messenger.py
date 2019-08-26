import logging
from crud.endpoints import SMPTMessenger
from crud.endpoints.smpt_messenger import sample_msg

exp1 = """To: abc@example.com
From: admin@smtp.example.com
Subject: Sample message generated on 2019-07-15 21:12:25.491568.

The message is: "Hello world"
"""


def test_messanger_smtp(capsys):

    M = SMPTMessenger(msg_t=sample_msg, to_addrs="abc@example.com")

    M.send({"msg_text": "Hello world"}, dryrun=True)

    if capsys:
        captured = capsys.readouterr()
        assert exp1 in captured.out


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    test_messanger_smtp(None)
