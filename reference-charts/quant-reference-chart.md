# Hehner's Notation for Mathematical Quantifiers

All quantification expressions are enclosed within a pair of angle brackets to delineate the scope of the dummies. The first section is used to describe their range. This is followed by a right arrow after which comes the term.

In the following table, $A$ is the domain, $n$ represents its cardinality, and $i$ is from the index set $I_A$.

|Type|Example|Description|
|-|-|-|
|Universal|$\land\langle 0\le i<n\rightarrow m\|A_i\rangle$|Starts with a conjunction symbol, and the term is boolean. The example states that every element of the set is divisible by $m$|
|Existential|$\lor\langle 0\le i<n\rightarrow A_i<0\rangle$|Starts with a disjunction symbol, and the term is boolean. The example states that some elements of the set are negative|
|Sum|$+\langle 0\le i<n\rightarrow A_i\times \alpha^i \rangle$|Starts with an addition symbol, and the term is numeric. The example add every element of the set after multiplying it with a factor raised to the index|
|Product|$\times\langle 0\le i<n\rightarrow x-i\rangle$|Starts with a multiplication symbol, and the term is numeric. The example is a quantified form of the falling factorial $x^{\underline{n}}$ which is $x(x-1)(x-2)\ldots(x-n+1)$|
|Maximum|$\uparrow\langle 0\le i<n\rightarrow A_i\rangle$|Starts with an up arrow symbol, and the term is numeric. The example is the maximum of the set|
|Minimum|$\downarrow\langle 0\le i<n\rightarrow A_i\rangle$|Starts with a down arrow symbol, and the term is numeric. The example is the minimum of the set|
|Count|$\#\langle 0\le i<n\rightarrow A_i<0\rangle$|Starts with a sharp symbol, and the term is boolean. The first example is the number of negative values in the set. The second is essentially the cardinality of the set|
||$\#\langle x:int\rightarrow x\in A_i\rangle$||
