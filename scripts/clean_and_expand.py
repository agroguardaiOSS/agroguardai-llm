#!/usr/bin/env python3
"""Remove exact question duplicates and add thin-coverage entries."""
import json
from collections import Counter

with open("data/agri_qa.json") as f:
    data = json.load(f)

# ── Remove exact duplicates ──────────────────────────────────────
seen = {}
clean = []
removed = 0
for e in data:
    q = e["question"].strip()
    if q in seen:
        removed += 1
    else:
        seen[q] = len(clean)
        clean.append(e)

print(f"Removed {removed} duplicates. Kept {len(clean)} entries.")

# Re-ID to fill gaps
for i, e in enumerate(clean):
    e["id"] = f"agri-{i + 1}"

data = clean
existing_ids = {e["id"] for e in data}
last_num = max(int(e["id"].replace("agri-", "")) for e in data)
next_num = last_num + 1

def add(region, dialect, crop, question, answer, source, category):
    global next_num
    while f"agri-{next_num}" in existing_ids:
        next_num += 1
    eid = f"agri-{next_num}"
    existing_ids.add(eid)
    next_num += 1
    data.append({
        "id": eid, "region": region, "dialect": dialect, "crop": crop,
        "question": question.strip(), "answer": answer.strip(),
        "source": source, "category": category,
    })

# ── Thin coverage: teff (only 7 entries) ─────────────────────────
add("Ethiopia", "Amharic", "teff",
    "የጤፍ (teff) ሰብል ላይ ትንሽ ነጠብጣቦች እና ቡናማ ቀለም ታይቷል። ምንድን ነው?",
    "የጤፍ ሰብል ላይ ነጠብጣቦች እና ቡናማ ቀለም የጤፍ ዝገት (teff rust) በሽታ ሊሆን ይችላል። (1) በሽታው በእርጥበት ወቅት ይበዛል፣ ስለዚህ የውሃ ፍሳሽ ቦይ ያረጋግጡ። (2) የታመሙትን ተክሎች አስወግዱ። (3) ተከላካይ ፈንገስ መድኃኒት (mancozeb) በ2 ሳምንታት ልዩነት ይርጩ። (4) በቀጣዩ ወቅት የተለያየ ዘር አይነት ይጠቀሙ። (5) ለተጨማሪ ምክር የአካባቢውን ባለሙያ ያማክሩ።",
    "EIAR Teff Disease Guide; FAO Teff Rust Management", "disease diagnosis")

add("Ethiopia", "Amharic", "teff",
    "የጤፍ (teff) አፈር ምን አይነት ነው? እንዴት ማዘጋጀት እችላለሁ?",
    "የጤፍ አፈር አዘገጃጀት፡ (1) ጤፍ ለስላሳና በደንብ የተፈለቀ አፈር ይፈልጋል። (2) የአፈር አሲዳማነት (pH) 5.5-7.0 መሀከል መሆን አለበት። (3) ከመዝራት በፊት ሶስት ጊዜ ማረስ ያስፈልጋል። (4) ኦርጋኒክ ማዳበሪያ (ኩበት) ከመጨረሻው ማረሻ በፊት ይጨምሩ። (5) መጋቢት-ሚያዝያ ወቅት መዝራት ይመረጣል።",
    "EIAR Teff Production Guide; ATA Teff Agronomy", "cultural practice")

add("Ethiopia", "Amharic", "teff",
    "ጤፍ (teff) ላይ አረም ችግር አለብኝ። ምን ማድረግ አለብኝ?",
    "የጤፍ አረም ቁጥጥር፡ (1) ከመዝራት በፊት ማሳውን በደንብ ማረስ ያስፈልጋል። (2) የጤፍ ዘር በጣም ትንሽ ስለሆነ ንጹህ ዘር መጠቀም በጣም አስፈላጊ ነው። (3) ከዘራ በኋላ 3-4 ጊዜ በእጅ ማረም (hand weeding) ይስፈልጋል። (4) ለሰፋፊ ማሳ 2,4-D የተባለ ፀረ-አረም በጥንቃቄ መጠቀም ይቻላል። (5) የግብርና ባለሙያን ያማክሩ።",
    "EIAR Teff Weed Management; CIMMYT Small Grain Weed Control", "pest management")

