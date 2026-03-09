# Ethics

**220 DefCx** + **85 AbdCx** = **305 examples**

**Subdomains:** autonomy, benevolence, charity, complicity, consent, courage, cowardice, cruelty, desert, duty, envy, exploitation, forgiveness, gratitude, honesty, integrity, justice, loyalty, mercy, moral luck, moral obligation, moral responsibility, paternalism, promise keeping, prudence, punishment, reparation, rights, shame, supererogation, temperance, virtue theory

---

## DefCx Examples

Each example presents a definition as necessary and sufficient conditions, then constructs a scenario that reveals the definition's insufficiency.

### 1. virtue theory

**Definition:** An action is virtuous if and only if (i) it proceeds from a stable disposition of character, (ii) it is done knowingly, and (iii) it is done for its own sake.

> The proposed analysis holds that an action is virtuous if and only if it proceeds from a stable disposition of character, is done knowingly, and is done for its own sake. Upon examination, however, one may construct a case which reveals the insufficiency of this analysis. Consider a man who, from a stable disposition of generosity, knowingly gives a large sum to what he takes to be a charitable organisation, and does so purely for its own sake. Unknown to him, the organisation is fraudulent, and his money serves only to enrich its directors. The three conditions are satisfied — the action proceeds from a stable disposition, is done knowingly, and is done for its own sake — yet we should hesitate to call the action virtuous, for it achieves nothing of value and was directed at a phantom object. The definition, it appears, fails to account for the requirement that the object of the virtuous action be genuine.

*Missing condition:* The object of the virtuous action must be genuine, not illusory.

### 2. justice

**Definition:** A distribution of goods is just if and only if (i) each person receives a share proportional to his contribution, (ii) no person is arbitrarily excluded, and (iii) the distribution is made by a competent authority.

> It is sometimes proposed that a distribution of goods is just if and only if each person receives a share proportional to his contribution, no person is arbitrarily excluded, and the distribution is made by a competent authority. Yet one may imagine a case in which these three conditions are satisfied and the resulting distribution is nonetheless unjust. Suppose a factory owner, recognised as a competent authority, distributes wages in strict proportion to each worker's output, and excludes no one from the arrangement. The proportions are scrupulously observed. But the base rate of compensation is set so low that even the most industrious worker cannot earn enough to feed his family. The three conditions are met — proportionality is maintained, nobody is excluded, and the authority is legitimate — yet one feels strongly that the distribution is unjust. It appears that the definition fails to capture a requirement of minimal adequacy: that the shares, however proportional, must not fall below a threshold beneath which human dignity is affronted.

*Missing condition:* The distribution must meet a minimum threshold of adequacy for each participant.

### 3. moral obligation

**Definition:** A person is morally obligated to perform an action if and only if (i) he is aware that another person is in need, (ii) he has the capacity to help, and (iii) the cost to himself is not excessive.

> One might propose that a person is morally obligated to perform an action if and only if he is aware that another person is in need, he has the capacity to help, and the cost to himself is not excessive. This analysis, though initially plausible, admits of cases that strain our moral intuitions. Consider a physician who reads in the morning paper that a man in a distant country requires a kidney transplant. The physician is aware of the need, possesses the surgical skill to help, and the cost to himself — the inconvenience of travel, say — is not, by most reckonings, excessive. The three conditions are satisfied. Yet we should hesitate to say that the physician is morally obligated to travel across the world to perform the operation. The definition has failed to capture the role of proximity and special relationship in generating obligations; without such a condition, the analysis would impose upon every capable person an obligation to assist every needy stranger, which seems an unacceptable conclusion.

*Missing condition:* There must be some special relationship or proximity between the agent and the person in need.

### 4. consent

**Definition:** Consent is valid if and only if (i) it is given voluntarily, (ii) the consenting party is competent, and (iii) it is expressed in a recognised form.

> It is natural to suppose that consent is valid if and only if it is given voluntarily, the consenting party is competent, and it is expressed in a recognised form. Yet this analysis may be shown to be insufficient. Suppose a competent adult is asked to participate in a medical trial. He is told, falsely, that the trial involves a harmless dietary supplement, when in fact it involves an experimental drug with serious risks. He voluntarily signs the consent form — a recognised instrument — and does so with full mental competence. The three conditions are satisfied: the consent is voluntary, the party is competent, and the form is proper. Yet we should surely deny that his consent is valid, for he has consented to something quite different from what he was led to believe. The definition, it appears, omits a crucial requirement: that the consenting party be adequately informed about the nature of the matter to which he gives his consent.

*Missing condition:* The consenting party must be adequately informed about the nature of what he consents to.

### 5. desert

