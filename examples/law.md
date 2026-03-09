# Law

**223 DefCx** + **74 AbdCx** = **297 examples**

**Subdomains:** agency legal, arbitration, bailment, causation, consent, contract, covenant, criminal intent, due process, duress, easement, equity, estoppel, evidence legal, fiduciary duty, fraud, good faith, habeas corpus, indemnity, injunction, jurisdiction, liability, lien, negligence, ownership, person, precedent, property, restitution, self defence, statutory interpretation, surety, testimony legal, tort

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. contract

**Definition:** An agreement is a valid contract if and only if (i) there is an offer and acceptance, (ii) there is consideration, and (iii) both parties have the capacity to contract.

> The orthodox analysis holds that an agreement is a valid contract if and only if there is an offer and acceptance, there is consideration, and both parties have the capacity to contract. These three conditions, taken together, are said to constitute the essential elements of a binding agreement. Yet the analysis is incomplete. Consider two competent adults who agree that one shall sell to the other a painting which both know to have been stolen from a public gallery. There is an offer (to sell the painting) and an acceptance (to buy it). There is consideration (the agreed price). Both parties are competent adults with full capacity to contract. The three conditions are met. Yet no court would enforce this agreement, for its object is illegal. The definition has omitted a condition that is essential to the validity of any contract: that its object be lawful. Without this requirement, the analysis would validate agreements whose enforcement would be contrary to public policy and the rule of law.

*Missing condition:* The object of the contract must be lawful; a contract for an illegal purpose is void regardless of the presence of offer, acceptance, consideration, and capacity.

### 2. negligence

**Definition:** A person is negligent if and only if (i) he owes a duty of care to another, (ii) he breaches that duty by failing to exercise reasonable care, and (iii) his breach causes harm to the other.

> It is said that a person is negligent if and only if he owes a duty of care to another, he breaches that duty by failing to exercise reasonable care, and his breach causes harm to the other. The third condition — causation — is more treacherous than it may appear. Consider a physician who, owing a duty of care to his patient, prescribes the wrong medication. This is plainly a breach. But an attentive pharmacist notices the error and dispenses the correct drug. The patient suffers no harm. The first two conditions are satisfied, but the third fails, and we rightly say the physician was careless but not, in the legal sense, negligent — for negligence in law requires actual damage. Now consider a different case: a physician prescribes the wrong drug, the patient takes it, and the patient dies. But investigation reveals that the patient's illness was terminal and that he would have died at the same time regardless of which drug he took. The breach did not cause the harm. The definition requires that the breach be the cause of the harm, and this requirement of causation proves far more difficult to apply than the bare statement of the condition would suggest.

*Missing condition:* The breach must be the proximate cause of the harm, not merely a but-for cause; and harm must actually result.

### 3. self defence

**Definition:** The use of force in self-defence is justified if and only if (i) the defender faces an imminent threat, (ii) the force used is proportional to the threat, and (iii) there is no reasonable alternative to the use of force.

> The doctrine of self-defence holds that the use of force is justified if and only if the defender faces an imminent threat, the force used is proportional to the threat, and there is no reasonable alternative to the use of force. Yet consider a case in which a man, walking at night, is approached by a stranger who reaches into his coat. The man, reasonably believing that the stranger is drawing a weapon, strikes him. The force is proportional to the perceived threat, and there is no time to retreat. But it transpires that the stranger was reaching for a cigarette case, and there was no threat at all. The first condition — that the defender face an imminent threat — is not met, for there was in fact no threat. Yet many would say, and most legal systems would agree, that the man's use of force was justified, for his belief in the imminence of the threat was reasonable. The definition, as stated, requires an actual threat, but the moral and legal justification of self-defence turns on the reasonableness of the belief, not on the objective reality of the danger.

*Missing condition:* Justification may rest on a reasonable belief in the existence of a threat, not on the actual existence of the threat.

### 4. property

**Definition:** A person owns a piece of property if and only if (i) he has legal title to it, (ii) he has the right to exclude others from it, and (iii) he has the right to transfer it to another.

> It is commonly said that a person owns a piece of property if and only if he has legal title to it, he has the right to exclude others from it, and he has the right to transfer it to another. But the concept of ownership is more nuanced than this analysis suggests. Consider a landowner who holds legal title to his estate and may transfer it as he pleases. However, an ancient right of way runs across his land, permitting his neighbours to cross it. His right to exclude is thereby limited — he cannot bar his neighbours from the path. The second condition is only partially met. Yet we do not deny that he owns the land. Now consider the converse case: a man occupies a piece of land for thirty years, cultivating it, excluding trespassers, and treating it in every respect as his own. Under the doctrine of adverse possession, the law may recognise his claim even though he never held legal title. The first condition fails entirely. The definition has treated ownership as an all-or-nothing matter, when in truth it is a bundle of rights that may be held in varying combinations and degrees.