add("Ethiopia", "Amharic", "teff",
    "ጤፍ (teff) ሰብል ከጥቅምት በኋላ እንዴት ማከማቸት እችላለሁ?",
    "የጤፍ ክምችት አያያዝ፡ (1) ጤፍ ሙሉ በሙሉ ደርቆ መሆን አለበት (ከ13% በታች እርጥበት)። (2) በንጹህ ጆንያዎች ውስጥ ያስቀምጡት። (3) ማከማቻ ቦታው ደረቅና ንጹህ መሆን አለበት። (4) የሙቀት መጠን 20°C ያክል መሆን አለበት። (5) ነፍሳትን ለመከላከል የአየር ዝውውር መኖር አለበት። (6) ጆንያዎችን በፓሌት (pallets) ላይ ያስቀምጡ - መሬት ላይ በቀጥታ አያስቀምጡ።",
    "EIAR Post-Harvest Management; FAO Grain Storage Guide", "cultural practice")

add("Ethiopia", "Amharic", "teff",
    "ጤፍ (teff) ዘር ዋጋ ስንት ነው? ጥሩ ዘር ከየት ማግኘት እችላለሁ?",
    "የጤፍ ዘር ምንጭ፡ (1) በኢትዮጵያ የተሻሻሉ የጤፍ ዝርያዎችን (Quncho, Magna, Boset) ከኢትዮጵያ ዘር ድርጅት (ESE) ወይም ከወረዳ ግብርና ጽህፈት ቤት ማግኘት ይቻላል። (2) ዋጋው እንደየአካባቢው ይለያያል - ለተወሰነ ዋጋ የአካባቢዎን የግብርና ባለሙያ ያማክሩ። (3) የተሻሻሉ ዘሮች ከፍተኛ ምርት ይሰጣሉ። (4) በሽታን የሚቋቋሙ (የዝገት ተከላካይ) ዝርያዎችን ይምረጡ።",
    "Ethiopian Seed Enterprise (ESE) Varieties Catalog; ATA Teff Value Chain", "general inquiry")

# ── Thin region: Malawi (only 20 entries) ────────────────────────
add("Malawi", "English", "teff",
    "What fertilizer should I use for teff in Malawi? The leaves are pale yellow.",
    "Pale yellow teff leaves suggest nitrogen deficiency. (1) Apply NPK 23:21:0+4S at 100 kg/ha at planting. (2) Top-dress with urea (46-0-0) at 50 kg/ha at tillering stage. (3) Test your soil pH - teff prefers 5.5-7.0. (4) If soil is acidic, apply lime (2-3 t/ha) 2-3 months before planting. (5) Organic compost (5 t/ha) improves soil structure and nutrient availability. (6) Contact your local extension officer for specific soil testing recommendations.",
    "Malawi Ministry of Agriculture Crop Guide; ICRISAT Fertilizer Recommendations", "cultural practice")

add("Malawi", "English", "cassava",
    "My cassava roots are rotting in the ground. What is causing this?",
    "Cassava root rot is caused by soil-borne fungi (Phytophthora, Fusarium) or bacteria. (1) Improve drainage - cassava cannot tolerate waterlogged soils. (2) Remove and destroy all infected plants immediately. (3) Use disease-free stem cuttings from a certified source. (4) Practice crop rotation - do not plant cassava in the same field for 2-3 years. (5) Plant on ridges or mounds in heavy soils. (6) Resistant varieties: Mbundumali, Silira. Contact your extension officer.",
    "IITA Cassava Disease Guide; Malawi DARS Root Rot Management", "disease diagnosis")

