import socket
import time


HOST = "irc.chat.twitch.tv"  # the twitch irc server
PORT = 6667  # always use port 6667
NICK = "rprtr258"  # twitch username, lowercase
PASS = "oauth:token"  # your twitch OAuth token
CHAN = "#screamlark"  # the channel you want to join


def chat(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\r\n".encode("utf-8"))


def ban(sock, user):
    chat(sock, ".ban {}".format(user))


ss = [
"bots","nicknames","list"
]

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
       s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
       print("Pong")
    # ban for 30 users at once to overcome twitch dropping connect
    c = 0
    while c < 30:
        n = ss[0]
        ban(s, n)
        ss = ss[1:]
        c += 1
    time.sleep(10)
