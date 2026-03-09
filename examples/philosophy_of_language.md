# Philosophy of Language

**208 DefCx** + **71 AbdCx** = **279 examples**

**Subdomains:** ambiguity, analyticity, assertion, communication, compositionality, context dependence, conventional meaning, definition, denotation, implicature, indexicals, intensionality, irony, literal meaning, logical form, meaning, metaphor, modality linguistic, naming, natural meaning, negation, performatives, predication, presupposition, propositional attitudes, quotation, reference, semantic role, speech acts, synonymy, translation, truth conditions, understanding linguistic, vagueness

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. meaning

**Definition:** A sentence is meaningful if and only if (i) it is grammatically well-formed, (ii) each of its constituent words has a definite sense, and (iii) the senses of the words combine to yield a determinate proposition.

> A natural account of linguistic meaning proposes that a sentence is meaningful if and only if it is grammatically well-formed, each of its constituent words has a definite sense, and the senses of the words combine to yield a determinate proposition. Yet this analysis may be challenged. Consider the sentence 'Colourless green ideas sleep furiously.' It is grammatically impeccable, conforming to the syntactic rules of English. Each of its constituent words has a perfectly definite sense: we know what 'colourless' means, what 'green' means, what 'ideas' are, and so forth. But the senses do not combine to yield any determinate proposition — one cannot say what state of affairs would make the sentence true. The third condition fails. Yet we should hesitate to pronounce the sentence meaningless. It is understood by every competent speaker of English, and its absurdity is itself a meaningful property that distinguishes it from mere gibberish. The definition has drawn the boundary of meaningfulness too narrowly, excluding sentences which, though they express no determinate proposition, are nonetheless intelligible.

*Missing condition:* Meaningfulness may not require that the combined senses yield a determinate proposition; it may be sufficient that the sentence be interpretable as a linguistic act.

### 2. reference

**Definition:** A name refers to an object if and only if (i) the speaker intends to pick out that object, (ii) there is a causal-historical chain connecting the speaker's use of the name to the object, and (iii) the name is used in accordance with the conventions of the linguistic community.

> A theory of reference might hold that a name refers to an object if and only if the speaker intends to pick out that object, there is a causal-historical chain connecting the speaker's use of the name to the object, and the name is used in accordance with the conventions of the linguistic community. This theory, though powerful, encounters a difficulty. Consider the name 'Madagascar.' When a European speaker today uses this name, he intends to refer to the large island off the south-eastern coast of Africa, and his usage accords with the conventions of his linguistic community. But historical evidence suggests that the name was originally applied by Marco Polo, or his sources, to a region of the African mainland, and was only later transferred to the island through a geographical error. The causal-historical chain thus connects the name not to the island but to the mainland. Yet the speaker's reference plainly succeeds — he refers to the island, not to the mainland. The definition has failed to account for the possibility that current convention may override the original causal-historical chain.

*Missing condition:* Current communal convention may override the original causal-historical chain when the two diverge.

### 3. translation

**Definition:** A translation is adequate if and only if (i) it preserves the reference of the original, (ii) it preserves the sense, and (iii) it preserves the illocutionary force.

> It is natural to suppose that a translation is adequate if and only if it preserves the reference of the original, preserves the sense, and preserves the illocutionary force. By this account, a translation that refers to the same objects, expresses the same thoughts, and performs the same speech acts as the original is a fully adequate translation. Yet consider the translation of a poem. One may render each line into the target language in such a way that the reference is preserved — the same objects are mentioned — the sense is preserved — the same thoughts are expressed — and the illocutionary force is preserved — assertions remain assertions, questions remain questions. The three conditions are met. Yet if the translation has lost the rhyme, the metre, the assonance, and the rhythmic structure of the original, we should be reluctant to call it an adequate translation of the poem. For a poem is not merely a sequence of propositions; it is a verbal artefact whose meaning is inseparable from its form. The definition has failed to account for the aesthetic dimension of translation, which in literary contexts may be paramount.

*Missing condition:* For literary works, adequacy of translation requires preserving aesthetic and formal properties, not only semantic and pragmatic ones.

### 4. naming

**Definition:** A proper name is a word that (i) denotes a particular individual, (ii) has no descriptive content, and (iii) is assigned by an act of baptism or convention.

> One might propose that a proper name is a word that denotes a particular individual, has no descriptive content, and is assigned by an act of baptism or convention. This analysis has the merit of distinguishing names from descriptions, but it proves too restrictive. Consider the name 'Dartmouth.' It denotes a particular town in Devon; it was assigned, one may suppose, by convention. But it plainly has descriptive content: it describes the town as being situated at the mouth of the River Dart. The second condition — that a proper name have no descriptive content — is violated. Yet no one would deny that 'Dartmouth' is a proper name. Indeed, the town might have moved away from the river's mouth, and the name would persist. The definition has confused two things: the etymological origin of a name, which may be descriptive, and its current semantic function, which may have nothing to do with that origin. A proper name may bear descriptive content on its surface while functioning, in use, as a non-descriptive tag.

