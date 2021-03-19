import socket
from time import sleep


HOST = "irc.chat.twitch.tv"  # the twitch irc server
PORT = 6667  # always use port 6667
NICKs_PASSs = [ # twitch username, lowercase and your twitch OAuth token
    ("rprtr258", "oauth:")
]
CHAN = "#screamlark"  # the channel you want to join

MAX_MESSAGE_LENGTH = 500 # maximum message length for twitch


def chat(socks, msg):
    for sock in socks:
        sock.send(f"PRIVMSG {CHAN} :{msg}\r\n".encode("utf-8"))
while True:
    try:
        s = [socket.socket() for _ in NICKs_PASSs]
        for ss, NICKPASS in zip(s, NICKs_PASSs):
            NICK, PASS = NICKPASS
            ss.connect((HOST, PORT))
            ss.send("PASS {}\r\n".format(PASS).encode("utf-8"))
            ss.send("NICK {}\r\n".format(NICK).encode("utf-8"))
            ss.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

        spam_word = "OOOO"
        spam_count = (MAX_MESSAGE_LENGTH - 1) // (len(spam_word) + 1)
        message = " ".join([spam_word] * spam_count)

        while True:
            for _ in range(100):
                chat(s, message)
            print("Waiting 10 secs...", flush=True)
            sleep(2)
    except:
        print("Dropped connection", flush=True)
        pass
