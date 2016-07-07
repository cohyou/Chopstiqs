#! usr/bin/env python
def clear_color():
    print('\x1b[49m', end='')
    print('\x1b[39m', end='')

clear_color()

white = '\x1b[49m'

print(white + '\x1b[30m@\x1b[34m||' + white, end=' ')
# print(white + '\x1b[30m@\x1b[32m|>' + white, end=' ')
# print(white + '\x1b[30m@\x1b[31m[]' + white, end=' ')
clear_color()

inputed = input()
print(inputed)

clear_color()
