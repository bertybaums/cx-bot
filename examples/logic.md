# Logic

**213 DefCx** + **83 AbdCx** = **296 examples**

**Subdomains:** abstraction, analogy, argument form, axiomatisation, completeness logical, conditional, consistency, contingency, contradiction, deduction, definability, demonstration, disjunction, entailment, fallacy, formal systems, identity, implication, induction logical, inference rules, logical consequence, logical independence, modal logic, necessity logical, paradoxes, possible worlds, predicate, proposition, quantification, soundness, tautology, truth functions, truth value, validity

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. validity

**Definition:** An argument is valid if and only if (i) the premises logically support the conclusion, (ii) the conclusion follows from the premises by recognised rules of inference, and (iii) there is no assignment of truth-values that makes the premises true and the conclusion false.

> One naturally says that an argument is valid if and only if the premises logically support the conclusion, the conclusion follows from the premises by recognised rules of inference, and there is no assignment of truth-values that makes the premises true and the conclusion false. The third condition is the precise one, and it admits of a surprising consequence. Consider the argument: 'The cat is on the mat; therefore, either it is raining or it is not raining.' The conclusion is a tautology — it is true under every assignment of truth-values. There is therefore no assignment that makes the premise true and the conclusion false. By the third condition, the argument is valid. Yet the premise is entirely irrelevant to the conclusion: the fact that the cat is on the mat has nothing whatever to do with the weather. The definition, faithfully applied, pronounces the argument valid, though many would feel that an argument whose premises are irrelevant to its conclusion is defective in some important sense. The classical notion of validity, it appears, is indifferent to relevance — a feature which some logicians have regarded as a deficiency in the classical account.

*Missing condition:* Validity in the formal sense does not require relevance of premises to conclusion; one may wish to add a relevance condition, but this goes beyond classical validity.

### 2. soundness

**Definition:** An argument is sound if and only if (i) it is valid, (ii) all its premises are true, and (iii) it employs no informal fallacies.

> The standard definition holds that an argument is sound if and only if it is valid, all its premises are true, and it employs no informal fallacies. Yet one may construct a case in which these conditions are satisfied and the argument is nevertheless wholly without value as a piece of reasoning. Suppose one argues: 'All events that will occur in the year 2030 are events that will occur; the next solar eclipse visible from London will occur in the year 2030; therefore, the next solar eclipse visible from London will occur.' This argument is valid: the conclusion follows from the premises. The premises are, we may suppose, true. And no informal fallacy is committed. The argument is sound. Yet it is entirely useless, for the conclusion is at least as certain as the premises, and arguably more so. The premises do not illuminate the conclusion; they merely restate it in a more complex form. The definition of soundness, it appears, captures the logical correctness of an argument but not its value as a justification. One may wish to add a requirement that the premises be more evident than the conclusion, but this goes beyond what soundness, strictly defined, provides.

*Missing condition:* Soundness in the logical sense does not guarantee intellectual value; the premises must also be more evident than the conclusion if the argument is to serve as a justification.

### 3. logical consequence

**Definition:** A proposition Q is a logical consequence of a set of propositions P if and only if (i) in every model where all members of P are true, Q is true, (ii) the inference from P to Q preserves truth, and (iii) the connection holds in virtue of the logical form of P and Q alone.

> It is held that a proposition Q is a logical consequence of a set of propositions P if and only if in every model where all members of P are true, Q is true, the inference preserves truth, and the connection holds in virtue of the logical form of P and Q alone. This third condition is meant to exclude inferences that depend on the specific content of the terms involved. Yet the boundary between logical form and content is not always clear. Consider the inference from 'this object is red' to 'this object is coloured.' In every possible circumstance where the premise is true, the conclusion is true; the inference preserves truth without exception. The first two conditions are satisfied. But the third condition fails: the connection between 'red' and 'coloured' is a matter of meaning, not of logical form. If we substitute other predicates of the same logical form — say, 'this object is heavy' and 'this object is fragile' — the inference fails. The definition correctly excludes such material consequences, but in doing so it reveals that the notion of 'logical form' upon which it relies is itself in need of clarification.

