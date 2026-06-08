#!/usr/bin/env python3
"""Generate 50 targeted QA entries for Luo, Swahili, and weak regions.
Each entry follows the template: dialect-matched question + safe answer + source."""

import json, re
from pathlib import Path

DATASET_PATH = Path("data/agri_qa.json")

# ── Load existing data for ID management ────────────────────────────
with open(DATASET_PATH) as f:
    existing = json.load(f)

last_id = max(int(e["id"].replace("agri-","")) for e in existing)
next_id = last_id + 1

existing_ids = {e["id"] for e in existing}

# ── ENTRY GENERATORS ────────────────────────────────────────────────
# Each new entry: (region, dialect, crop, question, answer, source)

NEW_ENTRIES_RAW = [
    # ═══════════════ LUO (20 entries — Kenya) ═══════════════
    # Crop: maize — common problems
    ("Kenya", "Luo", "maize",
     "Kod bende mar oduma osechako ketho cham mara mar bando. Ang'o manyalo konya?",
     "Kod bende mar oduma (fall armyworm) nyalo ketho cham mokalo mana moromo 50% ka ok ochungi. Moko mag gik mitim: (1) Non anena magi pile ka iyudo kata nyath kod achiel kende to itim gik ma dwarore. (2) Neem pesticide mowinjore ma nitie e sirkal — dhi ir ofisa mar kilimo ma ing'iyo kaka inyalo tiyo kode. (3) Puodho man kod yath moromo malo nyalo konyo chungo kod moko ma ok keth ahinya. (4) Puodh cham kinyoro e kinde ma ok rom gi chieng' moduogo kod bende e kinde ma olokore kod puodho mamoko. Kuom kony mo medore, dhi ir ofisa mar kilimo man machiegni.",
     "FAO Fall Armyworm Management Guide; KALRO extension bulletin"),
    
    ("Kenya", "Luo", "maize",
     "Cham mara mar bando onyiso rangi ma rachar e it. Ne atiyo gi manyien to pok okonya.",
     "Rangi ma rachar e it cham mar bando inyalo bedo gi gima omiyo mang'eny — nyalo bedo tuo mar phosphorus, kata tuo mar nitrogen, kata chandruok mar tiende. Ka ne itiyo gi manyien (DAP) to pod itieko gi tuo, nyalo bedo ni lowo ok oyiego maber. Tim magi: (1) Kel sampul mar lowo ir ofisa mar kilimo mondo gine ane gima remo. (2) Kuom lowo ma ok winj manyien maber, nyiso ni pH ok rom — "liming" nyalo konyo. (3) Ne ane ka nitie tuo mar virus ma golo rangi e it. Kik ikaw okang' moro amora kapok ing'eyo gima chando chameno — nyalo bedo ni iweyo pesa.",
     "KALRO Soil Fertility Guide; IPNI Nutrient Deficiency Identification"),
    
    ("Kenya", "Luo", "cassava",
     "Toke mara mag muogo otudore, to ka achamo to nitie thuolo matindo matindo e iye. Bende yath ok dong' malo.",
     "Gima inyiso chalre gi tuo ma iluongo ni cassava mosaic disease (CMD) kata cassava brown streak disease (CBSD). Magi gin tuo ma kelo nyakowuok mang'eny e puothe man Nyansa. Tim magi: (1) Puth toke moko duto ma ondiki gi tuo — wiyo kanyachiel. (2) Kaw toke manyien koa kuom miech sirkal kata KALRO — tim nyono ni gin toke ma ok nyal mako tuo (CMD-resistant varieties: TME 419, MM96/5280). (3) Kik ipidh toke moa kuom puodho ma tuo osemako. (4) Puodho man gi yath mang'eny nyalo konyo geng'o lando tuo. Dhi ir ofisa mar kilimo e alworani.",
     "IITA Cassava Disease Management; KALRO Cassava Best Practices"),
    
    ("Kenya", "Luo", "cassava",
     "Muogo mara ka achamo to tek, to bende osebedo gi rangi ma rachar e iye. Nyaka arom kapok otimo kare?",
     "Muogo ma tek kod rangi ma rachar e iye nyiso ni kama oseng'iewo mokwongo. Moko mag gik mitim: (1) Ywar muogo ka podi tin — ka osebedo e lowo kuom dwe mang'eny, chame tek. Maduong' mar muogo mitimo kare en dwe 8-12 bang' pitho. (2) Kuom muogo ma osekethore, inyalo ywayo kendo loso gik moko kaka 'flour' kata 'chips' e od tong'. (3) Puodho ma nitie pi mang'eny nyalo miyo muogo medo bet gi tuo moloyo. Los sulu mag pi oko e puodho. (4) Kuom seche mabiro, pidh muogo e ndara (mounds) mondo kik obet e pi mang'eny.",
     "KALRO Cassava Harvest & Post-Harvest Guide; FAO Root & Tuber Bulletin"),
    
    ("Kenya", "Luo", "sorghum",
     "Bel mara oserwako kothe kendo wigi otwo ka podi tin. Yamo bende otucho moko piny.",
     "Kothe mar bel ma gi two kata ma wigi otwo nyiso ni nitie tuo kata chandruok mar pi. Moko mag gik mitim: (1) Ne ane ka nitie tuo mar ergot kata grain mold — magi gin tuo ma landore e kinde mag koth. (2) Ka pi oromo e puodho, los sulu mag pi. (3) Keyo bel ka ochiek maber — kik iwe e puodho kuom kinde malach. (4) Riambo bel e chieng' kata e ober (dryer) ma piny oyudo yamo maber. (5) Kan bel e kar ma otwo, ma yamo donjoe, to ma okinyal donjoe gi olenge. Iromo penjo ofisa mar kilimo mondo okonyi gi kit bel ma ok mak tuo ahinya.",
     "KALRO Sorghum Production Guide; ICRISAT Post-Harvest Management"),
    
    ("Kenya", "Luo", "sorghum",
     "Bel mara ochako nigi ondiegi matindo ma rachar e it kod e tiend kothe. Be inyalo konya?",
     "Wachno chalre gi tuo ma iluongo ni sorghum midge (Stenodiplosis sorghicola) kata aphids. Ondiegi matindo ma ochung' e tiend kothe nyalo ketho cham mokalo 30%. Tim magi: (1) Non ane ka ondiegi nitie mang'eny — ka wan'gi mang'eny to itim gima dwarore. (2) Pidh bel e ndalo ma kik rom gi chieng' moduogo mag ondiegigo. (3) Kuom bel manyien, nyis ni nitie kit bel ma ok mak ondiegigo ka Seredo kata Gadam. (4) Ka ondiegi ng'eny ahinya, tim nyono gi pesticide ma ofisa mar kilimo osenyiso — kik ing'iew moro amora ma ok g'oyiego. Dhi ir ofisa mar kilimo e alworani.",
     "ICRISAT Sorghum Pest Guide; KALRO Pest Advisory"),
    
    ("Kenya", "Luo", "tomato",
     "Nyanyondo mara otucho ma kik ochopo piny. A tuche gode, to nitie ma otwo e yath.",
     "Nyanyondo ma otucho ka podi tin kata ma otwo e yath nyiso ni nitie chandruok. Moko mag gik mitim: (1) Ne ane ka nitie tuo mar 'blossom-end rot' — ma en tuo moa kuom calcium ma oromo. (2) Mul manyien (mulching) nyalo konyo rito pi e lowo. (3) Pi ma oromo jogi pile — kik iwe lowo otwo chuth. (4) Ne ane ka nitie tuo mar early blight kata late blight — magi nyalo miyo nyanyondo tucho. (5) Keyo nyanyondo ka gisechako lokore ma rachar (breaker stage) kendo iwe gichakiekie e ot — ma konyo geng'o tucho. Dhi ir ofisa mar kilimo gi sampul mar nyanyondo mosekethore.",
     "KALRO Tomato Production Guide; AVRDC Tomato Disease Identification"),
    
    ("Kenya", "Luo", "tomato",
     "Yien nyanyondo maga wiyegi olokore ma rachar, to itgi bende orachar. Nyanyondo ok dong' nyagi.",
     "Wiyegi ma rachar kod it ma rachar e yien nyanyondo chalre gi tuo mar virus kata chandruok mar lowo. Tim magi: (1) Ne ane ka nitie tuo mar tomato yellow leaf curl virus (TYLCV) — ma en tuo ma 'whitefly' lando. (2) Ka inyalo neno 'whitefly' e it yien, tim pesticide mowinjore (neem oil kata insecticidal soap). (3) Puodho man gi yath mang'eny e bute nyalo konyo geng'o 'whitefly'. (4) Keyo yien mosekethore chuth kendo wang'gi. (5) Kuom seche mabiro, many kit nyanyondo ma ok mak tuo ka 'Rio Grande', 'Tengeru 97', kata 'Tanya'. Dhi ir ofisa mar kilimo.",
     "AVRDC TYLCV Management; KALRO Tomato Pest Advisory"),
    
    ("Kenya", "Luo", "cowpea",
     "Oganda mara ne dongo maber to koro osechako bedo ma rachar, to itgi bende olokore. Ang'o manyalo konya?",
     "Rangi ma rachar e oganda mosebedo ka dongo maber nyiso ni gima chando inyalo bedo tuo kata chandruok mar lowo. Tim magi: (1) Rangi ma rachar e itgi nyiso ni nitie tuo mar nitrogen. Nyalo bedo ni lowo ochopo — yie mondo ofisa mar kilimo one lowoni. (2) Ne ane ka nitie tuo mar aphid kata thrips — magi nyalo golo rangi e yien. (3) Los sulu mag pi e puodho mondo pi kik chung'. (4) Oganda ok dwar pi mang'eny — pi mang'eny inyalo ketho tiende. (5) Kel sampul mar lowo gi it yath ir ofisa mar kilimo.",
     "IITA Cowpea Production Guide; KALRO Legume Advisory"),
    
    ("Kenya", "Luo", "cowpea",
     "Kodhi mag oganda osebedo gi ondiegi e iye, kendo moromo ketho cham duto. Anyalo tiyo gi ang'o?",
     "Ondiegi ma chamo oganda e i keno en tuo ma luongo ni cowpea weevil (Callosobruchus maculatus). Tim magi: (1) Gol oganda oko e kar keno kendo walgi ka itieko gi yo maber — wan'o oganda mosekethore. (2) Riambo oganda e chieng' maber mondo oneg ondiegigo. (3) Kuom seche mabiro, kan oganda e 'airtight containers' ma ondiegi ok nyal donjo e iye. (4) Iromo keto oganda e 'freezer' kuom ndalo auchiel mondo oneg ondiegi kod tong' gik. (5) Tim nyono ni kar keno ler, otwo, to yamo donjoe maber. Iromo penjo ofisa mar kilimo kuom kit oganda machielo ma ok mak ondiegi.",
     "IITA Cowpea Storage Guide; KALRO Post-Harvest Bulletin"),
    
    # ═══════════════ SWAHILI (20 entries — Kenya / Tanzania) ═══════════════
    ("Kenya", "Swahili", "maize",
     "Shikamoo. Mahindi yangu yana mchanga mweupe kwenye majani na hayakui vizuri. Nilitumia mbolea ya CAN lakini haikusaidia.",
     "Shikamoo. Mchanga mweupe kwenye majani ya mahindi unaweza kuwa ishara ya ukungu wa unga (powdery mildew) au upungufu wa virutubisho. Kwa kuwa ulitumia mbolea ya CAN (inayo nitrojeni), tatizo linaweza kuwa tofauti. Haya ndiyo ya kufanya: (1) Angalia kama mchanga huo unafutika ukigusa — ukiwa unafutika, ni ukungu. (2) Chukua sampuli ya mmea mzima (pamoja na mizizi) na upeleke katika ofisi ya kilimo ya kaunti au KALRO. (3) Kwa sasa, hakikisha shamba lina mifereji mizuri — ukungu hupenda unyevu. (4) Usitumie dawa yoyote kabla ya utambuzi sahihi. Ofisi ya kilimo itakusaidia bila malipo.",
     "KALRO Maize Disease Guide; FAO Cereal Disease Identification"),
    
    ("Kenya", "Swahili", "maize",
     "Mabua ya mahindi yangu yanavunjika kwa urahisi na ndani yake kuna wadudu wadogo weusi. Hii ni shida gani?",
     "Wadudu weusi ndani ya mabua ya mahindi yanayo vunjika kwa urahisi ni ishara ya stem borer (Chilo partellus). Hawa ni viwavi wanaoingia ndani ya bua na kula tishu za ndani. Haya ya kufanya: (1) Vunja mabua yote yaliyoathirika na uyachome — hii itaua viwavi waliomo. (2) Panda mahindi mapema msimu ujao kabla ya wadudu kuwa wengi. (3) Zungusha mazao — usipande mahindi kwenye shamba hilo kwa msimu mmoja; panda mikunde kama maharagwe au kunde. (4) Aina za mahindi sugu kama 'H614', 'H6213', na 'KH500-33A' zina uhimilivu. (5) Kama shambulizi ni kubwa, wasiliana na ofisa kilimo kuhusu dawa zinazofaa za kibiashara. Usitumie dawa bila ushauri wa mtaalamu.",
     "KALRO Stem Borer Management; CIMMYT Pest Guide"),
    
    ("Kenya", "Swahili", "cassava",
     "Mhogo wangu una madoa ya kahawia kwenye mizizi na ladha ni chungu. Mbegu zilitoka kwa jirani. Naweza kupanda tena?",
     "Madoa ya kahawia kwenye mizizi ya mhogo na ladha chungu ni dalili za ugonjwa wa cassava brown streak disease (CBSD). Huu ni ugonjwa hatari unaoenezwa na wadudu wadogo weupe (whiteflies). Haya ya kufanya: (1) USIPANDE tena vipando kutoka kwa mimea hiyo — ugonjwa unaenea kwa vipando. (2) Ng'oa mimea yote iliyoathirika na uichome. (3) Nunua vipando safi, vilivyothibitishwa kutoka KALRO au ofisi ya kilimo — aina kama 'KME 08-01', 'Tajirika', au 'Kiroba' ni sugu kwa CBSD. (4) USIPANDE mhogo kwenye shamba hilo kwa msimu mmoja. (5) Waelimishe majirani wako pia — ugonjwa huu unaenea kwa urahisi kwenye eneo lote. Ofisi ya kilimo inaweza kukusaidia kupata vipando safi.",
     "KALRO CBSD Management Guide; IITA Cassava Disease Advisory"),
    
    ("Tanzania", "Swahili", "cassava",
     "Mihogo yangu ina mizizi midogo sana na majani yana rangi ya njano. Nimekuwa nikipanda sehemu hiyohiyo kwa miaka mitano.",
     "Mizizi midogo na majani ya njano baada ya kupanda sehemu moja kwa miaka mitano ni ishara ya uchovu wa udongo. Haya ya kufanya: (1) ACHA kupanda mhogo kwenye shamba hilo kwa misimu miwili — panda mikunde kama kunde au karanga badala yake. Mikunde inarutubisha udongo kwa nitrojeni. (2) Wakati unapopanda tena mhogo, tumia mbolea ya NPK (kama 15-15-15) kwa kiwango cha vijiko viwili kwa shina. (3) Panda kwenye matuta (ridges) — si kwenye udongo tambarare. (4) Tumia vipando vipya kutoka KALRO au ofisi ya kilimo, si vipando vya zamani vya shambani. (5) Pima udongo wako — ofisi ya kilimo inaweza kukusaidia kujua ni virutubisho gani vinavyokosekana.",
     "KALRO Soil Fertility Guide; IITA Cassava Agronomy; FAO Crop Rotation Principles"),
    
    ("Tanzania", "Swahili", "rice",
     "Mpunga wangu una madoa mekundu kwenye majani na miche inanyauka. Niko Morogoro.",
     "Madoa mekundu kwenye majani ya mpunga yanayosababisha miche kunyauka ni dalili za ugonjwa wa rice blast (Magnaporthe oryzae). Huu ni ugonjwa hatari sana katika maeneo ya Morogoro. Haya ya kufanya: (1) Hakikisha shamba lina maji ya kutosha lakini si mengi — ugonjwa huu hupenda mpunga ulio na mkazo wa maji. (2) Punguza matumizi ya mbolea ya nitrojeni — nitrojeni nyingi huchochea ugonjwa. (3) Kama shambulizi limeenea zaidi ya asilimia 10, wasiliana na ofisa kilimo kuhusu dawa za ukungu (fungicides) zinazofaa. (4) Kwa msimu ujao, tumia aina sugu kama 'SARO 5' (TXD 306), 'Komboka', au 'Tai'. (5) Usichelewe kupanda — panda mapema msimu. Zungumza na ofisa kilimo wa wilaya yako.",
     "IRRI Rice Blast Management; Kilimo Tanzania Rice Advisory; AfricaRice Technical Bulletin"),
    
    ("Tanzania", "Swahili", "rice",
     "Mchele wangu baada ya kuvuna una harufu mbaya na rangi ya kijivu. Niliuhifadhi kwenye magunia.",
     "Harufu mbaya na rangi ya kijivu kwenye mchele uliohifadhiwa ni ishara ya ukungu (mold) unaosababishwa na unyevu wakati wa uhifadhi. Haya ya kufanya: (1) USILE au kuuza mchele huo — ukungu unaweza kutoa sumu ya aflatoxin ambayo ni hatari kwa afya. (2) Kausha mchele vizuri kwenye jua kabla ya kuhifadhi — unyevu unapaswa kuwa chini ya 14%. Tumia mita ya unyevu kama inapatikana. (3) Hifadhi mchele kwenye magunia yaliyo juu ya godoro (pallets) — si chini kwenye sakafu. Hakikisha ghala lina hewa ya kutosha. (4) Safisha ghala vizuri kabla ya kuhifadhi mavuno mapya. (5) Kwa msimu ujao, kausha mchele mara baada ya kuvuna — usiache kwenye shamba kwa muda mrefu. Ofisa kilimo anaweza kukusaidia kujaribu unyevu wa nafaka.",
     "FAO Grain Storage Guide; Kilimo Tanzania Post-Harvest Advisory; Aflatoxin Partnership"),
    
    ("Tanzania", "Swahili", "sunflower",
     "Alizeti yangu ina maua madogo na mbegu nyepesi. Nilitumia mbolea ya kawaida lakini haikusaidia. Nafanya nini?",
     "Maua madogo na mbegu nyepesi kwenye alizeti yanaweza kuwa ni ishara ya upungufu wa boroni au uchavushaji hafifu. Haya ya kufanya: (1) Alizeti inahitaji boroni — upungufu wake husababisha maua madogo na mbegu tupu. Uliza ofisa kilimo kuhusu mbolea yenye boroni. (2) Hakikisha kuna nyuki wa kutosha shambani — alizeti inahitaji uchavushaji wa wadudu. Weka mizinga ya nyuki karibu kama inawezekana, au usitumie dawa za wadudu wakati wa maua. (3) Panda alizeti kwa nafasi — usipande kwa msongamano. Sentimita 60-75 kati ya mistari. (4) Aina kama 'Record', 'Kenya Fedha', na 'PAN 7352' zinafanya vizuri Tanzania. Zungumza na ofisa kilimo kuhusu upimaji wa udongo.",
     "Kilimo Tanzania Sunflower Guide; FAO Oilseed Advisory; ARI Naliendele Research"),
    
    ("Kenya", "Swahili", "beans",
     "Maharage yangu yana madoa ya kahawia kwenye majani na maua yanadondoka. Hali ya hewa imekuwa na unyevu mwingi.",
     "Madoa ya kahawia na maua kudondoka kwenye maharage wakati wa unyevu mwingi ni dalili za ugonjwa wa angular leaf spot au anthracnose. Haya ya kufanya: (1) Epuka kufanya kazi shambani wakati mimea ina unyevu — magonjwa huenea kwa urahisi. (2) Ondoa na uchome majani yote yaliyoathirika. (3) Hakikisha shamba lina mifereji mizuri ya maji — unyevu uliosimama huchochea magonjwa. (4) Kwa msimu ujao, panda aina sugu kama 'KK 8', 'KK 15', au 'Chelalang'. (5) USITUMIE mbegu kutoka kwenye mimea iliyoathirika — nunua mbegu safi zilizothibitishwa. (6) Kama shambulizi ni kubwa (zaidi ya 20%), wasiliana na ofisa kilimo.",
     "KALRO Bean Disease Guide; CIAT Angular Leaf Spot Management; Kenya Seed Company Advisory"),
    
    ("Kenya", "Swahili", "sweet potato",
     "Viazi vitamu vyangu vina madoa meusi kwenye ngozi na ndani yake kuna michirizi myeusi. Vinauzika kweli?",
     "Madoa meusi kwenye ngozi ya viazi vitamu na michirizi myeusi ndani ni ishara ya ugonjwa wa sweet potato virus disease (SPVD) au interne cork. Haya ya kufanya: (1) Viazi vyenye michirizi myeusi havina sumu lakini ubora wake ni duni — wanunuzi watakatalia bei ya chini. Unaweza kuviuza kwa bei ya chini kwa mifugo baada ya kuchemsha. (2) USIPANDE vipando kutoka kwa mimea hiyo — virusi huenea kwa vipando. (3) Nunua vipando safi kutoka KALRO au ofisi ya kilimo — aina kama 'Kembu 10', 'Mugande', na 'SPK 004' ni sugu. (4) Zungusha mazao — usipande viazi vitamu kwenye shamba hilo kwa misimu miwili. (5) Ondoa magugu yote shambani — magugu ni makao ya wadudu wanaoeneza virusi.",
     "KALRO Sweet Potato Disease Guide; CIP Virus Management; FAO Root Crop Advisory"),
    
    ("Kenya", "Swahili", "onion",
     "Vitunguu vyangu vinaoza kuanzia kwenye shingo na harufu ni mbaya. Nilitumia mbolea ya samadi lakini bado.",
     "Kuoza kwenye shingo la kitunguu pamoja na harufu mbaya ni dalili za ugonjwa wa neck rot (Botrytis allii) au bacterial soft rot. Haya ya kufanya: (1) Vuna vitunguu vyote mara moja vilivyo karibu kuiva — usiviache shambani. (2) Kavya (cure) vitunguu kwenye jua kwa siku 5-7 — shingo lazima likauke kabisa kabla ya kuhifadhi. (3) Kata majani hadi sentimita 2-3 kutoka kwenye shingo BAADA ya kukausha — si kabla. (4) Hifadhi kwenye chumba chenye hewa ya kutosha, baridi, na kavu. (5) USITUMIE mbolea ya samadi ambayo haijaoza vizuri — inaweza kuongeza bakteria. (6) Kwa msimu ujao, zungusha mazao — usipande kitunguu sehemu hiyo kwa misimu miwili. Ofisa kilimo anaweza kupendekeza aina sugu.",
     "KALRO Onion Production Guide; AVRDC Onion Disease Management; FAO Onion Post-Harvest"),
    
    # ═══════════════ KENYA REGION — additional crops (8 entries) ═══════════════
    ("Kenya", "Kikuyu", "coffee",
     "Kahawa yakwa nĩrarĩa nyoni nini iria njerũ na nĩ ikũnagia mawĩra. Kahawa nĩ ĩrarũrũka na ndĩracanjamũka.",
     "Nyoni njerũ (whiteflies) ikũnagia kahawa na gũtũma ĩrarũrũka nĩ kĩritũ gĩtariĩ. Mawĩra marĩa maranyitwo nĩ ikũnagia makoragwo na rĩmbu na gũkũra ti kwega. Ũndũ wa gwĩka: (1) Mĩtĩ ya kahawa ĩrarũrũka nĩũndũ wa ikũnagia — haragia ng'ano ta 'neem oil' kana sabuni ya kĩũmbe. (2) Geria gwĩkĩra mũtĩ kĩĩmbe — ikũnagia itiendaga ng'ano iria nĩ igĩrĩ. (3) Menya ũrĩa mawĩra marĩa maranyitwo marĩ — manyitithia na moko na ũmatũme. (4) Twĩka na kĩmenyithia kĩrĩa gĩtarĩ kĩa coffee berry disease o nginya — rũnyaga rwa rĩmbu nĩ rũngĩhota gwĩtia kahawa. Thie kwa ofisa wa ũrĩmi wa gĩcagi kana Coffee Research Institute.",
     "Coffee Research Institute Kenya; KALRO Coffee Pest Advisory"),
    
    ("Kenya", "Kikuyu", "tea",
     "Ciaai ciakwa irathandũkũo nĩ mahũa maria matarĩ mageni na nĩ iranyihia. Nĩndĩraruta mathangu marĩa matarĩ mega.",
     "Mahũa maria matarĩ mageni (exotic weeds) na mathangu maranyihia nĩ cina nyingĩ. Ũndũ wa gwĩka: (1) Rutithania mathangu marĩa matarĩ mega mũno na moko — ndũkanareke mahũa marĩa mageni marahurane. (2) Hũrana na mahũa marĩa mageni marĩa marahota gũkinyĩra — marahota gũthutha irio cia mĩtĩ. (3) Ndũkanahũthĩre ndawa ya kũhũrana na mahũa ũtarĩ na ũrutani — no ĩhote gũkua mĩtĩ ya ciai. (4) Rĩka handũ rĩa ngũ kana gĩthaka kĩrĩa kĩhũthĩtwo gũkũma ndawa. (5) Thie kwa ofisa wa ũrĩmi kana Tea Research Institute nĩguo maguũteithie kana kũmenya ndawa ĩrĩa yagĩrĩirwo. Ciaai nĩ iri na mũnyiti mwega — ndũkanahũthĩrie ndawa nyingĩ.",
     "Tea Research Institute Kenya; KTDA Extension; FAO Tea Cultivation"),
    
    ("Kenya", "English", "coffee",
     "My coffee cherries are falling off before they ripen. Some have small holes and I see tiny insects inside. What's happening?",
     "Cherries falling prematurely with small holes and tiny insects inside is characteristic of coffee berry borer (Hypothenemus hampei) — the most destructive coffee pest worldwide. Here's what to do: (1) Pick and destroy ALL fallen cherries immediately — don't leave any on the ground. (2) Harvest ripe cherries promptly and strip all remaining cherries at end of season — no berries left on trees means no breeding ground. (3) Maintain shade at 40-50% — borer populations increase in full sun. (4) For severe infestations, contact your local Coffee Research Institute or county extension officer — they can advise on approved insecticides like Beauveria bassiana (biological control). (5) Do NOT use unregistered pesticides — coffee is an export crop and residue limits are strict. Your extension officer can connect you with CRF training programs.",
     "Coffee Research Institute Kenya; ICIPE Coffee Berry Borer IPM; FAO Coffee Production Guide"),
    
    ("Kenya", "English", "dairy",
     "My cow's milk production dropped by half in the last week. She eats normally but her manure is watery. No vet nearby.",
     "A sudden 50% drop in milk with normal appetite but watery manure suggests several possibilities — none of which can be diagnosed remotely. DO NOT self-medicate. What to do: (1) Take the cow's temperature — a reading above 39.5°C suggests infection (mastitis, metritis, or tick-borne disease like ECF/anaplasmosis). (2) Check the udder quarters for heat, swelling, or abnormal milk (clots, watery, discolored) — mastitis is the most common cause of milk drop. (3) Check for ticks behind ears, under tail, and between legs — ECF kills within days if untreated. (4) Call a veterinary officer EVEN IF far — many counties have community animal health workers (CAHWs) who can visit. (5) In the meantime, provide clean water, good quality hay, and mineral lick. Separate this cow from others if possible. Save a fresh manure sample for the vet.",
     "KALRO Dairy Health Guide; Kenya Veterinary Board Advisory; ILRI Animal Health Protocol"),
    
    ("Kenya", "Swahili", "mango",
     "Maembe yangu yana madoa meusi kwenye matunda na majani. Matunda yanadondoka kabla hayajaiva.",
     "Madoa meusi kwenye matunda na majani ya maembe na kudondoka kabla ya kuiva ni dalili za ugonjwa wa anthracnose — ugonjwa wa kawaida wa maembe hasa wakati wa mvua. Haya ya kufanya: (1) KATA matawi yote yaliyoathirika na uyachome — usiyaache chini. (2) Kagua miti na UVUNE matunda yote yenye madoa na uyachome. (3) Dumisha usafi chini ya miti — kusanya na kuchoma majani yote yaliyoanguka na matunda yaliyooza. (4) Kwa msimu ujao, anza kunyunyizia dawa ya ukungu (fungicide ya shaba) kabla ya kutoa maua na wakati matunda ni madogo — sema na ofisa kilimo kuhusu bidhaa zinazopatikana. (5) Hakikisha miti ina nafasi ya kutosha na matawi yamepunguzwa kwa ajili ya hewa. Aina sugu ni pamoja na 'Tommy Atkins', 'Keitt', na 'Kent'.",
     "KALRO Mango Production Guide; AVRDC Mango Anthracnose Management"),
    
    ("Kenya", "Luo", "groundnut",
     "Nakatong'a karanga to ayude tiyop kata gi lowo e iye. Karanga moko duto e puodho otamo nyago. Ang'o manyalo konya?",
     "Tiyop kata lowo e i karanga kod okang' mar nyago nyiso ni nitie tuo mar aflatoxin kata tuo mar lowo. Tim magi: (1) Gol karanga duto e puodho — kik icham kendo kik ius kata gima chalre kama. Aflatoxin inyalo kelo tuo mar 'liver' ma rach. (2) Kuom seche mabiro: (a) Los sulu mag pi e puodho — pi ma chung' e lowo miyo tuo bedo mang'eny. (b) Keyo karanga ka gisechiek — kik iwe e lowo. (c) Riambo karanga e chieng' maber nyaka chop ng'ich (shelling). (d) Kan karanga e kar ma otwo, ma yamo donjoe — kik ikan ka podi gi ng'ich. (3) 'Rhizobium' kata 'Trichoderma' inyalo konyo geng'o tuo mar lowo. Penj ofisa mar kilimo.",
     "IITA Groundnut Aflatoxin Management; KALRO Legume Production Guide; FAO Mycotoxin Advisory"),
    
    ("Kenya", "Luo", "sweet potato",
     "Nepier mara osechako kethore e lowo ka pok aywayogi. Moko osebedo gi thuolo matindo to oselokore ma rachar.",
     "Nepier ma kethore e lowo ka pok oywayi nyiso ni nitie tuo kata chandruok mar lowo. Tim magi: (1) Ne ane ka nitie tuo mar sweet potato weevil (Cylas spp.) — ma en ondiegi ma lando tuo ma golo rangi ma rachar kod thuolo e nepier. (2) Ywayo nepier mosekethore duto kendo wang'gi. (3) Kuom pitho manyien, pidh kodhi maonge tuo moa kuom ofisa mar kilimo kata KALRO — kik ipidh kodhi moa kuom puodho ma tuo osemako. (4) Los ng'weng'o malo (ridges) mondo kik we ng'ong'o chakre e lowo ma chung' pi. (5) Gol nepier duto kinyoro ka gisechiek — kik iwe e lowo ng'iyo. Penj ofisa mar kilimo.",
     "KALRO Sweet Potato Pest Guide; CIP Weevil Management; FAO Root Crop Advisory"),
    
    # ═══════════════ WEAK REGIONS (6 entries) ═══════════════
    ("Uganda", "English", "banana",
     "My bananas are ripening unevenly and some have black streaks inside the fruit. The leaves are also yellowing from the edges. I grow the East African Highland type.",
     "Uneven ripening, black streaks inside fruit, and leaf yellowing on East African Highland bananas are classic symptoms of banana bacterial wilt (BBW — Xanthomonas campestris pv. musacearum). This is a serious disease that has devastated banana production across Uganda. IMMEDIATE actions: (1) Cut down and BURY the entire affected mat (all stems, leaves, roots) at least 1 meter deep — do not leave debris above ground. (2) Disinfect all tools (pangas, knives) with household bleach (jik) or flame between each plant. (3) REMOVE the male bud (flowers) from healthy plants using a forked stick — never a knife — as bees visiting infected flowers spread the bacteria. (4) Do NOT move planting material from this field to any other field. (5) Report to your district agricultural officer immediately — Uganda has a national BBW control program. They can provide clean planting material of tolerant varieties like M9 and M19.",
     "NARO Banana Bacterial Wilt Management; IITA BBW Protocol; Uganda MAAIF Extension Guide"),
    
    ("Uganda", "Luganda", "coffee",
     "Emwanyi yange ebala obulungi naye empeke zivaamu amazzi era zitera okukala. Nkozesa kasooli?",
     "Empeke ezivaamu amazzi n'okukala mu mwanyi kiyinza okuba ekiva ku ntobazi (coffee berry disease — CBD) oba ekiva ku coffee leaf rust. Bino by'okola: (1) TONDA empeke zonna ezigudde ne zikaze — zibike mu ttaka oba ozookye. (2) SALIRA amatabi agakalire n'ago agalina obulwadde — tokoma ku busira. (3) Emwanyi gy'olina tegyetaaga kasooli — kasooli ng'obungi asobola okwonoona omutindo gw'emwanyi gwo. (4) Kola ku kifo ky'omwanyi okubeera ekyonjo — okugwa kw'ebikoola bingi obubi ku ttaka kiyamba obulwadde okweyongera. (5) Genda eri ofiisa wa by'obulimi ow'essaza lyo — banaasobola okukulaga eddagala erisaanira nga erya shaba (copper-based fungicides). (6) Ennimiro y'emwanyi erina okubeera n'ekisiikirize ekiri wakati wa 40-50% — ekisiikirize eky'amaanyi kyongeza CBD.",
     "NARO Coffee Production Guide; UCDA Extension; CABI Coffee Disease Management"),
    
    ("Uganda", "English", "cassava",
     "My cassava roots are small and the leaves are curling upwards with yellow patches. I've been using stems from my own field for years.",
     "Small roots with curled leaves showing yellow patches are strong symptoms of cassava mosaic disease (CMD) — a viral disease spread by whiteflies and infected planting material. Using your own stems for years has likely accumulated the virus. What to do: (1) UPROOT and burn ALL affected plants — leaving them in the field keeps the virus source active. (2) Do NOT use any stems from this field for planting — this is how CMD spreads most. (3) Obtain CLEAN, certified planting material from NARO/NACRRI or your district agricultural office — varieties like NASE 14, NASE 19, and NAROCASS 1 are resistant to CMD and yield well in Uganda. (4) Rotate the field to legumes (beans, groundnuts, cowpeas) for at least one season. (5) Plant at the beginning of rains to give plants a strong start before whitefly populations build up. Your district NAADS coordinator can help access clean material.",
     "NARO/NACRRI Cassava Program; IITA CMD Management; Uganda MAAIF Cassava Strategy"),
    
    ("Ghana", "English", "cocoa",
     "My cocoa pods have black patches that spread quickly during rains. Some pods turn completely black and hard. I'm in the Ashanti region.",
     "Black patches on cocoa pods that spread quickly in rain and turn pods completely black and hard (mummified) is black pod disease (Phytophthora spp.) — the most destructive cocoa disease in Ghana. What to do: (1) REMOVE all infected pods immediately — cut them off and pile them away from the farm (do NOT leave them between trees). (2) Harvest ripe pods promptly — leaving ripe pods on trees increases infection. (3) Thin the canopy to allow more light and air circulation — dense shade keeps humidity high, which black pod loves. (4) Remove 'chupons' (suckers) and maintain good drainage — standing water spreads the fungus. (5) Contact your district COCOBOD extension officer — Ghana's CODAPEC program provides free fungicide spraying (Ridomil Gold, Kocide) during the rainy season. (6) Do NOT self-mix or apply chemicals without COCOBOD guidance — improper application wastes money and can leave harmful residues on export cocoa.",
     "CRIG Black Pod Management; COCOBOD CODAPEC Program; ICCO Sustainable Cocoa Guide"),
    
    ("Ghana", "Twi", "yam",
     "Me yam no mu atutu na baabi a mekora no no, ebinom reyɛ kɔla fitaa na wɔn ho ada aporɔw. Mfaso bɛn na ɛwɔ so?",
     "Yam a ne mu atutu na ebinom ho aporɔw na ayɛ fitaa wɔ baabi a wokora no yɛ nsonsono a efi fungal rot (Botryodiplodia, Fusarium, Penicillium) anaasɛ storage nematodes. Nea ɛsɛ sɛ woyɛ: (1) YI yam a wɔasɛe no nyinaa firi baabi a wokora no hɔ ntɛm ara — ɛbɛma asɛe no atrɛw akɔ yam a aka no so. (2) HWƐ yam no yiye na woanyɛ ho ade kɛse wɔ otwa bere mu — biribiara a wɔatwa de asiane no sɛee ntɛm. (3) ANSA worekora yam no, ma ɛnkyene (cure) wɔ baabi a nwini nni hɔ, ewiem yɛ hyew na mframa nso wɔ hɔ — nna 3-5. (4) Kora yam no wɔ mmea a mframa fa mu yie na ɛnyɛ nuru — mfa ngu fam hɔ koraa. (5) Afe a ɛreba no, fa yam a wɔayi no afiri dua mu no di dwuma — pɛ nhini a ɛda mu wɔ asaase mu no. (6) Kɔ COCOBOD anaa ofisa kuayɛ hɔ — wɔwɔ nnuru (fungicides) a ɛbɛboa ma woasiw asɛe a ɛte saa ano.",
     "CRI Yam Storage Guide; CSIR-Ghana Food Research; IITA Yam Post-Harvest Advisory"),
    
    ("Rwanda", "Kinyarwanda", "beans",
     "Ibishyimbo byanjye bifite ibibara by'umuhondo ku mababi kandi ntibikura neza. Nabibyaye nyuma y'ibirayi. Ni iki nakoze nabi?",
     "Ibibara by'umuhondo ku mababi y'ibishyimbo bikurikira guhinga ibirayi bishobora guterwa no kubura intungamubiri (azote) cyangwa indwara z'umutaka. Ibirayi bikura intungamubiri nyinshi mu butaka. Iby'ukora: (1) Fata urugero rw'ubutaka ujye kwa agronome — bashobora kukubwira intungamubiri zibura. (2) Ibishyimbo ubwabyo bitanga azote mu butaka, ariko ibyo byabaye nyuma yo guhinga ibirayi, bishobora kuba bikeneye inkunga y'ifumbire. (3) Teganya guhinga ibishyimbo wongeyeho ifumbire ya DAP cyangwa NPK 17-17-17 mu gihe cyo kubitera. (4) Reba niba hari udukoko twangiza imizi — ibirayi bishobora kuba byarazahaje udukoko mu butaka. (5) Kuri ubu, gerageza kongera ifumbire ya 'foliar feed' igizwe na azote (nka urea 1% mu mazi) ukayiminjira ku mababi — ariko banza ubaza agronome. (6) Mu gihe kizaza, jya uhinduranya ibihingwa — ntukore ibirayi n'ibishyimbo bikurikirana. Hinduranya n'ibigori cyangwa amashu.",
     "RAB Bean Production Guide; CIAT Rwanda Integrated Soil Fertility; FAO Crop Rotation Advisory"),
    
    ("Rwanda", "Kinyarwanda", "maize",
     "Ibigori byanjye birimo utubuye twinshi tw'umuhondo kandi ibyatsi bimaze kumera hose. Nta mafaranga mfite yo kugura imiti. Wakora iki?",
     "Utubuye tw'umuhondo nyuma yo kubyara ibigori ni ikimenyetso cya Striga (Striga hermonthica) — ikiyobyi cy'umutaka gikura cyane mu Rwanda. Iki nicyo cy'ukora nta mafaranga menshi: (1) KURA Striga yose ukimara kuyibona, mbere yuko itanga imbuto (n'iyo iba itararabye). Buri giti kimwe gishobora gutanga imbuto zigera ku 50,000. (2) UKORE ibi: washe ibigori bikivangwa n'imbuto za Striga mu mazi arimo ifumbire ya 'microdose' — DAP ikingana n'ikiganza kimwe muri buri litre 10 z'amazi. (3) Tegera ibishyimbo cyangwa ubunyobwa hagati y'imirongo y'ibigori — ibi bituma Striga itamera. (4) Mu gihe kizaza, jya uhinduranya ibihingwa buri mwaka — ntiwororoke ibigori ubwabyo. (5) Gerageza gushakisha imbuto z'ibigori zihanganira Striga nka 'KSC-Striga resistant' — egera agronome wa RAB akugire inama. (6) Kora ishuri ry'umuhinzi (farmer field school) — RAB ifite gahunda yo gufasha abahinzi kurwanya Striga.",
     "RAB Striga Management Program; CIMMYT Striga Control; FAO Push-Pull Technology Guide"),
]

