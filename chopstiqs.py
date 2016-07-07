#! usr/bin/env python

def clear_color():
    print('\x1b[49m', end='')
    print('\x1b[39m', end='')

class Tokn:
    pass

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

    output = '('
    for c in inputed:
        if c == ' ':
            output += ') ('
        else:
            output += c

    output += ')'

    b = Briq()

    print(output + ' ' + repr(b))

    clear_color()