add("Malawi", "English", "groundnut",
    "How do I control aphids on my groundnut crop without expensive chemicals?",
    "Low-cost aphid control for groundnut: (1) Plant early (first rains) to avoid peak aphid season. (2) Intercrop with maize or sorghum - this confuses aphids. (3) Spray neem extract: boil 500g neem leaves in 5L water for 30 min, strain, add 10ml liquid soap, dilute to 20L and spray. (4) Spray ash solution: mix 2kg wood ash in 10L water, strain, apply weekly. (5) Encourage beneficial insects (ladybirds, lacewings) by planting flowering borders. (6) Remove and destroy heavily infested plants.",
    "ICRISAT Groundnut IPM; Malawi Ministry of Agriculture Low-Cost Pest Control", "pest management")

add("Malawi", "English", "millet",
    "When is the best time to plant finger millet in Malawi?",
    "Finger millet planting in Malawi: (1) Main season: November-December (with first effective rains of at least 30mm). (2) In some areas, January planting is possible for late-maturing varieties. (3) Prepare the seedbed to a fine tilth - millet seeds are very small. (4) Sow seeds shallow (1-2 cm) at 3-5 kg/ha. (5) Row spacing: 30 cm between rows, thin to 10 cm within rows. (6) Apply basal fertilizer NPK 23:21:0+4S at planting. (7) Top-dress with urea at 50 kg/ha when plants reach knee height.",
    "Malawi DARS Finger Millet Production Guide; ICRISAT Millet Agronomy", "cultural practice")

add("Malawi", "English", "sunflower",
    "My sunflower heads are small and seeds are empty. What went wrong?",
    "Small heads and empty seeds in sunflower indicate poor pollination or nutrient deficiency. (1) Ensure adequate boron - apply 10 kg/ha borax before planting. (2) Sunflower needs bee pollination - maintain 2-3 beehives per hectare, or avoid spraying insecticides during flowering. (3) Plant at correct spacing: 75 cm × 30 cm. (4) Avoid nitrogen excess which delays flowering. (5) Ensure adequate potassium - apply K₂O at 60 kg/ha. (6) Water stress during seed fill causes empty seeds - irrigate if possible during dry spells.",
    "FAO Sunflower Production Manual; Malawi Ministry of Agriculture Oilseed Guide", "cultural practice")

# ── Thin region: Uganda (only 27 entries) ────────────────────────
add("Uganda", "Luganda", "watermelon",
    "Ensuwa zange za watermelon ziwedde okukula. Nnyinza kuzitya?",
    "Ensuwa za watermelon eziwedde okukula oba nga ziwedde emyezi 3-4 oba nga zisonze. (1) Kuba ensuwa - bw'eba n'eddoboozi ery'omuwulira afa, ewedde okwengera. (2) Ekikoola eky'okumpi n'ensuwa kiba ekaze. (3) Ekisenge ekiri wansi we nsuwa kifuuka kyenvu. (4) Salako ensuwa n'akamwa akawanvu 3-5 cm okugiremako. (5) Teriikiriza kugikuba wansi oba kugitwala mu bukwatane. (6) Tereka mu kifo eky'empewo (10-15°C) okumala wiiki 1-2. (7) Bw'oba ogitunda, giraze ku ssenduuku so si ku ttaka.",
    "NARO Uganda Watermelon Guide; FAO Post-Harvest Management", "cultural practice")

add("Uganda", "Luganda", "sunflower",
    "Esimu zange za sunflower ziri kufuluma obulungi naye ebimuli bisuukirira. Kiki ekibaleeta?",
    "Ekimuli ekisukirira mu sunflower kiyinza okuva ku ndwadde oba ebiwuka. (1) Bwekiri obuwuka bwa sunflower moth - spray ne lambda-cyhalothrin ng'ebimuli bitandika okufuluma. (2) Bwekiri obulwadde bwa sclerotinia (head rot) - yongeramu calcium (gypsum 200 kg/ha) mu ttaka. (3) Funa engeri gy'osobola okukendeeza ennyonta mu kiseera eky'ebimuli. (4) Tosimbira kumpi nnyo - ssenke wakati wa sentimita 75. (5) Simba ensigo eza resistanti eziri ku katale ka NARO. Funayo omukenkufu w'ebyobulimi.",
    "NARO Uganda Sunflower Pest Guide; ASARECA Oilseed Manual", "pest management")

