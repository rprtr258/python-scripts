import urllib.request, time, pickle
 
def getURL(url):
    pageSource = urllib.request.urlopen(url).read().decode()
    return pageSource
    
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
    
def parseRow(info, columns):
    i = 0
    res = []
    for column in columns:
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
    table = source[source.find("<div id=\"course_table\"") : source.find("</table>")]

    tableHead = table.split("</thead>")[0]
    tableRows = tableHead.split("</tr>")
    tableColumns1 = tableRows[0].split("</td>")[: -1]
    tableColumns2 = tableRows[1].split("</td>")[: -1]
    tableColumns1 = [extractColumn(s) for s in tableColumns1]
    tableColumns2 = [extractColumn(s) for s in tableColumns2]

    columns = []
    j = 0
    for i in range(len(tableColumns1)):
        mainColumn = tableColumns1[i]
        if j >= len(tableColumns2):
            print(columns)
        else:
            columnGroup = [mainColumn, tableColumns2[j]]
        j += 1
        if columnGroup[1] != "":
            while j < len(tableColumns2) and tableColumns2[j] != "":
                columnGroup.append(tableColumns2[j])
                j += 1
        columns.append(columnGroup)
    return columns

def parseUsers(source, columns):
    table = source[source.find("<div id=\"course_table\"") : source.find("</table>")]
    tableBody = table.split("</thead>")[1]
    tableRows = tableBody.split("</tr>")[: -1]
    
    rows = [["<td" + x for x in s.split("<td")][1 :] for s in tableRows]
    rows = [[extractColumn(s[0])] + [extractColumn(s[1])] + [x[x.find("class=\"") + 7 :] for x in s[2 :]] for s in rows]
    rows = [s[: 2] + [(extractGlyphicon(x) if x.find("separator") != -1 else x[: x.find("\"")]) for x in s[2 :]] for s in rows]
    
    users = [parseRow(row, columns) for row in rows]

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
        for i in range(max(3, len(savedColumns)), len(columns)):
            pack = columns[i][0]
            if pack == "":
                continue
            tasks = [task for task in columns[i][1 :] if task != ""]
            res.append("added pack %s: %s" % (pack, ", ".join(tasks)))
                
    for i in range(len(users)):
        user = users[i]
        if i <= len(savedUsers):
            res.append("%s user appeared" % (user[0][0]))
            savedUsers.append(user[:])
            for j in range(len(user)):
                savedUsers[i][j] = ["task" if note.find("task") != -1 else note for note in user[j]]
                
    for i in range(len(users)):
        user = users[i]
        savedUser = savedUsers[i]
        if user == savedUser:
            continue
        for j in range(len(user)):
            if j < len(savedUser) and user[j] == savedUser[j]:
                continue
            for k in range(len(user[j])):
                if j < len(savedUser) and user[j][k] == savedUser[j][k]:
                    continue
                if user[j][k] == "task" and user[j][k] == "":
                    continue
                if columns[j] == [""]:
                    res.append("\x1b[%sm%s got %s medal for pack %s!\x1b[0m" % ("4;35;40", user[0], medals[user[j][k]], columns[j - 1][0]))
                    res.append("name: %s" % (user[0]))
                    res.append("medal: %s" % (medals[user[j][k]]))
                    res.append("medal color: %s" % (user[j][k]))
                    res.append("pack: %s" % (columns[j - 1][0]))
                else:
                    username = user[0][0]
                    task = columns[j][0] + "." + columns[j][k + 1]
                    if j > 2:
                        messageCol = messageColor[user[j][k]]
                        if j < len(savedUser):
                            res.append("\x1b[%sm%s changed task %s state from \"%s\" to \"%s\"\x1b[0m" % (messageCol, username, task, renames[savedUser[j][k]], renames[user[j][k]]))
                        else:
                            res.append("\x1b[%sm%s changed task %s state to \"%s\"\x1b[0m" % (messageCol, username, task, renames[user[j][k]]))
                    else:
                        res.append("\x1b[%sm%s changed todos %s to %s\x1b[0m" % ("3;32;40", username, savedUser[1][0], user[1][0]))
    return res

savedSource = getURL("http://hwproj.me/courses/24")
savedColumns, savedUsers = [], []
try:
   with open("save.txt", "rb") as file:
       savedColumns = pickle.load(file)
       savedUsers = pickle.load(file)
except:
   pass

while True:
    source = getURL("http://hwproj.me/courses/24")
    if source == savedSource:
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
