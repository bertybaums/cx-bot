#!/usr/bin/env python3
"""
Reduce Eurocentric bias and de-duplicate Inca entries in the cx-bot dataset.

Three tasks:
1. De-duplicate Inca entries in philosophy_of_history (keep 4, replace 11)
2. Add non-Western starting points in aesthetics (reverse 5 entries)
3. Add female philosopher references (~10 entries across domains)

Prints BEFORE/AFTER for each modified field, then writes back.
"""

import json
import os
import copy
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IDs that must NOT be modified (being edited by another agent)
DO_NOT_TOUCH = {
    "defcx_aesthetics_taste_1154",
    "defcx_epistemology_epistemic_virtue_0018",
}


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def save_jsonl(path, entries):
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def print_diff(entry_id, field, before, after):
    if before == after:
        return
    print(f"\n{'='*80}")
    print(f"ID: {entry_id} | FIELD: {field}")
    print(f"--- BEFORE ---")
    if isinstance(before, list):
        for item in before:
            print(f"  - {item}")
    else:
        print(before[:500] + ("..." if len(str(before)) > 500 else ""))
    print(f"+++ AFTER +++")
    if isinstance(after, list):
        for item in after:
            print(f"  + {item}")
    else:
        print(after[:500] + ("..." if len(str(after)) > 500 else ""))


# =============================================================================
# TASK 1: De-duplicate Inca entries in philosophy_of_history
# =============================================================================

