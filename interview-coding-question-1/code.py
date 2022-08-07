def iteration(l):
    search = list(l.keys())
    new_final = {}
    deleting_keys = []
    breaker = True
    for i in search:
        if breaker:
            for d in l.keys():
                if i[1] == d[0]:
                    value = l[i]
                    value = value - ((value * l[d]) / 100)
                    key = (i[0], d[1])
                    if key in l:
                        new_set_value = l[key]+value
                        new_final.update({key: new_set_value})
                    else:
                        new_final.update({key: value})
                    deleting_keys.append(d)
                    deleting_keys.append(i)
                    breaker = False
        if i not in new_final:
            new_final.update({i: l[i]})
    for key in deleting_keys:
        if key in new_final.keys():
            del new_final[key]
    return new_final


if __name__ == "__main__":
    l = {
        ('a', 'b'): 40,
        ('a', 'c'): 30,
        ('a', 'd'): 10,
        ('b', 'e'): 40,
        ('b', 'f'): 50,
        ('d', 'f'): 50,
        ('f', 'g'): 100,
        ('g', 'f'): 100,
    }
    i = 0
    while i < 10:
        l = iteration(l)
        i += 1
