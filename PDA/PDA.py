import csv

def read_csv(file_name):
    """
    Читает CSV файл с таблицей переходов автомата.
    Возвращает:
    - transitions: dict с ключами (state, input_symbol, stack_top) -> (new_state, stack_action)
    - start_state: начальное состояние автомата
    - accept_states: множество допускающих состояний
    """
    transitions = {}
    start_state = None
    accept_states = set()

    with open(file_name, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            if not row:
                continue
            key = row[0].strip()
            if key == '->':
                # Начальное состояние
                start_state = row[1].strip()
            elif key == '*':
                # Допускающие состояния
                accept_states.update(s.strip() for s in row[1:])
            elif key == 'abc':
                # Заголовок, пропускаем
                continue
            else:
                # Правило вида "state;input;stacktop", value "new_state;stack_action"
                # В файле это записано через запятую, поэтому соединяем и потом разделяем
                rule_key = key
                rule_value = row[1].strip() if len(row) > 1 else ''
                transitions[rule_key] = rule_value

    return transitions, start_state, accept_states

def update_stack(stack, action):
    """
    Обновляет стек автомата согласно действию.
    action - строка, символы которой заменяют верхушку стека
    'e' означает "пусто" (удалить символ без добавления)
    """
    if stack:
        stack.pop()
    for ch in reversed(action):
        if ch != 'e':
            stack.append(ch)

def process_input(transitions, start_state, accept_states, input_str):
    """
    Обрабатывает входную строку automaton с переходами transitions.
    """
    current_state = start_state
    stack = ['z']  # Начальный символ стека

    for i, symbol in enumerate(input_str):
        top = stack[-1] if stack else None
        rule_key = f"{current_state};{symbol};{top}"
        print(f"Обрабатываем символ '{symbol}', правило: {rule_key}")

        if rule_key not in transitions:
            print(f"Правило {rule_key} не найдено. Недопускающая цепочка.")
            return False

        # Получаем новое состояние и действие со стеком
        new_state, stack_action = transitions[rule_key].split(';')
        current_state = new_state
        update_stack(stack, stack_action)

        # Обрабатываем эпсилон-переходы (если есть)
        while True:
            top = stack[-1] if stack else None
            epsilon_rule = f"{current_state};e;{top}"
            if epsilon_rule in transitions:
                print(f"Эпсилон-переход: {epsilon_rule}")
                new_state, stack_action = transitions[epsilon_rule].split(';')
                current_state = new_state
                update_stack(stack, stack_action)
            else:
                break

    # После обработки всей строки проверяем состояние и стек
    if (not stack or stack == ['z']) and current_state in accept_states:
        print("Допускающая цепочка")
        return True
    else:
        print("Недопускающая цепочка")
        return False

if __name__ == "__main__":
    transitions, start_state, accept_states = read_csv("ww1.csv")
    user_input = input("Введите строку для проверки: ")
    process_input(transitions, start_state, accept_states, user_input)
