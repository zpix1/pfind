#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import product, islice, cycle, groupby, permutations
from collections import defaultdict, deque, Counter
import argparse

ncolors = None
connections = None
p = None
colors = None


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


def get_period(arr):
    larr = len(arr)
    for i in range(2, larr + 1):
        if larr % i == 0:
            for j in range(0, larr // i - 1):
                if arr[j*i+i:j*i+2*i] != arr[0:i]:
                    break
            else:
                return arr[0:i]


def shift(l, n):
    return list(islice(cycle(l), n, n+len(l)))


def normalize_lex(arr):
    n = len(arr)
    ans = arr
    for colors_perm in permutations(colors):
        t0 = list([colors_perm[c] for c in arr])
        for i in range(n):
            t = shift(t0, i)
            if t < ans:
                ans = t
        for i in range(n):
            t = shift(list(reversed(t0)), i)
            if t < ans:
                ans = t
    return ans


def normalize_color(arr):
    c = list(map(lambda e: e[0], sorted(Counter(arr).items(), key=lambda e: (e[1], e[0]), reverse=True)))
    return list(map(lambda x: c.index(x), arr))


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


def get_state_set(start_config):
    ans = set()
    for p_nh in product(colors, repeat=2*p):
        start_state = list(p_nh[:p]) + start_config + list(p_nh[p:])
        # color_states = list([get_color_state(start_state, p + start_config.index(i))
        #                      for i in colors])
        color_states = list([None for _ in colors])
        for i in range(len(start_config)):
            if color_states[start_config[i]] != None:
                if color_states[start_config[i]] != get_color_state(start_state, p + i):
                    break
            else:
                color_states[start_config[i]] = get_color_state(start_state, p + i)
        todo = deque()
        todo.append(start_state)
        idx = 0
        while len(todo) != 0:
            current = todo.popleft()
            ncurrent = len(current)
            if ncurrent > 2*p + len(start_config) and ncurrent % 2 == 0:
                if current[:ncurrent // 2] == current[ncurrent // 2:]:
                    if perfect_check(current):
                        to_add = current[:ncurrent // 2]
                        to_add_n = tuple(get_period(normalize_lex(normalize_color(to_add))))
                        ans.add(to_add_n)
                        break
            c = 0
            for new_color in colors:
                state = get_color_state(current + [new_color], ncurrent - p)
                if color_states[current[ncurrent - p]] == state:
                    c += 1
                    todo.append(current + [new_color])
            if c == 2:
                print('12312312')
            idx += 1
            # if len(todo) == 1:
            #     if len(todo[0]) > 1000:
            #         print(todo[0])
            #         break
    return ans

def print_bc_table(bc_table):
    lj = 3
    print('*'.ljust(lj), end='')
    for i in range(1, 7):
        print('{}'.format(i).ljust(lj), end='')
    print()
    for i in range(1, 7):
        print('{}'.format(i).ljust(lj), end='')
        for j in range(1, 7):
            if bc_table.get((j, i)):
                print('{}'.format(bc_table.get((j, i))).ljust(lj), end='')
            else:
                print('-'.ljust(lj), end='')
        print('')

def print_table(table):
    lj = 3
    print('*'.ljust(lj), end='')
    for i in range(len(table[0])):
        print('{}'.format(i).ljust(lj), end='')
    print()
    for i in range(len(table)):
        print('{}'.format(i).ljust(lj), end='')
        for j in range(len(table[i])):
            print('{}'.format(table[i][j]).ljust(lj), end='')
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--ncolors', type=int, default=2, help='number of colors')
    parser.add_argument('-c', '--connections', nargs='+', default=[1, 2, 4], type=int, help='array of connections')
    args = parser.parse_args()
    
    ncolors = args.ncolors
    connections = args.connections
    p = max(connections)
    colors = list(range(ncolors))

    print('ncolors={}'.format(ncolors))
    print('connections={}'.format(connections))
    start_configs = None
    if ncolors == 2:
        start_configs = [[0, 1]]
    elif ncolors == 3:
        start_configs = [[0] + [1] * n + [2] for n in range(1, 11)]
    else:
        print('invalid number of colors: {}'.format(ncolors))
        exit(1)

    state_set = set()

    for start_config in start_configs:
        state_set.update(get_state_set(start_config))

    state_list = list(state_set)
    state_list.sort(key=lambda s: (len(s), s))
    bc_table = defaultdict(int)
    for key, group in groupby(state_list, key=len):
        print('p={}'.format(key))
        for state in group:
            if not perfect_check(state):
                print('!!! CRITICAL BUG, COLORING IS NOT PERFECT !!!')
            table = []
            for color in colors:
                table.append(get_color_state(state, state.index(color), cycled=True))
            if ncolors == 2:
                b, c = table[0][1], table[1][0]
                print("({}, {})".format(b, c), state)
                bc_table[(b,c)] += 1
            else:
                print(state)
                print_table(table)
            
    if ncolors == 2:
        print('B/C Table')
        print_bc_table(bc_table)
    print('total={}'.format(len(state_list)))
   