# Mathematics

**214 DefCx** + **82 AbdCx** = **296 examples**

**Subdomains:** algebraic closure, cardinality, closure, compactness, completeness, computability, connectedness, consistency math, constructibility, continuity, convergence, decidability, density, dimension, embedding, equivalence, finiteness, function, group, independence, infinity, isomorphism, limit, linearity, measure, number, primality, proof, recursion, set, symmetry math, topology, well ordering

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. continuity

**Definition:** A function is continuous if and only if (i) it is defined at every point in its domain, (ii) its graph can be drawn without lifting the pen, and (iii) small changes in the input produce small changes in the output.

> The naive account of continuity holds that a function is continuous if and only if it is defined at every point in its domain, its graph can be drawn without lifting the pen from the paper, and small changes in the input produce small changes in the output. This account serves well enough for the functions encountered in elementary analysis. Yet the work of Weierstrass revealed a case that tells against any identification of continuity with smoothness. There exists a function, defined at every real number, whose graph — could one draw it — would form an unbroken curve, and which satisfies the requirement that small perturbations of the argument produce correspondingly small perturbations of the value. The three conditions are met. Yet this function possesses no derivative at any point; its graph, though unbroken, is infinitely jagged. It is continuous in the rigorous sense but smooth at no point whatever. The definition, it appears, has failed to distinguish continuity from differentiability, and the intuitive picture of a curve 'drawn without lifting the pen' tacitly imports an assumption of regularity that the mathematical concept does not warrant.

*Missing condition:* The intuitive definition conflates continuity with smoothness; a function may satisfy all three conditions while being nowhere smooth.

### 2. primality

**Definition:** A number is prime if and only if (i) it is a positive integer, (ii) it is greater than zero, and (iii) it is divisible only by one and itself.

> It is commonly said that a number is prime if and only if it is a positive integer, is greater than zero, and is divisible only by one and itself. This definition, though it captures the ordinary intuition, admits of an awkward case. The number one is a positive integer, is certainly greater than zero, and is divisible only by one and itself — for in this case, one and itself are the same number. The three conditions are thus satisfied. Yet mathematicians do not regard one as a prime number, and there are excellent reasons for this exclusion: if one were admitted as prime, the fundamental theorem of arithmetic — the unique factorisation of every integer into primes — would fail, since one could be introduced as a factor any number of times. The definition has omitted a crucial requirement: that the number have exactly two distinct positive divisors. One has only a single divisor and must therefore be excluded from the class of primes.

*Missing condition:* A prime must be greater than one, or equivalently, must have exactly two distinct positive divisors.

### 3. convergence

**Definition:** An infinite series converges if and only if (i) it has infinitely many terms, (ii) the terms decrease in absolute value, and (iii) the partial sums remain bounded.

> One might suppose that an infinite series converges if and only if it has infinitely many terms, the terms decrease in absolute value, and the partial sums remain bounded. This definition, however, is refuted by well-known examples. Consider first the harmonic series, whose terms — one, one-half, one-third, one-quarter, and so on — decrease steadily in absolute value. The first two conditions are met, yet the partial sums grow without bound, and the series diverges. One might then retreat to the third condition and insist that bounded partial sums suffice. But consider the series one minus one plus one minus one, ad infinitum. Its partial sums oscillate between zero and one, and are therefore bounded. Its terms do not decrease, but if we amended the definition to require only bounded partial sums, this series would qualify as convergent, though it plainly does not converge to any definite value. The definition has confused two distinct requirements: that the partial sums be bounded and that they approach a single limit. Only the latter is sufficient for convergence in the proper sense.

*Missing condition:* Convergence requires that the partial sums approach a single definite limit, not merely that they remain bounded or that the terms diminish.

### 4. connectedness

**Definition:** A subset of the plane is connected if and only if (i) it is non-empty, (ii) it is in one piece, and (iii) any two points in it can be joined by a path lying entirely within the set.

> The intuitive notion of connectedness suggests that a subset of the plane is connected if and only if it is non-empty, is in one piece, and any two points in it can be joined by a path lying entirely within the set. Yet topology furnishes a case that separates these conditions. Consider the topologist's sine curve: the graph of sin(1/x) for positive x, together with the segment of the y-axis between minus one and one. This set is non-empty and, in the precise topological sense, connected — it cannot be partitioned into two disjoint non-empty open sets. It is, as we say, in one piece. Yet it is not the case that any two points in the set can be joined by a continuous path lying within the set. A point on the y-axis cannot be reached by a path from the oscillating portion of the curve, for the oscillations accumulate so rapidly near the origin that no continuous path can traverse them. The definition has identified connectedness with path-connectedness, but these are distinct: every path-connected set is connected, but not every connected set is path-connected.