def task1_dedup_inca():
    print("\n" + "#"*80)
    print("# TASK 1: De-duplicate Inca entries in philosophy_of_history")
    print("#"*80)

    path = os.path.join(BASE, "data", "defcx", "philosophy_of_history.jsonl")
    entries = load_jsonl(path)

    # Find all Inca entries
    inca_indices = []
    for i, entry in enumerate(entries):
        text = json.dumps(entry).lower()
        if "inca" in text:
            inca_indices.append(i)

    print(f"\nFound {len(inca_indices)} Inca entries")

    # Keep these 4 (varied definitions and rich detail):
    # Line 3  (defcx_..._0353): writing + monumental arch + priestly class — Machu Picchu, roads, Andes
    # Line 52 (defcx_..._2263): writing + urban + division of labour — Cuzco, Sacsayhuaman, roads
    # Line 117 (defcx_..._3768): writing + urban centres + centralised authority — Cusco, Sapa Inca
    # Line 53 (defcx_..._2264): decline subdomain — uses Tang China, Inca only mentioned in passing
    keep_lines = {3, 52, 117, 53}  # line indices

    # Lines to replace:
    replace_lines = [i for i in inca_indices if i not in keep_lines]
    print(f"Keeping {len(keep_lines)} Inca entries, replacing {len(replace_lines)}")

    # Replacement civilisations — each makes the same philosophical point
    # (a society can be a civilisation without writing)
    replacements = [
        # 1. Great Zimbabwe
        {
            "name": "Great Zimbabwe",
            "counterexample": (
                "Consider the civilisation centred upon Great Zimbabwe, whose massive stone "
                "enclosures — constructed without mortar and rising to heights of eleven metres "
                "— testify to extraordinary architectural and organisational achievement. The "
                "settlement sustained a population of perhaps eighteen thousand, supported "
                "specialised craftsmen in gold, iron, and ivory, and served as the hub of a "
                "trade network stretching from the East African coast to the interior. Yet "
                "the builders of Great Zimbabwe left no system of writing. No inscriptions "
                "have been found upon the walls; no manuscripts survive. The first condition "
                "fails, yet it would be perverse to deny that Great Zimbabwe was the seat of "
                "a civilisation."
            ),
            "missing_condition": (
                "The definition requires writing as a necessary condition, but the civilisation "
                "of Great Zimbabwe achieved monumental architecture, long-distance trade, and "
                "complex social organisation without any written script, demonstrating that "
                "literacy is not essential to civilisational complexity."
            ),
            "passage_fragment": (
                "Yet one must consider the civilisation centred upon Great Zimbabwe in "
                "southern Africa. Between the eleventh and fifteenth centuries, a Shona-speaking "
                "people constructed vast stone enclosures of remarkable sophistication — the "
                "Great Enclosure alone comprises some nine hundred thousand blocks of dressed "
                "granite fitted without mortar. The settlement sustained a large population, "
                "supported specialised craftsmen working in gold, iron, and ivory, and served "
                "as the centre of a trade network extending to the Swahili coast and beyond. "
                "The society maintained a complex political hierarchy and elaborate religious "
                "institutions. Yet no system of writing has been discovered at the site. No "
                "inscriptions mark the walls; no written records survive. The first condition "
                "of the definition is not satisfied. Yet it would be an extraordinary "
                "impoverishment of the concept of civilisation to exclude Great Zimbabwe on "
                "that account."
            ),
        },
        # 2. Aboriginal Australian culture
        {
            "name": "Aboriginal Australian",
            "counterexample": (
                "Consider the Aboriginal Australian peoples, who sustained a continuous "
                "culture for at least sixty thousand years — by far the longest enduring "
                "cultural tradition known to us. They developed elaborate systems of law, "
                "complex kinship structures governing social and economic relations, "
                "sophisticated astronomical knowledge, and land management practices "
                "including systematic burning that shaped the ecology of an entire continent. "
                "Yet they possessed no system of writing. Their vast body of knowledge was "
                "transmitted entirely through oral tradition, song, dance, and visual art. "
                "The first condition fails, yet one hesitates to deny the title of "
                "civilisation to a culture of such antiquity and sophistication."
            ),
            "missing_condition": (
                "The definition equates civilisation with writing, but Aboriginal Australian "
                "cultures achieved extraordinary longevity, legal complexity, and ecological "
                "knowledge through oral and artistic modes of transmission, revealing that "
                "writing is merely one means by which a culture may preserve and communicate "
                "complex information."
            ),
            "passage_fragment": (
                "Yet one must attend to the Aboriginal peoples of Australia, who sustained "
                "a continuous cultural tradition for at least sixty thousand years — a span "
                "that dwarfs any civilisation of the ancient Near East. They developed "
                "elaborate systems of customary law governing marriage, land tenure, and "
                "dispute resolution. Their kinship structures are of a complexity that has "
                "taxed the analytical resources of modern anthropology. They possessed "
                "sophisticated astronomical knowledge, employed systematic burning to manage "
                "the ecology of an entire continent, and maintained a rich tradition of "
                "visual art, song, and narrative. Yet they possessed no system of writing "
                "in any conventional sense. Their knowledge was transmitted orally, through "
                "ceremony and performance, across hundreds of generations. The first condition "
                "of the definition is not met. Yet to deny the Aboriginal Australians the "
                "status of a civilisation on that account would be to confuse one culturally "
                "specific mode of information storage with the broader phenomenon it serves."
            ),
        },
        # 3. West African (Mali Empire)
        {
            "name": "Mali Empire",
            "counterexample": (
                "Consider the Mali Empire of the thirteenth and fourteenth centuries, which "
                "governed a territory larger than western Europe, administered a sophisticated "
                "system of provincial government, and sustained the great centre of learning "
                "at Timbuktu. The empire maintained elaborate trade networks, a complex legal "
                "apparatus, and specialised occupational castes including griots, smiths, and "
                "leatherworkers. Yet the governance of the empire rested predominantly upon "
                "oral tradition. The transmission of law, history, and administrative knowledge "
                "was entrusted to the griot caste, whose prodigious feats of memory served "
                "the function that written archives served elsewhere. The first condition is "
                "at best doubtfully satisfied, yet the Mali Empire was manifestly a civilisation."
            ),
            "missing_condition": (
                "The definition privileges writing over other systems of knowledge preservation, "
                "but the Mali Empire demonstrates that oral traditions maintained by specialised "
                "classes may serve the same organisational and cultural functions as written "
                "records, so that the absence of writing does not preclude civilisational "
                "achievement."
            ),
            "passage_fragment": (
                "Yet one must consider the Mali Empire under Mansa Musa in the fourteenth "
                "century. The empire governed a territory stretching from the Atlantic coast "
                "to the bend of the Niger, administered a system of provincial government "
                "of great sophistication, and sustained the centre of learning at Timbuktu, "
                "which attracted scholars from across the Islamic world. The empire's wealth "
                "was legendary — Mansa Musa's pilgrimage to Mecca reportedly depressed the "
                "price of gold in Cairo for a decade. It maintained elaborate trade networks, "
                "a complex legal apparatus, and specialised occupational castes. Yet the "
                "governance of the empire rested predominantly upon oral tradition. The "
                "transmission of law, genealogy, and administrative knowledge was entrusted "
                "to the griot caste, whose prodigious feats of memory served the function "
                "that written archives served in literate societies. The first condition "
                "of the definition is at best doubtfully met, and yet no historian would "
                "deny that the Mali Empire constituted a civilisation of the first rank."
            ),
        },
        # 4. Polynesian navigation cultures
        {
            "name": "Polynesian",
            "counterexample": (
                "Consider the Polynesian peoples who, over the course of several millennia, "
                "colonised virtually every habitable island in the Pacific — a feat of "
                "navigation and cultural organisation without parallel. They developed "
                "complex chieftainship systems, elaborate religious institutions, monumental "
                "architecture such as the moai of Rapa Nui and the marae of Tahiti, and "
                "sophisticated agricultural techniques adapted to diverse island environments. "
                "Their navigational knowledge — reading stars, ocean swells, bird flight "
                "patterns, and cloud formations — was a body of empirical science transmitted "
                "entirely without writing. The first condition fails, yet the achievement "
                "of Polynesian civilisation is beyond serious dispute."
            ),
            "missing_condition": (
                "The definition fails to recognise that complex navigational, agricultural, "
                "and political knowledge may be accumulated and transmitted across generations "
                "through oral and practical traditions rather than through writing, and that "
                "such traditions may sustain civilisational achievement of the highest order."
            ),
            "passage_fragment": (
                "Yet one must attend to the Polynesian peoples, who over the course of "
                "several millennia colonised virtually every habitable island across the "
                "vast expanse of the Pacific Ocean — a feat of exploration and cultural "
                "organisation without parallel in human history. They developed complex "
                "chieftainship systems with elaborate hierarchies of authority, sophisticated "
                "religious institutions, and monumental architecture: the great moai of "
                "Rapa Nui, the marae platforms of Tahiti, and the terraced gardens of "
                "Hawaii. Their navigational knowledge — the reading of stars, ocean swells, "
                "bird flight patterns, and cloud formations — constituted a body of "
                "empirical science of extraordinary precision, transmitted entirely through "
                "oral instruction and practical apprenticeship, without any system of "
                "writing. The first condition of the definition is not satisfied. Yet to "
                "deny civilisational status to the peoples who accomplished the greatest "
                "feat of maritime exploration in human history would be to reveal the "
                "poverty of the definition rather than any deficiency in the culture it "
                "purports to classify."
            ),
        },
        # 5. Haudenosaunee (Iroquois) Confederacy
        {
            "name": "Haudenosaunee",
            "counterexample": (
                "Consider the Haudenosaunee Confederacy — the league of the Seneca, Cayuga, "
                "Onondaga, Oneida, and Mohawk nations — which maintained one of the oldest "
                "participatory democracies in the world. The Confederacy possessed a "
                "constitution (the Great Law of Peace) governing relations among its member "
                "nations, a sophisticated system of checks and balances, and deliberative "
                "assemblies in which decisions required broad consensus. It sustained "
                "specialised roles in diplomacy, warfare, and governance. Yet the "
                "Haudenosaunee possessed no system of writing; the Great Law was transmitted "
                "orally, with wampum belts serving as mnemonic aids rather than scripts. "
                "The first condition fails, yet the political sophistication of the "
                "Confederacy is not in doubt."
            ),
            "missing_condition": (
                "The definition requires writing, but the Haudenosaunee Confederacy achieved "
                "constitutional governance, diplomatic sophistication, and political "
                "organisation of a high order through oral transmission supplemented by "
                "wampum, demonstrating that writing is not necessary for complex political "
                "life."
            ),
            "passage_fragment": (
                "Yet one must consider the Haudenosaunee Confederacy — the league of the "
                "Seneca, Cayuga, Onondaga, Oneida, and Mohawk nations — which maintained "
                "one of the oldest participatory democracies known to history. The "
                "Confederacy's constitution, known as the Great Law of Peace, established "
                "a system of governance with checks and balances, provisions for the "
                "adoption of new members, and deliberative assemblies in which decisions "
                "were reached by broad consensus. It maintained specialised diplomatic "
                "and military roles and sustained complex inter-national relations over "
                "centuries. The political sophistication of this arrangement was such that "
                "it influenced the framers of the United States Constitution. Yet the "
                "Haudenosaunee possessed no system of writing; the Great Law was transmitted "
                "orally from generation to generation, with wampum belts serving as mnemonic "
                "aids rather than scripts. The first condition of the definition is not met. "
                "Yet it would be quite untenable to deny that the Haudenosaunee achieved "
                "a level of political civilisation that many literate societies have failed "
                "to match."
            ),
        },
        # 6. Pre-literate Norse
        {
            "name": "Pre-literate Norse",
            "counterexample": (
                "Consider the Norse peoples of the early Viking Age, prior to the widespread "
                "adoption of the Latin alphabet. They constructed ocean-going longships of "
                "extraordinary sophistication, established trade routes from Scandinavia to "
                "Byzantium and the North American coast, maintained complex systems of law "
                "administered through regional assemblies (things), and developed elaborate "
                "religious and mythological traditions. Whilst they possessed the runic "
                "alphabet, it was used primarily for short inscriptions rather than for the "
                "recording of laws, literature, or administrative records. The first "
                "condition is not clearly satisfied, yet the Norse achievement in navigation, "
                "law, and trade constitutes civilisation by any reasonable standard."
            ),
            "missing_condition": (
                "The definition requires a system of writing, but the pre-literate Norse "
                "achieved complex legal institutions, long-distance trade, and technological "
                "sophistication with only rudimentary use of runes, demonstrating that even "
                "within European history, civilisational complexity need not depend upon "
                "a fully developed writing system."
            ),
            "passage_fragment": (
                "And lest one suppose that this difficulty afflicts only non-European "
                "societies, one should consider the Norse peoples of the early Viking Age, "
                "prior to the widespread adoption of the Latin alphabet. They constructed "
                "ocean-going longships of extraordinary technical sophistication — vessels "
                "capable of crossing the North Atlantic — and established trade routes "
                "stretching from Scandinavia to Byzantium and, remarkably, to the coast "
                "of North America. They maintained complex systems of customary law "
                "administered through regional assemblies known as things, at which disputes "
                "were adjudicated and legislation enacted. They developed elaborate religious "
                "and mythological traditions of great complexity. Whilst they possessed the "
                "runic alphabet, its use was restricted to short memorial inscriptions rather "
                "than to the recording of laws, literature, or administrative records in the "
                "manner that the definition envisages. The first condition is not clearly "
                "met. Yet the Norse achievement in navigation, jurisprudence, and commerce "
                "constitutes civilisation by any reasonable standard, and its exclusion by "
                "the proposed definition reveals that the requirement of writing is drawn "
                "too narrowly."
            ),
        },
        # 7. Benin Kingdom (West Africa)
        {
            "name": "Kingdom of Benin",
            "counterexample": (
                "Consider the Kingdom of Benin, which flourished in what is now southern "
                "Nigeria from the thirteenth century onwards. Benin City was surrounded by "
                "an extraordinary system of earthwork walls and moats — among the largest "
                "pre-mechanical constructions in the world. The kingdom sustained specialised "
                "guilds of bronze-casters, ivory-carvers, and other craftsmen whose work "
                "ranks among the finest in the history of art. It maintained a complex "
                "political hierarchy centred upon the Oba, with an elaborate system of "
                "titled officials and provincial governance. Yet Benin possessed no "
                "indigenous system of writing. The first condition fails, yet the "
                "sophistication of Benin's political, artistic, and architectural "
                "achievement is beyond question."
            ),
            "missing_condition": (
                "The definition requires writing, but the Kingdom of Benin achieved "
                "monumental earthwork construction, political complexity, and artistic "
                "excellence of the highest order without any written script, demonstrating "
                "that literacy is not a prerequisite for civilisational achievement."
            ),
            "passage_fragment": (
                "Yet one must attend to the Kingdom of Benin, which flourished in what is "
                "now southern Nigeria from the thirteenth century onwards. Benin City was "
                "surrounded by an extraordinary system of earthwork walls and moats, "
                "extending for some sixteen thousand kilometres in total — among the largest "
                "pre-mechanical constructions in the world. The kingdom sustained specialised "
                "guilds of bronze-casters whose work, when first encountered by European "
                "travellers, was acknowledged to rival the finest sculpture of Renaissance "
                "Italy. It maintained a complex political hierarchy centred upon the Oba, "
                "with an elaborate apparatus of titled officials, provincial administrators, "
                "and tributary relations. Yet Benin possessed no indigenous system of "
                "writing. The administration of this remarkable polity, and the transmission "
                "of its artistic techniques, were accomplished entirely through oral and "
                "practical tradition. The first condition of the definition is not met. Yet "
                "to exclude Benin from the category of civilisation would be to reveal the "
                "definition's parochialism rather than any limitation of the kingdom itself."
            ),
        },
        # 8. Mississippian culture (Cahokia)
        {
            "name": "Mississippian (Cahokia)",
            "counterexample": (
                "Consider the Mississippian civilisation centred upon Cahokia, near present-day "
                "St. Louis, which at its height around 1100 CE was one of the largest cities "
                "north of Mexico. Cahokia's population may have exceeded twenty thousand; its "
                "great earthen mound — Monks Mound — is the largest pre-Columbian earthwork "
                "in the Americas. The society sustained a complex hierarchy, specialised "
                "craftsmen, and long-distance trade networks. Yet the Mississippians possessed "
                "no system of writing. The first condition fails, yet the scale and "
                "complexity of Cahokia's achievement is that of a civilisation."
            ),
            "missing_condition": (
                "The definition requires writing, but the Mississippian civilisation at "
                "Cahokia achieved urban scale, monumental construction, and complex social "
                "organisation without any written script, demonstrating that the absence "
                "of writing does not preclude civilisational development."
            ),
            "passage_fragment": (
                "Yet one must consider the Mississippian civilisation centred upon Cahokia, "
                "near present-day St. Louis, which at its height around 1100 CE was one of "
                "the largest cities anywhere north of Mexico. Its population may have exceeded "
                "twenty thousand souls. The great earthen mound at its centre — known as "
                "Monks Mound — is the largest pre-Columbian earthwork in the Americas, "
                "covering an area greater than the base of the Great Pyramid of Giza. The "
                "society sustained a complex social hierarchy, specialised craftsmen in "
                "pottery, shell-working, and copper, and long-distance trade networks "
                "extending across much of eastern North America. Yet the Mississippians "
                "possessed no system of writing. No inscriptions survive; no written records "
                "document the governance of this remarkable settlement. The first condition "
                "of the definition is not satisfied. Yet the scale and complexity of "
                "Cahokia's achievement — its urbanism, its monumental architecture, its "
                "far-flung trade — is that of a civilisation, and the definition must be "
                "judged too narrow in excluding it."
            ),
        },
        # 9. Ancestral Puebloans (Chaco Canyon)
        {
            "name": "Ancestral Puebloan (Chaco Canyon)",
            "counterexample": (
                "Consider the Ancestral Puebloan civilisation centred upon Chaco Canyon in "
                "the American Southwest, which between the ninth and twelfth centuries "
                "constructed great houses of hundreds of rooms, built a network of ceremonial "
                "roads extending across the desert, and maintained astronomical observatories "
                "of notable precision. The society supported specialised roles in architecture, "
                "astronomy, and trade, and sustained long-distance exchange networks bringing "
                "goods from as far as the Pacific coast and Mesoamerica. Yet the Ancestral "
                "Puebloans possessed no system of writing. The first condition fails, yet "
                "the architectural and organisational achievement of Chaco Canyon bespeaks "
                "a civilisation."
            ),
            "missing_condition": (
                "The definition requires writing, but the Ancestral Puebloan civilisation "
                "achieved monumental architecture, astronomical knowledge, and complex "
                "trade networks without any written script, revealing that the definition "
                "conflates one particular mode of information storage with civilisational "
                "complexity as such."
            ),
            "passage_fragment": (
                "Yet one should consider the Ancestral Puebloan civilisation centred upon "
                "Chaco Canyon in the American Southwest. Between the ninth and twelfth "
                "centuries, these peoples constructed great houses of hundreds of rooms, "
                "built a network of ceremonial roads extending across the desert landscape, "
                "and maintained astronomical observatories capable of tracking solstices "
                "and lunar cycles with notable precision. The society supported specialised "
                "roles in architecture, astronomy, and trade, and sustained exchange "
                "networks bringing turquoise, shells, macaw feathers, and copper bells "
                "from as far as the Pacific coast and Mesoamerica. Yet the Ancestral "
                "Puebloans possessed no system of writing. No inscriptions survive; the "
                "knowledge required to plan and construct the great houses was transmitted "
                "through practical apprenticeship and oral tradition. The first condition "
                "of the definition is not met. Yet the architectural sophistication and "
                "organisational scale of Chaco Canyon bespeak a civilisation of considerable "
                "attainment, and its exclusion by the proposed definition is a defect of "
                "the definition, not of the culture."
            ),
        },
        # 10. Tonga Empire (Pacific)
        {
            "name": "Tuʻi Tonga Empire",
            "counterexample": (
                "Consider the Tuʻi Tonga Empire, which from the tenth to the fifteenth "
                "century exercised political authority across a vast maritime domain in the "
                "western Pacific, encompassing Tonga, Samoa, Fiji, and numerous smaller "
                "island groups. The empire maintained a complex aristocratic hierarchy, "
                "constructed monumental stone tombs (the langi), and sustained long-distance "
                "maritime trade. Specialised craftsmen produced fine bark cloth, elaborate "
                "carvings, and distinctive pottery. Yet the Tuʻi Tonga possessed no system "
                "of writing. The first condition fails, yet the political and cultural "
                "achievement of this maritime empire is that of a civilisation."
            ),
            "missing_condition": (
                "The definition requires writing, but the Tuʻi Tonga Empire achieved "
                "maritime political organisation across vast distances, monumental "
                "construction, and cultural sophistication without any written script, "
                "demonstrating that complex governance and cultural achievement are "
                "possible through oral tradition alone."
            ),
            "passage_fragment": (
                "Yet one must consider the Tuʻi Tonga Empire, which from the tenth to the "
                "fifteenth century exercised political authority across a vast maritime "
                "domain in the western Pacific. The empire encompassed not only the Tongan "
                "archipelago but extended its influence to Samoa, Fiji, and numerous smaller "
                "island groups — a political reach spanning hundreds of thousands of square "
                "miles of ocean. The Tuʻi Tonga maintained a complex aristocratic hierarchy, "
                "constructed monumental stone tombs known as langi, and sustained "
                "long-distance maritime trade networks of great complexity. Specialised "
                "craftsmen produced fine bark cloth, elaborate carvings, and distinctive "
                "pottery. Yet the Tuʻi Tonga possessed no system of writing. The "
                "administration of this far-flung maritime polity was accomplished "
                "entirely through oral communication, ceremonial protocol, and personal "
                "authority. The first condition of the definition is not satisfied. Yet "
                "the political and cultural achievement of this maritime empire is "
                "manifestly that of a civilisation, and its exclusion reveals the "
                "inadequacy of the definition."
            ),
        },
        # 11. Kingdom of Kongo
        {
            "name": "Kingdom of Kongo",
            "counterexample": (
                "Consider the Kingdom of Kongo, which at its height in the fifteenth and "
                "sixteenth centuries governed a territory in west-central Africa with a "
                "population of several million. The kingdom maintained a centralised "
                "bureaucracy, a system of provincial governance, specialised guilds of "
                "weavers, potters, and metalworkers, and an elaborate system of taxation "
                "and tribute. Its capital, Mbanza Kongo, was a substantial urban centre. "
                "Yet the Kingdom of Kongo possessed no indigenous system of writing prior "
                "to Portuguese contact. The first condition fails, yet the political and "
                "economic sophistication of the kingdom is not in doubt."
            ),
            "missing_condition": (
                "The definition requires writing, but the Kingdom of Kongo maintained "
                "centralised governance, provincial administration, and economic complexity "
                "through oral and ceremonial traditions, demonstrating that administrative "
                "sophistication does not require a written script."
            ),
            "passage_fragment": (
                "Yet one must attend to the Kingdom of Kongo, which at its height in the "
                "fifteenth and sixteenth centuries governed a substantial territory in "
                "west-central Africa. The kingdom maintained a centralised bureaucracy "
                "with appointed provincial governors, a system of taxation and tribute, "
                "and specialised guilds of weavers whose raffia cloth served as currency "
                "throughout the region. Its capital, Mbanza Kongo, was an urban centre of "
                "considerable size. The kingdom's political organisation was sufficiently "
                "sophisticated to engage in diplomatic relations with Portugal on terms "
                "of approximate equality. Yet the Kingdom of Kongo possessed no indigenous "
                "system of writing prior to the arrival of the Portuguese. The governance "
                "of this complex polity was accomplished through oral tradition, ceremonial "
                "protocol, and the personal authority of appointed officials. The first "
                "condition of the definition is not satisfied. Yet the political and "
                "economic sophistication of the kingdom is beyond dispute, and its "
                "exclusion from the category of civilisation speaks to the narrowness of "
                "the definition rather than to any deficiency in the society it describes."
            ),
        },
    ]

    # Map replace_lines to replacements
    # We have 11 replacements for 11 lines to replace
    # replace_lines from inca_indices minus keep_lines
    # Inca indices: [3, 32, 42, 52, 53, 62, 75, 84, 92, 107, 117, 123, 132, 143, 152, 163]
    # Keep: {3, 52, 117, 53}
    # Replace: [32, 42, 62, 75, 84, 92, 107, 123, 132, 143, 152, 163]
    # That's 12, but we have 11 replacements. Let's add one more keep.
    # Actually let me recount. keep_lines = {3, 52, 117, 53}
    # From the list: 3(keep), 32, 42, 52(keep), 53(keep), 62, 75, 84, 92, 107, 117(keep), 123, 132, 143, 152, 163
    # Replace = [32, 42, 62, 75, 84, 92, 107, 123, 132, 143, 152, 163] = 12 entries
    # We need one more replacement. Let me use the 12th: Kerma (Nubia)

    replacements.append({
        "name": "Kerma (Nubia)",
        "counterexample": (
            "Consider the Kingdom of Kerma in ancient Nubia, which flourished between "
            "approximately 2500 and 1500 BCE. Kerma developed monumental mud-brick "
            "architecture, including the great deffufa — a massive ceremonial structure "
            "rivalling the temples of contemporary Egypt. The kingdom sustained a complex "
            "social hierarchy, specialised craftsmen in bronze, pottery, and gold, and "
            "maintained extensive trade relations with Egypt and the wider ancient world. "
            "Yet Kerma possessed no indigenous system of writing; Egyptian hieroglyphs "
            "appear only on imported objects. The first condition fails, yet Kerma was "
            "manifestly a civilisation."
        ),
        "missing_condition": (
            "The definition requires writing, but the Kingdom of Kerma achieved monumental "
            "architecture, social stratification, and long-distance trade without any "
            "indigenous script, revealing that civilisation may develop in the immediate "
            "vicinity of a literate culture without itself adopting writing."
        ),
        "passage_fragment": (
            "Yet one must consider the Kingdom of Kerma in ancient Nubia, which flourished "
            "between approximately 2500 and 1500 BCE along the upper Nile. Kerma developed "
            "monumental mud-brick architecture of impressive scale, including the great "
            "deffufa — a massive ceremonial structure that rivalled the temples of "
            "contemporary Egypt. The kingdom sustained a complex social hierarchy, as "
            "attested by the elaborate royal tombs, and supported specialised craftsmen "
            "in bronze, pottery, and gold whose work was of high quality. It maintained "
            "extensive trade relations with Egypt, exchanging cattle, gold, and ivory for "
            "manufactured goods. Yet Kerma possessed no indigenous system of writing; "
            "Egyptian hieroglyphs appear only on imported objects, not as a native "
            "practice. The first condition of the definition is not met. Yet Kerma "
            "was manifestly a civilisation, flourishing for a millennium in the "
            "immediate vicinity of literate Egypt without itself developing a script, "
            "and its exclusion by the definition reveals a conflation of one cultural "
            "practice with civilisational achievement as such."
        ),
    })

    assert len(replace_lines) <= len(replacements), \
        f"Need {len(replace_lines)} replacements but only have {len(replacements)}"

    modified_count = 0
    for idx, line_num in enumerate(replace_lines):
        entry = entries[line_num]
        if entry["id"] in DO_NOT_TOUCH:
            print(f"\nSKIPPING {entry['id']} (protected)")
            continue

        repl = replacements[idx]
        old_entry = copy.deepcopy(entry)

        # Replace counterexample
        entry["counterexample"] = repl["counterexample"]
        print_diff(entry["id"], "counterexample", old_entry["counterexample"], entry["counterexample"])

        # Replace missing_condition
        entry["missing_condition"] = repl["missing_condition"]
        print_diff(entry["id"], "missing_condition", old_entry["missing_condition"], entry["missing_condition"])

        # Replace passage - need to swap out the Inca-specific portion
        # The passages typically have a structure:
        # 1. State the definition
        # 2. Give examples that fit
        # 3. "Yet" introduce the counterexample
        # We replace the counterexample portion of the passage
        old_passage = entry["passage"]

        # Find the "Yet" pivot where the Inca discussion begins
        # Common patterns: "Yet one must consider", "Yet one might observe", "Yet consider"
        # We'll find the sentence that introduces the Inca
        import re
        # Find where "Inca" first appears and back up to the start of that sentence or the "Yet" before it
        inca_pos = old_passage.lower().find("inca")
        if inca_pos == -1:
            # Check if there's a more general reference
            inca_pos = old_passage.lower().find("yet one")
            if inca_pos == -1:
                inca_pos = old_passage.lower().find("yet consider")

        if inca_pos != -1:
            # Back up to find "Yet" that starts the counterexample section
            # Search backwards from inca_pos for "Yet "
            search_region = old_passage[:inca_pos]
            yet_positions = [m.start() for m in re.finditer(r'Yet ', search_region)]
            if yet_positions:
                pivot = yet_positions[-1]  # Last "Yet" before "Inca"
            else:
                # Try finding sentence start
                pivot = inca_pos
                while pivot > 0 and old_passage[pivot-1] != '.':
                    pivot -= 1
                if pivot > 0:
                    pivot += 1  # Skip the period's space

            # Replace from pivot to end with our new passage fragment
            new_passage = old_passage[:pivot].rstrip() + " " + repl["passage_fragment"]
            entry["passage"] = new_passage
        else:
            # Fallback: just append the new passage fragment
            entry["passage"] = old_passage + " " + repl["passage_fragment"]

        print_diff(entry["id"], "passage", old_passage[:300], entry["passage"][:300])
        modified_count += 1

    save_jsonl(path, entries)
    print(f"\nTask 1 complete: modified {modified_count} entries in {path}")