*Missing condition:* Proper names may have etymological descriptive content without this content being part of their current semantic function.

### 5. metaphor

**Definition:** An utterance is metaphorical if and only if (i) the speaker says something literally false, (ii) the speaker intends the hearer to recognise the literal falsity, and (iii) the speaker intends to communicate a resemblance between the literal subject and the metaphorical vehicle.

> A familiar theory of metaphor holds that an utterance is metaphorical if and only if the speaker says something literally false, intends the hearer to recognise the literal falsity, and intends to communicate a resemblance between the literal subject and the metaphorical vehicle. This theory accounts well for cases such as 'Juliet is the sun,' which is literally false and communicates a resemblance between Juliet and the sun. But consider the utterance 'No man is an island.' This is literally true — no man is, in fact, a body of land surrounded by water. The first condition, literal falsity, is not satisfied. Yet the utterance is plainly metaphorical: it communicates something about human interconnection by invoking the image of an island's isolation. The definition has erred in requiring literal falsity as a necessary condition of metaphor. Metaphorical utterance may proceed by applying a frame or vocabulary from one domain to another, and this may result in statements that are literally true as well as literally false.

*Missing condition:* Metaphor need not involve literal falsity; it may involve the application of a term or frame from one domain to another, regardless of truth-value.

*... and 203 more DefCx examples in [`data/defcx/philosophy_of_language.jsonl`](../data/defcx/philosophy_of_language.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. speech acts

**Definition:** A performative utterance succeeds if and only if (i) it is spoken by the appropriate person, (ii) it follows the correct procedure, and (iii) it is uttered in the appropriate circumstances.

> Consider three cases of successful performative utterance. A judge says 'I sentence you to five years' in a courtroom, and the defendant is thereby sentenced. A bride says 'I do' at her wedding, and a marriage is thereby contracted. A head of state says 'I declare war,' and a state of war thereby obtains. From these cases one might extract the following definition: a performative utterance succeeds if and only if it is spoken by the appropriate person, follows the correct procedure, and is uttered in the appropriate circumstances.
>
> Yet consider a case in which a judge, sitting in the proper courtroom and following every procedural requirement, sentences a defendant to imprisonment — but it emerges that the defendant was acquitted of the charge by a higher court the previous day. The judge is the appropriate person, the procedure is correct, and the circumstances appear appropriate. The three conditions are met. Yet the sentence is void; it has no legal effect. The background cases all involved performatives issued in contexts free of prior legal nullification. The definition failed to include a condition about the absence of overriding countervailing acts — acquittals, annulments, revocations — that may render the performative void even when all surface conditions are satisfied.

*Abductive insight:* The background cases all involved performatives issued in a context free of prior legal nullification. The definition failed to include a condition about the absence of overriding countervailing acts that void the procedure.

### 2. vagueness

**Definition:** A predicate is precise if and only if (i) it divides its domain into two exhaustive classes, (ii) every object in the domain determinately belongs to one class, and (iii) the boundary between the classes can be specified exactly.

> Consider the following observations. A man six feet tall is clearly tall; a man five feet tall is clearly not tall. A head with a full covering of hair is clearly not bald; a completely bare scalp is clearly bald. A pile of one million grains of sand is clearly a heap; a single grain is clearly not a heap. In each case the predicate cleanly divides its domain at the extremes. From these observations one might conclude that a predicate is precise if and only if it divides its domain into two exhaustive classes, every object determinately belongs to one class, and the boundary between the classes can be specified exactly.
>
> But this analysis mistakes what holds at the extremes for what holds throughout the domain. Consider a man five feet ten inches tall. Is he tall? The predicate 'tall' does not determinately assign him to either class. No exact boundary can be drawn: there is no height h such that everyone at least h inches tall is tall and everyone below h is not. The third condition fails, and arguably the second as well. Yet 'tall' is a perfectly meaningful and useful predicate. The background cases all involved clear instances — the extremes where assignment is unproblematic — and the definition was abstracted from these easy cases. It failed to accommodate the borderline region where vague predicates resist precise classification.

*Abductive insight:* The background cases involved clear instances at the extremes, where assignment was unproblematic. The definition assumed that what holds at the extremes holds throughout the domain, but vague predicates have borderline cases where the third condition systematically fails.

### 3. implicature

**Definition:** A speaker conversationally implicates a proposition if and only if (i) the literal content of his utterance does not state the proposition, (ii) the hearer can derive the proposition by assuming the speaker is being cooperative, and (iii) the speaker can cancel the implication by adding further words without contradiction.

> Consider the following cases. Asked how his student is doing, a professor writes only that the student has excellent handwriting; the reader infers that the student is not a capable philosopher. A guest, asked whether she enjoys the wine, replies that it is certainly red; the host infers that she does not enjoy it. A man, asked about a colleague's lecturing, says he is always punctual; the hearer infers that the lectures are poor. From these cases one might extract a definition of conversational implicature: a speaker implicates a proposition if and only if the literal content of his utterance does not state it, the hearer can derive it by assuming the speaker is being cooperative, and the speaker can cancel the implication by adding further words without contradiction.
>
> Yet this definition encounters difficulty with sarcasm. A man says 'He is a fine friend,' meaning that the person is a treacherous one. The literal content does not state this; the hearer derives the intended meaning by assuming, in some broad sense, that the speaker is being communicatively cooperative. But can the speaker cancel the sarcastic meaning? If he adds 'and I mean that sincerely,' the literal content is coherent — there is no contradiction at the level of what is said. Yet the pragmatic force of the sarcasm is destroyed in a way quite unlike the cancellation of ordinary implicature. The background cases all involved implicatures generated by deliberate irrelevance or understatement, where adding a clarifying remark simply withdrew the inference. The definition treated cancellability as a uniform operation, but sarcastic meaning resists cancellation in a manner that the standard cases do not.

*Abductive insight:* The background cases all involved implicatures generated by deliberate understatement or irrelevance, where cancellation was straightforward. The definition failed to distinguish between literal cancellability (which sarcasm shares) and pragmatic cancellability (which sarcasm may resist).

### 4. presupposition

**Definition:** A sentence S presupposes a proposition P if and only if (i) the truth of S requires the truth of P, (ii) the negation of S also requires the truth of P, and (iii) the falsity of P renders S neither true nor false.

> Consider three cases of presupposition. The question 'Have you stopped taking sugar in your tea?' presupposes that the addressee used to take sugar. The sentence 'The king of France is wise' presupposes that there is a king of France. And 'John regrets having missed the lecture' presupposes that John did miss the lecture. In each case, both the sentence and its negation appear to require the truth of the presupposed proposition, and the falsity of that proposition renders the sentence problematic. From these cases one might define presupposition: a sentence S presupposes a proposition P if and only if the truth of S requires the truth of P, the negation of S also requires the truth of P, and the falsity of P renders S neither true nor false.
>
> But consider the sentence 'If the king of France exists, then the king of France is wise.' The embedded clause 'the king of France is wise' presupposes, by the definition, that there is a king of France. Yet the conditional as a whole does not seem to presuppose this. When France has no king, the antecedent is false, and by the standard account of conditionals the whole sentence is vacuously true — not truth-valueless. The presupposition has been absorbed or neutralised by the conditional structure. The background cases were all simple, unembedded sentences; the definition captured what holds in those local environments but failed to anticipate how embedding within conditionals, disjunctions, and other complex structures can filter presuppositions, preventing them from projecting to the level of the whole sentence.

*Abductive insight:* The background cases were all simple sentences in which presuppositions could not be neutralised by the surrounding linguistic context. The definition captured presupposition as it appears in simple sentences but failed to account for the way complex sentence structures — conditionals, disjunctions, modal contexts — can filter or block presuppositions.

### 5. analyticity

**Definition:** A statement is analytic if and only if (i) it is true, (ii) its truth can be established by reflecting on the meanings of its terms alone, and (iii) it can be transformed into a logical truth by substituting synonyms.

> Consider three statements. 'All bachelors are unmarried' is true in virtue of the meaning of 'bachelor.' 'No widow has a living husband' is true in virtue of the meaning of 'widow.' 'All vixens are foxes' is true in virtue of the meaning of 'vixen.' In each case, one can transform the statement into a logical truth by replacing a term with its synonym: 'bachelor' with 'unmarried man,' 'widow' with 'woman whose husband has died,' 'vixen' with 'female fox.' From these cases one might define analyticity: a statement is analytic if and only if it is true, its truth can be established by reflecting on the meanings of its terms, and it can be transformed into a logical truth by substituting synonyms.
>
> Yet consider the statement 'Every event has a cause.' A long tradition in philosophy has held this to be true and indeed necessary — its denial has been thought inconceivable. If one reflects upon the concept of an event, it may seem that being caused is part of what it is to be an event. The first two conditions are, on this view, satisfied. But the third condition fails: one cannot transform 'Every event has a cause' into a logical truth by substituting synonyms, for 'cause' has no synonym that reduces the statement to a tautology. The background cases all turned on simple definitional relations — 'bachelor' is defined as 'unmarried man' — and the definition assumed that all analytic truths rest upon such neat synonym pairs. The concept of analyticity, it appears, is wider than the method of synonym substitution can reach.

*Abductive insight:* The background cases all involved definitional truths whose key terms admitted of straightforward synonymy relations — 'bachelor' means 'unmarried man,' 'vixen' means 'female fox.' The definition assumed that all analytic truths rest on such synonym pairs, but some apparently analytic truths resist reduction to logical form because their key concepts lack neat synonyms.

*... and 66 more AbdCx examples in [`data/abdcx/philosophy_of_language.jsonl`](../data/abdcx/philosophy_of_language.jsonl)*
