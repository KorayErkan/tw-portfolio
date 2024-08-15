# Modern Quantifiers

## Basic Syntax

All quantification expressions have an operator at the start used between the elements pairwise, and a pair of angle brackets delineating the scope of the expressions enclosed. The first section within the quantifier is used to describe the range. This is followed by a right arrow after which comes the term.

$$<operator> \langle <range-definition> \rightarrow <term> \rangle$$

Quantifiers should be inductively valid forms of expanded expressions such as

$$1+\frac{1}{x}+\frac{1}{x^2}+\ldots+\frac{1}{x^n}$$

or

$$P(x_0)\land P(x_1)\land\ldots\land P(x_{n-1})$$

## The Operators

The operators that can be used for quantification are:

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

|<div style="width:250px">Example</div>|Description|
|-|-|
|$\land\langle 0\le i<n\rightarrow A_i\le m\rangle$|The variable $i$ ranges between $0$ and $n$ with upper bound not inclusive|
|$+\langle k\rightarrow x\times{n\choose k}\rangle$|No range is specified for $k$ since by convention the "n choose k" expression is assumed to be zero for $k$ outside $0\ldots n$|
|$\#\langle v:int\rightarrow v\in f[p..q)\rangle$|The variable $v$ is an integer, and count quantifier returns 1 only if it is in the range of the function specified by $p$ and $q$|
|$+\langle 0\le d<n \land a\le x\le b\rightarrow x\rangle$|The sum of values in the $[0..n)$ range that are between $a$ and $b$|
|$\uparrow\langle x\in S\land d\ \|\ x\rightarrow x\rangle$|The largest of all values in $S$ that are divisible by $d$|

## Empty Range

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

## Merging and Splitting Ranges

Multiple quantifiers of the same type can be merged if their ranges are adjusted accordingly. This is known as _range merging_, and merging the ranges is done with the following rules.

|Qauntifiers|After range merging|
|-|-|
|$\land\langle x\in S\rightarrow P(x)\rangle\land\land\langle x\in T\rightarrow P(x)\rangle$|$\land\langle x\in S\cup T\rightarrow P(x)\rangle$<br/>$\land\langle x\in S\lor x\in T\rightarrow P(x)$|
|$\land\langle x\in S\rightarrow P(x)\rangle\lor\land\langle x\in T\rightarrow P(x)\rangle$|$\land\langle x\in S\cap T\rightarrow P(x)\rangle$<br/>$\land\langle x\in S\land x\in T\rightarrow P(x)$|
|$\lor\langle x\in S\rightarrow P(x)\rangle\lor\lor\langle x\in T\rightarrow P(x)\rangle$|$\lor\langle x\in S\cup T\rightarrow P(x)\rangle$<br/>$\lor\langle x\in S\lor x\in T\rightarrow P(x)$|
|$\lor\langle x\in S\rightarrow P(x)\rangle\land\lor\langle x\in T\rightarrow P(x)\rangle$|$\lor\langle x\in S\cap T\rightarrow P(x)\rangle$<br/>$\lor\langle x\in S\land x\in T\rightarrow P(x)$|
|$+\langle x\in S\rightarrow f(x)\rangle++\langle x\in T\rightarrow f(x)\rangle$|$+\langle x\in S\cup T\rightarrow f(x)\rangle$|
|$+\langle x\in S\rightarrow f(x)\rangle-+\langle x\in T\rightarrow f(x)\rangle$|$+\langle x\in S\land x\not\in T\rightarrow f(x)\rangle$|

Similarly, an element in the range can be separated from the rest for an inductively valid operation. This is known as _range splitting_:

|Quantification|After range split|
|-|-|
|$\land\langle 0\le x<n+1\rightarrow P(x)\rangle$|$\land\langle 0\le x<n\rightarrow P(x)\rangle\land P(n)$|
|$\land\langle x\in S\cup\set{z}\rightarrow P(x)\rangle$|$\land\langle x\in S\rightarrow P(x)\rangle\land P(z)$|
|$\lor\langle 0\le x<n+1\rightarrow P(x)\rangle$|$+\langle 0\le x<n\rightarrow P(x)\rangle\lor P(n)$|
|$+\langle 0\le k<n+1\rightarrow f(k)\rangle$|$+\langle 0\le k<n\rightarrow f(k)\rangle+f(n)$|

## Distributivity

Free terms can distributed over quantifiers.

|Quantification|After distribution|
|-|-|
|$\land\langle x\in S\rightarrow P(x)\rangle\lor Q(z)$|$\land\langle x\in S\rightarrow P(x)\lor Q(z)\rangle$|
|$+\langle 0\le k<n\rightarrow f(k)\rangle\times\alpha$|$+\langle 0\le k<n\rightarrow \alpha\times f(k)\rangle$|
|$\uparrow\langle 0\le k<n\rightarrow f(k)\rangle+\alpha$|$\uparrow\langle 0\le k<n\rightarrow \alpha+f(k)\rangle$|

## Trading

Quantifier ranges also have specific relations with their terms. Moving the range definition to the term section is known as _trading_, and the relation with the term has to be stated based on predicate calculus.

|Expression|After trading|
|-|-|
|$\land\langle x\in S\rightarrow P(x)\rangle$|$\land\langle x\rightarrow x\in S\implies P(x)\rangle$|
|$\lor\langle x\in S\rightarrow P(x)\rangle$|$\lor\langle x\rightarrow x\in S\land P(x)\rangle$|
|$+\langle x\in S\rightarrow f(x)\rangle$|$+\langle x\rightarrow \#\langle y\in S\rightarrow y=x\rangle\times f(x)\rangle$|
|$\#\langle x\in S\rightarrow P(x)\rangle$|$\#\langle x\rightarrow x\in S\land P(x)\rangle$|
