import json
from collections import Counter

with open("data/agri_qa.json") as f:
    data = json.load(f)

last_id = max(int(e["id"].replace("agri-", "")) for e in data)
next_id = last_id + 1
existing_ids = {e["id"] for e in data}

def add(region, dialect, crop, question, answer, source, category):
    global next_id
    eid = f"agri-{next_id}"
    next_id += 1
    while eid in existing_ids:
        next_id += 1
        eid = f"agri-{next_id}"
    existing_ids.add(eid)
    data.append({
        "id": eid, "region": region, "dialect": dialect, "crop": crop,
        "question": question.strip(), "answer": answer.strip(),
        "source": source, "category": category,
    })

add("Nigeria", "Yoruba", "tomato",
    "Awon tomati mi ti baje ati pe awon eya ara re ti sun. Kini a le se?",
    "Awon tomati ti o baje ati ti o sun ni blossom-end rot. (1) Ko se aisan kokoro - o je aini kalisiomu (calcium). (2) Ma lo ajile nitrogen pupo - o da kalisiomu duro. (3) Rii pe ile ni kalisiomu to - fi awon epo eyin (egg shells) tabi lime kun ile. (4) Fi omi kun awon tomati ni deede - ma je ki ile gbe ju tabi tutu ju. (5) Lo mulch lati da omi duro. (6) Gbin awon tomati ti o le fa: Tengeru 97, Rio Grande. Kan si osise ADP.",
    "ADP Tomato Blossom-end Rot Guide; AVRDC Calcium Management", "disease diagnosis")

add("Nigeria", "Kanuri", "maize",
    "Nga dala makkabe har yaye kambu yaye am kare so. Nya?",
    "Makkabe dala kambu yaye ndu stem borers. (1) Kare makkabe mabe kambu yaye am nyi baade. (2) Ku makkabe raadu ma nyi tando laaro. (3) Kare makkabe late ma seed dressing firi ADP. (4) Ku makkabe pilla gonya - borers yaye tilo. (5) Kare makkabe ndi raduguma ma nyi funti juwu. (6) Dala neem oil (5ml/lita) re borers jiiro.",
    "ADP Maize Borer Guide; CIMMYT Stem Borer Control", "pest management")

add("Nigeria", "Tiv", "beans",
    "Ikyura m (beans) sule a kwagh u a ve sha ikyum. Annom?",
    "Ikyum a ve sha m ikyura yo, a kwagh u bean weevil. (1) Nyor ikyura la sha ahar (sun) - yo tumen weevil. (2) Nyor ikyura la a airtight container. (3) Nyor ikyura la a freezer (7 days). (4) Nyor ikyura la sha ahar ne ater u zi. (5) Nyor ikyura raadu - i gbenda yough la a soo kpa ha. (6) Kongo ADP ne iwe u ikyura.",
    "ADP Bean Weevil Guide; CIAT Storage Management", "pest management")

add("Nigeria", "Fulfulde", "beans",
    "Nebbe am na nawa e nder suudu. Ko mbada?",
    "Nebbe de nawa e nder cuudi ko weevils. (1) Yooru nebbe den e naange haa selli. (2) Wintoo nder container di henndu naatataa. (3) Wintoo nder frigidaire (freezer) balde 7. (4) Nebbe ruftude den lartu. (5) Lartu cuudi di dadanotonoo. (6) Yeewtu e ADP.",
    "ADP Bean Weevil Control; CIAT Storage Advisory", "pest management")

add("Ethiopia", "Amharic", "sunflower",
    "የሱፍ አበባ (sunflower) ዘር ለመዝራት የተሻለ ጊዜ?",
    "የሱፍ አበባ ዘር ለመዝራት የተሻለ ጊዜ የክረምት ወቅት መጀመሪያ ነው። (1) መጋቢት እስከ ሚያዝያ (March-April) ወር ይምረጡ። (2) ሱፍ አበባ በቀላል ዓይነት አፈር ውስጥ ይበቅላል። (3) ከመዝራት በፊት NPK 10:20:10 ማዳበሪያ ይጠቀሙ። (4) ዘሩን 3-5 ሴ.ሜ በሆነ ጥልቀት ዝሩ። (5) በእጽዋት መካከል 75 ሴ.ሜ እና በረድፍ መካከል 30 ሴ.ሜ ርቀት ይኑር። (6) ለተጨማሪ እርዳታ የግብርና ባለሙያውን ያነጋግሩ።",
    "EIAR Sunflower Planting Guide; ICRISAT Sunflower Agronomy", "cultural practice")

with open("data/agri_qa.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

rc = Counter(e["region"] for e in data)
print(f"FINAL: {len(data)} entries")
for r,n in rc.most_common():
    print(f"  {r:15s}: {n:4d}")
print(f"  {'TOTAL':15s}: {len(data):4d}")
