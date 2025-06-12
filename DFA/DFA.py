import csv

def dfa(transitions, start_state, input_str):
    current_state = start_state
    accepting_states = {state for (_, _, state) in transitions if '*' in state}

    for i, symbol in enumerate(input_str):
        key = (current_state, symbol)
        if key in transitions:
            current_state = transitions[key]
            print(f"Шаг {i+1}: символ '{symbol}' → состояние '{current_state}'")
        else:
            print(f"Ошибка: нет перехода из состояния '{current_state}' по символу '{symbol}'")
            print("Цепочка НЕ допускается.")
            return

    if current_state in accepting_states:
        print(f"Конечное состояние '{current_state}' допускающее. Цепочка ДОПУСКАЕТСЯ.")
    else:
        print(f"Конечное состояние '{current_state}' не допускающее. Цепочка НЕ допускается.")

if __name__ == '__main__':
    transitions = {}

    with open('DFA.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row) != 3:
                continue  # пропускаем некорректные строки
            src, symbol, dest = row
            transitions[(src, symbol)] = dest

    print("Таблица переходов:")
    for key, val in transitions.items():
        print(f"{key} -> {val}")

    input_str = input("Введите цепочку значений: ")
    dfa(transitions, start_state='A', input_str=input_str)
