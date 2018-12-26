from websocket import create_connection
import sys
import json

def distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def getAlph(dist):
    #alph = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ( )._+-={}[]abcdefghijklmnopqrstuvwxyz"
    alph = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ( )_.+-={}[]"
    res = ""
    full = dist("")
    print("Full length: " + str(full))
    sys.stdout.flush()
    for c in alph:
        if dist(c) < full:
            res += c
    return res + " "

def guess(dist):
    alph = getAlph(dist)
    print("Alph: \"" + alph + "\"")
    sys.stdout.flush()
    res = ""
    curDist = dist(res)
    found = True
    while found:
        found = False
        for c in alph:
            newS = res
            newDist = curDist
            for i in range(len(res), -1, -1):
                newS = res[:i] + c + res[i:]
                newDist = dist(newS)
                if newDist < curDist:
                    break
            if newDist < curDist:
                found = True
                res = newS
                curDist = newDist
                print(res, curDist)
                sys.stdout.flush()
    return res

email = ""
password = ""
fhqws = create_connection("ws://freehackquest.com:1234/api-ws/")
fhqws.send(json.dumps({"cmd": "login", "m": "m100", "email": email,"password": password}))
fhqws.recv()

def d(s):
    fhqws.send(json.dumps({"cmd": "quest_pass", "m": "m100", "questid": int(sys.argv[1]), "answer": s}))
    resp = json.loads(fhqws.recv())
    answ = ""
    if "error" in resp:
        answ = resp["error"].split()[-1]
    if answ == "" or answ == "passed":
        return 0
    return int(answ)
    
def fixedString(s):
    return lambda x:distance(x, s)

#print(guess(fixedString("WELCOME")))
print(guess(d))
