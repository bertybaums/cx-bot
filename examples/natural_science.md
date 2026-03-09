# Natural Science

**207 DefCx** + **79 AbdCx** = **286 examples**

**Subdomains:** adaptation, causation, cell, chemical reaction, climate, continent, disease, ecosystem, element, energy, evolution, experiment, extinction, force, fossil, gene, habitat, instinct, life, measurement, mineral, observation, organism, planet, scientific law, species, symbiosis

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. species

**Definition:** A group of organisms constitutes a species if and only if (i) its members can interbreed with one another, (ii) they produce fertile offspring, and (iii) they are reproductively isolated from other such groups.

> The biological species concept holds that a group of organisms constitutes a species if and only if its members can interbreed with one another, they produce fertile offspring, and they are reproductively isolated from other such groups. This definition serves well in many cases, but it encounters a significant difficulty with ring species. Consider the Larus gulls, whose populations form a ring around the Arctic. Each population can interbreed with its immediate neighbours and produce fertile offspring. But the populations at the two ends of the ring, where it closes in Europe, are reproductively isolated from one another: they do not interbreed. The conditions of the definition are satisfied locally — each adjacent pair meets the requirements — but fail globally, for the terminal populations are as distinct as any two species. The definition implicitly assumes that reproductive compatibility is a transitive relation: if A can breed with B, and B with C, then A can breed with C. Ring species demonstrate that this assumption is false, and that the biological species concept, for all its utility, admits of cases it cannot cleanly resolve.

*Missing condition:* The definition assumes that reproductive compatibility is a transitive relation, which ring species demonstrate it is not.

### 2. life

**Definition:** An entity is alive if and only if (i) it metabolises, (ii) it reproduces, and (iii) it responds to stimuli from its environment.

> A familiar definition holds that an entity is alive if and only if it metabolises, reproduces, and responds to stimuli from its environment. This definition captures a wide range of living things, from bacteria to elephants. Yet it encounters difficulty at the boundaries. Consider a virus. Outside a host cell, it is inert: it does not metabolise, it does not respond to stimuli, it does nothing at all. Inside a host cell, however, it commandeers the cell's machinery to reproduce itself, often with remarkable efficiency. The virus satisfies one of the three conditions (reproduction, after a fashion) but fails the other two. Yet it possesses a genome, it evolves by natural selection, and its behaviour is intimately bound up with the living world. To exclude it entirely from the category of life seems arbitrary. Now consider a mule, the offspring of a horse and a donkey. A mule metabolises, responds to stimuli, and is by every ordinary measure alive. But it cannot reproduce. The second condition fails, yet no one would deny that a mule is alive. The definition, it appears, identifies conditions that are characteristic of life but neither jointly sufficient to capture all cases nor individually necessary for every living thing.

*Missing condition:* The definition must accommodate borderline cases and may need to treat life as a cluster concept rather than one defined by necessary and sufficient conditions.

### 3. planet

**Definition:** A celestial body is a planet if and only if (i) it orbits a star, (ii) it has sufficient mass for its gravity to give it a roughly spherical shape, and (iii) it is the dominant body in its orbital zone.

> The current astronomical definition holds that a celestial body is a planet if and only if it orbits a star, it has sufficient mass for its self-gravity to overcome rigid body forces and assume a roughly spherical shape, and it has cleared the neighbourhood around its orbit, being the dominant body in its orbital zone. This definition, adopted to resolve the status of certain distant bodies in our solar system, proves vulnerable to the following case. Suppose a body of planetary mass and spherical form, which has for millions of years been the dominant body in its orbital zone, is ejected from its solar system by a close gravitational encounter with another massive body. It now drifts through interstellar space, orbiting no star. The first condition fails: the body does not orbit a star. Yet in its composition, its mass, its shape, and its geological complexity, it is indistinguishable from a body we would unhesitatingly call a planet. The definition has made planethood contingent upon an external relationship — the orbital connection to a star — rather than upon the intrinsic properties of the body itself.

*Missing condition:* The definition is tied to a current orbital relationship that may be disrupted by dynamical processes, yet the intrinsic planetary nature of the body seems unchanged.

### 4. disease

**Definition:** A condition is a disease if and only if (i) it involves a departure from normal biological functioning, (ii) it has an identifiable cause, and (iii) it causes suffering or impairment in the affected individual.

> A natural account of disease holds that a condition is a disease if and only if it involves a departure from normal biological functioning, it has an identifiable cause, and it causes suffering or impairment in the affected individual. This definition captures the paradigm cases — pneumonia, diabetes, malaria — in which all three conditions are plainly met. But consider an individual who carries the tubercle bacillus in his lungs. There is a departure from normal functioning: the bacillus has established itself in the tissue. There is an identifiable cause: the bacterium itself. Yet the individual is entirely asymptomatic. He suffers no impairment, no discomfort, no limitation of activity. The third condition fails. Yet the physician would not hesitate to say that the man has tuberculosis, for the pathological process is present and may at any time become active. Moreover, the man is capable of transmitting the disease to others. The definition has erred in requiring actual suffering; a disease may be present even when its characteristic harms have not yet manifested.

