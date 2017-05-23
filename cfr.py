# -*- coding: utf-8 -*-
import urllib.request, random
 
def getURL(url):
	return str(urllib.request.urlopen(url).read())

str = [getURL("http://codeforces.com/problemset/status/page/%d?order=BY_ARRIVED_DESC" % (i)) for i in range(1, 6)]
rows = []
for s in str:
    t, sub = "", ""
    t = s[s.find("status-frame-datatable") - 14 + 1 : (s[s.find("status-frame-datatable") - 14 + 1:]).find("</table>") + 1]
    t = ("</tr>".join((t[t.find("<tr data-submission-id"):len(t) - 21]).split("</tr>"))).replace("    \\r\\n\\r\\n\\r\\n\\r\\n\\r\\n", "")
    t = t.split("<a")
    rows += [kappa[kappa.find('\"') + 1 : kappa.find('\"', kappa.find('\"') + 1)] for kappa in t if kappa.find("submissionVerdictWrapper") != -1]
print(random.choice(rows))