add("Uganda", "Luganda", "teff",
    "Nze ndi mulimi wa teff mu Uganda. Nnina kukola ki bulungi ennyo okusinga?",
    "Obulimi bwa teff mu Uganda: (1) Teff esobola okumerwa mu bitundu bya Uganda ebiri mu bukiikakkono n'ebuvanjuba. (2) Enkuba eya mm 450-550 buli mwaka emala. (3) Sikaalisa ettaka okutuusa bwe liba eddene. (4) Siga ensigo mu Gwokusatu oba Gwokuna (March-April). (5) Teeka NPK 23:21:0 olubuto ku 100 kg/ha. (6) Gya omuddo mu maaso (3-4 emirundi) kubanga teff terina mpaka nnyo. (7) Kungaanya ng'ekimala emyezi 2.5-3, ng'essubi liri mu kyenvu. (8) Funayo omukenkufu w'ebyobulimi ow'omu kitundu.",
    "NARO Teff Adaptation Trial; FAO Teff Production Guide", "cultural practice")

add("Uganda", "Luganda", "cowpea",
    "Ebikoola bya cowpea yange bitandise okufuuka bya kyenvu era nga biri wansi. Nnyinza kukola ki?",
    "Ebikoola ebya kyenvu era eby'okufa ku cowpea biraga obulwadde bwa fusarium wilt oba ebirya ebya nematode. (1) Kebera emirandira - bw'eba nga erina obuzitowa obutono obutono, nematode. (2) Ekyuma mu ttaka (soil solarization) okumala wiiki 4-6 nga tonnasimba. (3) Funa ensigo eza resistanti (SECOW 2W, SECOW 5T) okuva mu NARO. (4) Tokyusa cowpea mu nimiro ze zimu okumala sizoni 2-3. (5) Teekamu omusulo gwa organic compost okutuusa tt 5 buli yiika okuzimba obulamu bw'ettaka. (6) Funa omukenkufu w'ebyobulimi bw'oba okyalina okubuusabuusa.",
    "IITA Cowpea Disease Manual; NARO Uganda Cowpea Improvement Program", "disease diagnosis")

add("Uganda", "Luganda", "dairy",
    "Ente yange ekozesa amata amatono nnyo okusinga. Nnyinza kweyongera okukama?",
    "Okweyongera amata mu nte: (1) Wa ente emmere ey'enjawulo - omuddo omulungi (Napier grass, brachiaria) awamu n'ebikoola by'ebimera eby'obugimu (calliandra, leucaena). (2) Teekamu emmere ey'omumyufu (dairy meal/concentrate) 2 kg buli lunaku buli nte ekama. (3) Amazzi amalungi ge wamuwa buli kiseera - ente ekama eyetaaga L 40-60 buli lunaku. (4) Kama emirundi ebiri buli lunaku mu budde bwe bumu. (5) Wekennenye obulwadde (mastitis, East Coast Fever) embulire. (6) Funayo vet w'ente okugikebera. (7) Ente ennungi (Friesian cross, Jersey cross) ekama L 10-15 buli lunaku.",
    "NARO Uganda Dairy Manual; ILRI East Africa Dairy Development", "general inquiry")

# ── Watermelon (26 entries, add to hit ~30) ──────────────────────
add("Nigeria", "Yoruba", "watermelon",
    "Awon eso watermelon mi ti n fo lori oko. Kini o nfa eyi?",
    "Awon eso watermelon ti o fo lori oko le je nitori (1) Iyato ninu omi - rii pe o n fi omi kun ni gbogbo igba. (2) Aini calcium - fi gypsum tabi calcium nitrate si ile. (3) Arun blossom-end rot - wo calcium deficiency. (4) Ki o ma fi omi kun ju ni igba kan ati pe ki omi ma ni fo pelu ibaje. (5) Rii pe pH ile wa ni aarin 6.0-6.5. (6) Gbin iru eso ti o le fa: Kaolack, Crimson Sweet. (7) Lo mulch lati da omi duro ni ile.",
    "IITA Watermelon Guide; ADP Fruit Cracking Advisory", "disease diagnosis")