*Missing condition:* A condition may constitute a disease even in the absence of suffering or impairment, provided it involves a pathological process that characteristically causes harm.

### 5. element

**Definition:** A substance is a chemical element if and only if (i) it cannot be decomposed into simpler substances by chemical means, (ii) it consists of atoms of a single kind, and (iii) it occupies a definite place in the periodic table.

> A traditional definition holds that a substance is a chemical element if and only if it cannot be decomposed into simpler substances by chemical means, it consists of atoms of a single kind, and it occupies a definite place in the periodic table. The second condition, however, proves problematic when examined closely. Consider the element carbon. Natural carbon consists of atoms of at least two kinds: carbon-12, with six neutrons, and carbon-14, with eight neutrons. These atoms differ in mass and in their nuclear properties — carbon-14 is radioactive, carbon-12 is not. If 'atoms of a single kind' means atoms that are identical in all respects, then carbon fails the second condition. Yet carbon is indisputably an element. The definition has used the phrase 'atoms of a single kind' without sufficient precision. What makes carbon a single element is that all its atoms share the same number of protons — six — and hence the same atomic number. The concept of 'kind' must be understood in terms of atomic number, not in terms of identity in all nuclear properties.

*Missing condition:* Atoms of the same element share the same atomic number (number of protons), but may differ in mass (isotopes); 'single kind' must be understood as 'same atomic number.'