**Definition:** A person deserves a reward if and only if (i) he has performed a meritorious action, (ii) the action was within his control, and (iii) the reward is proportionate to the merit of the action.

> One is tempted to say that a person deserves a reward if and only if he has performed a meritorious action, the action was within his control, and the reward is proportionate to the merit of the action. But consider the following case. A wealthy merchant, hearing that the town council offers a prize for the most generous benefactor, donates a large sum to the local hospital — an indisputably meritorious action, entirely within his control. The prize he receives is proportionate to the merit of his donation. The three conditions are thus satisfied. Yet when it is discovered that the merchant's sole motive was to win the prize, and that he cares nothing for the hospital or its patients, one feels that his desert is diminished. He did the right thing, but for the wrong reason. The analysis, it seems, fails to capture the requirement that desert attaches not merely to the outward action but to the motive from which it springs. A man who does good only for the sake of reward does not deserve the reward in the fullest sense.

*Missing condition:* The meritorious action must proceed from an appropriate motive, not merely from desire for the reward itself.

*... and 215 more DefCx examples in [`data/defcx/ethics.jsonl`](../data/defcx/ethics.jsonl)*

---

## AbdCx Examples

Each example presents background cases that motivate a definition, then constructs a scenario revealing what the background cases shared but the definition missed.

### 1. punishment

**Definition:** Punishment is just if and only if (i) the person punished has committed an offence, (ii) the punishment is imposed by a legitimate authority, and (iii) the severity is proportional to the gravity of the offence.

> Consider the following cases of punishment. A thief is sentenced to imprisonment for stealing; we judge this just. A murderer is executed for his crime; this too strikes us as fitting. A negligent driver who causes an accident is fined; again, this seems appropriate. From such cases, one might extract the following definition: punishment is just if and only if the person punished has committed an offence, the punishment is imposed by a legitimate authority, and the severity of the punishment is proportional to the gravity of the offence.
>
> Yet this analysis, for all its plausibility, may be challenged. Consider a case in which a man committed a crime many years ago — a theft, let us say — and has since reformed entirely, becoming a benefactor to his community. He is discovered and punished according to the three conditions: he did commit the offence, the authority is legitimate, and the punishment is proportional. Yet many would doubt whether this punishment is just, for the man who is punished is in a relevant sense not the man who committed the crime. The background cases from which we drew our definition all involved punishment proximate to the offence; our definition failed to capture this temporal condition, and accordingly admits cases that strain our intuitions about justice.

*Abductive insight:* The background cases all involved punishment proximate to the offence. The definition dropped the temporal condition, admitting cases where punishment and offence are separated by fundamental personal change.

### 2. moral responsibility

**Definition:** A person is morally responsible for a harmful outcome if and only if (i) his action caused the outcome, (ii) he acted voluntarily, and (iii) he could have acted otherwise.

> Consider the following cases of moral responsibility. A man who deliberately trips a passer-by is held responsible for the resulting injury. A woman who knowingly sells spoiled food is held responsible for the illness it causes. A driver who recklessly speeds through a village is held responsible for striking a pedestrian. From these cases one might abstract the following definition: a person is morally responsible for a harmful outcome if and only if his action caused the outcome, he acted voluntarily, and he could have acted otherwise.
>
> But this definition proves too broad. Suppose a man, practising his marksmanship, fires a rifle at a target set up in a remote field. He acts voluntarily, he could have refrained, and his bullet strikes and injures a person who, unknown to the marksman, was concealed behind the target. His action caused the harm. The three conditions are satisfied. Yet we should hesitate to hold him morally responsible in the fullest sense, for the harm was entirely unforeseeable. The background cases from which we drew our definition all involved agents who could foresee, or ought to have foreseen, the harmful consequences of their actions. The definition failed to capture this element of foreseeability, and accordingly admits cases in which responsibility seems attenuated or absent.

*Abductive insight:* The background cases all involved agents who could foresee, or should have foreseen, the harmful consequence of their actions. The definition dropped the foreseeability condition.

### 3. moral luck

**Definition:** An agent is morally blameworthy for an outcome if and only if (i) the agent performed a voluntary action, (ii) the action caused the harmful outcome, and (iii) the agent intended the outcome or was reckless as to its occurrence.

