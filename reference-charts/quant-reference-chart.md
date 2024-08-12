# Modern Quantifiers

All quantification expressions start with an operator used in the quantification, followed by a pair of angle brackets to delineate the scope of the expression enclosed. The first section within the quantifier is used to describe the range. This is followed by a right arrow after which comes the term.

## Operators

The operators used are:

|Operator|Description|
|-|-|
|$\land$|_and_ (_conjunction_)|
|$\lor$|_or_ (_disjunction_)|
|$+$|_addition_ (_summation_)|
|$\times$|_multiplication_ (_product_)|
|$\uparrow$|_maximum_|
|$\downarrow$|_minimum_|
|$\#$|_count_ (_cardinality_)|

In the following table, $A$ is the domain, $n$ represents its cardinality, and $i$ is from the index set $I_A$.

|<div style="width:200px">Example</div>|Description|
|-|-|
|$\land\langle 0\le i<n\rightarrow m\|A_i\rangle$|The _forall_ quantifier. Also known as the _universal_ quantification in logic. The conjunction symbol indicates the terms are related with the _and_ operator, so the term is boolean.<br/>The example states that every element of the set is divisible by $m$|
|$\lor\langle 0\le i<n\rightarrow A_i<0\rangle$|The _there exists_ quantifier. Also known as _existential_ quantification in logic. The disjunction symbol indicates the terms are related with the _or_ operator, so the term is boolean.<br/>The example states that some elements of the set are negative|
|$+\langle 0\le i<n\rightarrow A_i\times \alpha^i \rangle$|The _sum_ quantifier. Starts with an addition symbol, so the term is numeric.<br/>The example add every element of the set after multiplying it with a factor raised to the index|
|$\times\langle 0\le i<n\rightarrow x-i\rangle$|The _product_ quantifier. Starts with a multiplication symbol, so the term is numeric.<br/>The example is the falling factorial $x^{\underline{n}}$ which is $x(x-1)(x-2)\ldots(x-n+1)$|
|$\uparrow\langle 0\le i<n\rightarrow A_i\rangle$|The _maximum_ quantifier. Starts with an up arrow symbol, so the term is numeric.<br/>The example is the maximum of the set|
|$\downarrow\langle 0\le i<n\rightarrow A_i\rangle$|The _minimum_ quantifier. Starts with a down arrow symbol, so the term is numeric.<br/>The example is the minimum of the set|
|$\#\langle 0\le i<n\rightarrow A_i<0\rangle$<br/>$\#\langle x:int\rightarrow x\in A_i\rangle$|The _count_ quantifier. Starts with a _number of_ symbol, and the term is boolean: every _true_ case is represented with a 1, and every _false_ case is represented with a 0.<br/>The first example is the number of negative values in the set.<br/>The second example indicates that $A$ is a subset of integers, and is essentially the cardinality of the set|

## Range Definitions

Range definitions have to be valid mathematical expressions that denote membership in a set. The following table provides some typical examples.

|<div style="width:200px">Example</div>|Description|
|-|-|
|$\land\langle 0\le i<n\rightarrow A_i\le m\rangle$|The variable $i$ ranges between $0$ and $n$ with upper bound not inclusive|
|$+\langle k\rightarrow x\times{n\choose k}\rangle$|No range is specified for $k$ since by convention the "n choose k" expression is assumed to be zero for $k$ outside $0\ldots n$|
|$\#\langle v:int\rightarrow v\in f[p..q)\rangle$|The variable $v$ is an integer, and count quantifier returns 1 only if it is in the range of the function specified by $p$ and $q$|
|$+\langle 0\le d<n \land a\le x\le b\rightarrow x\rangle$|The sum of values in the $[0..n)$ range that are between $a$ and $b$|
|$\uparrow\langle x\in S\land d\ \|\ x\rightarrow x\rangle$|The largest of all values in $S$ that are divisible by $d$|

Quantifiers with _empty_ ranges return the following values by default:

|Quantifier|Default Result|
|-|-|
|$\land\langle\rightarrow\rangle$|$T$|
|$\lor\langle\rightarrow\rangle$|$F$|
|$+\langle\rightarrow\rangle$|$0$|
|$\times\langle\rightarrow\rangle$|$1$|
|$\uparrow\langle\rightarrow\rangle$|$-\infty$|
|$\downarrow\langle\rightarrow\rangle$|$+\infty$|
|$\#\langle\rightarrow\rangle$|$0$|

## Range Splitting

Quantifiers can be used inductively with terms of the same type. This is known as _range splitting_. The following table illustrates this use.

|Expression|After range split|
|-|-|
|$\land\langle 0\le i<n+1\rightarrow p.i\rangle$|$\land\langle 0\le i<n\rightarrow p.i\rangle\land p.n$|
|$\lor\langle 0\le i<n+1\rightarrow p.i\rangle$|$\lor\langle 0\le i<n\rightarrow p.i\rangle\lor p.n$|
|$+\langle 0\le i<n+1\rightarrow f.i\rangle$|$+\langle 0\le i<n\rightarrow f.i\rangle+p.n$|
|$\times\langle 0\le i<n+1\rightarrow f.i\rangle$|$\times\langle 0\le i<n\rightarrow f.i\rangle\times p.n$|
|$\uparrow\langle 0\le i<n+1\rightarrow f.i\rangle$|$\uparrow\langle 0\le i<n\rightarrow f.i\rangle\uparrow p.n$|
|$\downarrow\langle 0\le i<n+1\rightarrow f.i\rangle$|$\downarrow\langle 0\le i<n\rightarrow f.i\rangle\downarrow p.n$|

Quantifier ranges also have specific relations with their terms. Moving the range definition to the terms is known as _trading_.

|Expression|After trading|
|-|-|
|$\land\langle x\in S\rightarrow P(x)\rangle$|$\land\langle x\rightarrow x\in S\implies P(x)\rangle$|
|$\lor\langle x\in S\rightarrow P(x)\rangle$|$\lor\langle x\rightarrow x\in S\land P(x)\rangle$|
|$+\langle x\in S\rightarrow f(x)\rangle$|$+\langle x\rightarrow \#\langle y\in S\rightarrow y=x\rangle\times f(x)\rangle$|
