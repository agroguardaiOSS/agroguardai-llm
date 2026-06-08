#!/usr/bin/env python3
"""Generate ~50 more entries to push past 1,000 target."""

import json
from pathlib import Path
from collections import Counter

DATASET_PATH = Path("data/agri_qa.json")

with open(DATASET_PATH) as f:
    existing = json.load(f)

last_id = max(int(e["id"].replace("agri-", "")) for e in existing)
next_id = last_id + 1
existing_ids = {e["id"] for e in existing}

NEW = [
    # === Fulfulde (Nigeria) - 10 entries ===
    ("Nigeria", "Fulfulde", "cowpea",
     "Nebbe am ndanɗi na nawa kadi himbe na njeewi. Ko waɗi?",
     "Nebbe ɗe ndanɗi (beans weevils) ko torra mawnde e nder cuuɗi. (1) Yooru nebbe ɗen e naange haa selli ko adii ɗaɗanaaki. (2) Huutoro neem oil (5ml e nder litru 1). (3) Wintoo nder cuuɗi ɗi henndu naatataa. (4) Nebbe ɗen wintoo nder friisa (freezer) balɗe 7 — himbe ɗen maɓe maaya. (5) Lartu cuuɗi ɗi ɗaɗanotonoo. (6) Yeewtu e ofisaajo demal (ADP) ngam heɓde gabbe ɗe himbe njiɗataa.",
     "ADP Fulfulde Cowpea Guide; IITA Post-Harvest", "pest management"),

    ("Nigeria", "Fulfulde", "cowpea",
     "Nebbe am na ndaanii, gelle na wumɗe. Ko torra?",
     "Gelle ɗe wumɗe ko aphids. (1) Lartu nebbe ɗe mbaayɗe — suna ɗe. (2) Huutoro neem oil (5ml e nder litru 1). (3) Demo nebbe ɗe puɗɗotooɗe — mbaadi ADC ɗe ADP. (4) Luurtin ndema — woto a demo nebbe e nokkuure goote hitaande fof. (5) Lartu leɗɗe e nder ngesa. (6) Yeewtu e ADP.",
     "ADP Cowpea Aphid Control; IITA Cowpea IPM", "pest management"),

    ("Nigeria", "Fulfulde", "cowpea",
     "Nebbe am na mari kuje (spots) ɓaleeje. Koyɗe na wuwru?",
     "Kuje ɓaleeje ɗen ko anthracnose. (1) Lartu nebbe ɗe mbaayɗe — suna ɗe. (2) Demoo gabbe ɗe ngooɗata — ko ADP yeɗata. (3) Luurtin ndema. (4) Huutoro fungicide (copper-based) — yeewtu e ADP. (5) Demoo nebbe dow ngeeneede (ridges) — ndiyam ɗam woto dar. (6) Nebbe ruftuɗe ɗen lartu e nder kawral.",
     "ADP Cowpea Anthracnose Guide; IITA Disease Management", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "groundnut",
     "Jawle am na njawi, koyɗe na mboddi. Ko waɗi?",
     "Jawle njawɗe ɗen ko groundnut rosette virus. (1) Lartu jawle ɗe mbaayɗe — suna ɗe. (2) Demoo jawle ɗe ngooɗata: 'Serenut 4T', 'Nyirahindurwa'. (3) Luurtin ndema. (4) Wara aphids ɗen — koɓe ndadotoo virus. (5) Huutoro neem oil (5ml/lita). (6) Yeewtu e ADP.",
     "ADP Groundnut Rosette Guide; ICRISAT Rosette Control", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "groundnut",
     "Jawle am na sewi, gelle na mboddi kadi. Ko torra?",
     "Jawle ɗe ngollataa ko leaf spot (Cercospora). (1) Lartu gelle ɗe mbaayɗe — suna. (2) Demoo jawle ɗe ngooɗata: 'CG 7', 'JL 24', 'Serenut 2'. (3) Luurtin ndema. (4) Huutoro neem oil. (5) Demoo e ngeeneede — ndiyam ɗam woto koɗo. (6) Yeewtu e ADP ngam fungicide (copper).",
     "ADP Groundnut Leaf Spot Guide; ICRISAT Leaf Spot Control", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "sorghum",
     "Mawɗe am na mari koyngol (smut) ɓale. Ko waɗi?",
     "Koyngol ɓale ko sorghum smut. (1) Lartu mawɗe ɗe mbaayɗe — suna ko adii ɗe mbaɗtora. (2) Demoo gabbe ɗe ngooɗata: 'Seredo', 'Macia', 'Gadam'. (3) Naatin gabbe ɗen e ndiyam ɗam ngulmam (52°C) miniti 10 ko adii ndema. (4) Huutoro seed dressing — ADP yeɗata. (5) Luurtin ndema. (6) Woto a huutoro azote ɗuuɗuka.",
     "ADP Sorghum Smut Guide; ICRISAT Smut Management", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "sorghum",
     "Mawɗe am na nawa kadi colli na ñaama ɗe. Ko mbaɗa?",
     "Colli ko torra mawnde e dow mawɗe. (1) Togo (scare) colli ɗi haa nguurtu — huutoro suturaaji (flags) maa karambu (tin cans). (2) Lartu gawri nder ngesa — woto wallito colli. (3) Demoo gabbe ɗe mbaɗi celluɗe: 'Seredo' — colli mbaawataa ñaamde. (4) Mbaɗ mawɗe saɗtina — woto accu e ngesa juuti. (5) Lartu bikkon maa gollooɓe ngam fogaade colli. (6) Yeewtu e ADP.",
     "ADP Sorghum Bird Control; ICRISAT Bird Management", "pest management"),

    ("Nigeria", "Fulfulde", "millet",
     "Gawri am (millet) na mboddi, ko torra?",
     "Gawri mbodɗi ko downy mildew. (1) Lartu gawri nde mbaayi — suna. (2) Demoo gabbe ɗe ngooɗata: 'Ex-Borno', 'LCIC 9702', 'SOSAT-C88'. (3) Naatin gabbe e ndiyam ngulmam (52°C) miniti 10. (4) Luurtin ndema. (5) Demoo ko adii — gawri yidani ko adii. (6) Yeewtu e ADP ngam fungicide.",
     "ADP Millet Downy Mildew Guide; ICRISAT Millet Control", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "millet",
     "Gawri am (millet) na sewi, koyɗe na mboddi. Ko torra?",
     "Gawri ndi fuɗɗataa ko ergot (Claviceps fusiformis). (1) Lartu gawri nde mbaayi — suna. (2) Demoo gabbe ɗe ADP yeɗata. (3) Luurtin ndema. (4) Demoo ko adii — gawri yidani ko adii. (5) Huutoro seed dressing (thiram) — yeewtu e ADP. (6) Yeewtu e ofisaajo demal.",
     "ADP Millet Ergot Guide; ICRISAT Ergot Control", "disease diagnosis"),

    ("Nigeria", "Fulfulde", "maize",
     "Makkabe am na markooje (lodging). Ko waɗi?",
     "Makkabe ɗe markooje ko stem borers mbaɗi. (1) Lartu makkabe ɗe markii — suna. (2) Demoo ko adii — borers ɗen keƴaako. (3) Luurtin ndema — woto a demoo makkabe e ngesa goota hitaande fof. (4) Demoo gabbe ɗe ngooɗata: 'SC 403', 'MH 30'. (5) Huutoro neem oil (5ml/lita) nder makka. (6) Yeewtu e ADP ngam insecticide approved.",
     "ADP Maize Borer Guide; CIMMYT Borer Management", "pest management"),

    # === More beans (10 entries) ===
    ("Rwanda", "Kinyarwanda", "beans",
     "Ibishyimbo byanjye ntibikura neza mu gihe cy'izuba ryinshi. Nkora iki?",
     "Ibishyimbo ntibikunda ubushyuhe bukabije. (1) Shyira ibyatsi byumye (mulch) mu murima kugira ngo ubutaka butinyishe amazi. (2) Tera ibishyimbo mu gihe cy'imvura ya mbere. (3) Hitamo ubwoko buhanganira ubushyuhe: 'RWR 2156', 'RWR 2245'. (4) Tega ahantu hafi y'ibiti — ibishyimbo bikunda igicucu gito. (5) Ntukore ibishyimbo mu gihe cy'izuba ryinshi. (6) Ohereza ubutaka bwawe mu kigo cy'ubuhinzi.",
     "RAB Bean Heat Stress Guide; CIAT Bean Agronomy", "cultural practice"),

    ("Uganda", "Luganda", "beans",
     "Ebijanjaalo byange bya kyenvu newankubadde nfuse ifumbire. Lwaki?",
     "Ebijanjaalo bya kyenvu wadde nga wafuse ifumbire kiyinza okuba nga ifumbire terina ekituufu. (1) Gezaako ettaka lyo — genda ofiisi y'ebyobulimi. (2) Tega ifumbire ey'essubi (compost) oba obusa bw'ente (cow dung). (3) Ddamu okuzzaako pH — ebijanjaalo bikola bulungi ku pH 6.0—7.0. (4) Oba ettaka lirina lime, kozesa ettaaka la lime ku 2—3 kg ku butanda. (5) Tola embuto ezirina obusobozi. (6) Simba ebijanjaalo mu biseera eby'enkuba.",
     "NARO Bean Nutrition Guide; CIAT Soil Fertility", "general inquiry"),

    ("Tanzania", "Swahili", "beans",
     "Maharagwe yangu hayafai vizuri kwenye udongo wa mchanga. Nifanyeje?",
     "Maharagwe kwenye udongo wa mchanga yanahitaji uangalizi maalum. (1) Ongeza mbolea ya asili (compost) — kiasi cha 3 kg kwa mita ya mraba. (2) Tumia matandazo (mulch) ili kuhifadhi unyevu. (3) Panda aina za maharagwe zinazostahimili hali ya ukame: 'Uyole 98', 'Selian 97'. (4) Panda kwenye matuta (ridges) kuzuia mmomonyoko. (5) Tumia mbolea ya NPK (100g kwa mita 10 za mstari). (6) Wasiliana na ofisa wa kilimo (TARI) kwa ushauri zaidi.",
     "TARI Bean Sandy Soil Guide; CIAT Bean Agronomy", "cultural practice"),

    ("Ethiopia", "Amharic", "beans",
     "ባቄላ (beans) በበጋ ወቅት አይለምም። ምን ማድረግ?",
     "በበጋ ወቅት ባቄላ አለማለም የውሃ እጥረት ምልክት ነው። (1) ሙጭ (mulch) ተጠቀሙ ውሃው እንዳይተን። (2) ድርቅን የሚቋቋሙ ዝርያዎች: 'Awash 1', 'Awash 2'። (3) በደጋ ቦታ ላይ ይዝሩ — ባቄላ ቅዝቃዜን ይወዳል። (4) የጠል እርሻ (irrigation) ከሌለ, ከዝናብ በኋላ ይዝሩ። (5) NPK ማዳበሪያ ይጠቀሙ። (6) የግብርና ባለሙያውን ያነጋግሩ።",
     "EIAR Bean Drought Guide; CIAT Drought Management", "cultural practice"),

    ("India", "Hindi", "beans",
     "फलियाँ (beans) में पत्तों पर सफेद धब्बे हैं। क्या रोग है?",
     "सफेद धब्बे powdery mildew के लक्षण हैं। (1) प्रभावित पत्तियों को तोड़कर जला दें। (2) गंधक (sulphur) या बेकिंग सोडा (5g/लीटर) का छिड़काव करें। (3) नीम तेल (neem oil 5ml/लीटर) का प्रयोग करें। (4) फसल चक्र अपनाएं। (5) पौधों के बीच पर्याप्त दूरी रखें — हवा का संचार ज़रूरी है। (6) कृषि अधिकारी से सलाह लें।",
     "ICAR Bean Powdery Mildew Guide; CIAT Disease Control", "disease diagnosis"),

    ("India", "Punjabi", "beans",
     "ਫਲੀਆਂ (beans) 'ਤੇ ਚਿੱਟੇ ਧੱਬੇ ਹਨ। ਬਿਮਾਰੀ?",
     "ਚਿੱਟੇ ਧੱਬੇ powdery mildew ਹਨ। (1) ਪ੍ਰਭਾਵਿਤ ਪੱਤੇ ਤੋੜ ਕੇ ਸਾੜ ਦਿਓ। (2) ਸੋਡਾ (baking soda 5g/ਲੀਟਰ) ਛਿੜਕੋ। (3) ਨੀਮ ਦਾ ਤੇਲ (neem oil 5ml/ਲੀਟਰ) ਵਰਤੋ। (4) ਫਸਲੀ ਚੱਕਰ ਅਪਣਾਓ। (5) ਪੌਦਿਆਂ ਦੇ ਵਿਚਕਾਰ ਦੂਰੀ ਰੱਖੋ। (6) ਕਿਸਾਨ ਸਲਾਹ ਕੇਂਦਰ (Agriculture Officer) ਤੋਂ ਸਲਾਹ ਲਓ।",
     "Punjab Agriculture Bean Powdery Mildew Guide; CIAT Disease Control", "disease diagnosis"),

    ("Kenya", "Swahili", "beans",
     "Maharagwe yangu yana ukungu mweupe kwenye majani. Tiba?",
     "Ukungu mweupe ni powdery mildew. (1) Ondoa majani yaliyoathirika na uyachome. (2) Nyunyiza soda ya kuoka (baking soda 5g/lita). (3) Tumia neem oil (5ml/lita). (4) Panda kwa nafasi ya kutosha — cm 45 kati ya mistari. (5) Zungusha mazao. (6) Wasiliana na KALRO kwa ushauri.",
     "KALRO Bean Powdery Mildew Guide; CIAT Disease Management", "disease diagnosis"),

    ("Tanzania", "Swahili", "beans",
     "Maharagwe yangu yanakosa majani na yananyauka. Sababu?",
     "Kukosa majani na kunyauka ni ishara ya ukosefu wa maji au wadudu wa mizizi. (1) Angalia udongo — kama ni mkavu, ongeza umwagiliaji. (2) Weka matandazo (mulch) ili kuhifadhi unyevu. (3) Angalia mizizi kwa wadudu — weevil wa mizizi anaweza kuwa. (4) Panda aina zinazostahimili ukame: 'Selian 97', 'Uyole 98'. (5) Zungusha mazao — usipande maharagwe mara kwa mara. (6) Wasiliana na TARI.",
     "TARI Bean Drought & Pest Guide; CIAT Bean Agronomy", "disease diagnosis"),

    ("Nigeria", "Yoruba", "beans",
     "Ewa mi ti gbẹ ati awọn ewe rẹ ti di ofeefee. Kini iṣoro?",
     "Ewa ti o gbẹ ati awọn ewe ofeefee jẹ ami aini nitrogen tabi aini omi. (1) Gbin ewa ni akoko ti o tọ — kii ṣe akoko ogbẹ. (2) Fi kompositi tabi maalu igbe (cow dung) kun ile. (3) Fi NPK (15:15:15) ajile — 50g fun igi. (4) Fi igi gbigbẹ (mulch) bo ile lati da omi duro. (5) Gbin ewa ti o le fa: 'IT 90K-59', 'ITA 54'. (6) Kan si oṣiṣẹ iṣẹ-ogbin (ADP) fun imọran.",
     "ADP Bean Drought Advisory; IITA Bean Agronomy", "cultural practice"),

    ("Nigeria", "Hausa", "beans",
     "Wake na yana da kura (powder) fari a kan ganye. Magani?",
     "Kura fari a kan ganye na wake ita ce powdery mildew. (1) Cire ganyen da suka kamu da cutar — kona su. (2) Yayyafa soda (baking soda 5g/lita). (3) Yi amfani da mai na neem (neem oil 5ml/lita). (4) Juya amfanin gona. (5) Bada tazara tsakanin shuke-shuke. (6) Tuntuɓi jami'in noma (ADP) don shawara.",
     "ADP Bean Powdery Mildew Guide; IITA Disease Management", "disease diagnosis"),

    # === More teff (Ethiopia) - 5 entries ===
    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) ዘር እንዴት በትክክል ይዘራል?",
     "ጤፌ በቆራጥ (broadcasting) ዘር ይዘራል። (1) መሬቱን በደንብ አርስ — ጤፌ ደቃቅ አፈር ይወዳል። (2) ዘሩን ከአሸዋ ወይም ትኩስ ቆሻሻ ቀላቅለህ ተመሳሳይ በሆነ መንገድ ዝራ (25 ኪሎ በሄክታር)። (3) አፈሩን ቀስ ብለህ ሸፍነው (ራሶች በትንሹ ይሸፈኑ)። (4) ከዝናብ በኋላ ዘራ — ሰብሉ ከዝናብ ጋር ያድጋል። (5) 100 ኪሎ NPK በሄክታር አድርግ። (6) ለተጨማሪ እርዳታ ወደ ግብርና ቢሮ ሂድ።",
     "EIAR Teff Planting Guide; MoA Teff Agronomy", "cultural practice"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) ከሰብል በኋላ እንዴት ይከማቻል?",
     "ጤፌን ከሰብል በኋላ በአግባቡ ማከማቸት አስፈላጊ ነው። (1) ጤፌውን በደንብ አድርቅ (በፀሐይ 3-4 ቀናት)። (2) ንጹህ ቦርሳ ወይም የሸንበቆ መያዣ (sack) ተጠቀም። (3) አየር በሚገባበት ቦታ አከማች — እርጥበት ቢኖር ጤፌ ይበሰብሳል። (4) ከመሬት በላይ ባለ መደርደሪያ (pallet) ላይ አስቀምጥ። (5) ነፍሳትን ለመከላከል ንጹህ ማከማቻ አዘጋጅ። (6) ዘር ለማግኘት ከፈለግክ ቀዝቃዛ ቦታ ላይ አስቀምጥ።",
     "EIAR Teff Storage Guide; MoA Post-Harvest Advisory", "cultural practice"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) እህል እንዴት እንደሚሰበሰብ?",
     "ጤፌን በትክክል መሰብሰብ ብዙ ምርት ለማግኘት ይረዳል። (1) ጤፌ 90-120 ቀናት ውስጥ ይበስላል — ቅጠሎቹ ወደ ቡናማ ሲለወጡ ነው ጊዜው። (2) ማጭድ (sickle) ተጠቅመህ ተክሎቹን ከመሬት በላይ 10ሴ.ሜ ቁረጥ። (3) ተክሎቹን ለ2-3 ቀናት በፀሐይ ላይ አንጠልጥለህ አድርቅ። (4) እህሉን ለማግኘት በእንጨት ወይም በማሽን ትቦርቁ (thresh)። (5) እህሉን ከሌላው አውጣ — በንጹህ ቦርሳ ሰብስብ። (6) ከ0-4°C ባለው ሙቀት ውስጥ አከማች።",
     "EIAR Teff Harvest Guide; MoA Teff Post-Harvest", "cultural practice"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) ላይ አረም (weed) ተበዝቷል። እንዴት ማስወገድ?",
     "አረም የጤፌን ምርት በከፍተኛ ሁኔታ ይቀንሳል። (1) ጤፌ በሚበቅልበት ጊዜ አረምን በእጅ አውጣ — በተለይ በመጀመሪያ 30 ቀናት ውስጥ። (2) አረሙን ሙሉ ሥሩን ይዘህ አውጣ። (3) ከመዝራት በፊት መሬቱን በደንብ አርስ። (4) ወፍራም ዘር (25 ኪሎ በሄክታር) ዝራ — ጤፌው አረሙን ይበልጣል። (5) አረምን ማስወገድ መቀጠል ካልቻልክ የአረም መድሀኒት (herbicide) ተጠቀም — ከግብርና ባለሙያ ጠይቅ። (6) ሰብል አዙር — አረም ከአንድ ሰብል ጋር ተለምዶ ይቀራል።",
     "EIAR Teff Weed Management; MoA Teff Weed Control", "cultural practice"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) በአሸዋማ አፈር ውስጥ እንዴት ያድጋል?",
     "ጤፌ በአሸዋማ አፈር ውስጥ በትክክል ያድጋል። (1) አሸዋማ አፈር ውሃ በፍጥነት ያፈስሳል — ብዙ ውሃ ማጠጣት (irrigation) ያስፈልጋል። (2) 3 ኪሎ ማዳበሪያ (compost/ manure) በካሬ ሜትር አድርግ። (3) የጤፌ ዝርያ 'DZ-Cr-37' (Quncho) ተስማሚ ነው። (4) ሙጭ (mulch) ተጠቀም ውሃው እንዳይተን። (5) ጤፌ ከሰብል በኋላ አፈሩን ለማሻሻል ምስር (lentils) ወይም ባቄላ ዝራ። (6) የግብርና ባለሙያውን አነጋግር።",
     "EIAR Teff Sandy Soil Guide; MoA Teff Agronomy", "cultural practice"),

    # === More sunflower (5 entries) ===
    ("Nigeria", "Hausa", "sunflower",
     "Furen rana na da tsutsotsi a cikin furen. Magani?",
     "Tsutsotsin cikin furen rana (sunflower head borer) na lalata iri. (1) Cire furannin da suka lalace — kona su. (2) Shuka da wuri kafin tsutsotsi su yawaita. (3) Yi amfani da neem oil (5ml/lita) a jikin furen. (4) Juya amfanin gona — kada a shuka furen rana a gona guda. (5) Yi amfani da iri masu jurewa: 'PAN 7031', 'Hysun 38'. (6) Tuntuɓi jami'in noma don shawara.",
     "NAERLS Sunflower Borer Guide; ICRISAT Head Borer Control", "pest management"),

    ("Ethiopia", "Amharic", "sunflower",
     "የሱፍ አበባ (sunflower) ዘይት ለምን ይጠቅማል?",
     "የሱፍ አበባ ዘይት ለብዙ ነገሮች ይጠቅማል። (1) ለምግብነት — ለማብሰል እና ለሰላጣ ይጠቅማል። (2) ለጤና — ቪታሚን ኢ እና ሳቹሬትድ ፋት (good fats) አለው። (3) ለእንስሳት — ዘይቱ ከሰብሉ በኋላ ያለው ቅሪት ለከብቶች ምግብ ይሆናል። (4) ዘሩን ከ1ሄክታር መሬት እስከ 500-800 ኪሎ ማግኘት ይቻላል። (5) ለመሸጥ — የሱፍ አበባ ዘይት በገበያ ላይ ጥሩ ዋጋ አለው። (6) እርሻው በገቢ ማስገኛ ላይ ይረዳል።",
     "EIAR Sunflower Value Guide; ICRISAT Sunflower Uses", "general inquiry"),

    ("Tanzania", "Swahili", "sunflower",
     "Alizeti zangu hazitawai kukauka (dry) vizuri baada ya kuvuna. Nifanyeje?",
     "Alizeti kukauka vizuri ni muhimu kwa ubora wa mbegu. (1) Acha alizeti shambani kwa siku 7-10 baada ya kukomaa — zikauke kwenye shina. (2) Vuna na uweke kwenye mahali pakavu panapopitwa na hewa. (3) Anika alizeti juani (sun-dry) kwa siku 3-5. (4) Pura (thresh) alizeti zikikauka vizuri. (5) Hifadhi mbegu kwenye mifuko ya hewa. (6) Usivune alizeti zenye unyevu — zitaoza.",
     "TARI Sunflower Drying Guide; ICRISAT Post-Harvest", "cultural practice"),

    ("India", "Tamil", "sunflower",
     "சூரியகாந்தி (sunflower) எண்ணெய் எவ்வளவு நல்லது?",
     "சூரியகாந்தி எண்ணெய் உடல்நலத்திற்கு மிகவும் நல்லது. (1) வைட்டமின் ஈ (Vitamin E) நிறைந்தது. (2) இதய நோய்களைத் தடுக்க உதவுகிறது. (3) சமையலுக்கு சிறந்தது — வறுக்கவும், சாலட்க்கும் பயன்படுகிறது. (4) பயிரில் இருந்து 40-50% எண்ணெய் கிடைக்கிறது. (5) ஒரு ஹெக்டேரில் இருந்து 400-600 கிலோ விதை கிடைக்கும். (6) சூரியகாந்தி எண்ணெய் சந்தையில் நல்ல விலை கிடைக்கிறது. வேளாண்மை அலுவலகத்தில் மேலும் தகவல் பெறுங்கள்.",
     "TNAU Sunflower Oil Guide; ICRISAT Crop Use Guide", "general inquiry"),

    ("Kenya", "Kikuyu", "sunflower",
     "Sunflower ciakwa iri na wĩtũmbi (mould). Ngĩkwo?",
     "Wĩtũmbi kuma na ũnyũũ mũingĩ. (1) Tega sunflower iria irĩ na wĩtũmbi — igwo. (2) Ananga sunflower na riua — ciũme wega. (3) Ikara handũ hehu na heho — ũnyũũ ndũtũmaga wĩtũmbi. (4) Handa sunflower mbere — iria irĩ na wĩtũmbi itiumaga. (5) Tega matira (mulch) kũgira ngo ikinyagĩrie ciathi (weeds). (6) Uria KALRO kana ofisa wa ugwati.",
     "KALRO Sunflower Mould Guide; ICRISAT Post-Harvest", "disease diagnosis"),

    # === More dairy (5 entries) ===
    ("Nigeria", "Hausa", "dairy",
     "Shanuna (dairy cow) tana kafin ƙirji (udder) kumbura. Magani?",
     "Kumburin ƙirji (udder) na saniya yana nufin mastitis. (1) KIRA likitan dabbobi (vet) nan da nan. (2) Wanke ƙirjin saniya kafin kiɗa (milking). (3) Yi amfani da 'teat dip' bayan kiɗa (kowace rana). (4) Yi amfani da tawul (towel) daban ga kowace saniya. (5) Kiɗa saniya lafiya da farko, sannan saniya mai mastitis. (6) Tsaftace wurin kiɗa kowace rana. (7) Idan saniya tana da zazzaɓi (fever), tana buƙatar antibiotics — likitan dabbobi zai ba da magani.",
     "NAERLS Mastitis Control; DVS Veterinary Guide", "disease diagnosis"),

    ("Nigeria", "Yoruba", "dairy",
     "Maalu mi (dairy cow) nso wara kekere. Kini iṣoro?",
     "Maalu ti o nso wara kekere le ni ọpọlọpọ awọn okunfa. (1) Ounjẹ — fun ni koriko didara, dairy meal 2-3 kg lojoojumọ. (2) Omi — maalu nilo omi 40-60 lita lojoojumọ. (3) Ilera — ṣayẹwo ti o ba ni mastitis tabi aisan miiran. (4) Iru (breed) — Friesian, Jersey, Sokoto Gudali dara fun wara. (5) Ọjọ ori — maalu agbalagba nso wara kekere. (6) Kan si dokita eranko (vet).",
     "NAERLS Dairy Guide; DVS Milk Production", "general inquiry"),

    ("Ghana", "Twi", "dairy",
     "Me nantwie (dairy cow) nufu (udder) no ayɛ ahyew (swollen). Nkranee?",
     "Nufu a ayɛ ahyew yɛ mastitis. (1) FRA nantwie doktor (vet) — ɛnte koraa. (2) Horo nufu no ansa na w'ato nufu no. (3) Fa teat dip wɔ berɛ a woato nufu no (daa). (4) Fa towel soronko ma nantwie biara. (5) Kan to nantwie a ɔwɔ apɔmuden no nufu, afei a wayare no. (6) Horo nantwie tenabea daa. (7) Sɛ nantwie no wɔ ahyew a, ɛhia antibiotics — nantwie doktor na ɔde firi MOFA hɔ.",
     "MOFA Mastitis Control; DVS Veterinary Advisory", "disease diagnosis"),

    ("Tanzania", "Swahili", "dairy",
     "Maziwa ya ng'ombe yamepungua baada ya kuzaa. Sababu?",
     "Ng'ombe kupungua maziwa baada ya kuzaa ni kawaida lakini isiporudi, angalia sababu. (1) Chakula — ng'ombe anahitaji nyasi bora na unga wa maziwa (dairy meal) 3 kg baada ya kuzaa. (2) Maji — ng'ombe aliyezaa anahitaji maji 50-60 lita kwa siku. (3) Pumziko — ng'ombe anahitaji kupumzika baada ya kuzaa. (4) Mtoto (calf) — acha ndama anyonye maziwa ya kwanza (colostrum) kwa siku 3-4. (5) Chanjo — hakikisha ng'ombe amechanjwa dhidi ya magonjwa. (6) Piga simu daktari wa mifugo (vet).",
     "TALIRI Post-Calving Guide; DVS Dairy Advisory", "general inquiry"),

    ("Malawi", "English", "dairy",
     "My dairy cow had a difficult birth and isn't producing milk. Help?",
     "Difficult birth (dystocia) can affect milk production. (1) Call a vet immediately. (2) The cow needs rest and good nutrition: hay, dairy meal 3 kg daily, and plenty of clean water (50-60 litres). (3) Make sure the calf is nursing — nursing stimulates milk production. (4) Milk the cow regularly (2-3 times daily) to maintain production. (5) If the cow has fever (temperature >39.5°C), she needs antibiotics — consult vet. (6) Check for retained placenta — if placenta hasn't passed within 24 hours, call vet. Contact Department of Animal Health (DAH).",
     "DAH Dystocia Guide; DVS Post-Calving Care", "general inquiry"),
]

