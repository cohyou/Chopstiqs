import System.IO
import Text.ParserCombinators.Parsec

data Briq = Int8 Integer | Text String | Smbl String | List [Briq]

data Cell = Cell String Briq Briq

data Annt = Annt String

newtype AnntList = AnntList { getList :: [Annt] }

data Aexp = Aexp AnntList Briq

instance Show Briq where
    show (Int8 i) = show i
    show (Text s) = "\"" ++ s ++ "\""
    show (Smbl s) = s
    show (List []) = ";"
    show (List (x:xs)) = "[" ++ show x ++ showG xs ++ "]"

showG [] = ""
showG (x:xs) = " " ++ show x ++ showG xs

instance Show Annt where
    show (Annt s) = "@" ++ s

instance Show AnntList where
    show (AnntList []) = ""
    show (AnntList (x:xs)) = show x ++ " " ++ show (AnntList xs)

instance Show Aexp where
    show (Aexp annot briq) = show annot ++ show briq

simple :: Parser Char
simple = letter

openClose :: Parser Char
openClose = do { char '('; char ')'}

parens :: Parser ()
parens = do
    char '('
    parens
    char ')'
    parens
    <|> return ()

-- testOr = string "(a)" <|> string "(b)"
{-
testOr1 = do
    char '('
    char 'a' <|> char 'b'
    char ')'
-}
-- testOr2 = try (string "(a)") <|> string "(b)"

testOr3 = do
    try (string "(a")
    char ')'
    return "(a)"
    <|> string "(b)"

nesting :: Parser Int
nesting = do
    char '('
    n <- nesting
    char ')'
    m <- nesting
    return (max (n+1) m)
    <|> return 0
{-
word :: Parser String
word = do
    c <- letter
    do
        cs <- word
        return (c:cs)
        <|> return [c]
-}

word :: Parser String
word = many1 letter

sentence :: Parser [String]
sentence = do
    words <- endBy1 word separator
    oneOf ".?!"
    return words

separator :: Parser ()
separator = skipMany1 (space <|> char ',')

smbl :: Parser Briq
smbl = do
    w1 <- many1 letter
    wt <- many alphaNum
    return (Smbl (w1++wt))

int8 :: Parser Briq
int8 = do
    i <- many1 digit
    return (Int8 (read i :: Integer))

list :: Parser [Briq]
list = sepEndBy briq spaces

text :: Parser Briq
text = do
    try (char '"')
    w <- many (noneOf "\"")
    char '"'
    return (Text w)

briq :: Parser Briq
briq = do
    spaces
    (do
        text <|> smbl <|> int8
        <|> do
            char '['
            spaces
            l <- list
            char ']'
            return (List l))

annt :: Parser Annt
annt = do
    char '@'
    w <- many alphaNum
    return (Annt w)

anntlist = do
    anntlist <- endBy annt spaces
    return (AnntList anntlist)

aexp :: Parser Aexp
aexp = do
    spaces
    al <- anntlist
    b <- briq
    return (Aexp al b)

main :: IO ()
main = do
    handle <- openFile "parse.iq" ReadMode
    text <- hGetContents handle
    print $ parse aexp "" text