*Missing condition:* Ownership is a bundle of rights that may be held in degrees; the conditions are typically present but not all strictly necessary in every case.

### 5. person

**Definition:** An entity is a legal person if and only if (i) it can hold rights, (ii) it can bear obligations, and (iii) it is a human being.

> A seemingly straightforward analysis holds that an entity is a legal person if and only if it can hold rights, can bear obligations, and is a human being. The first two conditions capture the functional core of legal personhood, but the third condition proves too restrictive. Consider a corporation. It can hold rights: it may own property, enter contracts, and sue for breach of those contracts. It can bear obligations: it must pay its debts, comply with regulations, and fulfil its contractual duties. The first two conditions are fully satisfied. But a corporation is not a human being; it is an artificial entity created by registration under the relevant statute. Yet in every modern legal system, a corporation is treated as a legal person, with standing to sue and be sued in its own name. The definition has confused legal personhood — a status conferred by law — with natural personhood. The law may attach the status of person to any entity it sees fit, and the class of legal persons has always been wider than the class of human beings.

*Missing condition:* Legal personhood is not restricted to human beings; it is a status conferred by law upon any entity that the legal system recognises as capable of holding rights and bearing obligations.

*... and 218 more DefCx examples in [`data/defcx/law.jsonl`](../data/defcx/law.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. causation

**Definition:** An event A is the cause of an event B if and only if (i) A occurred before B, (ii) but for A, B would not have occurred, and (iii) A and B are connected by a continuous chain of events.

> Consider three cases of causation in law. A man strikes another, who falls and breaks his arm; the blow caused the injury. A driver runs a red light and collides with a pedestrian; the driving caused the harm. A company dumps chemicals into a river, and downstream residents fall ill; the dumping caused the illness. From these cases one might extract a definition: an event A is the cause of an event B if and only if A occurred before B, but for A, B would not have occurred, and A and B are connected by a continuous chain of events.
>
> But this analysis falters in cases of overdetermination. Suppose two hunters, acting independently, fire at the same victim simultaneously. Either shot alone would have been fatal. The victim dies. Now apply the but-for test to hunter A: but for his shot, would the victim have died? Yes — from hunter B's shot. So the but-for condition is not satisfied. The same holds for hunter B. The but-for test exonerates both hunters, which is absurd — each plainly caused the death. The background cases all involved a single sufficient cause, and the but-for test works perfectly in such cases. The definition failed to anticipate situations where multiple independently sufficient causes converge, producing a result that each alone would have brought about.

*Abductive insight:* The background cases all involved a single sufficient cause. The definition's but-for test works when there is one cause but fails when there are multiple independently sufficient causes — a case the background examples did not include.

### 2. consent

**Definition:** Consent is legally valid if and only if (i) it is given voluntarily, (ii) the consenting party understands what he is consenting to, and (iii) the consent is expressed unambiguously.

> Consider three cases of valid consent. A patient agrees to surgery after the surgeon explains the risks; the consent is valid. A customer signs a lease after reading and understanding the terms; the consent is valid. A volunteer agrees to participate in a study after being briefed on the procedures; the consent is valid. From these cases one might define legal validity: consent is legally valid if and only if it is given voluntarily, the consenting party understands what he is consenting to, and the consent is expressed unambiguously.
>
> But consider a consumer who signs a contract with a large corporation. He reads the terms — all forty pages — and understands them. He signs voluntarily. His consent is unambiguous. The three conditions are met. But the terms are grossly one-sided: the consumer waives virtually all his rights, agrees to binding arbitration in a distant jurisdiction, and accepts unlimited liability for trivial breaches. No reasonable person, one feels, would agree to such terms if they were plainly presented, and yet the consumer did agree, voluntarily and knowingly. The background cases all involved agreements whose substantive terms were fair and reasonable; the definition captured the procedural dimension of consent — voluntariness, understanding, clarity — but dropped the substantive fairness that characterised the motivating examples. It admits agreements that are procedurally valid but substantively unconscionable.

*Abductive insight:* The background cases all involved agreements whose terms were substantively fair. The definition attended only to the process of consenting (voluntariness, understanding, expression) and dropped the substantive fairness that characterised the motivating cases.

### 3. liability

**Definition:** A person is liable for harm caused to another if and only if (i) the person performed an act or omission, (ii) the act or omission was a cause of the harm, and (iii) the person was at fault, whether through intention, negligence, or recklessness.

> Consider three cases in which liability follows from fault. A driver who runs a red light and injures a pedestrian is at fault, and liability attaches naturally. A surgeon who operates upon the wrong limb has been negligent, and the law holds the surgeon responsible for the resulting harm. A factory owner whose unsafe machinery injures a worker has failed in the duty to maintain safe conditions, and liability follows. From these cases one might define: a person is liable for harm caused to another if and only if the person performed an act or omission, the act or omission was a cause of the harm, and the person was at fault, whether through intention, negligence, or recklessness.
>
> But consider the celebrated case, drawn from the English reports, of a landowner who constructs a reservoir upon his land. The dam is carefully designed and competently built. Every reasonable precaution is taken. Yet the dam bursts, and the water floods the mines of a neighbouring landowner, causing extensive damage. The reservoir owner was not at fault in any ordinary sense: there was no negligence, no recklessness, no intention to cause harm. Yet the court held the owner liable, on the principle that a person who, for his own purposes, brings upon his land and collects there anything likely to do mischief if it escapes must keep it in at his peril, and is liable for all damage that is the natural consequence of its escape. The background cases all involved fault, and the definition required it. But the law recognises that certain activities are so inherently dangerous that responsibility for the consequences of their going wrong ought to rest on the person who undertook them, regardless of the care exercised. The definition failed to anticipate this category of strict liability.

*Abductive insight:* The background cases all involved clear fault on the part of the person held liable. The definition extracted fault as a necessary condition, but the law also imposes strict liability in cases where the activity is inherently dangerous, regardless of the care exercised by the defendant.

### 4. testimony legal

**Definition:** Testimony is reliable if and only if (i) the witness perceived the relevant events directly, (ii) the witness possesses the competence to understand and report what was perceived, and (iii) the witness's account is corroborated by other evidence.

> Consider three cases of accepted testimony. A bystander who witnessed a robbery from close range gives a clear account of the robber's appearance and actions; the court accepts the testimony. A doctor who examined the victim's injuries describes them with clinical precision; the expert testimony is admitted. A bank clerk who processed a fraudulent cheque identifies the signature as forged on the basis of professional experience; the testimony is received. In each case, the witness perceived the relevant events directly, possessed the competence to understand and report what was perceived, and the account was corroborated by other evidence — the stolen goods were recovered, the injuries matched the medical report, the forged signature was confirmed by a second expert. One might define: testimony is reliable if and only if the witness perceived the events directly, the witness is competent, and the account is corroborated.
>
> But suppose a woman walking alone at night is the sole witness to a hit-and-run accident. She perceived the events directly and with clarity. She is fully competent to understand and describe what she saw. Her account is detailed, consistent, and given promptly. Yet there is no corroborating evidence: no other witness, no relevant physical evidence, no camera footage. The third condition fails. Yet her testimony may be entirely reliable — accurate in every particular. The background cases all happened to involve corroboration, and the definition extracted this as a necessary condition. But reliability is a property of the testimony itself: its accuracy and its connection to what actually occurred. A single uncorroborated witness may give perfectly reliable testimony, and the law in many jurisdictions recognises that uncorroborated testimony may be sufficient to establish the facts.

*Abductive insight:* The background cases all happened to involve testimony supported by additional evidence. The definition extracted corroboration as a necessary condition, but reliability is a property of the testimony itself — its accuracy and trustworthiness — and a single uncorroborated witness may give perfectly reliable testimony.

### 5. statutory interpretation

**Definition:** A word in a statute bears its ordinary meaning if and only if (i) the word has a settled and commonly understood definition, (ii) that definition produces a sensible result when applied to the facts, and (iii) the context of the statute does not indicate a different meaning.

> Consider three cases in which the ordinary meaning of statutory language poses no difficulty. A statute forbids the sale of 'intoxicating liquors,' and a merchant selling whisky is prosecuted; 'intoxicating liquors' plainly includes whisky. A statute requires 'all buildings' to be insured against fire, and a warehouse owner who fails to insure is penalised; 'buildings' plainly includes warehouses. A statute imposes a tax on 'income from employment,' and a salaried clerk is assessed; the ordinary meaning of the words is clear. From these cases one might define: a word in a statute bears its ordinary meaning if and only if the word has a settled and commonly understood definition, that definition produces a sensible result when applied to the facts, and the context of the statute does not indicate a different meaning.
>
> But consider a statute enacted in the eighteenth century that grants certain rights to 'all persons.' The word 'persons' has a settled and commonly understood meaning today, and the context of the statute does not indicate any technical or restricted usage. The three conditions appear to be satisfied, and the word should bear its ordinary meaning. Yet when the statute was enacted, 'persons' was commonly understood in a far narrower sense, often excluding women, servants, and those without property. If one applies the modern ordinary meaning, the statute grants rights to all human beings; if one applies the historical ordinary meaning, the rights are restricted. The definition assumed that ordinary meaning is stable — that the settled definition of a word today is the same as it was when the statute was enacted. The background cases involved modern statutes whose language had not had time to shift. The definition failed to address the problem of linguistic change, which is among the most vexing difficulties in the interpretation of old statutes.

*Abductive insight:* The background cases all involved modern statutes applied shortly after enactment, where the ordinary meaning was stable and uncontested. The definition assumed that ordinary meaning is fixed, but language evolves, and a word in an old statute may bear a meaning quite different from its current ordinary sense.

*... and 69 more AbdCx examples in [`data/abdcx/law.jsonl`](../data/abdcx/law.jsonl)*
