# Chopstiqs
Programming language inspired by Lisp

## Traditional Lisp 'Cons Cell'

`:` makes cons cell.

```
> 1:2
1:2
```

We can get head of cons cell by using `#L`
and get tail by using `#G`.
(You may have the question why we select 'L' & 'G'...neither 'car' & 'cdr' nor 'L'(left) & 'R'(right) nor 'H'(head) & 'T'(tail). Please imagine what 'L' & 'G' stands for...)

```
> #L 1:2
1
> #G 1:2
2
```

`^$` makes symbol AST cell, and you can `#L` and `#G` them. You can use symbol by writing only name of it (please see last example below). If you are familiar with other Lisps, note that symbol is NOT evaluated. Symbol is still symbol on REPL result.

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
