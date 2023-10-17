import traceback

def recurse(i):
    if i > 0:
        recurse(i-1)
    b = 2
    here = True
    1/0
    b += 1
    here

try:
    a = 1
    recurse(5)
except Exception as ex:
    for tb, i in list(traceback.walk_tb(ex.__traceback__))[::-1]:
        print(tb.f_locals.get("here"))
    # print(ex)
    pass
