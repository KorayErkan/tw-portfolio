# Modern Mathematical Quantifiers

All quantification expressions start with an operator used in the quantification, followed by a pair of angle brackets to delineate the scope of the expression enclosed. The first section within the quantifier is used to describe the range. This is followed by a right arrow after which comes the term.

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

The quantifiers can be used inductively with terms of the same type. This is known as _range splitting_.

|Expression</div>|After range split|
|-|-|
|$\land\langle 0\le i<n+1\rightarrow p.i\rangle$|$\land\langle 0\le i<n\rightarrow p.i\rangle\land p.n$|
|$\lor\langle 0\le i<n+1\rightarrow p.i\rangle$|$\lor\langle 0\le i<n\rightarrow p.i\rangle\lor p.n$|
|$+\langle 0\le i<n+1\rightarrow f.i\rangle$|$+\langle 0\le i<n\rightarrow f.i\rangle+p.n$|
|$\times\langle 0\le i<n+1\rightarrow f.i\rangle$|$\times\langle 0\le i<n\rightarrow f.i\rangle\times p.n$|
|$\uparrow\langle 0\le i<n+1\rightarrow f.i\rangle$|$\uparrow\langle 0\le i<n\rightarrow f.i\rangle\uparrow p.n$|
|$\downarrow\langle 0\le i<n+1\rightarrow f.i\rangle$|$\downarrow\langle 0\le i<n\rightarrow f.i\rangle\downarrow p.n$|
