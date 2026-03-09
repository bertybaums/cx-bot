# Everyday Concepts

**193 DefCx** + **77 AbdCx** = **270 examples**

**Subdomains:** art, art everyday, chair, custom, family, food, friendship, game, gift, home, institution, language, lie, luck, meal, money, music, ownership, promise, punishment, sport, tool, vehicle, weapon, work

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. game

**Definition:** An activity is a game if and only if (i) it is governed by rules, (ii) it involves competition between participants, and (iii) it is undertaken for amusement.

> One is inclined to define a game as an activity governed by rules, involving competition between participants, and undertaken for amusement. This definition captures many familiar games — chess, football, card games of various kinds. But it proves too narrow. Consider a child who amuses herself by throwing a ball against a wall and catching it, counting the number of consecutive catches. She has imposed rules upon herself (she must catch the ball cleanly, she must not move from her spot), and the activity is undertaken for amusement. But there is no competition: she plays alone, against no opponent. The second condition fails, yet we should not hesitate to call this a game. Now consider a professional footballer who plays not for amusement but for his livelihood. The activity is governed by elaborate rules and involves intense competition, but the element of amusement may be entirely absent; the player may find the game exhausting and tedious. The third condition fails. Yet football remains a game. The definition has identified features that are typical of games but not essential to all of them.

*Missing condition:* Games need not involve competition, and the motive of amusement may be absent without disqualifying the activity as a game.

### 2. lie

**Definition:** A statement is a lie if and only if (i) it is false, (ii) the speaker believes it to be false, and (iii) the speaker intends to deceive the hearer.

> The common analysis holds that a statement is a lie if and only if it is false, the speaker believes it to be false, and the speaker intends to deceive the hearer. This definition, though plausible on first inspection, encounters a decisive objection. Consider a man who tells his friend, 'Your wife is faithful to you.' The man believes this to be false — he has heard rumours of infidelity and regards them as reliable. He makes the statement with the intention of deceiving his friend, wishing to spare him pain or to manipulate his behaviour. But it transpires that the rumours were unfounded: the wife is in fact entirely faithful. The statement is true. The first condition — that the statement be false — is not met. Yet the man has surely lied. He asserted what he believed to be false, with the deliberate aim of producing a false belief in his hearer. That the statement happened, by accident, to be true does not redeem it from being a lie. The definition has erred in requiring actual falsity; what matters for lying is the speaker's belief that his statement is false, not whether it is so in fact.

*Missing condition:* A lie requires that the speaker assert what he believes to be false with intent to deceive; the actual truth or falsity of the statement is irrelevant.

### 3. vehicle

**Definition:** An object is a vehicle if and only if (i) it is designed to transport persons or goods, (ii) it has wheels, and (iii) it is powered by a motor.

> It is tempting to define a vehicle as an object designed to transport persons or goods, having wheels, and powered by a motor. This definition fits the motorcar, the lorry, and the omnibus. But it excludes a great many things that are plainly vehicles. A rowing boat is designed to transport persons across water; it has no wheels and no motor, yet it is a vehicle. A horse-drawn cart has wheels and is designed to transport goods, but it is not powered by a motor; it too is a vehicle. A sedan chair has neither wheels nor motor; it is carried by men and is designed to transport a single person; and it has been called a vehicle since the seventeenth century. The definition has taken the motorcar as its paradigm and has mistaken contingent features of that paradigm — wheels, a motor — for essential features of the concept. What makes something a vehicle is its function: it is a means of conveyance. The mechanism by which conveyance is achieved — wheels, sails, oars, or human bearers — is incidental.

*Missing condition:* The definition is too closely tied to the motorcar as paradigm; vehiclehood requires only the function of conveyance, not a particular mechanism.

### 4. promise

**Definition:** An utterance is a promise if and only if (i) the speaker commits himself to performing a future action, (ii) the commitment is voluntarily undertaken, and (iii) the utterance is addressed to a specific person.

> A plausible analysis holds that an utterance is a promise if and only if the speaker commits himself to performing a future action, the commitment is voluntarily undertaken, and the utterance is addressed to a specific person. The third condition reflects the common view that a promise is essentially a social act — a commitment made to another. But consider a man who, after a period of self-destructive behaviour, makes a solemn private vow to himself: he will stop drinking. No one else is present; the vow is addressed to no specific person. The first two conditions are satisfied — there is a commitment to a future action, and it is voluntary — but the third fails. Yet the man has made a promise, and he would feel, should he break it, that he has violated an obligation. We commonly speak of promises to oneself, and such promises carry genuine moral weight. The definition has erred in treating the social dimension of promising as essential, when in fact the core of a promise — the binding of one's future will — may occur in the absence of any other person.