*Missing condition:* The definition conflates topological connectedness with path-connectedness; these are distinct properties.

### 5. computability

**Definition:** A function is computable if and only if (i) there exists a step-by-step procedure for evaluating it, (ii) each step is deterministic, and (iii) the procedure terminates in finitely many steps for every input.

> A natural definition of computability holds that a function is computable if and only if there exists a step-by-step procedure for evaluating it, each step is deterministic, and the procedure terminates in finitely many steps for every input. This definition captures what one ordinarily means by a mechanical calculation. Yet it is instructive to consider where it breaks down. Consider the function which, given a description of a Turing machine, returns one if the machine halts when started on blank tape and zero otherwise. One might propose the following procedure: simulate the machine step by step, and if it halts, return one. Each step of this simulation is perfectly deterministic. But the procedure does not satisfy the third condition, for if the machine does not halt, the simulation will continue forever, and the procedure will never terminate. One cannot repair this by adding a check for non-halting, for it has been shown that no such check is possible in general. The function is well-defined but not computable. The definition correctly requires termination, and it is precisely this requirement that distinguishes the computable from the merely well-defined.

*Missing condition:* The existence of a procedure that could in principle be followed is not sufficient; the procedure must be guaranteed to terminate for every input, which is not the case for the halting problem.

*... and 209 more DefCx examples in [`data/defcx/mathematics.jsonl`](../data/defcx/mathematics.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. cardinality

**Definition:** Two collections have the same size if and only if (i) there is a one-to-one correspondence between them, (ii) neither collection has elements left over, and (iii) a collection is always larger than any of its proper parts.

> Consider the following comparisons. A bag containing three apples and a bag containing three oranges have the same number of items; we verify this by pairing each apple with an orange. Two flocks of sheep can be compared by matching each sheep in one flock with a sheep in the other. The fingers on one hand and the toes on one foot are equal in number, as shown by one-to-one correspondence. From these cases one abstracts a definition: two collections have the same size if and only if there is a one-to-one correspondence between them, neither has elements left over, and a collection is always larger than any of its proper parts.
>
> Yet the third condition, so natural for finite collections, fails spectacularly in the infinite case. Consider the natural numbers and the even numbers. The function that maps each natural number n to the even number 2n establishes a perfect one-to-one correspondence; no element is left over on either side. The first two conditions are met. But the even numbers are a proper part of the natural numbers — every even number is a natural number, but not conversely. The third condition asserts that the whole must be larger than its proper part, yet the correspondence shows them to be the same size. The background cases were all finite, and the principle that the whole exceeds the part holds for finite collections. The definition failed to notice that this principle is a feature of finitude, not of size as such.

*Abductive insight:* The background cases all involved finite collections, for which the principle that the whole is greater than the part is trivially true. The definition imported this finite intuition into a context where it breaks down — the infinite.

### 2. decidability

**Definition:** A mathematical question is decidable if and only if (i) it can be formulated precisely, (ii) there exists a method that will in principle answer it, and (iii) the method can be carried out in a finite number of steps.

> Consider three cases in which a mathematical question is readily decided. Whether a natural number is even can be determined by inspecting its last digit. Whether a propositional formula is a tautology can be settled by constructing a truth table. Whether an integer is divisible by seven can be resolved by performing the division. In each case, the question is precisely formulated, a method exists to answer it, and the method terminates in finitely many steps. One might therefore define decidability: a mathematical question is decidable if and only if it can be formulated precisely, there exists a method that will in principle answer it, and the method terminates in a finite number of steps.
>
> But consider the question: does this Turing machine, started on empty tape, eventually halt? The question can be formulated with perfect precision — there is no ambiguity about what a Turing machine is or what halting means. The first condition is met. Yet no method exists that will answer this question for every Turing machine. The halting problem, as it is called, is undecidable: no algorithm can determine, for an arbitrary machine, whether it halts. The background cases were all questions about simple mathematical properties — parity, tautologyhood, divisibility — for which decision procedures happen to exist. The definition assumed that precise formulation suffices for decidability, but the theory of computation has shown that these come apart: some perfectly precise questions have no general decision procedure.

*Abductive insight:* The background cases all involved simple mathematical properties for which decision procedures exist. The definition assumed that precise formulation guarantees the existence of a decision method, but the existence of undecidable problems shows that formalisability and decidability come apart.

### 3. completeness

**Definition:** A number system is complete if and only if (i) it is equipped with a notion of distance or size, (ii) sequences whose terms grow arbitrarily close together have limits within the system, and (iii) the arithmetic operations are continuous with respect to the notion of distance.

> Consider three complete number systems. The real numbers form a complete ordered field: every non-empty set bounded above has a least upper bound, and every Cauchy sequence converges. The closed interval from zero to one is a complete metric space in its own right. And the p-adic numbers, equipped with a different metric, are complete with respect to that metric. From these cases one might define completeness: a number system is complete if and only if it is equipped with a notion of distance, sequences whose terms grow arbitrarily close together have limits within the system, and the arithmetic operations are continuous with respect to the distance.
>
> Yet the rational numbers, equipped with the usual absolute-value metric, satisfy the first and third conditions whilst failing the second. The rationals possess a perfectly good notion of distance, and the arithmetic operations — addition, subtraction, multiplication, division — are all continuous with respect to this distance. But the sequence of decimal approximations to the square root of two — 1, 1.4, 1.41, 1.414, and so on — is a Cauchy sequence whose terms grow arbitrarily close together, yet which has no limit among the rationals. The system is incomplete despite possessing a metric and continuous arithmetic. The background cases were systems in which completeness had already been secured, and the definition abstracted features common to those systems without recognising that a metric and continuous operations are necessary but not sufficient for completeness.

*Abductive insight:* The background cases were all systems in which completeness was already established by construction or by theorem. The definition captured the features these complete systems share but did not exclude systems that possess some of those features — a metric and continuous arithmetic — without possessing completeness itself.

### 4. infinity

**Definition:** A set is infinite if and only if (i) it is non-empty, (ii) it cannot be exhausted by any finite list, and (iii) it can be put into one-to-one correspondence with a proper part of itself.

> Consider three cases of infinite sets. The natural numbers form an infinite set, for one can always find another number beyond any given finite collection. The integers extend without bound in both directions, and no finite list exhausts them. The rational numbers between zero and one form an infinite set as well, for between any two rationals there is always a third. From these cases one might define infinity: a set is infinite if and only if it is non-empty, it cannot be exhausted by any finite list, and it can be placed in one-to-one correspondence with a proper part of itself.
>
> This definition is, so far as it goes, correct. Each of the background cases satisfies all three conditions: the natural numbers can be paired with the even numbers, the integers with the positive integers, and so on. But now consider the set of all subsets of the natural numbers — the power set. It too is non-empty, it cannot be finitely listed, and it can be put into correspondence with a proper part of itself. The three conditions are met. Yet this set is of a fundamentally different character from those in our background cases: Cantor demonstrated that it cannot be placed in one-to-one correspondence with the natural numbers. It is uncountably infinite — a larger infinity. The background cases, all countably infinite, misled us into a definition that, whilst correct as far as it goes, fails to register the profoundly important distinction between different magnitudes of infinity.

*Abductive insight:* The background cases were all countably infinite sets. The definition captured what they shared — inexhaustibility and self-embeddability — but because all three examples had the same cardinality, the definition failed to register the possibility of distinct magnitudes of infinity.

### 5. dimension

**Definition:** The dimension of a space is the number of independent coordinates required to specify a point within it, such that (i) the number is a non-negative integer, (ii) it equals the minimum number of real-valued parameters needed, and (iii) it is invariant under continuous deformation of the space.

> Consider three familiar cases. A line is one-dimensional: a single coordinate specifies any point upon it. A plane requires two coordinates; ordinary space requires three. From these cases one might define dimension: the dimension of a space is the number of independent coordinates needed to specify a point, this number being a non-negative integer, equal to the minimum number of real-valued parameters required, and invariant under continuous deformation.
>
> Yet this definition, drawn from smooth and regular spaces, encounters objects it cannot accommodate. Consider the Sierpinski triangle, a figure constructed by iteratively removing central triangles from an equilateral triangle, ad infinitum. The resulting set is embedded in the plane but has Lebesgue measure zero — it is, in a precise sense, thinner than any two-dimensional region. A continuous curve can be drawn through it, suggesting one-dimensionality, but the set branches and ramifies at every scale in a manner quite unlike any curve. Its Hausdorff dimension — a generalisation of the familiar notion — is log three divided by log two, approximately 1.585. This is not a non-negative integer. The first condition of our definition fails. The background cases were all smooth, homogeneous objects whose dimensions happened to be whole numbers. The definition captured the integer character of dimension in those well-behaved settings but could not anticipate objects whose geometry is so irregular that their dimension falls between the integers.

*Abductive insight:* The background cases — lines, planes, ordinary space — were all smooth, homogeneous objects whose dimensions are whole numbers. The definition captured the integer-valued character of dimension in these regular settings but could not accommodate fractal objects whose dimensions are non-integral.

*... and 77 more AbdCx examples in [`data/abdcx/mathematics.jsonl`](../data/abdcx/mathematics.jsonl)*