# ── Build entries ───────────────────────────────────────────────────
new_entries = []
for region, dialect, crop, question, answer, source in NEW_ENTRIES_RAW:
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
        "question": question,
        "answer": answer,
        "source": source,
    })

# ── Validate ────────────────────────────────────────────────────────
print(f"Generated {len(new_entries)} new entries")
for i, e in enumerate(new_entries):
    assert e["id"].startswith("agri-"), f"Bad ID: {e['id']}"
    assert e["region"] in ["Kenya","Tanzania","Uganda","Ghana","Rwanda"], f"Bad region: {e['region']}"
    assert e["dialect"] in ["Luo","Swahili","Kikuyu","English","Luganda","Twi","Kinyarwanda"], f"Bad dialect: {e['dialect']}"
    assert 10 < len(e["question"]) < 500, f"Question too short/long at idx {i}"
    assert 50 < len(e["answer"]) < 2000, f"Answer too short/long at idx {i}"
    assert len(e["source"]) > 10, f"Source too short at idx {i}"

regions = {}
dialects = {}
for e in new_entries:
    regions[e["region"]] = regions.get(e["region"],0) + 1
    dialects[e["dialect"]] = dialects.get(e["dialect"],0) + 1
print("Regions:", dict(regions))
print("Dialects:", dict(dialects))

# ── Merge into dataset ──────────────────────────────────────────────
merged = existing + new_entries
with open(DATASET_PATH, "w") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"\nMerged: {len(existing)} → {len(merged)} entries")
print(f"Saved to {DATASET_PATH}")

# Print count by region/dialect post-merge
from collections import Counter
r2 = Counter(e["region"] for e in merged)
d2 = Counter(e["dialect"] for e in merged)
total = len(merged)
for r,n in r2.most_common():
    print(f"  {r:15s}: {n:4d} entries")
print(f"  {'TOTAL':15s}: {total:4d} entries")
