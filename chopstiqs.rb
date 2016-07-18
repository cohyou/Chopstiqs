puts 'itadakimasu!'

class Lexer
    def initialize(input)
        @idx = 0
        @input = input
        @c = input[@idx] if not input.empty?
    end

    def consume
        @idx++
        @c = @input[@idx]
    end

    def next_token
        while @c != '\n'
            case @c
            when '"'
                puts 'orororo'
            else
                puts 'other'
            end
            break
        end
    end
end

while true
    print '@|| '
    line = STDIN.readline

    lexer = Lexer.new(line)
    lexer.next_token

    line.each_char do |c|
        if c =~ /[a-zA-z]/
            puts 'alpha'
        else
            puts 'not alpha'
        end
    end

    if line == "@@@\n"
        puts 'gochisosama!'
        break
    else
        print line
    end
end
