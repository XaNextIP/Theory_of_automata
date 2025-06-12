OPERATORS = set('.*|')
BRACKETS = set('()')

class TreeNode:
    def __init__(self):
        self.left, self.right, self.parent, self.value = None, None, None, None

    def create_left(self):
        self.left = TreeNode()
        self.left.parent = self
        return self.left

    def create_right(self):
        self.right = TreeNode()
        self.right.parent = self
        return self.right

    def create_parent(self):
        self.parent = TreeNode()
        self.parent.left = self
        return self.parent

    def __repr__(self):
        return str(self.value)

def construct_tree(regexp):
    root = TreeNode()
    current = root.create_left()

    alphabet = set(filter(lambda item: not item in OPERATORS | BRACKETS, regexp))
    concatenated_regex = get_concatenated_symbols_regex(regexp)

    for char in concatenated_regex:
        if char == '(':
            current = current.create_left()
            continue

        if char == ')':
            current = current.parent or current.create_parent()
            continue

        if char in alphabet:
            current.value = char
            current = current.parent or current.create_parent()
            continue

        if char in set('.|'):
            if current.value:
                current = current.create_parent()
            current.value = char
            current = current.create_right()
            continue

        if char == '*':
            if current.value:
                current = current.create_parent()
            current.value = char

    # Возвращаем корень дерева (подкорень после root)
    return root.left

def get_concatenated_symbols_regex(regexp):
    alphabet = set(filter(lambda item: not item in OPERATORS | BRACKETS, regexp))
    concatenated_regexp = str()

    for i, char in enumerate(regexp):
        concatenated_regexp += char
        if i + 1 < len(regexp) and regexp[i] in alphabet | set('*)') and regexp[i + 1] in alphabet | set('('):
            concatenated_regexp += '.'

    return concatenated_regexp

position_index = 1

def assign_tree_positions(root, pos_to_symbol):
    global position_index

    if root is None:
        return

    assign_tree_positions(root.left, pos_to_symbol)
    assign_tree_positions(root.right, pos_to_symbol)

    root.firstpos = set()
    root.lastpos = set()

    if root.value in OPERATORS:
        if root.value == '|':
            root.firstpos |= root.left.firstpos | root.right.firstpos
            root.lastpos |= root.left.lastpos | root.right.lastpos

        elif root.value == '.':
            if is_nullable(root.left):
                root.firstpos |= root.left.firstpos | root.right.firstpos
            else:
                root.firstpos |= root.left.firstpos

            if is_nullable(root.right):
                root.lastpos |= root.left.lastpos | root.right.lastpos
            else:
                root.lastpos |= root.right.lastpos

        elif root.value == '*':
            root.firstpos |= root.left.firstpos
            root.lastpos |= root.left.lastpos

    else:
        # Листовой узел — символ и позиция
        root.firstpos.add(position_index)
        root.lastpos.add(position_index)
        pos_to_symbol[position_index] = root.value
        position_index += 1

def is_nullable(node):
    if node is None:
        return True

    if node.value == '|':
        return is_nullable(node.left) or is_nullable(node.right)

    if node.value == '.':
        return is_nullable(node.left) and is_nullable(node.right)

    if node.value == '*':
        return True

    return False

def calculate_followpos(root, followpos):
    if root is None:
        return

    calculate_followpos(root.left, followpos)
    calculate_followpos(root.right, followpos)

    if root.value == '.':
        for position in root.left.lastpos:
            followpos[position - 1] |= root.right.firstpos

    if root.value == '*':
        for position in root.left.lastpos:
            followpos[position - 1] |= root.left.firstpos

def build_nfa(initial_positions, pos_to_symbol, followpos):
    final_states = []
    states = set()
    unhandled_states = set()

    unhandled_states.add(tuple(sorted(initial_positions)))

    while unhandled_states:
        current_state = unhandled_states.pop()
        if current_state not in states:
            for position in current_state:
                next_state = followpos[position - 1]
                if not next_state:
                    continue
                final_states.append((current_state, pos_to_symbol[position], tuple(sorted(next_state))))
                unhandled_states.add(tuple(sorted(next_state)))
            states.add(current_state)

    return states, final_states

if __name__ == '__main__':
    # Регулярное выражение, по которому строится НКА
    regular_expression = '(0|1)*01'
    regular_expression += '#'  # служебный символ конца выражения

    root_node = construct_tree(regular_expression)

    pos_to_symbol = dict()
    assign_tree_positions(root_node, pos_to_symbol)

    followpos_list = [set() for _ in range(len(pos_to_symbol))]
    calculate_followpos(root_node, followpos_list)

    automaton_states, automaton_transitions = build_nfa(root_node.firstpos, pos_to_symbol, followpos_list)

    print("Правила переходов для НКА:")
    for transition in automaton_transitions:
        current_state = ", ".join(map(str, transition[0]))
        next_state = ", ".join(map(str, transition[2]))
        symbol = transition[1]
        print(f"Из состояния {{{current_state}}} по символу '{symbol}' перейти в состояние {{{next_state}}}")
