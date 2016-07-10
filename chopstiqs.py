#! usr/bin/env python

# Lexer

TOKN_EOF = -1

TOKN_MARK = 1
TOKN_LLST = 3
TOKN_RLST = 4
TOKN_SMBL = 5
TOKN_DBQT = 6
TOKN_TEXT = 7
TOKN_DIGT = 8

TOKN_ANNT = 16 # @
TOKN_ENVR = 17 # %
TOKN_APLY = 18 # !
TOKN_CTXT = 19 # $
TOKN_COND = 20 # ?
TOKN_SQTP = 21 # \
TOKN_RETN = 22 # #

TOKN_CONS = 23 # :
TOKN_CONS_CNTT = 24

TOKN_LDCT = 64 # {
TOKN_RDCT = 65 # }
TOKN_LPRN = 66 # (_
TOKN_RPRN = 67 # )

TOKN_UNIT = 68 # ;

class Tokn:
    def __init__(self, tp, name):
        self.tp = tp
        self.name = name

    def __repr__(self):
        tokn_names = {
            TOKN_EOF:'eof',

            TOKN_MARK:'mark',
            TOKN_LLST:'l_list',
            TOKN_RLST:'r_list',
            TOKN_SMBL:'symbol',
            TOKN_DBQT:'double quote',
            TOKN_TEXT:'text',
            TOKN_DIGT:'digit',

            TOKN_ANNT:'annotation',
            TOKN_ENVR:'environment',
            TOKN_APLY:'application',
            TOKN_CTXT:'context',
            TOKN_COND:'condition',
            TOKN_SQTP:'seq_type',
            TOKN_RETN:'return_value',

            TOKN_CONS:'cons',
            TOKN_CONS_CNTT:'cons_content',

            TOKN_LDCT:'l_dict',
            TOKN_RDCT:'r_dict',
            TOKN_LPRN:'l_paren',
            TOKN_RPRN:'r_paren',

            TOKN_UNIT:'unit'}

        return tokn_names[self.tp] + '<' + self.name + '>'