# =============================================================================
# TASK 2: Add non-Western starting points in aesthetics
# =============================================================================

def task2_nonwestern_aesthetics():
    print("\n" + "#"*80)
    print("# TASK 2: Add non-Western starting points in aesthetics")
    print("#"*80)

    path = os.path.join(BASE, "data", "defcx", "aesthetics.jsonl")
    entries = load_jsonl(path)

    # We'll reverse 5 entries — rewrite definitions from non-Western aesthetic principles
    # and make the counterexample a Western case that breaks them.
    # Using entries at lines: 0, 32, 57, 46, 39

    reversals = {
        # Entry 0: defcx_aesthetics_beauty_0001
        # Original: symmetry + harmony + pleasure -> mountain landscape breaks it
        # New: wabi-sabi definition -> Western classical sculpture breaks it
        "defcx_aesthetics_beauty_0001": {
            "definition": (
                "An object is beautiful if and only if (i) it exhibits the marks of "
                "impermanence and the passage of time, (ii) its form is asymmetrical or "
                "irregular, and (iii) it evokes a contemplative awareness of transience "
                "in the observer."
            ),
            "conditions": [
                "exhibits the marks of impermanence and the passage of time",
                "its form is asymmetrical or irregular",
                "evokes a contemplative awareness of transience in the observer"
            ],
            "counterexample": (
                "A newly carved marble statue in the classical Greek tradition — a figure "
                "of Apollo, let us say, freshly chiselled and polished to a bright lustre "
                "— exhibits no marks of impermanence; it is designed to resist the passage "
                "of time. Its form is rigorously symmetrical, governed by precise mathematical "
                "ratios. And the contemplation it invites is one of timeless perfection "
                "rather than transience. All three conditions fail, yet the statue is "
                "beautiful by any reasonable standard."
            ),
            "missing_condition": (
                "The definition, rooted in the Japanese aesthetic of wabi-sabi, captures "
                "a genuine and profound species of beauty — the beauty of the weathered, "
                "the worn, the imperfect — but mistakes one aesthetic tradition's highest "
                "values for necessary conditions of beauty as such. Beauty may equally "
                "reside in the polished, the symmetrical, and the timeless."
            ),
            "passage": (
                "The Japanese aesthetic tradition of wabi-sabi suggests that an object is "
                "beautiful if and only if it exhibits the marks of impermanence and the "
                "passage of time, its form is asymmetrical or irregular, and it evokes "
                "a contemplative awareness of transience in the observer. This definition "
                "captures a distinctive and important class of beautiful objects: the "
                "cracked tea bowl whose glaze has crazed with age, the moss-covered stone "
                "in a temple garden, the faded silk whose colours have softened over "
                "centuries. In each case the beauty is inseparable from imperfection and "
                "the visible action of time. One might suppose that these conditions "
                "identify what is essential to beauty. Yet one must consider a newly "
                "carved marble statue in the classical Greek tradition — a figure of "
                "Apollo, let us say, freshly chiselled and polished to a brilliant lustre. "
                "The statue exhibits no marks of impermanence; it is designed precisely "
                "to resist the passage of time, to present an image of unchanging "
                "perfection. Its form is rigorously symmetrical, governed by the "
                "mathematical ratios codified by Polykleitos. And the contemplation it "
                "invites is not an awareness of transience but of timeless, ideal beauty "
                "— a beauty that aspires to escape the flux of the temporal altogether. "
                "All three conditions fail. Yet the statue is beautiful, and its beauty "
                "is of a kind that has been acknowledged for two and a half millennia. "
                "The difficulty is instructive. The definition has identified the "
                "conditions of beauty within one aesthetic tradition — a tradition of "
                "great depth and subtlety — but has mistaken them for necessary conditions "
                "of beauty as such. Beauty, it appears, is a wider category than any "
                "single cultural tradition can encompass, admitting of instances that owe "
                "their beauty to perfection and permanence no less than to imperfection "
                "and transience."
            ),
        },

        # Entry 32: defcx_aesthetics_beauty_0750
        # Original: harmony + disinterested pleasure + bilateral symmetry -> sunset breaks it
        # New: rasa theory definition -> Western abstract art breaks it
        "defcx_aesthetics_beauty_0750": {
            "definition": (
                "A work of art achieves aesthetic excellence if and only if (i) it "
                "embodies one of the recognised aesthetic moods (rasas), (ii) the artist "
                "has employed established formal means (vibhavas, anubhavas, and "
                "vyabhicharibhavas) to evoke that mood, and (iii) the cultivated spectator "
                "(sahridaya) experiences the corresponding generalised emotional state."
            ),
            "conditions": [
                "the work embodies one of the recognised aesthetic moods (rasas)",
                "the artist has employed established formal means to evoke that mood",
                "the cultivated spectator experiences the corresponding generalised emotional state"
            ],
            "counterexample": (
                "Consider a painting by Piet Mondrian — a composition of black lines and "
                "rectangles of primary colour upon a white ground. The work does not embody "
                "any of the rasas recognised in Indian aesthetic theory (the erotic, the "
                "heroic, the compassionate, the furious, the terrible, the odious, the "
                "marvellous, the comic, or the tranquil). It eschews representational content "
                "altogether and makes no attempt to evoke a determinate emotional mood "
                "through established formal means. Yet the painting achieves aesthetic "
                "excellence of a high order, and the cultivated observer finds in it a "
                "kind of austere perfection that resists assimilation to any rasa."
            ),
            "missing_condition": (
                "The definition, rooted in the Indian tradition of rasa theory as "
                "expounded by Bharata and refined by Abhinavagupta, captures the aesthetic "
                "logic of a vast body of Indian art, drama, and poetry, but cannot "
                "accommodate works whose aesthetic achievement lies in formal abstraction "
                "rather than in the evocation of determinate emotional moods."
            ),
            "passage": (
                "The Indian aesthetic tradition, as expounded in Bharata's Natyashastra "
                "and refined by Abhinavagupta, proposes that a work of art achieves "
                "aesthetic excellence if and only if it embodies one of the recognised "
                "aesthetic moods — the rasas — the artist has employed established "
                "formal means to evoke that mood, and the cultivated spectator experiences "
                "the corresponding generalised emotional state. This definition captures "
                "a profound truth about a vast body of Indian art, drama, and poetry. "
                "The rasa of the erotic (shringara) pervades the love poetry of Jayadeva; "
                "the heroic (vira) animates the epic narratives of the Mahabharata; the "
                "compassionate (karuna) suffuses the great scenes of separation and loss. "
                "In each case the work succeeds aesthetically precisely insofar as it "
                "evokes in the prepared spectator a generalised emotional resonance that "
                "transcends the particular circumstances depicted. Yet one must consider "
                "the case of Western abstract painting — a composition by Mondrian, let "
                "us say, consisting of black lines and rectangles of primary colour upon "
                "a white ground. The painting does not embody any of the rasas recognised "
                "in Indian aesthetic theory. It eschews representational content altogether "
                "and makes no attempt to evoke a determinate emotional mood. The cultivated "
                "observer finds in it a kind of austere formal perfection — a satisfaction "
                "in pure geometrical relation — that resists assimilation to any of the "
                "nine rasas. Yet the painting achieves aesthetic excellence of a high "
                "order, acknowledged by critics and artists across traditions. The "
                "difficulty reveals that the rasa framework, for all its subtlety and "
                "explanatory power within the tradition it was devised to illuminate, "
                "cannot serve as a universal definition of aesthetic excellence. Works "
                "whose achievement lies in formal abstraction rather than emotional "
                "evocation fall outside its compass."
            ),
        },

        # Entry 57: defcx_aesthetics_beauty_1150
        # Original: harmonious proportion + disinterested pleasure + luminous surface -> ruin breaks it
        # New: Chinese shan-shui (mountain-water) painting aesthetics -> Western portraiture breaks it
        "defcx_aesthetics_beauty_1150": {
            "definition": (
                "A painting achieves beauty if and only if (i) it renders the dynamic "
                "interplay of mountain and water (shan-shui), (ii) it employs empty space "
                "(liu bai) as an active compositional element, and (iii) its brushwork "
                "conveys the vital energy (qi yun) of the natural world."
            ),
            "conditions": [
                "the painting renders the dynamic interplay of mountain and water",
                "it employs empty space as an active compositional element",
                "its brushwork conveys the vital energy of the natural world"
            ],
            "counterexample": (
                "Consider Rembrandt's late self-portraits. These paintings achieve a beauty "
                "that is universally acknowledged. Yet they render no mountains and no water; "
                "their subject is the human face, aged and weathered. They employ no empty "
                "space as an active compositional element; the canvas is densely worked, "
                "the background dark and close. And whilst the brushwork is of extraordinary "
                "vitality, it conveys the inner life of a particular human being rather "
                "than the vital energy of the natural world. All three conditions fail, "
                "yet the paintings are beautiful."
            ),
            "missing_condition": (
                "The definition, derived from the Chinese shan-shui tradition as "
                "articulated by Xie He and elaborated over centuries of Chinese painting "
                "theory, captures the aesthetic logic of one of the world's great "
                "painting traditions but cannot accommodate beauty in portraiture, still "
                "life, or any subject that is not landscape."
            ),
            "passage": (
                "The Chinese tradition of painting theory, as articulated by Xie He in his "
                "Six Principles and elaborated by subsequent generations of critics, "
                "suggests that a painting achieves beauty if and only if it renders the "
                "dynamic interplay of mountain and water, employs empty space as an active "
                "compositional element, and conveys through its brushwork the vital energy "
                "of the natural world. This definition captures the aesthetic ideal of the "
                "shan-shui tradition with great precision. One thinks of the vast "
                "hanging scrolls of Fan Kuan, in which towering peaks and plunging "
                "waterfalls are set against expanses of luminous mist, and the brush moves "
                "with a vitality that seems to participate in the energy of the landscape "
                "it depicts. The empty spaces are not absences but presences — they are "
                "the breath of the painting, the intervals that give the mountains their "
                "grandeur and the water its life. Yet one must consider Rembrandt's late "
                "self-portraits. These paintings achieve a beauty that has been "
                "acknowledged by critics of every tradition. Yet they render no mountains "
                "and no water; their subject is the human face, lined and weathered by "
                "age. They employ no empty space as an active compositional element; the "
                "canvas is densely worked, the background dark and close, pressing upon "
                "the figure. And whilst the brushwork is of extraordinary vitality, it "
                "conveys the inner life of a particular man rather than the vital energy "
                "of the natural world. All three conditions fail. Yet the paintings are "
                "beautiful, and their beauty is of a kind that resists dismissal as "
                "merely different or lesser. The definition, rooted in one of the world's "
                "great painting traditions, has mistaken the aesthetic ideals of that "
                "tradition for necessary conditions of pictorial beauty as such."
            ),
        },

        # Entry 46: defcx_aesthetics_beauty_0764
        # Original: pleasing to eye + proportion/order + rare -> daisy breaks it
        # New: Yoruba aesthetic (iwa — character/essential nature) -> Western found art breaks it
        "defcx_aesthetics_beauty_0764": {
            "definition": (
                "An object possesses aesthetic merit if and only if (i) it exhibits iwa — "
                "that is, its form fully realises the essential nature or character proper "
                "to its kind, (ii) it displays oju-ona, a visible clarity of line and "
                "design, and (iii) it is recognised as aesthetically accomplished by "
                "those competent in the relevant artistic tradition."
            ),
            "conditions": [
                "it exhibits iwa — its form fully realises the essential nature proper to its kind",
                "it displays oju-ona, a visible clarity of line and design",
                "it is recognised as aesthetically accomplished by those competent in the tradition"
            ],
            "counterexample": (
                "Consider Marcel Duchamp's Fountain — a mass-produced porcelain urinal "
                "submitted to an art exhibition in 1917. The object does not fully realise "
                "the essential nature of any artistic kind; it is a manufactured commodity "
                "repurposed as art. It displays no special clarity of line or design beyond "
                "its industrial form. Yet it has been recognised as one of the most "
                "influential artworks of the twentieth century. The first two conditions "
                "fail, yet the object possesses aesthetic significance that cannot be "
                "dismissed."
            ),
            "missing_condition": (
                "The definition, rooted in the Yoruba aesthetic tradition as analysed by "
                "scholars such as Babatunde Lawal, captures the logic of a sophisticated "
                "evaluative framework in which beauty is inseparable from the realisation "
                "of essential character, but it cannot accommodate works whose aesthetic "
                "significance derives from the subversion or negation of established "
                "categories rather than from their fulfilment."
            ),
            "passage": (
                "The Yoruba aesthetic tradition, as analysed by scholars such as Babatunde "
                "Lawal, proposes that an object possesses aesthetic merit if and only if "
                "it exhibits iwa — that is, its form fully realises the essential nature "
                "or character proper to its kind — it displays oju-ona, a visible clarity "
                "of line and design, and it is recognised as aesthetically accomplished by "
                "those competent in the relevant artistic tradition. This definition "
                "captures a profound and systematic aesthetic sensibility. A Yoruba "
                "sculpture of an ori (head) achieves beauty precisely insofar as it "
                "realises the essential character of the human head in idealised form, "
                "its lines are clear and deliberate, and it is acknowledged by those "
                "versed in the tradition as successful. The aesthetic judgement is not "
                "arbitrary but grounded in a conception of excellence as the fulfilment "
                "of essential nature. Yet one must consider a case from the Western "
                "avant-garde. Marcel Duchamp's Fountain — a mass-produced porcelain "
                "urinal submitted to an art exhibition in 1917 — does not fully realise "
                "the essential nature of any artistic kind. It is a manufactured commodity "
                "deliberately repurposed as art, and its aesthetic significance derives "
                "precisely from its refusal to exhibit the qualities the definition "
                "requires. It displays no special clarity of line or design beyond its "
                "industrial form. Yet it has been recognised as one of the most "
                "influential artworks of the twentieth century, and its aesthetic "
                "significance — however one analyses it — cannot be dismissed. The "
                "definition, rooted in a tradition of considerable philosophical "
                "sophistication, has identified the conditions of aesthetic merit within "
                "a framework where excellence consists in the fulfilment of essential "
                "nature. But the Western avant-garde reveals that aesthetic significance "
                "may also arise from the deliberate subversion of such categories — a "
                "possibility the definition does not accommodate."
            ),
        },

        # Entry 39: defcx_aesthetics_beauty_0757
        # Original: formal unity + sensory richness + artefact intention -> butterfly breaks it
        # New: Islamic geometric aesthetics -> Western Romantic landscape painting breaks it
        "defcx_aesthetics_beauty_0757": {
            "definition": (
                "A work of decorative art is beautiful if and only if (i) it achieves an "
                "intricate geometric pattern derived from a finite set of symmetry operations, "
                "(ii) the pattern is non-representational, eschewing depiction of living "
                "beings, and (iii) the repetition of the pattern induces in the viewer a "
                "contemplative state directed towards the infinite."
            ),
            "conditions": [
                "it achieves an intricate geometric pattern derived from symmetry operations",
                "the pattern is non-representational, eschewing depiction of living beings",
                "the repetition induces a contemplative state directed towards the infinite"
            ],
            "counterexample": (
                "Consider a landscape painting by Caspar David Friedrich — the Wanderer "
                "above the Sea of Fog, let us say. The painting is representational in the "
                "highest degree, depicting a human figure overlooking a mountainous "
                "landscape. It makes no use of geometric pattern or symmetry operations. "
                "Yet it achieves a beauty that is universally acknowledged, and it induces "
                "a contemplative state that many would describe as spiritual. The first "
                "two conditions fail entirely, yet the work is beautiful."
            ),
            "missing_condition": (
                "The definition, rooted in the Islamic geometric tradition as realised in "
                "the great mosques and palaces of the medieval Islamic world, captures the "
                "aesthetic logic of a tradition that finds beauty in abstract pattern and "
                "mathematical order, but it cannot accommodate representational beauty "
                "or beauty that arises from the depiction of natural forms."
            ),
            "passage": (
                "The Islamic geometric tradition, as realised in the tile-work of the "
                "Alhambra, the muqarnas of the great mosques, and the illuminated pages "
                "of Quranic manuscripts, suggests that a work of decorative art is "
                "beautiful if and only if it achieves an intricate geometric pattern "
                "derived from a finite set of symmetry operations, the pattern is "
                "non-representational — eschewing the depiction of living beings — and "
                "the repetition of the pattern induces in the viewer a contemplative "
                "state directed towards the infinite. This definition captures a genuine "
                "and profound aesthetic achievement. The geometric tile-work of the "
                "Alhambra, which mathematicians have shown to instantiate all seventeen "
                "possible wallpaper symmetry groups, produces a beauty that is "
                "inseparable from its mathematical structure, and the contemplative "
                "state it induces has been described by many visitors as approaching "
                "the spiritual. Yet one must consider a landscape painting by Caspar "
                "David Friedrich — the Wanderer above the Sea of Fog, let us say. The "
                "painting is representational in the highest degree, depicting a human "
                "figure gazing out over a mountainous landscape shrouded in mist. It "
                "makes no use of geometric pattern or symmetry operations. Its beauty "
                "resides not in abstract mathematical structure but in the evocation of "
                "human feeling before the grandeur of nature. Yet it achieves a beauty "
                "that has been acknowledged across traditions, and it induces a "
                "contemplative state that many would describe as no less profound than "
                "that occasioned by the finest tile-work. The first two conditions fail "
                "entirely. The definition, rooted in a tradition of remarkable aesthetic "
                "and mathematical sophistication, has identified the conditions of beauty "
                "within one cultural framework, but it cannot serve as a universal "
                "account. Beauty, it appears, may arise from representation and natural "
                "form no less than from abstract geometric pattern."
            ),
        },
    }

    modified_count = 0
    for entry in entries:
        if entry["id"] in DO_NOT_TOUCH:
            continue
        if entry["id"] in reversals:
            old_entry = copy.deepcopy(entry)
            rev = reversals[entry["id"]]

            for field in ["definition", "conditions", "counterexample", "missing_condition", "passage"]:
                print_diff(entry["id"], field, old_entry[field], rev[field])
                entry[field] = rev[field]

            modified_count += 1

    save_jsonl(path, entries)
    print(f"\nTask 2 complete: modified {modified_count} entries in {path}")