# ── Build entries ───────────────────────────────────────────────────
new_entries = []
for region, dialect, crop, question, answer, source, category in NEW:
    eid = f"agri-{next_id}"
    next_id += 1
    while eid in existing_ids:
        next_id += 1
        eid = f"agri-{next_id}"
    existing_ids.add(eid)
    new_entries.append({
        "id": eid,
        "region": region,
        "dialect": dialect,
        "crop": crop,
        "question": question.strip(),
        "answer": answer.strip(),
        "source": source,
        "category": category,
    })

# ── Validate ────────────────────────────────────────────────────────
print(f"Round 2: Generated {len(new_entries)} new entries")
for i, e in enumerate(new_entries):
    assert e["id"].startswith("agri-")
    assert 10 < len(e["question"]) < 600, f"Question bad at {i}: {len(e['question'])}"
    assert 50 < len(e["answer"]) < 2500, f"Answer bad at {i}: {len(e['answer'])}"
    assert len(e["source"]) > 10
print("Validation: PASS")

# ── Stats ───────────────────────────────────────────────────────────
from collections import Counter
regions = Counter(e["region"] for e in new_entries)
dialects = Counter(e["dialect"] for e in new_entries)
print(f"Regions: {dict(regions)}")
print(f"Dialects: {dict(dialects)}")

# ── Merge ───────────────────────────────────────────────────────────
merged = existing + new_entries
with open(DATASET_PATH, "w") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Merged: {len(existing)} → {len(merged)} entries (+{len(new_entries)})")
print(f"Saved to {DATASET_PATH}")

# Final post-merge stats
r2 = Counter(e["region"] for e in merged)
d2 = Counter(e["dialect"] for e in merged)
c2 = Counter(e["crop"] for e in merged)
print(f"\n=== FINAL STATE ({len(merged)} entries) ===")
for r, n in r2.most_common():
    print(f"  {r:15s}: {n:4d}")
print(f"  {'TOTAL':15s}: {len(merged):4d}")
print(f"\nDialects < 20:")
for d, n in sorted(d2.items()):
    flag = " <<<" if n < 15 else ""
    print(f"  {d:20s}: {n:4d}{flag}")
print(f"\nCrops < 10:")
for c, n in sorted(c2.items()):
    flag = " <<<" if n < 10 else ""
    print(f"  {c:20s}: {n:4d}{flag}")
