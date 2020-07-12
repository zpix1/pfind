from itertools import product, islice, cycle
from collections import defaultdict, deque

ncolors = 2
connections = [1, 2, 4]

p = max(connections)
start_config = [0, 1]

colors = list(range(ncolors))


def get_color_state(arr, i, cycled=False):
    color_state = list([0 for _ in colors])
    if cycled:
        n = len(arr)
        for conn in connections:
            color_state[arr[(i + conn) % n]] += 1
            color_state[arr[(i - conn) % n]] += 1
    else:
        for conn in connections:
            color_state[arr[i + conn]] += 1
            color_state[arr[i - conn]] += 1
    return color_state


def shift(l, n):
    return list(islice(cycle(l), n, n+len(l)))


def normalize_lex(arr):
    n = len(arr)
    ans = arr
    for i in range(n):
        t = shift(arr, i)
        if t < ans:
            ans = t
    for i in range(n):
        t = shift(list(reversed(ans)), i)
        if t < ans:
            ans = t
    return ans


def normalize_color(arr):
    c0count = arr.count(0)
    c1count = arr.count(1)
    c0 = 0
    if c0count <= c1count:
        c0 = 1
    return list(map(lambda x: 0 if x == c0 else 1, arr))


def perfect_check(arr):
    color_states = list([None for _ in colors])
    for i in range(len(arr)):
        state = get_color_state(arr, i, cycled=True)
        if color_states[arr[i]] != None:
            if color_states[arr[i]] != state:
                return False
        else:
            color_states[arr[i]] = state
    return True


def get_state_set():
    ans = set()
    for p_nh in product(colors, repeat=2*p):
        start_state = list(p_nh[:p]) + start_config + list(p_nh[p:])
        color_states = list([get_color_state(start_state, p + i)
                             for i in range(len(start_config))])
        todo = deque()
        todo.append(start_state)
        idx = 0
        while len(todo) != 0:
            # print(len(todo))
            current = todo.popleft()

            ncurrent = len(current)

            if ncurrent > 2*p + len(start_config) and ncurrent % 2 == 0:
                if current[:ncurrent // 2] == current[ncurrent // 2:]:
                    if perfect_check(current):
                        to_add = current[:ncurrent // 2]
                        to_add_n = tuple(normalize_lex(normalize_color(to_add)))
                        if to_add_n == (0, 0, 0, 0, 1, 1):
                            print('to_add', to_add)
                            print('cur', current)
                        ans.add(to_add_n)
                        break

            for new_color in colors:
                state = get_color_state(current + [new_color], ncurrent - p)
                if color_states[current[ncurrent - p]] == state:
                    todo.append(current + [new_color])
            idx += 1
    return ans

def print_bc_table(bc_table):
    print('* ', end='')
    for i in range(1, 7):
        print('{} '.format(i), end='')
    print()
    for i in range(1, 7):
        print('{} '.format(i), end='')
        for j in range(1, 7):
            if bc_table.get((j, i)):
                print('{} '.format(bc_table.get((j, i))), end='')
            else:
                print('- ', end='')
        print('')


if __name__ == "__main__":
    state_list = list(get_state_set())
    state_list.sort(key=lambda s: (len(s), s))
    bc_table = defaultdict(int)
    for state in state_list:
        table = []
        for color in colors:
            table.append(get_color_state(state, state.index(color), cycled=True))
        b, c = table[0][1], table[1][0]
        bc_table[(b,c)] += 1
        print("({}, {})".format(b, c), state)

    print_bc_table(bc_table)
   