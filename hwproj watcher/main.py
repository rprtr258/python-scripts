import urllib.request, time, pickle
 
def getURL(url):
	return urllib.request.urlopen(url).read().decode()
    
def extractColumn(str):
    res = []
    inTag = False
    for c in str:
        if c == "<":
            inTag = True
        elif c == ">":
            inTag = False
        elif not inTag and not c in "\n ":
            res.append(c)
    return "".join(res)
    
def extractGlyphicon(str):
    if str.find("#") == -1:
        return ""
    str = str[str.find("#") + 1 :]
    str = str[: str.find("\"")]
    return str
    
def parseInfo(info, columns):
    i = 0
    res = []
    for column in columns[1 :]:
        currentRow = []
        if column != [""]:
            for j in range(len(column) - 1):
                currentRow.append(info[i])
                i += 1
        else:
            currentRow.append(info[i])
            i += 1
        res.append(currentRow)
    return res
    
def parseColumns(source):
    table = source[source.find("<div id=\"course_table\"") : source.find("<h2>Задачи</h2>")]

    tableHead = table.split("</thead>")[0]
    tableColumns1 = tableHead.split("</tr>")[0].split("</td>")[: -1]
    tableColumns2 = tableHead.split("</tr>")[1].split("</td>")[: -1]
    tableColumns1 = [extractColumn(s) for s in tableColumns1]
    tableColumns2 = [extractColumn(s) for s in tableColumns2]

    columns = [[tableColumns1[0]]]
    j = 1
    for i in range(1, len(tableColumns1)):
        columnGroup = [tableColumns1[i]]
        if tableColumns1[i] != "":
            while tableColumns2[j] != "":
                columnGroup.append(tableColumns2[j])
                j += 1
        else:
            j += 1
        columns.append(columnGroup)
    return columns

def parseUsers(source, columns):
    table = source[source.find("<div id=\"course_table\"") : source.find("<h2>Задачи</h2>")]

    tableBody = table.split("</thead>")[1]
    
    tableRows = tableBody.split("</tr>")[: -1]
    
    rows = [["<td" + x for x in s.split("<td")][1 :] for s in tableRows]
    rows = [[extractColumn(s[0])] + [extractColumn(s[1])] + [x[x.find("class=\"") + 7 :] for x in s[2 :]] for s in rows]
    rows = [s[: 2] + [(extractGlyphicon(x) if x.find("separator") != -1 else x[: x.find("\"")]) for x in s[2 :]] for s in rows]

    users = [[info[0]] + parseInfo(info[1 :], columns) for info in rows]
    return users

def getChanges(savedColumns, columns, savedUsers, users):
    renames = {
        "task" : "no submissions",
        "task task-with-submissions" : "first solution sent",
        "task task-with-notes" : "added notes",
        "task task-with-new-submissions-and-notes" : "new submission sent",
        "task accepted-task" : "solution accepted"
    }
    messageColor = {
        "task" : "0;30;47",
        "task task-with-submissions" : "1;32;45",
        "task task-with-notes" : "1;33;41",
        "task task-with-new-submissions-and-notes" : "2;31;43",
        "task accepted-task" : "1;37;42"
    }
    medals = {
        "EEC900" : "gold",
        "B0A6A4" : "silver",
        "D98719" : "bronze"
    }
    res = []
    if len(columns) > len(savedColumns):
        for i in range(len(savedColumns), len(columns)):
            if columns[i] == [""]:
                continue
            res.append("added pack %s" % (columns[i][0]))
            for task in columns[i][1 :]:
                res.append("added task %s.%s" % (columns[i][0], task))
                
    for i in range(len(users)):
        if users[i] == savedUsers[i]:
            continue
        for j in range(len(users[i])):
            if j < len(savedUsers[i]) and users[i][j] == savedUsers[i][j]:
                continue
            for k in range(len(users[i][j])):
                if j < len(savedUsers[i]) and users[i][j][k] == savedUsers[i][j][k] or users[i][j][k] == "task" or users[i][j][k] == "":
                    continue
                if columns[j] == [""]:
                    res.append("\x1b[%sm%s got %s medal for pack %s!\x1b[0m" % ("4;35;40", users[i][0], medals[users[i][j][k]], columns[j - 1][0]))
                else:
                    username = users[i][0]
                    task = columns[j][0] + "." + columns[j][k + 1]
                    if j > 2:
                        messageCol = messageColor[users[i][j][k]]
                        if j < len(savedUsers[i]):
                            res.append("\x1b[%sm%s changed task %s state from \"%s\" to \"%s\"\x1b[0m" % (messageCol, username, task, renames[savedUsers[i][j][k]], renames[users[i][j][k]]))
                        else:
                            res.append("\x1b[%sm%s changed task %s state to \"%s\"\x1b[0m" % (messageCol, username, task, renames[users[i][j][k]]))
                    else:
                        res.append("\x1b[%sm%s changed todos %s to %s\x1b[0m" % ("3;32;40", username, savedUsers[i][1][0], users[i][1][0]))
    return res


savedSource = getURL("http://hwproj.me/courses/24")
savedColumns, savedUsers = [], []
with open("save.txt", "rb") as file:
    savedColumns = pickle.load(file)
    savedUsers = pickle.load(file)

while True:
    source = getURL("http://hwproj.me/courses/24")
    if source == savedSource: # may be commented out
        time.sleep(5)
        continue
    columns = parseColumns(source)
    users = parseUsers(source, columns)
    
    if columns != savedColumns or users != savedUsers:
        print("\7", end = "")
        timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        changes = getChanges(savedColumns, columns, savedUsers, users)
        print("\n".join([timestamp + ": " + log for log in changes]))
        with open("log.txt", "w+") as file:
            file.write("\n".join([timestamp + ": " + log for log in changes]))
    
    if users != savedUsers:
        savedSource = source
        savedColumns = columns
        savedUsers = users
            
        with open("save.txt", "wb+") as file:
            pickle.dump(savedColumns, file)
            pickle.dump(savedUsers, file)
        
    time.sleep(5)
