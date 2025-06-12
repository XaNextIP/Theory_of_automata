import csv

def turing_machine(table, start, tape_str):
    tape = list(tape_str)
    i = 0
    state = start

    # Добавим пустой символ, если требуется
    if i >= len(tape):
        tape.append('B')
    if i < 0:
        tape.insert(0, 'B')
        i = 0

    admitting_states = [s for s in table if '*' in s]
    accepting = any('*' in state for state in table)

    print("Начальная лента:", ''.join(tape))

    while True:
        symbol = tape[i] if i < len(tape) else 'B'
        transitions = table.get(state, {})
        action = transitions.get(symbol)

        if not action:
            break

        new_state, new_symbol, direction = action
        tape[i] = new_symbol
        state = new_state

        if direction == 'R':
            i += 1
            if i >= len(tape):
                tape.append('B')
        elif direction == 'L':
            i -= 1
            if i < 0:
                tape.insert(0, 'B')
                i = 0
        else:
            print(f"Неверное направление: {direction}")
            break

        print(f"Состояние: {state}, Лента: {''.join(tape)}")

    if any(adm in state for adm in admitting_states):
        print("Цепочка допускается.")
    else:
        print("Цепочка НЕ допускается.")

def read_turing_table(filename):
    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        table = {}
        symbols = ['0', '1', 'X', 'Y', 'B']

        for row in reader:
            state = row[0]
            transitions = {}
            for idx, cell in enumerate(row[1:]):
                if cell:
                    parts = cell.split('-')
                    if len(parts) == 3:
                        transitions[symbols[idx]] = tuple(parts)
            table[state] = transitions
    return table

if __name__ == '__main__':
    table = read_turing_table('Turing.csv')
    print("Таблица переходов:")
    for state, rules in table.items():
        print(state, ":", rules)

    tape_str = input("Введите цепочку значений: ")
    turing_machine(table, 'q0', tape_str)
