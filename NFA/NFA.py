import csv

def epsilon_closure(table, states):
    """Возвращает множество состояний, достижимых по ε-переходам"""
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        epsilon_states = table[state][2]
        for eps in epsilon_states:
            if eps not in closure:
                closure.add(eps)
                stack.append(eps)
    return closure

def nfa(table, start, STR):
    admitting_states = {s for s in table if '*' in s}
    
    current_states = epsilon_closure(table, start)
    print(f"Стартовые состояния: {current_states}")

    for char in STR:
        next_states = set()
        for state in current_states:
            if char == '0':
                next_states.update(table[state][0])
            elif char == '1':
                next_states.update(table[state][1])
        current_states = epsilon_closure(table, next_states)
        print(f"После символа '{char}' состояния: {current_states}")

    if any(s in admitting_states for s in current_states):
        print(f"Цепочка '{STR}' ДОПУСКАЕТСЯ.")
    else:
        print(f"Цепочка '{STR}' НЕ допускается.")

if __name__ == '__main__':
    with open("NFA.csv", encoding='utf-8') as rfd:
        file_read = csv.reader(rfd, delimiter=";")
        NFA = {}

        for row in file_read:
            state = row[0]
            transitions = []
            for i in range(1, 4):  # 0, 1, ε
                if i < len(row) and row[i]:
                    transitions.append(set(row[i].split('-')))
                else:
                    transitions.append(set())
            NFA[state] = transitions

    print("Таблица NFA:")
    for k, v in NFA.items():
        print(k, "=>", v)

    STR = input("Введите цепочку значений: ")
    nfa(NFA, {'q0'}, STR)
