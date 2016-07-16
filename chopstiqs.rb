line = STDIN.readline

line.each_char do |c|
    if c =~ /[a-zA-z]/
        puts 'alpha'
    else
        puts 'not alpha'
    end
end

print line