*Missing condition:* Promises need not be addressed to another person; one may make binding commitments to oneself.

### 5. chair

**Definition:** An object is a chair if and only if (i) it has a seat, (ii) it has a back, (iii) it has legs, and (iv) it is designed for one person to sit on.

> One might define a chair as an object that has a seat, a back, legs, and is designed for one person to sit on. This definition captures the paradigm case — the four-legged wooden chair with a backrest — but it proves too narrow upon reflection. A beanbag has no rigid seat, no back, and no legs; it is an amorphous sack filled with polystyrene beads. Yet it is designed for one person to sit on, and it is sold as a chair, called a chair, and used as a chair. A hanging chair, suspended from the ceiling by a chain, has no legs whatever. A backless stool, if we are generous with our categories, might be called a chair in some contexts. In each case, one or more of the structural conditions fail, yet the object serves the function of a chair and is recognised as such. The definition has mistaken the typical features of chairs — seats, backs, legs — for essential features. What makes something a chair is not its structure but its function: it is an object designed and used for the purpose of seating a single person.

*Missing condition:* The concept of a chair is defined by its function (seating one person) rather than by structural features that are typical but not essential.

*... and 188 more DefCx examples in [`data/defcx/everyday_concepts.jsonl`](../data/defcx/everyday_concepts.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. tool

**Definition:** An object is a tool if and only if (i) it is a physical artefact, (ii) it is designed for a specific practical purpose, and (iii) it extends the capabilities of the human hand.

> Consider three familiar tools. A hammer is used to drive nails; a saw is used to cut wood; a screwdriver is used to turn screws. Each is a physical artefact, each is designed for a specific practical purpose, and each extends the capabilities of the human hand. From these cases one might define a tool: an object is a tool if and only if it is a physical artefact, it is designed for a specific practical purpose, and it extends the capabilities of the human hand.
>
> But this definition proves both too narrow and, in a different respect, too restrictive. Consider a stone picked up from a riverbed and used, without any modification, to crack a walnut. The stone is not an artefact — it was not designed or manufactured — yet it functions as a tool. The first condition fails, yet we should say the stone is being used as a tool. Now consider a computer program designed to perform complex calculations. It is designed for a specific practical purpose and extends human capabilities far beyond what the hand can achieve. But it is not a physical object. The background cases were all manufactured physical implements; the definition captured what those particular tools had in common but failed to accommodate both the primitive tool — the unmodified natural object pressed into service — and the modern tool that exists only as information.

*Abductive insight:* The background cases were all manufactured implements. The definition required both artefactuality and physicality, but tool-use predates manufacture (unmodified stones are tools when used as such) and extends beyond the physical (software is a tool in the relevant functional sense).

### 2. language

**Definition:** A system of communication is a language if and only if (i) it has a vocabulary of distinct symbols or words, (ii) it has a grammar governing how symbols are combined, and (iii) it is used by a community of speakers for communication.

> Consider three cases of language. English has a vocabulary, a grammar, and is spoken by a community of speakers. French has its own vocabulary, grammar, and community. Mandarin has a distinct writing system, grammar, and the largest community of native speakers in the world. From these cases one might define language: a system of communication is a language if and only if it has a vocabulary of distinct symbols or words, a grammar governing how symbols are combined, and it is used by a community of speakers for communication.
>
> But consider the language of propositional logic. It has a vocabulary: the symbols p, q, r, together with connectives and brackets. It has a grammar: precise rules specify which strings of symbols are well-formed formulae. Yet it is not used by any community as a medium of ordinary communication; it is a formal system employed within the discipline of logic for the analysis of arguments. The first two conditions are met, but the third is at best doubtful, for logicians do not converse in propositional logic. Yet we do not hesitate to call it a language — a formal language. The background cases were all natural languages serving everyday communicative purposes; the definition was drawn from these and failed to accommodate formal and artificial languages whose purpose is structural rather than communicative.

*Abductive insight:* The background cases were all natural languages used for everyday communication. The definition captured the social function of these languages but excluded formal and artificial languages that satisfy the structural conditions without serving the communicative function of natural language.

### 3. money

**Definition:** An object is money if and only if (i) it is made of or backed by a precious material, (ii) it is produced by a governmental authority, and (iii) it is widely accepted in exchange for goods and services.

> Consider three cases of money. A gold sovereign is accepted in exchange for goods, retains its value over time, and is minted by a government. A banknote issued by the Bank of England circulates in commerce, maintains a reasonably stable value, and is printed under governmental authority. A silver dollar circulates widely, holds its value, and is coined by the United States Mint. From these cases one might extract a definition: an object is money if and only if it is made of or backed by a precious material, it is produced by a governmental authority, and it is widely accepted in exchange for goods and services.
>
> But this definition, drawn from the monetary systems of modern industrial states, proves too restrictive. Consider the large stone discs, known as rai, used as currency on the island of Yap in the western Pacific. These discs, some of considerable size, are made of ordinary limestone quarried from a distant island and transported by canoe. Limestone is not a precious material by any standard. The discs are not produced by any governmental authority; they are quarried and fashioned by individual families. Yet they are widely accepted in exchange for goods and services within the Yapese community, and they function as money in every practical respect: debts are denominated in rai, transactions are conducted with reference to them, and their value is socially established and maintained. The first two conditions fail. The background cases were all instances of metallic currency issued by modern states; the definition mistook the incidental features of these particular systems — precious metal, governmental authority — for essential features of money as such. Money, it appears, is a social convention, not a material or governmental fact.

*Abductive insight:* The background cases all involved metallic currencies issued by modern nation-states. The definition treated precious material and governmental issuance as essential, but these were incidental features of the particular monetary systems observed, not universal requirements of money as such.

### 4. food

**Definition:** A substance is food if and only if (i) it is of organic origin, (ii) it provides caloric or nutritional value when ingested, and (iii) it is consumed primarily for the purpose of nourishment.

> Consider three staples of the human diet. Bread is consumed for nourishment; it provides carbohydrates and is a dietary staple across cultures. An apple provides vitamins, fibre, and sugars that sustain the body. Roast beef is consumed for its protein and caloric content. From these cases one might extract a definition: a substance is food if and only if it is of organic origin, it provides caloric or nutritional value when ingested, and it is consumed primarily for the purpose of nourishment.
>
> But this definition, drawn from calorie-rich organic substances, proves too narrow. Consider salt. Human beings have consumed salt throughout recorded history; wars have been fought over it, economies built upon it, and entire trade routes established for its transport. Salt is essential for bodily function: without sufficient sodium, the human body cannot maintain fluid balance, transmit nerve impulses, or contract muscles. Yet salt is not of organic origin; it is a mineral. And salt provides no calories whatever. The first condition fails, and the second is at best only partially met (salt provides nutritional value in the sense of an essential mineral, but not caloric value). Yet salt is indisputably part of the human diet and has been treated as a food, or at minimum as an indispensable component of food, since antiquity. The background cases were all calorie-rich organic staples; the definition abstracted organic origin and caloric value as essential, when in truth the concept of food extends to inorganic, non-caloric substances that are nonetheless vital to nourishment.

*Abductive insight:* The background cases were all calorie-rich organic staples. The definition assumed that all food is organic and caloric, but essential dietary components such as salt and water are inorganic and non-caloric, yet integral to what it means to eat and be nourished.

### 5. friendship

**Definition:** Two persons are friends if and only if (i) they spend time together regularly, (ii) they enjoy one another's company, and (iii) they know one another's personal histories and characters in some detail.

> Consider three cases of friendship. Two schoolboys who play together daily, confide in one another, and defend each other against bullies are friends. Two women who have shared a flat for years, celebrated each other's successes, and supported each other through adversity are friends. Two colleagues who meet regularly outside the office, enjoy each other's company, and trust one another with personal matters are friends. From these cases one might define friendship: two persons are friends if and only if they spend time together regularly, they enjoy one another's company, and they know one another's personal histories and characters in some detail.
>
> But this definition, drawn from friendships sustained by physical proximity, proves too narrow. Consider two men who met once as young scholars at a conference and thereafter maintained a correspondence spanning several decades. They exchange long, thoughtful letters about their work, their families, their disappointments, and their hopes. Each knows the other's character with an intimacy that few face-to-face acquaintances achieve. Each regards the other as his closest friend. Yet they do not spend time together in any ordinary sense: they have not been in the same room since that first meeting. The first condition fails. The background cases all involved friends who met regularly in person; the definition treated this regular physical contact as essential to friendship. But friendship, it appears, may be sustained and even deepened through correspondence alone, without any physical co-presence whatever. The definition has confused a common circumstance of friendship with a necessary condition of it.

*Abductive insight:* The background cases all involved friends in physical proximity who met regularly. The definition treated regular face-to-face contact as essential, but friendship may be sustained entirely through correspondence or other forms of communication at a distance.

*... and 72 more AbdCx examples in [`data/abdcx/everyday_concepts.jsonl`](../data/abdcx/everyday_concepts.jsonl)*
