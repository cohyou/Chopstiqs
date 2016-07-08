#! usr/bin/env python

def clear_color():
    print('\x1b[49m', end='')
    print('\x1b[39m', end='')

class Tokn:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '^[TOKN "' + self.name + '"]'


class Briq:
    def __init__(self):
        self.type = 'type'
        self.mark = ''
        self.lval = ''
        self.gval = ''

    def __repr__(self):
        return '^[' + self.mark + ' ' + self.lval + ':' + self.gval + ']'

white = '\x1b[49m'
black_forecolor = '\x1b[30m'

def is_alpha(c):
    return ord(c) in range(65, 90) or ord(c) in range(97, 122)

def is_whitespace(c):
    return c in [' ', '\t', '\n']

def is_cell_prefix(c):
    return c == '^'

def is_annot_prefix(c):
    return c in ['@', '%', '!', '$', '?', '\\', '#']

print('itadakimasu!')

while True:
    clear_color()
    print(white + black_forecolor + '@@\x1b[34m||' + white, end=' ')
    # print(white + black_forecolor + '\x1b[30m@@\x1b[32m|>' + white, end=' ')
    # print(white + black_forecolor + '\x1b[30m@@\x1b[31m[]' + white, end=' ')
    clear_color()

    inputed = input()

    if inputed in ['@@[]', 'gochi', '@@@', '@@quit', 'gochidesu']:
        print('gochisosama!')
        break

    if is_alpha(inputed[0]):
        print('alphabet!')
        continue

    tokens = inputed.split()
    token_instances = []
    for t in tokens:
        token_instances.append(Tokn(t))

    output = ''

    b = Briq()

    print(repr(token_instances))

    clear_color()