add("Ghana", "Twi", "watermelon",
    "Me watermelon nhwiren ne nhaban no nyinaa reyɛ akɔkɔɔ. Ɛyɛ yare?",
    "Watermelon nhwiren ne nhaban a ɛyɛ akɔkɔɔ betumi ayɛ downy mildew. (1) Ɛyɛ fungal yare a ɛtaa ba bere a nsu tɔ bebree. (2) Yi nhaban a ayɛ akɔkɔɔ no nyinaa fi hɔ. (3) Fa fungicide a ɛne mancozeb (50g/15L nsu) pɛte bere biara a wubehu sɛ ɛreba. (4) Ma mframa fa nnua no mu yiye - nnyɛ dua nnware nnware. (5) Nsu a ɛwɔ nhaban no so no mma fungi no ntumi ntrɛw. Enti gugu nsu wɔ tɔɔfe so, na ɛnyɛ wɔ ahabanmono so. (6) Fa organic mulch si fam na ɛmma asase mforo nkɔ ahabanmono so. (7) Kɔ MoFA hɔ konya afotu.",
    "MoFA Ghana Watermelon Production; CSIR-CRI Disease Guide", "disease diagnosis")

# ── Sunflower (20 entries, add to hit ~26) ───────────────────────
add("Tanzania", "Swahili", "sunflower",
    "Alizeti yangu ina madoa meusi kwenye majani. Inaweza kuwa ugonjwa gani?",
    "Madoa meusi kwenye majani ya alizeti yanaweza kuwa alternaria leaf spot. (1) Hii ni ugonjwa wa kuvu unaosababishwa na Alternaria helianthi. (2) Ondoa na uchome majani yote yenye dalili za ugonjwa. (3) Tumia dawa ya kuvu (mancozeb 50g/20L) baada ya wiki 2. (4) Punguza unyevu kwenye shamba - hakikisha mifereji ya maji inafanya kazi vizuri. (5) Panda alizeti kwa nafasi ya kutosha (75cm x 30cm) ili kuruhusu hewa kuzunguka. (6) Zungusha mazao - usipande alizeti kwenye shamba lilelile kwa miaka 2-3 mfululizo. (7) Tumia mbegu za alizeti zinazostahimili magonjwa kama Record au PAN 7352.",
    "TARI Tanzania Sunflower Disease Guide; FAO Sunflower Pest & Disease Manual", "disease diagnosis")

add("Kenya", "Kikuyu", "sunflower",
    "Mahua ma sunflower makwa nĩ manini mũno na nĩ kũũma. Mbeca?",
    "Mahua manini na kũũma kwa sunflower nĩ ihinda rĩa mũũru rĩa gũkundĩra (poor pollination) kana ũnyumu (drought). (1) Tũmĩra njũkĩ (bees) kũgũthondekera ũcũngũrĩra - njũkĩ 2-3 nĩcũthondekera mahũa ma ũthiũ. (2) Ndũkahũũre dawa cia gũkinyanĩra mĩnyamũ mahinda-inĩ ma kũrua mahũa. (3) Mũnyitĩrĩre boroni (borax 10 kg/ha) mbere ya gũhaanda. (4) Ũhũũre ũiyũrie (irrigation) mahinda-inĩ ma ũnyumu. (5) Haanda ndagĩka 75 cm gatagatĩ-inĩ wa mĩhari na ndagĩka 30 cm gatagatĩ-inĩ wa mĩmera. (6) Tũmĩra mũthemba wa Record kana Hysun - nĩĩyathimĩre nĩ KALRO.",
    "KALRO Sunflower Guide; FAO Sunflower Pollination Manual", "cultural practice")

with open("data/agri_qa.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

rc = Counter(e["region"] for e in data)
cc = Counter(e["crop"] for e in data)
print(f"\nFINAL: {len(data)} entries, {len(set(e['dialect'] for e in data))} dialects, {len(cc)} crops")
print(f"Teff: {cc.get('teff', 0)}, Sunflower: {cc.get('sunflower', 0)}, Watermelon: {cc.get('watermelon', 0)}")
print(f"Malawi: {rc.get('Malawi', 0)}, Uganda: {rc.get('Uganda', 0)}")