class Lexer:
    STATE_NORMAL = 0
    STATE_STRSTT = 1
    STATE_STREND = 2
    STATE_CNSSMB = 3
    STATE_ANNTNM = 4
    STATE_CNSSTT = 5
    STATE_CNSEND = 6
    STATE_MRKSTT = 7

    STATE_LSTSTT = 16
    STATE_LSTEND = 17
    STATE_DCTSTT = 18
    STATE_DCTEND = 19
    STATE_PRNSTT = 20
    STATE_PRNEND = 21

    STATE_UNTDLM = 22

    idx = 0
    c = ''
    state = STATE_NORMAL

    def __init__(self, inputed):
        self.inputed = inputed
        self.c = inputed[self.idx]

    def consume(self):
        self.idx += 1
        if self.idx >= len(self.inputed):
            self.c = ''
        else:
            self.c = self.inputed[self.idx]

    def is_whitespace(self, c):
        return c in [' ', '\t', '\n', '']

    def consume_whitespace(self):
        while self.is_whitespace(self.c):
            if self.c == '': break
            self.consume()

    def is_alpha(self, c):
        if len(c) == 0: return False
        return ord(c) in range(65, 90) or ord(c) in range(97, 122)

    def is_digit(self, c):
        if len(c) != 1: return False
        return ord(c) in range(48, 57)

    def scan_digit(self):
        digit_content = ''
        while self.is_digit(self.c):
            digit_content += self.c
            self.consume()
        return Tokn(TOKN_DIGT, digit_content)

    def scan_string(self):
        string_content = ''
        while self.c != '"':
            string_content += self.c
            self.consume()
        self.state = self.STATE_STREND
        return Tokn(TOKN_TEXT, string_content)

    def is_delimiter(self):
        return self.c in ['[', ']', '{', '}', '(', ')', ';']

    def scan_delim(self):
        c = self.c
        tokn_type_dict = {
            '[':TOKN_LLST,
            ']':TOKN_RLST,
            '{':TOKN_LDCT,
            '}':TOKN_RDCT,
            '(':TOKN_LPRN,
            ')':TOKN_RPRN,
            ';':TOKN_UNIT}
        t = tokn_type_dict[self.c]
        self.change_state_delim()
        self.consume()
        return Tokn(t, c)

    def change_state_delim(self):
        state_dict = {
            '[':self.STATE_LSTSTT,
            ']':self.STATE_LSTEND,
            '{':self.STATE_DCTSTT,
            '}':self.STATE_DCTEND,
            '(':self.STATE_PRNSTT,
            ')':self.STATE_PRNEND,
            ';':self.STATE_UNTDLM}
        self.state = state_dict[self.c]

    def scan_mark_name(self):
        symbol_name = ''
        while not self.is_whitespace(self.c):
            if self.is_delimiter():
                self.change_state_delim()
                break
            else:
                symbol_name += self.c
            self.consume()
        return Tokn(TOKN_SMBL, symbol_name)

    def scan_annotation_name(self):
        symbol_name = ''
        while not self.is_whitespace(self.c):
            if self.is_delimiter():
                self.change_state_delim()
                break
            else:
                symbol_name += self.c
            self.consume()
        return Tokn(TOKN_SMBL, symbol_name)

    def scan_cons_content(self):
        symbol_name = ''
        while not self.is_whitespace(self.c):
            if self.c == ':':
                self.state = self.STATE_CNSSTT
                return Tokn(TOKN_CONS_CNTT, symbol_name)
            elif self.is_delimiter():
                self.change_state_delim()
                break
            else:
                symbol_name += self.c
            self.consume()
        return Tokn(TOKN_CONS_CNTT, symbol_name)

    def scan_symbol(self):
        symbol_name = ''
        while not self.is_whitespace(self.c):
            if self.c == ':':
                self.state = self.STATE_CNSSTT
                return Tokn(TOKN_SMBL, symbol_name)
            elif self.is_delimiter():
                self.change_state_delim()
                break
            else:
                symbol_name += self.c
            self.consume()
        return Tokn(TOKN_SMBL, symbol_name)

    def next_token(self):
        while self.c != '':
            # print('c: %s' % self.c)
            if self.state == self.STATE_NORMAL:
                if self.is_whitespace(self.c):
                    self.consume_whitespace()
                elif self.c == '^':
                    self.consume()
                    self.state = self.STATE_MRKSTT
                    return Tokn(TOKN_MARK, '^')
                elif self.c == '"':
                    self.consume()
                    self.state = self.STATE_STRSTT
                    return Tokn(TOKN_DBQT, '"')
                elif self.is_digit(self.c):
                    if self.idx+1 < len(self.inputed) and self.inputed[self.idx+1] == ':':
                        self.state = self.STATE_CNSSTT
                    return self.scan_digit()
                elif self.c in ['@', '%', '!', '$', '?', '\\', '#']:
                    tokn_type_dict = {
                        '@' :TOKN_ANNT,
                        '%' :TOKN_ENVR,
                        '!' :TOKN_APLY,
                        '$' :TOKN_CTXT,
                        '?' :TOKN_COND,
                        '\\':TOKN_SQTP,
                        '#' :TOKN_RETN}
                    t = tokn_type_dict[self.c]
                    c = self.c
                    self.consume()
                    self.state = self.STATE_ANNTNM
                    return Tokn(t, c)
                elif self.c == ':':
                    self.state = self.STATE_CNSSTT
                    # self.consume()
                    return Tokn(TOKN_CONS_CNTT, '')
                elif self.is_delimiter():
                    return self.scan_delim()
                else:
                    if self.is_alpha(self.c):
                        return self.scan_symbol()
                    else:
                        print('scan error: %s' % self.c)
                        break
            elif self.state == self.STATE_MRKSTT:
                self.state = self.STATE_NORMAL
                return self.scan_mark_name()
            elif self.state == self.STATE_STRSTT:
                return self.scan_string()
            elif self.state == self.STATE_STREND:
                if self.idx+1 < len(self.inputed) and self.inputed[self.idx+1] == ':':
                    self.state = self.STATE_CNSSTT
                else:
                    self.state = self.STATE_NORMAL
                self.consume()
                return Tokn(TOKN_DBQT, '"')
            elif self.state == self.STATE_ANNTNM:
                self.state = self.STATE_NORMAL
                return self.scan_annotation_name()
            elif self.state == self.STATE_CNSSTT:
                self.consume()
                self.state = self.STATE_CNSEND
                return Tokn(TOKN_CONS, ':')
            elif self.state == self.STATE_CNSEND:
                self.state = self.STATE_NORMAL
                if self.is_whitespace(self.c):
                    return Tokn(TOKN_CONS_CNTT, '')
                elif self.c in [']', '}', ')', ';']:
                    return Tokn(TOKN_CONS_CNTT, '')
                # return self.scan_cons_content()
            elif self.state in [self.STATE_LSTSTT, self.STATE_LSTEND,
                                self.STATE_DCTSTT, self.STATE_DCTEND,
                                self.STATE_PRNSTT, self.STATE_PRNEND,
                                self.STATE_UNTDLM]:

                # cons(:) is valid for no whitespaces
                if self.state in [self.STATE_LSTEND, self.STATE_DCTEND,
                                  self.STATE_PRNEND, self.STATE_UNTDLM]:
                    if self.c == ':':
                        self.state = self.STATE_CNSSTT
                    else:
                        self.state = self.STATE_NORMAL
                else:
                    self.state = self.STATE_NORMAL
                    if self.is_delimiter():
                        return self.scan_delim()
            else:
                print('invalid state!')
                break
        if self.state == self.STATE_CNSEND:
            self.state = self.STATE_NORMAL
            return Tokn(TOKN_CONS_CNTT, '')
        else:
            return Tokn(TOKN_EOF, '<eof>')


# Parser

class Parser:
    def __init__(self, input_str):
        self.inputed = input_str

    def scan(self):
        lexer = Lexer(self.inputed)
        tokn = lexer.next_token()
        while tokn.tp != TOKN_EOF:
            print(tokn)
            tokn = lexer.next_token()
        print(tokn)


# REPL

WHITE = '\x1b[49m'
BLACK_FORECOLOR = '\x1b[30m'

def clear_color():
    print(WHITE, end='')
    print('\x1b[39m', end='')


while True:
    clear_color()
    print(WHITE + BLACK_FORECOLOR + '@@\x1b[34m||' + WHITE, end=' ')
    # print(WHITE + BLACK_FORECOLOR + '\x1b[30m@@\x1b[32m|>' + WHITE, end=' ')
    # print(WHITE + BLACK_FORECOLOR + '\x1b[30m@@\x1b[31m[]' + WHITE, end=' ')
    clear_color()

    inputed = input()

    if inputed in ['@@[]', 'gochi', '@@@', '@@quit', 'gochidesu']:
        print('gochisosama!')
        break

    parser = Parser(inputed)
    parser.scan()

"""
class Briq:
    def __init__(self):
        self.type = 'type'
        self.mark = ''
        self.lval = ''
        self.gval = ''

    def __repr__(self):
        return '^[' + self.mark + ' ' + self.lval + ':' + self.gval + ']'
"""
