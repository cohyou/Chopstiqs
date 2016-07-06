# Chopstiqs
Programming language inspired by Lisp

## Traditional Lisp 'Cons Cell'

`:` makes cons cell.

```
> 1:2
1:2
```

We can get head of cons cell by using `#L`
and can get tail by using `#G`.
(You may have the question why we select 'L' & 'G'...neither 'car' & 'cdr' nor 'L'(left) & 'R'(right) nor 'H'(head) & 'T'(tail). Please imagine what 'L' & 'G' stands for...)

```
> #L 1:2
1
> #G 1:2
2
```

`^$` makes symbol AST cell, and you can `#L` and `#G` them. You can use symbol by writing only name of it (please see last example below). If you are familiar with other Lisps, note that symbol is NOT 'eval'ed. Symbol is still symbol on REPL result.

```
> ^$ "a":1
^<SMBL "a":1>

> #L ^$ "a":1
"a"

> #G ^$ "a":1
1

> a
^<SMBL "a":>
```

`^\` makes lambda AST cell. L of it is symbol, and G of it is body of lambda.

```
> ^\ x:x
^<FUNC x -> x>

> #L ^\ x:x
^<SMBL "x">

> #G ^\ x:x
^<SMBL "x">
```

`^N` bevaves like 'NULL', 'nil', 'null' for other languages.
Chopstiqs call this 'none'.
L of N is N, and also G of N is N.
You can use `N` instead of `^N`.

```
> ^N
N

> N
N

> #L ^N
N

> #G ^N
N
```

`^F` means false.
L of F is N, and also G of F is itself.
You can use `F` instead of `^F`.

```
> ^F
F

> F
F

> #L ^F
N

> #G ^F
F
```

`^T` means true.
L of T is itself, and also G of T is N
(this is the opposite behavior to F).
You can use `T` instead of `^T`.

```
> ^T
T

> T
T

> #L ^T
T

> #G ^T
N
```

You can make tuple AST cell by `^*`. Instead of `^*`, you can use `{` & `}`. See examples below.

```
> ^* 1:(^* N:N)
{1}

> {1 2}
{1 2}
```

As you expected, you can make nested tuple AST cell by multiple using of `:`.

```
> ^* 1:(^* 2:(^* "a":(^* N:N)))
{1 2 "a"}
```

Empty tuple is `{}`. This equals `^* N:N`.

```
> ^* N:N
{}

> {}
{}
```

## List and Record
Like other Lisps, list consist of cons cells.
You can use `;` or `[]` for empty list instead of `N:N`.
```
> N:N
[]

> ;
;

> []
[]

> 1:2:3:4:5:[]
[1 2 3 4 5]
```

Record looks like tuple that have child cons cells.

```
> {a:1 b:2 c:3}
{a:1 b:2 c:3}

> #L {a:1 b:2 c:3}
a:1

> #G {a:1 b:2 c:3}
{b:2 c:3}

> ^* (a:1):(^* (b:2):(^* (c:3):{}))
{a:1 b:2 c:3}
```

## Condition
Condition cons cell begins with `^?`.
L of it is condition, T or F.
G of it is 'return value' cons cell.
You may already understand,
L of 'return value cons cell' is value for T,
G of 'return value cons cell' is value for F.

```
> ^? F:("That's T!":"That's F!")
"That's F!"

```
