#!/usr/bin/env python3
"""
Add LGBTQ+ representation to the cx-bot philosophical counterexample dataset.

Rewrites ~8 entries that assume heterosexual couples to include same-sex couples,
preserving the philosophical logic and analytic-philosophy register throughout.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── Replacement specifications ──────────────────────────────────────────────
# Each spec: (file_path, entry_id, {field: (old_text, new_text), ...})

REPLACEMENTS = [
    # ── 1. defcx_ethics_forgiveness_2804 ── Female same-sex couple ──────────
    (
        ROOT / "data" / "defcx" / "ethics.jsonl",
        "defcx_ethics_forgiveness_2804",
        {
            "counterexample": (
                "Consider a wife whose husband has been unfaithful. She tells him she forgives him, and she sincerely means it. She relinquishes any wish for retribution and does not hold the wrong against him. Years pass, and though she never again raises the matter and bears no conscious resentment, she finds that she cannot trust him as she once did. Her involuntary wariness — a flinch when he is late, an anxious glance at his correspondence — persists despite her genuine desire to forgive completely. All three conditions are met: resentment has ceased, retribution has been relinquished, and forgiveness has been communicated. Yet one might hesitate to say that forgiveness is complete, for the residual distrust bespeaks a wound that the definition cannot register.",
                "Consider a woman whose wife has been unfaithful. She tells her she forgives her, and she sincerely means it. She relinquishes any wish for retribution and does not hold the wrong against her. Years pass, and though she never again raises the matter and bears no conscious resentment, she finds that she cannot trust her wife as she once did. Her involuntary wariness — a flinch when her wife is late, an anxious glance at her correspondence — persists despite her genuine desire to forgive completely. All three conditions are met: resentment has ceased, retribution has been relinquished, and forgiveness has been communicated. Yet one might hesitate to say that forgiveness is complete, for the residual distrust bespeaks a wound that the definition cannot register.",
            ),
            "passage": (
                "One might define genuine forgiveness as the cessation of resentment, the relinquishment of claims to retribution, and the communication of pardon. This definition has the merit of identifying the principal elements that distinguish forgiveness from mere forbearance or strategic overlooking. The person who forgives does not merely refrain from punishment; she surrenders her resentment and lets the wrongdoer know it. Yet a case which reveals the insufficiency of this characterisation arises in the domain of intimate betrayal. Suppose a wife whose husband has been unfaithful tells him, with complete sincerity, that she forgives him. She relinquishes any desire for retribution. She does not raise the matter again, and she bears no conscious resentment. All three conditions are satisfied. Yet years later, she discovers that she cannot trust her husband as she once did. When he is late returning home, she feels an involuntary anxiety. When she notices an unfamiliar name on his correspondence, her heart quickens. These responses persist despite her genuine desire to forgive fully, and despite the absence of any conscious resentment. One might observe that what remains is not resentment but its residue — an involuntary wariness that is not within the control of the will. The definition, by requiring only the cessation of resentment, the relinquishment of retribution, and the communication of pardon, captures the deliberate and volitional aspects of forgiveness but does not address the involuntary emotional aftermath that may persist long after the will has done its work. It appears that forgiveness, in its fullest sense, involves something more than the definition provides — the restoration of a trust that cannot simply be willed into existence.",
                "One might define genuine forgiveness as the cessation of resentment, the relinquishment of claims to retribution, and the communication of pardon. This definition has the merit of identifying the principal elements that distinguish forgiveness from mere forbearance or strategic overlooking. The person who forgives does not merely refrain from punishment; she surrenders her resentment and lets the wrongdoer know it. Yet a case which reveals the insufficiency of this characterisation arises in the domain of intimate betrayal. Suppose a woman whose wife has been unfaithful tells her, with complete sincerity, that she forgives her. She relinquishes any desire for retribution. She does not raise the matter again, and she bears no conscious resentment. All three conditions are satisfied. Yet years later, she discovers that she cannot trust her wife as she once did. When her wife is late returning home, she feels an involuntary anxiety. When she notices an unfamiliar name on her wife's correspondence, her heart quickens. These responses persist despite her genuine desire to forgive fully, and despite the absence of any conscious resentment. One might observe that what remains is not resentment but its residue — an involuntary wariness that is not within the control of the will. The definition, by requiring only the cessation of resentment, the relinquishment of retribution, and the communication of pardon, captures the deliberate and volitional aspects of forgiveness but does not address the involuntary emotional aftermath that may persist long after the will has done its work. It appears that forgiveness, in its fullest sense, involves something more than the definition provides — the restoration of a trust that cannot simply be willed into existence.",
            ),
        },
    ),
    # ── 2. defcx_ethics_paternalism_0208 ── Male same-sex couple ────────────
    (
        ROOT / "data" / "defcx" / "ethics.jsonl",
        "defcx_ethics_paternalism_0208",
        {
            "counterexample": (
                "A wife, knowing that her husband is about to make a disastrous business decision, withholds from him a letter containing the offer he intends to accept, and replaces it with a forged letter declining the offer. She does not restrict his liberty — he is free to go where he pleases, to make telephone calls, to visit the other party. What she restricts is his access to information. The first condition fails in its literal sense, for no liberty of movement or action is curtailed. Yet her action is paradigmatically paternalistic: she manipulates his circumstances for what she takes to be his own good, without his consent.",
                "A man, knowing that his husband is about to make a disastrous business decision, withholds from him a letter containing the offer he intends to accept, and replaces it with a forged letter declining the offer. He does not restrict his husband's liberty — his husband is free to go where he pleases, to make telephone calls, to visit the other party. What he restricts is his husband's access to information. The first condition fails in its literal sense, for no liberty of movement or action is curtailed. Yet his action is paradigmatically paternalistic: he manipulates his husband's circumstances for what he takes to be his husband's own good, without his consent.",
            ),
            "passage": (
                "A natural definition of paternalism holds that an action is paternalistic if and only if it restricts the liberty of another person, the restriction is imposed for that person's own good, and the restriction is imposed without that person's consent. This captures the familiar cases: the state that forbids the use of certain drugs for the citizen's own health, the parent who locks the door to prevent a child from running into the street. In each case liberty is curtailed, the motive is benevolent, and consent is absent. Yet the definition proves too narrow. Consider a wife who knows that her husband is about to accept a disastrous business offer. Rather than forbidding him or physically restraining him, she intercepts the letter containing the offer and replaces it with a forged letter declining on his behalf. The husband's liberty is not restricted in any ordinary sense: he is free to go where he pleases, to make his own decisions, to act as he sees fit. What has been restricted is his access to accurate information. He acts freely but upon a false picture of the world that his wife has deliberately constructed. The first condition fails if 'liberty' is understood as freedom of action. Yet the wife's behaviour is paradigmatically paternalistic. She has manipulated his circumstances for what she takes to be his own good, without his knowledge or consent. The definition has modelled paternalism upon coercive interference and has thereby overlooked the manipulative and deceptive varieties, which may be equally objectionable.",
                "A natural definition of paternalism holds that an action is paternalistic if and only if it restricts the liberty of another person, the restriction is imposed for that person's own good, and the restriction is imposed without that person's consent. This captures the familiar cases: the state that forbids the use of certain drugs for the citizen's own health, the parent who locks the door to prevent a child from running into the street. In each case liberty is curtailed, the motive is benevolent, and consent is absent. Yet the definition proves too narrow. Consider a man who knows that his husband is about to accept a disastrous business offer. Rather than forbidding him or physically restraining him, he intercepts the letter containing the offer and replaces it with a forged letter declining on his husband's behalf. The husband's liberty is not restricted in any ordinary sense: he is free to go where he pleases, to make his own decisions, to act as he sees fit. What has been restricted is his access to accurate information. He acts freely but upon a false picture of the world that his partner has deliberately constructed. The first condition fails if 'liberty' is understood as freedom of action. Yet his partner's behaviour is paradigmatically paternalistic. He has manipulated his husband's circumstances for what he takes to be his husband's own good, without his knowledge or consent. The definition has modelled paternalism upon coercive interference and has thereby overlooked the manipulative and deceptive varieties, which may be equally objectionable.",
            ),
        },
    ),
    # ── 3. defcx_ethics_promise_keeping_0468 ── Male same-sex couple ────────
    (
        ROOT / "data" / "defcx" / "ethics.jsonl",
        "defcx_ethics_promise_keeping_0468",
        {
            "counterexample": (
                "Suppose that a man promises his dying wife that he will never remarry. At the time of promising, the action — refraining from remarriage — is certainly possible. The promise is made freely, by a competent adult, to a competent adult. All three conditions are satisfied. But twenty years later, circumstances have changed profoundly: the man is lonely, his children have grown and departed, and he has met a woman who would make him a good companion. One might ask whether the promise remains binding in these altered circumstances, and many persons of good moral sense would say that it does not — that a promise made to a dying spouse, decades ago, under the pressure of extreme emotion, ought not to govern the whole of the rest of one's life. The definition provides no resources for releasing the promisor, for all three conditions were satisfied.",
                "Suppose that a man promises his dying husband that he will never remarry. At the time of promising, the action — refraining from remarriage — is certainly possible. The promise is made freely, by a competent adult, to a competent adult. All three conditions are satisfied. But twenty years later, circumstances have changed profoundly: the man is lonely, his children have grown and departed, and he has met a man who would make him a good companion. One might ask whether the promise remains binding in these altered circumstances, and many persons of good moral sense would say that it does not — that a promise made to a dying spouse, decades ago, under the pressure of extreme emotion, ought not to govern the whole of the rest of one's life. The definition provides no resources for releasing the promisor, for all three conditions were satisfied.",
            ),
            "passage": (
                "One might hold that a promise is binding if and only if the promisor and promisee are both competent adults, the promise was made freely and without coercion, and the promised action is possible at the time of promising. This definition appears to state necessary and sufficient conditions for the bindingness of a promise. And in many cases it serves well enough. But consider a person who promises his dying wife that he will never remarry. At the time of the promise, all three conditions are satisfied. Both are competent adults. The promise is made freely — the wife asks, and the husband, moved by love and grief, gives his word. The action is possible: he can refrain from remarriage. The promise is binding. But twenty years pass. The wife has long been dead. The man's children have grown and departed. He lives alone, in circumstances his wife could not have foreseen. He meets a woman of excellent character who would be a true companion to him in his remaining years. Must he refuse her, and live in solitude, because of words spoken two decades ago at a deathbed? Many persons of mature moral judgement would say that the promise, though genuinely binding at its making, has been overtaken by changes so profound that it no longer commands observance. Yet the definition provides no mechanism for release. It states the conditions under which a promise is binding but says nothing about the conditions under which it may cease to be so. It captures the genesis of obligation but not its dissolution.",
                "One might hold that a promise is binding if and only if the promisor and promisee are both competent adults, the promise was made freely and without coercion, and the promised action is possible at the time of promising. This definition appears to state necessary and sufficient conditions for the bindingness of a promise. And in many cases it serves well enough. But consider a person who promises his dying husband that he will never remarry. At the time of the promise, all three conditions are satisfied. Both are competent adults. The promise is made freely — the husband asks, and his partner, moved by love and grief, gives his word. The action is possible: he can refrain from remarriage. The promise is binding. But twenty years pass. The husband has long been dead. The man's children have grown and departed. He lives alone, in circumstances his husband could not have foreseen. He meets a man of excellent character who would be a true companion to him in his remaining years. Must he refuse him, and live in solitude, because of words spoken two decades ago at a deathbed? Many persons of mature moral judgement would say that the promise, though genuinely binding at its making, has been overtaken by changes so profound that it no longer commands observance. Yet the definition provides no mechanism for release. It states the conditions under which a promise is binding but says nothing about the conditions under which it may cease to be so. It captures the genesis of obligation but not its dissolution.",
            ),
        },
    ),
    # ── 4. defcx_ethics_virtue_theory_1300 ── Female same-sex couple ────────
    (
        ROOT / "data" / "defcx" / "ethics.jsonl",
        "defcx_ethics_virtue_theory_1300",
        {
            "counterexample": (
                "Consider the virtue of courage. A soldier who throws himself upon a grenade to save his comrades acts from a stable disposition and does so voluntarily. Yet the consequence for the soldier himself is death. The action produces beneficial consequences for those around him, but one might equally note that the soldier's children are left fatherless and his wife a widow; the consequences, taken in their totality, are a mixture of benefit and harm. More troubling still is the case of a person who courageously tells an unpopular truth that brings ruin upon himself and distress to his audience. The third condition fails, yet courage remains a virtue.",
                "Consider the virtue of courage. A soldier who throws herself upon a grenade to save her comrades acts from a stable disposition and does so voluntarily. Yet the consequence for the soldier herself is death. The action produces beneficial consequences for those around her, but one might equally note that the soldier's children are left motherless and her wife a widow; the consequences, taken in their totality, are a mixture of benefit and harm. More troubling still is the case of a person who courageously tells an unpopular truth that brings ruin upon herself and distress to her audience. The third condition fails, yet courage remains a virtue.",
            ),
            "passage": (
                "One might propose that a character trait is a virtue if and only if it is a stable disposition, exercised voluntarily, that produces beneficial consequences for those affected by the agent's actions. The definition captures a good deal of what is ordinarily meant by virtue. Generosity is a stable disposition; the generous man gives freely and by choice; and the recipients of his generosity are benefited. Honesty, similarly, is a settled feature of character; the honest man speaks the truth voluntarily; and those who rely upon his word are well served by his truthfulness. Yet one must consider courage. A soldier who throws himself upon a live grenade to save his comrades acts from a stable disposition of character — he is not merely startled into action — and he does so voluntarily, by a deliberate act of will. But the consequences of his action are not uniformly beneficial. His comrades are saved, to be sure, but the soldier himself is killed. His children are left without a father, his wife without a husband, and his parents without a son. The consequences, taken in their totality, are a mixture of benefit and harm, and it is by no means obvious that the beneficial consequences outweigh the harmful ones. One might consider, further, the case of a person who tells an unpopular truth — who speaks out against a powerful injustice at great personal cost. His honesty brings no benefit to his audience, who are distressed and angered by what he says, and it brings ruin upon himself. The third condition of the definition fails. The analysis has mistaken a frequent accompaniment of virtue for its essence. What makes courage a virtue is not that it tends to produce good consequences but that it is intrinsically noble — that it involves the willing acceptance of danger in the service of something worthy.",
                "One might propose that a character trait is a virtue if and only if it is a stable disposition, exercised voluntarily, that produces beneficial consequences for those affected by the agent's actions. The definition captures a good deal of what is ordinarily meant by virtue. Generosity is a stable disposition; the generous man gives freely and by choice; and the recipients of his generosity are benefited. Honesty, similarly, is a settled feature of character; the honest man speaks the truth voluntarily; and those who rely upon his word are well served by his truthfulness. Yet one must consider courage. A soldier who throws herself upon a live grenade to save her comrades acts from a stable disposition of character — she is not merely startled into action — and she does so voluntarily, by a deliberate act of will. But the consequences of her action are not uniformly beneficial. Her comrades are saved, to be sure, but the soldier herself is killed. Her children are left without a mother, her wife without her partner, and her parents without a daughter. The consequences, taken in their totality, are a mixture of benefit and harm, and it is by no means obvious that the beneficial consequences outweigh the harmful ones. One might consider, further, the case of a person who tells an unpopular truth — who speaks out against a powerful injustice at great personal cost. His honesty brings no benefit to his audience, who are distressed and angered by what he says, and it brings ruin upon himself. The third condition of the definition fails. The analysis has mistaken a frequent accompaniment of virtue for its essence. What makes courage a virtue is not that it tends to produce good consequences but that it is intrinsically noble — that it involves the willing acceptance of danger in the service of something worthy.",
            ),
        },
    ),
    # ── 5. defcx_ethics_punishment_3805 ── Male same-sex couple ─────────────
    (
        ROOT / "data" / "defcx" / "ethics.jsonl",
        "defcx_ethics_punishment_3805",
        {
            "counterexample": (
                "Suppose a court of competent jurisdiction finds a man guilty of theft and sentences him to a fine proportionate to the offence. The sentence also serves a clear deterrent purpose, discouraging others from similar conduct. All three conditions are met. Yet suppose the man committed the theft under extreme duress — a criminal gang credibly threatened to kill his family unless he stole the goods in question. In such circumstances, we should hesitate to say that punishment is morally justified, for the man's wrongful act was compelled by circumstances that substantially diminished his moral culpability.",
                "Suppose a court of competent jurisdiction finds a man guilty of theft and sentences him to a fine proportionate to the offence. The sentence also serves a clear deterrent purpose, discouraging others from similar conduct. All three conditions are met. Yet suppose the man committed the theft under extreme duress — a criminal gang credibly threatened to kill his family unless he stole the goods in question. In such circumstances, we should hesitate to say that punishment is morally justified, for the man's wrongful act was compelled by circumstances that substantially diminished his moral culpability.",
            ),
            "passage": (
                "One might propose that punishment is morally justified whenever a competent authority has found the offender guilty, the penalty is proportionate, and the punishment serves a deterrent purpose. This formulation captures the institutional, proportional, and consequentialist elements that are commonly invoked in discussions of punitive justice. Yet a case which reveals the insufficiency of this proposal may be constructed by attending to the circumstances under which offences are committed. Suppose a man is brought before a court of competent jurisdiction and found guilty of theft. The court imposes a fine proportionate to the gravity of the offence, and the fine plainly serves a deterrent function: it discourages others from committing similar acts. All three conditions are met. Yet suppose it subsequently emerges that the man committed the theft under extreme duress. A criminal gang had credibly threatened to kill his wife and children unless he stole the goods in question. He acted not from greed or malice but from a desperate concern for the lives of his family, in circumstances where no lawful means of protection was available to him. In such a case, we should hesitate to say that the punishment is morally justified, notwithstanding the finding of guilt, the proportionality of the sentence, and its deterrent efficacy. It appears that the definition, by attending only to the institutional verdict, the proportionality of the penalty, and its deterrent function, cannot accommodate the moral relevance of the conditions under which the wrongful act was performed. One might observe that justification for punishment requires not merely that the offender be found guilty but that his moral culpability not be substantially diminished by extenuating circumstances.",
                "One might propose that punishment is morally justified whenever a competent authority has found the offender guilty, the penalty is proportionate, and the punishment serves a deterrent purpose. This formulation captures the institutional, proportional, and consequentialist elements that are commonly invoked in discussions of punitive justice. Yet a case which reveals the insufficiency of this proposal may be constructed by attending to the circumstances under which offences are committed. Suppose a man is brought before a court of competent jurisdiction and found guilty of theft. The court imposes a fine proportionate to the gravity of the offence, and the fine plainly serves a deterrent function: it discourages others from committing similar acts. All three conditions are met. Yet suppose it subsequently emerges that the man committed the theft under extreme duress. A criminal gang had credibly threatened to kill his husband and children unless he stole the goods in question. He acted not from greed or malice but from a desperate concern for the lives of his family, in circumstances where no lawful means of protection was available to him. In such a case, we should hesitate to say that the punishment is morally justified, notwithstanding the finding of guilt, the proportionality of the sentence, and its deterrent efficacy. It appears that the definition, by attending only to the institutional verdict, the proportionality of the penalty, and its deterrent function, cannot accommodate the moral relevance of the conditions under which the wrongful act was performed. One might observe that justification for punishment requires not merely that the offender be found guilty but that his moral culpability not be substantially diminished by extenuating circumstances.",
            ),
        },
    ),
    # ── 6. abdcx_ethics_punishment_0453 ── Female same-sex couple ───────────
    (
        ROOT / "data" / "abdcx" / "ethics.jsonl",
        "abdcx_ethics_punishment_0453",
        {
            "counterexample": (
                "Consider a case in which a man is sentenced to two years' imprisonment for a serious assault. The punishment satisfies all three conditions. But the man has a wife and three young children who depend entirely upon his earnings. His imprisonment plunges them into destitution. The punishment is directed solely at the offender, yet in practice it falls with terrible weight upon persons who have committed no wrong at all. The definition has no resources with which to address this difficulty, for it attends only to the relation between the punishment and the offender and takes no account of the collateral suffering visited upon the innocent.",
                "Consider a case in which a woman is sentenced to two years' imprisonment for a serious assault. The punishment satisfies all three conditions. But the woman has a wife and three young children who depend entirely upon her earnings. Her imprisonment plunges them into destitution. The punishment is directed solely at the offender, yet in practice it falls with terrible weight upon persons who have committed no wrong at all. The definition has no resources with which to address this difficulty, for it attends only to the relation between the punishment and the offender and takes no account of the collateral suffering visited upon the innocent.",
            ),
            "abductive_insight": (
                "The background cases all involved offenders whose punishment could be conceived as affecting them alone — the burglar, the fraudster, the assailant. The definition abstracted from these cases the principle that punishment is a transaction between the state and the wrongdoer. But the imprisoned father reveals that punishment rarely affects the offender alone; it radiates outward to dependants and associates, and a definition of just punishment that ignores these effects is incomplete, for justice must attend not only to the guilt of the offender but to the suffering of the innocent.",
                "The background cases all involved offenders whose punishment could be conceived as affecting them alone — the burglar, the fraudster, the assailant. The definition abstracted from these cases the principle that punishment is a transaction between the state and the wrongdoer. But the imprisoned mother reveals that punishment rarely affects the offender alone; it radiates outward to dependants and associates, and a definition of just punishment that ignores these effects is incomplete, for justice must attend not only to the guilt of the offender but to the suffering of the innocent.",
            ),
            "passage": (
                "Consider three cases of just punishment. A court sentences a burglar to six months' imprisonment. A tribunal orders a fraudster to repay what he stole and to perform community labour. A magistrate fines a man for assault, calibrating the fine to the severity of the injury. From these cases one might define just punishment: a punishment is just if and only if it is imposed upon a person found to have committed a specific wrong, its severity corresponds to the gravity of that wrong, and it is directed solely at the person who committed the wrong.\n\nBut this definition, drawn from cases in which the punishment could be conceived as touching the offender alone, proves inadequate when the punishment's effects extend beyond him. Consider a man sentenced to two years' imprisonment for a serious assault. He has committed a specific wrong. The sentence corresponds to its gravity. It is directed solely at him. All three conditions are satisfied. But the man has a wife and three young children who depend entirely upon his earnings. His imprisonment leaves them without income, without support, and without a father. They are plunged into hardship through no fault of their own. The definition pronounces the punishment just, for it attends only to the relation between the sentence and the offender, but it is silent about the destitution of the offender's family. The background cases involved offenders who could be imagined as isolated individuals, and the definition abstracted from these a conception of punishment as a bilateral affair between the wrongdoer and the authority that punishes him. It overlooked the plain fact that punishment rarely affects the offender alone. It radiates outward, falling upon wives, children, parents, and dependants who have committed no offence. A complete account of just punishment must reckon with these collateral consequences, for justice that is blind to the suffering of the innocent is justice of a very imperfect sort.",
                "Consider three cases of just punishment. A court sentences a burglar to six months' imprisonment. A tribunal orders a fraudster to repay what he stole and to perform community labour. A magistrate fines a man for assault, calibrating the fine to the severity of the injury. From these cases one might define just punishment: a punishment is just if and only if it is imposed upon a person found to have committed a specific wrong, its severity corresponds to the gravity of that wrong, and it is directed solely at the person who committed the wrong.\n\nBut this definition, drawn from cases in which the punishment could be conceived as touching the offender alone, proves inadequate when the punishment's effects extend beyond her. Consider a woman sentenced to two years' imprisonment for a serious assault. She has committed a specific wrong. The sentence corresponds to its gravity. It is directed solely at her. All three conditions are satisfied. But the woman has a wife and three young children who depend entirely upon her earnings. Her imprisonment leaves them without income, without support, and without a mother. They are plunged into hardship through no fault of their own. The definition pronounces the punishment just, for it attends only to the relation between the sentence and the offender, but it is silent about the destitution of the offender's family. The background cases involved offenders who could be imagined as isolated individuals, and the definition abstracted from these a conception of punishment as a bilateral affair between the wrongdoer and the authority that punishes her. It overlooked the plain fact that punishment rarely affects the offender alone. It radiates outward, falling upon spouses, children, parents, and dependants who have committed no offence. A complete account of just punishment must reckon with these collateral consequences, for justice that is blind to the suffering of the innocent is justice of a very imperfect sort.",
            ),
        },
    ),
    # ── 7. abdcx_ethics_moral_responsibility_1302 ── Male same-sex couple ───
    (
        ROOT / "data" / "abdcx" / "ethics.jsonl",
        "abdcx_ethics_moral_responsibility_1302",
        {
            "passage": (
                "But one must consider a person who is addicted to a powerful narcotic substance. He knows that the drug is destroying his health — his physician has told him so in the plainest terms. He is aware that it is ruining his relationships; his wife has left him and his children no longer speak to him.",
                "But one must consider a person who is addicted to a powerful narcotic substance. He knows that the drug is destroying his health — his physician has told him so in the plainest terms. He is aware that it is ruining his relationships; his husband has left him and his children no longer speak to him.",
            ),
        },
    ),
    # ── 8. abdcx_social_philosophy_institution_1003 ── Inclusive reference ───
    (
        ROOT / "data" / "abdcx" / "social_philosophy.jsonl",
        "abdcx_social_philosophy_institution_1003",
        {
            "passage": (
                "Its obligations — the duties of parent to child, of husband to wife, of brother to sister — are sustained by custom, sentiment, religious precept, and tacit understanding rather than by any written code.",
                "Its obligations — the duties of parent to child, of spouse to spouse, of sibling to sibling — are sustained by custom, sentiment, religious precept, and tacit understanding rather than by any written code.",
            ),
        },
    ),
]


def load_jsonl(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def save_jsonl(path: Path, entries: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def apply_replacements():
    # Group replacements by file
    file_groups: dict[Path, list[tuple[str, dict]]] = {}
    for file_path, entry_id, field_replacements in REPLACEMENTS:
        file_groups.setdefault(file_path, []).append((entry_id, field_replacements))

    total_modified = 0

    for file_path, entry_specs in file_groups.items():
        entries = load_jsonl(file_path)
        entry_map = {e["id"]: e for e in entries}

        for entry_id, field_replacements in entry_specs:
            if entry_id not in entry_map:
                print(f"ERROR: Entry {entry_id} not found in {file_path.name}")
                sys.exit(1)

            entry = entry_map[entry_id]
            print(f"\n{'='*72}")
            print(f"ENTRY: {entry_id}")
            print(f"FILE:  {file_path.relative_to(ROOT)}")
            print(f"{'='*72}")

            for field, (old_text, new_text) in field_replacements.items():
                current_value = entry[field]
                if old_text not in current_value:
                    print(f"  WARNING: old_text not found in field '{field}'")
                    print(f"  Searching for partial match...")
                    # Show first 120 chars of old_text for debugging
                    print(f"  old_text starts with: {old_text[:120]!r}")
                    print(f"  field starts with:    {current_value[:120]!r}")
                    sys.exit(1)

                print(f"\n  FIELD: {field}")
                print(f"  ORIGINAL (excerpt): ...{old_text[:100]}...")
                new_value = current_value.replace(old_text, new_text)
                entry[field] = new_value
                print(f"  MODIFIED (excerpt): ...{new_text[:100]}...")

            total_modified += 1

        save_jsonl(file_path, entries)
        print(f"\n  Wrote {file_path.relative_to(ROOT)}")

    print(f"\n{'='*72}")
    print(f"DONE: Modified {total_modified} entries across {len(file_groups)} files.")
    print(f"{'='*72}")


if __name__ == "__main__":
    apply_replacements()
