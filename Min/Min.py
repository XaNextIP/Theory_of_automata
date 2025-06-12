import csv

def gen(lst):
    new = []
    for i in range(len(lst)):
        for y in range(i+1, len(lst)):
            new.append(lst[i] + lst[y])
    return new

def update(DFA, pair):
    # Разделяем пару состояний на компоненты
    if len(pair) == 4:
        pair = list(pair)
        pair[0] += '*'
        pair[1] = pair[2] + '*'
        pair.pop(3)
        pair.pop(2)

    first = DFA[pair[0]][0] + DFA[pair[1]][0]
    second = DFA[pair[0]][1] + DFA[pair[1]][1]

    pervay = ''.join(DFA[pair[0]][0])
    vtoray = ''.join(DFA[pair[0]][1])

    if first.count(pervay) == 1:
        first = ''.join(first)
        if second.count(vtoray) == 1:
            second = ''.join(second)
            del DFA[pair[0]]
            del DFA[pair[1]]
            new_key = ''.join(pair)
            DFA[new_key] = [[first], [second]]
        else:
            del DFA[pair[0]]
            del DFA[pair[1]]
            new_key = ''.join(pair)
            DFA[new_key] = [[first], [second[0]]]
    else:
        if second.count(vtoray) == 1:
            second = ''.join(second)
            del DFA[pair[0]]
            del DFA[pair[1]]
            new_key = ''.join(pair)
            DFA[new_key] = [[first[0]], [second]]
        else:
            del DFA[pair[0]]
            del DFA[pair[1]]
            new_key = ''.join(pair)
            DFA[new_key] = [[first[0]], [second[0]]]

def up(DFA):
    print("Обновленный DFA:")
    for state in DFA:
        try:
            _ = DFA[DFA[state][0][0]]
        except KeyError:
            for key in DFA:
                if DFA[state][0][0] in key:
                    DFA[state][0] = [key]
        try:
            _ = DFA[DFA[state][1][0]]
        except KeyError:
            for key in DFA:
                if DFA[state][1][0] in key:
                    DFA[state][1] = [key]
    print(DFA)

def read():
    with open("DFA.csv", encoding='utf-8') as rfd:
        reader = csv.reader(rfd, delimiter=";")
        DFA = {}
        for row in reader:
            DFA[row[0]] = []
            for i in range(1, len(row)):
                if row[i] == "":
                    DFA[row[0]].append([])
                else:
                    DFA[row[0]].append(row[i].split(','))
    return DFA

def write(DFA):
    with open('DFA1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for i in DFA:
            writer.writerow([i, DFA[i][0][0], DFA[i][1][0]])

if __name__ == '__main__':
    DFA = read()
    print("Исходный DFA:", DFA)

    condition = {}
    admitting_value = [state for state in DFA if '*' in state]
    matrix = list(DFA.keys())
    new = gen(matrix)

    if len(admitting_value) == 1:
        for i in new:
            if admitting_value[0] in i:
                condition[i] = 'D'
            else:
                condition[i] = 'I'
    elif len(admitting_value) == 2:
        for i in new:
            if admitting_value[0] in i and admitting_value[1] in i:
                condition[i] = 'I'
            elif admitting_value[0] in i or admitting_value[1] in i:
                condition[i] = 'D'
            else:
                condition[i] = 'I'
    else:
        for i in new:
            if (admitting_value[0] in i and admitting_value[1] in i) or \
               (admitting_value[0] in i and admitting_value[2] in i) or \
               (admitting_value[1] in i and admitting_value[2] in i):
                condition[i] = 'I'
            elif admitting_value[0] in i or admitting_value[1] in i or admitting_value[2] in i:
                condition[i] = 'D'
            else:
                condition[i] = 'I'

    Run = True
    y = 0
    while Run:
        y += 1
        for i in new:
            if condition[i] == 'D':
                continue
            paw = list(i)
            if len(paw) == 4:
                paw[0] += '*'
                paw[1] = paw[2] + '*'
                paw.pop(3)
                paw.pop(2)

            first = DFA[paw[0]][0] + DFA[paw[1]][0]
            second = DFA[paw[0]][1] + DFA[paw[1]][1]

            if first.count(first[0]) == 1:
                retr = ''.join(first)
                try:
                    if condition[retr] == 'D':
                        condition[i] = 'D'
                except KeyError:
                    first[0], first[1] = first[1], first[0]
                    retr = ''.join(first)
                    if condition.get(retr) == 'D':
                        condition[i] = 'D'

            if second.count(second[0]) == 1:
                retr = ''.join(second)
                try:
                    if condition[retr] == 'D':
                        condition[i] = 'D'
                except KeyError:
                    second[0], second[1] = second[1], second[0]
                    retr = ''.join(second)
                    if condition.get(retr) == 'D':
                        condition[i] = 'D'

        if y == 2:
            Run = False

    print("Условия различимости:", condition)
    for i in condition:
        if condition[i] == 'D':
            continue
        update(DFA, i)

    up(DFA)

    write(DFA)