> Consider three cases of moral blame. A marksman aims carefully and kills his target; we blame him for the death. A thief plans and executes a robbery; we blame him for the theft. A perjurer gives false testimony deliberately; we blame him for the injustice that follows. From these cases one might extract a definition: an agent is morally blameworthy for an outcome if and only if the agent performed a voluntary action, the action caused the harmful outcome, and the agent intended the outcome or was reckless as to its occurrence.
>
> Yet this analysis is embarrassed by a simple variant. Suppose two drivers, equally reckless, each run the same red light at the same speed on the same road. The first passes through without incident, for no pedestrian happens to be crossing. The second strikes and kills a pedestrian who steps into the road at the fatal moment. Both performed voluntary actions; both were reckless as to the risk. But only the second caused a death. The definition assigns full blame to the second and none — or at most, blame for the recklessness alone — to the first. Yet the only difference between them is a matter of fortune: the presence or absence of a pedestrian at a particular instant. One might observe that the background cases from which the definition was drawn all involved scenarios in which the agent's conduct reliably produced the harmful result — there was no gap between culpable action and harmful consequence for luck to occupy. The definition captured the tight coupling of agency and outcome but failed to accommodate cases in which identical conduct issues in radically different results by sheer contingency.

*Abductive insight:* The background cases all involved agents whose voluntary actions reliably produced the harmful outcomes. The definition captured agency, causation, and culpable mental state but dropped the implicit assumption that outcome and effort are correlated, leaving it unable to handle cases where identical conduct yields different results by sheer fortune.

### 4. supererogation

**Definition:** An action is morally praiseworthy if and only if (i) it conforms to a recognised moral obligation, (ii) the agent performs it from a sense of duty, and (iii) the performance involves overcoming some difficulty or temptation.

> Consider three cases of praiseworthy conduct. A man repays a debt punctually, even when he might plausibly have delayed; we commend him. A woman tells a difficult truth when asked, though evasion would have been easier; we praise her honesty. A citizen obeys a just but burdensome law; we regard him as dutiful. From these cases one might extract the following definition: an action is morally praiseworthy if and only if it conforms to a recognised moral obligation, the agent performs it from a sense of duty, and the performance involves overcoming some difficulty or temptation.
>
> Yet consider a case that falls outside the reach of this analysis. A stranger walking along a riverbank sees a child being swept away by floodwaters. Without hesitation he dives into the torrent, at grave risk to his own life, and succeeds in pulling the child to safety. No recognised moral obligation requires a man to risk his life for a stranger's child; no code of conduct prescribes such extreme self-sacrifice. The man acts not from a sense of duty — he has no time for deliberation — but from spontaneous compassion. The first condition is plainly unsatisfied, and the second is doubtful. Yet the action is praiseworthy in the highest degree, surpassing in our moral estimation the punctual repayment of debts and the telling of difficult truths. The background cases from which the definition was drawn were all instances of compliance with obligation; the definition therefore confined praiseworthiness to the sphere of duty and failed to accommodate actions that go beyond what any obligation demands.

*Abductive insight:* The background cases were all instances of compliance with recognised obligations. The definition captured the praiseworthy as the dutiful-despite-difficulty, but dropped the possibility that praiseworthiness might attach to actions that exceed obligation entirely — the supererogatory.

### 5. gratitude

**Definition:** Gratitude is the appropriate response to another's action if and only if (i) the other has provided a benefit to oneself, (ii) the provision was voluntary, and (iii) the provision involved some cost or effort on the other's part.

> Consider three cases in which gratitude seems the natural response. A neighbour lends his tools freely when asked, and the borrower feels grateful. A teacher gives extra lessons to a struggling pupil without charge, and the pupil's parents are grateful. A stranger gives directions to a lost traveller, and the traveller feels a warm moment of appreciation. From these cases one might define the conditions under which gratitude is appropriate: gratitude is the fitting response to another's action if and only if the other has provided a benefit, the provision was voluntary, and it involved some cost or effort on the other's part.
>
> Yet this analysis is challenged by a case of the following sort. In a footrace, a competitor stumbles and, in falling, inadvertently blocks a rival who would otherwise have overtaken the runner in third place. The third-place runner benefits materially — he finishes in a better position than he would otherwise have achieved. The fallen competitor's participation in the race was voluntary, and running a race certainly involves effort. All three conditions are satisfied. Yet it would be absurd to suggest that the third-place runner ought to feel grateful to the man who stumbled; the benefit was entirely accidental, a by-product of misfortune rather than of any intention to help. The background cases from which the definition was drawn all involved benefactors who intended the benefit they conferred. The definition captured the outward features — voluntariness, effort, benefit — but dropped the requirement of beneficent intent, which is essential if gratitude is to be more than appreciation of fortunate coincidence.

*Abductive insight:* The background cases all involved agents who intended the benefit they conferred. The definition captured voluntariness and cost but omitted the requirement that the benefactor have intended to benefit the recipient — that the benefit not be merely a fortunate by-product of unrelated action.

*... and 80 more AbdCx examples in [`data/abdcx/ethics.jsonl`](../data/abdcx/ethics.jsonl)*