*Missing condition:* The definition must distinguish formal logical consequence from material consequence, which depends on the non-logical content of the terms involved.

### 4. paradoxes

**Definition:** A statement is paradoxical if and only if (i) it leads by valid reasoning to a contradiction, (ii) the reasoning employs only apparently acceptable premises, and (iii) the statement involves self-reference.

> A tempting definition holds that a statement is paradoxical if and only if it leads by valid reasoning to a contradiction, the reasoning employs only apparently acceptable premises, and the statement involves self-reference. This definition captures the structure of familiar paradoxes such as the Liar ('this statement is false') and Russell's paradox (the set of all sets that do not contain themselves). But it excludes a class of paradoxes that have no element of self-reference whatever. Consider the Sorites paradox. One grain of sand, we agree, does not constitute a heap. And we accept, as apparently obvious, that adding a single grain to a collection that is not a heap cannot transform it into a heap. By repeated application of this principle, we conclude that no number of grains of sand can constitute a heap — which contradicts our plain experience of heaps. The reasoning is valid, the premises are apparently acceptable, and the conclusion is contradictory. Yet there is no self-reference in the argument. The definition has identified a feature that is common to some paradoxes but is by no means essential to all.

*Missing condition:* Self-reference is characteristic of some paradoxes (the Liar, Russell's) but not all; the definition should not require it as a necessary condition.

### 5. consistency

**Definition:** A set of propositions is consistent if and only if (i) no contradiction can be derived from them, (ii) each proposition is individually possible, and (iii) the propositions can all be simultaneously true.

> One might define consistency by saying that a set of propositions is consistent if and only if no contradiction can be derived from them, each proposition is individually possible, and the propositions can all be simultaneously true. The third condition is the crucial one, and it is worth seeing how the second condition, taken alone, is insufficient. Consider the three propositions: 'A is taller than B,' 'B is taller than C,' and 'C is taller than A.' Each of these propositions, taken by itself, is perfectly possible — there is nothing self-contradictory about any one of them. And from any pair of them, no contradiction follows. Yet the three cannot all be simultaneously true, for the relation 'taller than' is transitive: if A is taller than B and B is taller than C, then A is taller than C, which contradicts the third proposition. The set is inconsistent, though each member is individually possible. The definition correctly requires simultaneous truth, but this requirement cannot be verified by examining the propositions individually — one must consider their logical interrelations as a whole.

*Missing condition:* Individual possibility does not guarantee joint consistency; the definition must attend to the logical relations among the propositions taken as a whole.

*... and 208 more DefCx examples in [`data/defcx/logic.jsonl`](../data/defcx/logic.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. entailment

**Definition:** A conclusion is entailed by a set of premises if and only if (i) denying the conclusion while affirming the premises leads to a contradiction, (ii) the inference can be formalised in a logical system, and (iii) the conclusion adds no information not already contained in the premises.

> Consider three cases of entailment. 'All men are mortal; Socrates is a man; therefore Socrates is mortal' — the conclusion is plainly entailed. 'If it rains the ground is wet; it rains; therefore the ground is wet' — the conclusion follows necessarily. 'No birds are mammals; all sparrows are birds; therefore no sparrows are mammals' — again, the entailment is beyond dispute. From these cases one might extract a definition: a conclusion is entailed by a set of premises if and only if denying the conclusion while affirming the premises leads to a contradiction, the inference can be formalised in a logical system, and the conclusion adds no information not already contained in the premises.
>
> But the third condition proves troublesome. Consider: 'All dogs bark; Rex is a dog; therefore Rex barks.' The conclusion is certainly entailed — denying it while affirming the premises leads to a contradiction, and the inference is formally valid. But does the conclusion add no information? In a logical sense, perhaps not — the conclusion is implicit in the premises. But in an intellectual or practical sense, the conclusion may be genuinely informative: one may not have considered Rex in particular before drawing the inference. The background cases were all simple enough that the conclusion seemed obviously contained in the premises. The definition mistook this appearance for a necessary feature of entailment, confusing logical containment with absence of intellectual novelty.

*Abductive insight:* The background cases all had conclusions that seemed intuitively 'contained' in the premises. The definition mistook this appearance of containment for a general feature of entailment, but deductive conclusions can be psychologically novel even when logically implicit.

### 2. definability

**Definition:** A concept is definable if and only if (i) necessary and sufficient conditions for its application can be stated, (ii) the conditions are finitely expressible, and (iii) competent speakers agree on the extension of the concept.

> Consider three cases of successful definition. A square is defined as a rectangle all of whose sides are equal; this definition picks out precisely the squares and nothing else. A prime is defined as an integer greater than one divisible only by one and itself; this picks out precisely the primes. A bachelor is defined as an unmarried adult male; this picks out the bachelors. From these cases one might conclude that a concept is definable if and only if necessary and sufficient conditions for its application can be stated, the conditions are finitely expressible, and competent speakers agree on the extension of the concept.
>
> But consider the concept of a game. Competent speakers of English agree on the clear cases: chess is a game, football is a game, ring-a-ring-o'-roses is a game, taxation is not a game, ploughing a field is not a game. Agreement on the extension exists, at least for central cases. And the concept is finitely expressible in natural language. But no one has succeeded in stating necessary and sufficient conditions that capture all and only games. Some games involve competition, others do not. Some have rules, others are improvisatory. Some are played for amusement, others professionally. The first condition fails, yet the concept is perfectly serviceable. The background cases all involved tidy, well-bounded concepts; the definition assumed all concepts share this structure, but many of our most important concepts are united by family resemblance rather than by a common set of necessary and sufficient conditions.

*Abductive insight:* The background cases involved tidy, well-bounded concepts (square, prime, bachelor). The definition assumed all concepts have this crisp structure, but many important concepts are held together by family resemblance rather than by necessary and sufficient conditions.

### 3. tautology

**Definition:** A proposition is a tautology if and only if (i) it is a well-formed formula of propositional logic, (ii) its truth can be verified by the truth-table method, and (iii) it is true under every possible assignment of truth-values to its atomic components.

> Consider three familiar tautologies. The proposition 'P or not-P' is true under every assignment of truth-values to its atomic components; we recognise it as the law of excluded middle. The proposition 'If P, then P' is similarly immune to falsification by any assignment. And the proposition 'Not both P and not-P' is a tautology expressing the principle of non-contradiction. From these cases one might define: a proposition is a tautology if and only if it is a well-formed formula of propositional logic, its truth can be verified by the truth-table method, and it is true under every possible assignment of truth-values to its atomic components.
>
> But this definition proves too narrow when one moves beyond the propositional calculus. Consider the proposition 'For all x, if x is a bachelor then x is unmarried.' This proposition cannot be falsified under any interpretation of the predicate symbols; it is, in an important sense, necessarily true. Yet it is not a well-formed formula of propositional logic. It contains quantifiers and predicate symbols that have no place in the propositional calculus. Nor can its truth be verified by the truth-table method, for the truth-table method applies only to formulae composed of a finite number of propositional variables joined by truth-functional connectives. The background cases were all propositional in character, and the definition was tailored to them. It captured what makes certain propositional formulae necessarily true but excluded an entire class of logical truths whose necessity arises from the structure of quantification and predication rather than from truth-functional combination alone.

*Abductive insight:* The background cases were all propositional formulae with finitely many atomic components. The definition captured this finiteness but excluded logical truths whose necessity arises from the structure of quantifiers and predicates rather than from truth-functional composition.

### 4. implication

**Definition:** A conditional 'if P then Q' is true if and only if (i) there exists a genuine connection between P and Q, (ii) whenever P obtains, Q obtains as a consequence, and (iii) denying Q while affirming P leads to an absurdity.

> Consider three cases of implication that function as we expect. From 'If it is raining, the streets are wet' and the observation that it is raining, we conclude the streets are wet. From 'If a number is divisible by four, it is divisible by two' and the fact that eight is divisible by four, we conclude that eight is divisible by two. From 'If the switch is on, the light is on' and the fact that the switch is on, we infer the light is on. In each case there is a genuine connection between antecedent and consequent, the obtaining of the antecedent brings about the consequent, and denying the consequent while affirming the antecedent would be absurd. One might define: a conditional 'if P then Q' is true if and only if there is a genuine connection between P and Q, whenever P obtains Q obtains, and denying Q while affirming P leads to an absurdity.
>
> But consider the conditional 'If five is even, then London is the capital of France.' The antecedent is false: five is not even. In classical logic, a material conditional with a false antecedent is true regardless of the consequent. The conditional is therefore true. Yet there is no genuine connection between the evenness of five and the status of London. Denying the consequent while affirming the antecedent — asserting that five is even and London is not the capital of France — is not absurd but merely a conjunction of falsehoods. None of the three conditions is satisfied, yet classical logic pronounces the conditional true. The background cases were all instances where the antecedent was true and a real connection obtained. The definition, drawn from these congenial cases, failed to anticipate the behaviour of the material conditional when the antecedent is false — a behaviour that many logicians have regarded as paradoxical.

*Abductive insight:* The background cases all involved conditionals with true antecedents and a causal or logical connection between antecedent and consequent. The definition extracted the notion of genuine connection from these cases, but classical logic evaluates the material conditional purely truth-functionally, rendering it true whenever the antecedent is false, regardless of any connection.

### 5. deduction

**Definition:** A piece of reasoning is a deduction if and only if (i) the conclusion follows necessarily from the premises, (ii) the reasoning proceeds from universal premises to a particular conclusion, and (iii) the conclusion contains no information not already present in the premises.

> Consider three paradigmatic deductions. From 'All men are mortal' and 'Socrates is a man,' we deduce that Socrates is mortal. From 'All even numbers are divisible by two' and 'Fourteen is even,' we deduce that fourteen is divisible by two. From 'No reptiles are mammals' and 'All snakes are reptiles,' we deduce that no snakes are mammals. In each case the conclusion follows necessarily from the premises, the reasoning moves from universal premises to a particular or restricted conclusion, and the conclusion seems to contain nothing beyond what was already implicit in the premises. One might therefore define: a piece of reasoning is a deduction if and only if the conclusion follows necessarily from the premises, the reasoning proceeds from universal premises to a particular conclusion, and the conclusion contains no information not already present in the premises.
>
> But consider the following argument: 'If it is raining, then the match is cancelled. It is raining. Therefore, the match is cancelled.' The conclusion follows necessarily from the premises; this is an instance of modus ponens, one of the most elementary forms of deductive reasoning. Yet neither premise is a universal generalisation. The first is a conditional about a particular event — this rain and this match — and the second is a particular observation about the weather. The second condition of the definition, requiring that deduction proceed from universal premises to a particular conclusion, is not satisfied. The background cases were all syllogisms — arguments with universal major premises — and the definition was drawn from that special form. But deduction is not defined by the form of its premises; it is defined by the necessity of the connection between premises and conclusion. A deductive argument may proceed from particulars to particulars, from particulars to universals, or indeed in any direction, provided the conclusion cannot be false when the premises are true.

*Abductive insight:* The background cases were all syllogisms proceeding from universal premises. The definition abstracted the direction of reasoning from these paradigm cases, but deduction is characterised by the necessity of the inference, not by the logical form of the premises; deductive arguments from particular premises are entirely possible.

*... and 78 more AbdCx examples in [`data/abdcx/logic.jsonl`](../data/abdcx/logic.jsonl)*