*... and 202 more DefCx examples in [`data/defcx/natural_science.jsonl`](../data/defcx/natural_science.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. ecosystem

**Definition:** A system is an ecosystem if and only if (i) it comprises a community of living organisms, (ii) the organisms interact with one another and with their physical environment, and (iii) energy flows through the system.

> Consider three examples of ecosystems. A coral reef comprises corals, fish, algae, and microorganisms interacting in a marine environment. A temperate forest contains trees, fungi, insects, birds, and mammals in a complex web of interdependence. A grassland savanna supports grasses, herbivores, and predators in a nutrient cycle driven by sunlight. From these cases one might define an ecosystem: a system comprising a community of living organisms that interact with one another and with their physical environment, through which energy flows.
>
> But consider a sealed glass terrarium sitting on a desk. It contains soil, mosses, small ferns, and soil microorganisms. The organisms interact with one another — the plants photosynthesise, the microorganisms decompose organic matter, and a miniature water cycle operates within the glass. Energy flows through the system from sunlight. The three conditions are satisfied. Yet the terrarium seems too small and too artificial to merit the name 'ecosystem' in the sense that a coral reef or a temperate forest does. The background cases were all large, naturally occurring, self-sustaining systems. The definition captured their functional properties — community, interaction, energy flow — but dropped the scale, complexity, and natural origin that characterised them, admitting miniature artificial arrangements alongside the great systems of the natural world.

*Abductive insight:* The background cases were all large-scale, naturally occurring systems. The definition captured the functional properties of these systems but dropped the scale and naturalness that characterised them, admitting miniature artificial systems alongside genuine ecosystems.

### 2. gene

**Definition:** A gene is a segment of DNA if and only if (i) it encodes a single protein, (ii) it is inherited as a unit, and (iii) it occupies a fixed position on a chromosome.

> Consider three cases of genes. The gene for eye colour in fruit flies is a segment of DNA that determines whether the fly has red or white eyes. The gene for sickle cell anaemia encodes the beta-globin protein, and a single mutation in this gene produces the disease. The gene for antibiotic resistance in bacteria encodes an enzyme that degrades the antibiotic. From these cases one might extract a definition: a gene is a segment of DNA that encodes a single protein, is inherited as a unit, and occupies a fixed position on a chromosome.
>
> But consider the phenomenon of alternative splicing, widespread in complex organisms. A single stretch of DNA may be transcribed and then spliced in different ways, producing two, three, or even dozens of distinct proteins from the same genetic locus. The first condition — that a gene encodes a single protein — fails entirely. Yet these stretches of DNA are unquestionably genes. The background cases were all examples of simple genes with a tidy one-to-one correspondence between DNA segment and protein product. The definition assumed this correspondence was universal, but molecular biology has shown that the relationship between gene and protein is far more complex: a single gene may encode many proteins, and conversely, a single protein may require the coordinated action of several genes.

*Abductive insight:* The background cases all involved simple genes with a one-to-one correspondence between DNA segment and protein. The definition assumed this correspondence was universal, but alternative splicing, overlapping reading frames, and non-coding RNA genes break the one-gene-one-protein rule.

### 3. extinction

**Definition:** A species is extinct if and only if (i) its population has been reduced to zero, (ii) the reduction was caused by an identifiable external pressure, and (iii) the species occupied a geographically restricted range at the time of its disappearance.

> Consider three cases of extinction. The dodo of Mauritius, a flightless bird, was hunted to extinction by sailors and the animals they introduced; no living individuals remain. The passenger pigeon, once perhaps the most numerous bird on earth, was driven to extinction by relentless commercial hunting; the last bird, named Martha, died in the Cincinnati Zoo in 1914. The thylacine of Tasmania was systematically destroyed through a government bounty programme; the last known individual died in the Hobart Zoo in 1936. From these cases one might extract a definition: a species is extinct if and only if its population has been reduced to zero, the reduction was caused by an identifiable external pressure, and the species occupied a geographically restricted range at the time of its disappearance.
>
> But this definition, drawn from island and regional extinctions, proves too narrow. Consider the extinction of the non-avian dinosaurs some sixty-six million years ago. Their population was reduced to zero, and the cause has been identified: the impact of a large asteroid and the catastrophic climatic disruption that followed. But the dinosaurs were not geographically restricted. They inhabited every continent, thriving in environments from tropical forests to polar regions. The third condition fails entirely. Yet the extinction of the dinosaurs is perhaps the most celebrated extinction event in the history of the earth. The background cases were all species confined to islands or small regions, and the definition mistook this incidental geographic restriction for an essential feature of extinction. A species may go extinct regardless of how wide its range, provided the external pressure is sufficiently global.

*Abductive insight:* The background cases all involved island or regionally confined species vulnerable to localised pressures. The definition abstracted geographic restriction as essential, when it was merely incidental to the particular examples chosen.

### 4. adaptation

**Definition:** A trait is an adaptation if and only if (i) it confers a current fitness advantage, (ii) it arose by natural selection, and (iii) its current function is the same as the function for which it was originally selected.

> Consider three cases of biological adaptation. The long neck of the giraffe enables it to browse on foliage that shorter-necked competitors cannot reach; the trait arose through natural selection for this feeding advantage. The thick blubber of the seal insulates the animal against the extreme cold of the ocean; this trait was selected for thermal regulation. The camouflage colouring of the peppered moth enables it to rest upon tree bark without being detected by predators; this colouring arose through selection for concealment. From these cases one might define adaptation: a trait is an adaptation if and only if it confers a current fitness advantage, it arose by natural selection, and its current function is the same as the function for which it was originally selected.
>
> But this definition, drawn from cases where current and original functions coincide, proves too restrictive. Consider the feathers of birds. Feathers confer an unmistakable fitness advantage: they enable flight, the defining capacity of most avian species. And feathers arose by natural selection. Yet the palaeontological evidence strongly suggests that feathers first evolved in theropod dinosaurs for thermal insulation — as a covering to retain body heat — long before any lineage took to the air. The current function of feathers (flight) differs from their original function (insulation). The third condition fails. Yet feathers are among the most celebrated adaptations in the biological world. The background cases all involved traits whose current use matched the purpose for which they were first selected; the definition mistook this coincidence for a universal requirement, excluding the many important traits that have been co-opted for functions their evolutionary history did not originally anticipate.

*Abductive insight:* The background cases all involved traits whose current function matched their original selective function. The definition assumed this match was universal, but many important adaptations have been co-opted for functions quite different from those for which they were first selected.

### 5. symbiosis

**Definition:** A biological association is symbiotic if and only if (i) it involves two species living in sustained physical proximity, (ii) each species provides a resource or service that the other requires, and (iii) the removal of either partner would harm the other.

> Consider three cases of biological symbiosis. The clown fish shelters among the stinging tentacles of the sea anemone, gaining protection from predators, while the anemone benefits from nutrients in the fish's waste. Mycorrhizal fungi colonise the roots of trees, supplying the tree with mineral nutrients from the soil while receiving sugars produced by the tree's photosynthesis. The oxpecker bird perches upon the rhinoceros, feeding on ticks and parasites that infest the animal's hide, thus benefiting both bird and beast. From these cases one might extract a definition: a biological association is symbiotic if and only if it involves two species living in sustained physical proximity, each species provides a resource or service that the other requires, and the removal of either partner would harm the other.
>
> Yet this definition, drawn exclusively from mutualistic partnerships, is too narrow. Consider the relationship between grazing cattle and the cattle egret. The egret follows the herd, feeding on insects and other small creatures disturbed from the grass by the cattle's movement. The association is sustained: the egrets return to the herd daily and maintain their proximity throughout the grazing period. The egret benefits considerably, obtaining food it could not otherwise access. But the cattle derive no measurable benefit from the egret's attendance, and the removal of the egrets would not harm the cattle in any observable way. The second and third conditions fail for one of the two partners. Yet the relationship is classified by biologists as commensal symbiosis. The background cases were all reciprocally beneficial; the definition treated this reciprocity as essential, when in truth symbiosis encompasses a broader range of interspecific associations, including those in which the benefit flows in one direction only.

*Abductive insight:* The background cases were all mutualistic associations in which both partners demonstrably benefited. The definition treated reciprocal benefit as essential, but symbiosis in its broader biological sense encompasses commensalism, in which only one partner benefits and the other is merely unaffected.

*... and 74 more AbdCx examples in [`data/abdcx/natural_science.jsonl`](../data/abdcx/natural_science.jsonl)*