# =============================================================================
# TASK 3: Add female philosopher references
# =============================================================================

def task3_female_philosophers():
    print("\n" + "#"*80)
    print("# TASK 3: Add female philosopher references")
    print("#"*80)

    # Each modification: (file_path, entry_id, old_text, new_text)
    # We insert female philosopher references naturally into passages
    modifications = [
        # 1. Epistemology: perception_0004 — Ayer, Mill -> add Stebbing
        (
            "data/defcx/epistemology.jsonl",
            "defcx_epistemology_perception_0004",
            "Phenomenalism, as expounded by Mill and later refined by Ayer, proposes",
            "Phenomenalism, as expounded by Mill and later refined by Ayer — and subjected to penetrating criticism by Stebbing — proposes",
        ),
        # 2. Epistemology: a_priori_0002 — Broad -> add Stebbing (colleagues at Cambridge)
        (
            "data/defcx/epistemology.jsonl",
            "defcx_epistemology_a_priori_0002",
            "Broad and others have drawn attention to such cases of material incompatibility",
            "Broad, and in a related vein Stebbing, have drawn attention to such cases of material incompatibility",
        ),
        # 3. Ethics: courage_2808 — Aristotle -> add Anscombe and Foot
        (
            "data/defcx/ethics.jsonl",
            "defcx_ethics_courage_2808",
            "Aristotle, one might recall, placed courage as a mean between cowardice and rashness, and the mountaineer's action falls on the side of rashness.",
            "Aristotle, one might recall, placed courage as a mean between cowardice and rashness — a point to which Anscombe returned in her discussion of moral virtue — and the mountaineer's action falls on the side of rashness. As Foot has observed, courage requires not merely the willingness to face danger but a kind of practical wisdom about which dangers are worth facing.",
        ),
        # 4. Aesthetics: sublimity_1902 — Burke -> add Iris Murdoch
        (
            "data/defcx/aesthetics.jsonl",
            "defcx_aesthetics_sublimity_1902",
            "This definition draws upon a tradition that stretches from Longinus through Burke to the Romantic poets",
            "This definition draws upon a tradition that stretches from Longinus through Burke to the Romantic poets — and finds echoes in Murdoch's account of the way in which great art unsettles and enlarges the self",
        ),
        # 5. Metaphysics: substance_3200 — Aristotle, Descartes, Locke -> add Anscombe
        (
            "data/defcx/metaphysics.jsonl",
            "defcx_metaphysics_substance_3200",
            "Aristotle's primary substances, Descartes's res cogitans and res extensa, and Locke's substrata all conform in broad outline to this pattern.",
            "Aristotle's primary substances, Descartes's res cogitans and res extensa, and Locke's substrata all conform in broad outline to this pattern — though one recalls Anscombe's observation that the concept of substance is less transparent than its long philosophical career might suggest.",
        ),
        # 6. Logic: paradoxes_0001 — Russell -> add Stebbing
        (
            "data/defcx/logic.jsonl",
            "defcx_logic_paradoxes_0001",
            "This definition captures the structure of familiar paradoxes such as the Liar ('this statement is false') and Russell's paradox",
            "This definition captures the structure of familiar paradoxes such as the Liar ('this statement is false') and Russell's paradox — cases which Stebbing analysed with characteristic precision in her work on logical thinking",
        ),
        # 7. Political philosophy: legitimacy_1173 — Hobbes, Locke -> add MacDonald
        (
            "data/defcx/political_philosophy.jsonl",
            "defcx_political_philosophy_legitimacy_1173",
            "it draws upon a tradition of contractarian thought that stretches from Hobbes and Locke to the present day.",
            "it draws upon a tradition of contractarian thought that stretches from Hobbes and Locke to the present day — a tradition whose assumptions Margaret MacDonald subjected to searching criticism in her analysis of the language of political theory.",
        ),
        # 8. Philosophy of mind: personal_identity_2102 — Locke -> add Anscombe
        (
            "data/defcx/philosophy_of_mind.jsonl",
            "defcx_philosophy_of_mind_personal_identity_2102",
            "The memory condition captures Locke's insight that personal identity is bound up with the capacity to recall one's past.",
            "The memory condition captures Locke's insight that personal identity is bound up with the capacity to recall one's past — an insight whose difficulties Anscombe later explored in her work on the first person.",
        ),
        # 9. Philosophy of religion: immortality_0217 — Kant -> add Emmet
        (
            "data/defcx/philosophy_of_religion.jsonl",
            "defcx_philosophy_of_religion_immortality_0217",
            "The definition has identified rational warrant with empirical evidence, overlooking the Kantian tradition in which practical reason provides its own distinctive grounds for belief.",
            "The definition has identified rational warrant with empirical evidence, overlooking the Kantian tradition — developed in a different direction by Emmet in her work on the nature of metaphysical thinking — in which practical reason provides its own distinctive grounds for belief.",
        ),
        # 10. Epistemology: truth_0015 — Ayer -> add Stebbing and Warnock
        (
            "data/defcx/epistemology.jsonl",
            "defcx_epistemology_truth_0015",
            "The verification principle, associated with the logical positivists and with Ayer's formulation in particular",
            "The verification principle, associated with the logical positivists and with Ayer's formulation in particular — a principle that Stebbing examined with rigour and that Warnock later placed in broader philosophical context",
        ),
    ]

    # Group by file
    from collections import defaultdict
    by_file = defaultdict(list)
    for filepath, entry_id, old_text, new_text in modifications:
        by_file[filepath].append((entry_id, old_text, new_text))

    total_modified = 0
    for filepath, mods in by_file.items():
        full_path = os.path.join(BASE, filepath)
        entries = load_jsonl(full_path)

        mod_dict = {eid: (old, new) for eid, old, new in mods}

        for entry in entries:
            if entry["id"] in DO_NOT_TOUCH:
                continue
            if entry["id"] in mod_dict:
                old_text, new_text = mod_dict[entry["id"]]
                old_passage = entry["passage"]
                if old_text in old_passage:
                    new_passage = old_passage.replace(old_text, new_text, 1)
                    entry["passage"] = new_passage
                    print_diff(entry["id"], "passage (philosopher addition)",
                              old_text, new_text)
                    total_modified += 1
                else:
                    print(f"\nWARNING: Could not find text in {entry['id']}")
                    print(f"  Looking for: {old_text[:100]}")

        save_jsonl(full_path, entries)

    print(f"\nTask 3 complete: modified {total_modified} entries across multiple files")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("Starting bias reduction edits...")
    print(f"Base directory: {BASE}")
    print(f"Protected IDs: {DO_NOT_TOUCH}")

    task1_dedup_inca()
    task2_nonwestern_aesthetics()
    task3_female_philosophers()

    print("\n" + "="*80)
    print("All tasks complete.")
