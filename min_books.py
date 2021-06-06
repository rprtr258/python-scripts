from os import walk, path
from sys import argv

from toolz import pipe, juxt, compose, identity
from toolz.curried import take, map, mapcat, get, do, drop


if len(argv) < 2:
    print("Usage:")
    print("python main.py n m")
    print("To drop n first lines and show m lines after")
    exit()

to_drop, to_show = map(int, argv[1:3])

print(pipe(
    "E:/books/",
    walk,
    map(juxt(get(0), get(2))),
    mapcat(
        lambda x: pipe(
            x,
            get(1),
            map(lambda y: path.join(x[0], y)),
            map(juxt(identity, path.getsize)))),
    lambda xs: sorted(xs, key=get(1)),
    drop(to_drop),
    take(to_show),
    map(str),
    "\n".join))
