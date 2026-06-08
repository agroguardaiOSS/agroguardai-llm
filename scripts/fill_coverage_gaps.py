#!/usr/bin/env python3
"""Generate ~200 entries to fill coverage gaps from 815 to 1,000+ entries.
Targets: Kinyarwanda, Luganda, Twi, Kanuri, Tiv, Ibibio, beans, sunflower, dairy, weak combos."""

import json
from pathlib import Path
from collections import Counter

DATASET_PATH = Path("data/agri_qa.json")

with open(DATASET_PATH) as f:
    existing = json.load(f)

last_id = max(int(e["id"].replace("agri-", "")) for e in existing)
next_id = last_id + 1
existing_ids = {e["id"] for e in existing}

# ── GENERATORS ──────────────────────────────────────────────────────
# (region, dialect, crop, question, answer, source, category)

NEW = [

    # ═══════════════ KINYARWANDA — Rwanda (20 entries) ═══════════════
    # beans
    ("Rwanda", "Kinyarwanda", "beans",
     "Ibishyimbo byanjye biribwa n'udukoko duto dutukura tw'ijosi. Hari umuti nta kiguzi?",
     "Udusimba tw'ijosi dutukura ni aphids. Hano ni uko wabirwanya nta mafaranga: (1) Tegura amazi y'isabune y'inkari (5g ya sabuni ya materasi mu litre 1 y'amazi) hanyuma uyicishe kuri ibyo bimera. (2) Shaka ibishyimbo bitandukanye — nk'ibishyimbo by'umweru n'ibijima — byoroshya imirire y'ubutaka. (3) Ntuterane cyane — haga umwanya hagati y'ibishyimbo. (4) Koresha ibishara (mulch) nk'ibyatsi byumye kugira ngo ubutaka butinyishe amazi. (5) Niba ibishyimbo byaranduye cyane, urabe ukura kandi ukayitwika kure y'umurima.",
     "RAB Bean Production Guide; CIAT Bean Pest Management", "pest management"),

    ("Rwanda", "Kinyarwanda", "beans",
     "Ibishyimbo byanjye byera ibara ry'umuhondo kandi ntibikura neza. Byabaye iki?",
     "Ibara ry'umuhondo ku bishyimbo bishobora guterwa n'ibintu byinshi: (1) Kubura azote (nitrogen) — ibishyimbo bikora azote ubwabyo, ariko niba ubutaka bufite aside nyinshi (pH iri hasi), ntibishobora gukora neza. (2) Indwara ya virus (Bean Common Mosaic Virus) — iyi virus iterwa n'aphids. (3) Kubura amazi — ibishyimbo bikenera amazi mu gihe cyo gukura. Ingamba: (1) Ohereza ubutaka mu kigo cy'ubuhinzi (RAB) kugira ngo bapime pH. (2) Niba aside nyinshi, shyiramo ifumbire y'inka cyangwa lime. (3) Hitamo imbuto zihanganira indwara — zigwa mu biro by'ubuhinzi. (4) Jya uhinduranya ibihingwa — ntukore ibishyimbo ku murima umwe buri mwaka.",
     "RAB Soil Fertility Guide; CIAT Bean Disease Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "maize",
     "Ibigori byanjye ntibikura neza n'ibibara byabyo ni ibishya, ndetse n'ibiti byabyo biroroshye. Mbona imizi yabyo ari mito. Ngize iki?",
     "Ibi byose ni ibimenyetso byo kubura fosifori (phosphorus) mu butaka. Iki ni ikibazo kenshi mu Rwanda aho ubutaka buffite aside nyinshi. (1) Ohereza ubutaka bwawe mu ishami rya RAB riri hafi yawe kugira ngo bapime. (2) Shyiramo ifumbire ikize kuri fosifori (DAP) ubwo uhinga, ikiganza kimwe ku giti cy'ibigori. (3) Koresha ifumbire y'inka cyangwa ifumbire y'ibimera (compost) — byongera ubuzima bw'ubutaka. (4) Hitamo imbuto z'ibigori zikura vuba — zikenera fosifori nke. (5) Mu gihe kizaza, kora imirongo izenguruka imisozi (contour ridging) kugira ngo ubutaka butazanywa n'amazi.",
     "RAB Maize Nutrition Guide; CIMMYT Soil Fertility", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "maize",
     "Ibigori byanjye birimo utuntu twinshi tw'umukara ku mpusu. Ibi bintu ni ibiki?",
     "Uwo ni ugukanya k'ibigori (maize smut — Ustilago maydis). Ni indwara y'ibigori ikunze kugaragara mu Rwanda igihe cy'ubushyuhe bukabije. (1) Kura utwo tuntu mbere y'uko tumeneka — bitabarika utwo tuntu dusohora imyanda y'indwara mu butaka. (2) Twika utwo tuntu kure y'umurima — ntukabishyire mu kirundo cy'ifumbire. (3) Hinduranya ibihingwa — ntuhinge ibigori aho wabikoze umwaka ushize. (4) Hitamo imbuto zihanganira indwara nka 'PAN 691' cyangwa 'SC 403'. (5) Ntukoreshe ifumbire ya azote nyinshi — iyo ikabije ituma indwara ikura cyane.",
     "RAB Maize Disease Guide; CIMMYT Smut Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "coffee",
     "Ikawa yanjye ifite amabara y'umuhondo ku mababi kandi amababi arahinduka. Mbona utuntu tw'umweru munsi y'amababi. Ni iki gitari?",
     "Ibi ni ibimenyetso by'udukoko twa 'berry borer' (Hypothenemus hampei) n'utuntu tw'umweru ni indwara ya 'white stem borer'. (1) Kura amababi yose yanduye hanyuma uyature kure y'umurima. (2) Kora isuku mu murima w'ikawa — kura ibyatsi byose n'ibiti byapfuye. (3) Tegura amazi y'isabune (5g sabuni mu litre 1 y'amazi) hanyuma uyicishe kuri buri giti. (4) Hitamo ibiti by'ikawa bihanganira indwara — shyira mu giti cya RAB cyangwa OCIR-Café. (5) Shyira ibiti bitanga igicucu (shade trees) nk'ibiti by'amaseri (grevillea) cyangwa ibiti by'amasaka. (6) Ntukoreshe imiti ikomeye itaragiiwe inama n'umugenzuzi w'ubuhinzi.",
     "OCIR-Café Coffee Pest Guide; RAB Coffee Advisory", "pest management"),

    ("Rwanda", "Kinyarwanda", "coffee",
     "Imbuto z'ikawa zanjye zirahinduka umukara zikanyanyagira hasi mbere y'igihe. Ni iki gitari?",
     "Ibi ni indwara ya Coffee Berry Disease (Colletotrichum kahawae). Ni indwara ikomeye mu Rwanda ihitana imbuto z'ikawa nyinshi. (1) Kura imbuto zanduye zirimo umukara hanyuma uzitwike. (2) Mu gihe cy'imvura nyinshi, jya ugenda urabona imbuto zanduye ukazikura. (3) Hitamo ubwoko bw'ikawa buhanganira indwara: BM 139, BM 71, cyangwa BM 229. (4) Shyira ibiti bitanga igicucu — ikawa ikora neza mu gicucu gito. (5) Niba indwara ikaze cyane, ugomba kugura umuti ufasha ubutaka — shaka inama mu biro by'ubuhinzi. (6) Ntukabike imbuto zanduye hamwe n'iziza — zabasanya indwara.",
     "OCIR-Café CBD Management; RAB Coffee Disease Guide", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "banana",
     "Ibiti by'ibiteme byanjye bibika amababi y'umuhondo kandi imbuto nto zirahita zinyanyagira. Ni iki gitari?",
     "Ibi ni indwara ya Banana Xanthomonas Wilt (BXW). Ni indwara ikomeye mu Rwanda yibasira ibiteme. (1) TEMUKA ubutayu buti bw'ibiti byanduye ku butaka, ukabutema, hanyuma ukabuTWIKE. (2) Koresha umuhoro umwe gusa ku biti byose — ukoresheje amavuta y'agakoko (engine oil) kugira ngo wirinde ko indwara ikwirakwira. (3) Ntukajyane imbuto z'ibiteme ziva ku biti byanduye. (4) Hitamo imbuto z'ibiteme ziva mu biro by'ubuhinzi — aho zigenzuwe neza. (5) Menyesha abaturanyi bawe — BXW ishobora kwangiza umurima wose. (6) Mu gihe cy'amezi 6 nyuma yo gukura ibiti byanduye, ntuhinge ibiteme aho hantu.",
     "RAB BXW Control Program; IITA Banana Disease Advisory", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "banana",
     "Ibiti by'ibiteme byanjye ntibikura neza kandi amababi arabangirika. Mbona utuntu tw'umuhondo ku mababi. Ni iki?",
     "Utuntu tw'umuhondo ku mababi y'ibiteme ni indwara ya Banana Streak Virus (BSV) cyangwa ikibazo cy'udukoko twa thrips. (1) Hitamo imbuto z'ubutayu buti bw'ibiteme ziva mu nzego z'ubuhinzi — aho zigenzuwe neza. (2) Kura amababi yanduye ukayature kure y'umurima. (3) Shyira ibyatsi byumye (mulch) ku giti cy'ibiteme kugira ngo ubutaka bugumane amazi. (4) Shyiramo ifumbire y'ibimera (compost) ku giti — ibiteme bikenera ifumbire nyinshi. (5) Hitamo ubwoko bw'ibiteme buhanganira indwara: 'Pisang Awak', 'Yangambi KM5' cyangwa 'FHIA-17'. (6) Jya uhinduranya ibiti by'ibiteme nyuma y'imyaka 3—5.",
     "RAB Banana Production Guide; IITA BSV Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "cassava",
     "Imiyege yanjye ifite amababi ahindagurika kandi imizi yanjiye ikora ibara ry'umukara. Twakora iki?",
     "Ibi ni indwara ya Cassava Mosaic Disease (CMD). (1) Kura ibiti byanduye wongere ubitwike — ntibikure. (2) Hitamo ibiti by'imiyege bihanganira CMD: TME 419, MM96/5280 cyangwa 'NASE 14'. (3) Ntukore imiyege aho wayikoze umwaka ushize — hinduranya ibihingwa. (4) Imiyege ikenera imvura ihagije, ariko ngo itanyara amazi. Kora imirongo kugira ngo amazi ataguma mu murima. (5) Jya ugura ibiti by'imiyege mu biro by'ubuhinzi — aho zigenzuwe neza ntibizana indwara.",
     "RAB Cassava Disease Guide; IITA CMD Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "sweet potato",
     "Ibijumba byanjye bifite utubuye twinshi mu mizi n'ibara ry'umukara. Nta cyiza nkura. Ni iki gitari?",
     "Utubuye twinshi n'ibara ry'umukara mu bijumba ni indwara ya Sweet Potato Weevil (Cylas formicarius). (1) Kora isuku — kura ibijumba byose byanduye hanyuma ubitwike. (2) Hitamo imbuto z'ibijumba zihanganira udukoko — RAB ifite ubwoko bwiza. (3) Kora imirongo (ridges) kugira ngo ubutaka butinyishe amazi neza. (4) Ntukore ibijumba aho wabikoze umwaka ushize — hinduranya ibihingwa. (5) Ijumba rikura neza mu butaka butose ndetse bufite pH ya 5.5—6.5. Ohereza ubutaka bwawe mu kigo cy'ubuhinzi. (6) Saruza ibijumba vuba — ntibikare mu butaka igihe kirekire nyuma yo gukura.",
     "RAB Sweet Potato Guide; IITA Weevil Management", "pest management"),

    ("Rwanda", "Kinyarwanda", "sweet potato",
     "Ibijumba byanjye byera ibara ry'ijosi (brown) mu mizi ndetse binogeye uburo. Ni iki gitari?",
     "Ibara ry'ijosi n'uburo mu bijumba ni indwara ya Sweet Potato Virus (SPVD) cyangwa ikibazo cyo kubura potasiyumu (potassium). (1) Hitamo imbuto z'ibijumba zihanganira indwara — RAB ifite ubwoko bwiza. (2) Ohereza ubutaka bwawe mu kigo cy'ubuhinzi kugira ngo bapime. (3) Shyiramo ifumbire ikize kuri potasiyumu — ifumbire y'inka cyangwa ifumbire y'ibimera. (4) Ntukore ibijumba aho wayikoze umwaka ushize. (5) Kura ibiti byanduye ukabitwike. (6) Ijumba rikenera imvura nke ugereranije n'indi mbuto — nirinyara amazi menshi, indwara ziyongera.",
     "RAB Sweet Potato Disease Guide; CIP SPVD Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "dairy",
     "Inka yanjye ifite amata make nyuma yo kubyara. Ndiyagira iki?",
     "Inka igira amata make nyuma yo kubyara biterwa n'impamvu nyinshi. (1) Ibyo kurya — inka ikenera amafunguro meza: ubwatsi bwiza, amashaka (dairy meal) 2—3 kg ku munsi. (2) Amazi — inka igira amata myinshi iyo inyoye amazi meza menshi: litiro 40—60 ku munsi. (3) Indwara — inka ishobora kuba ifite indwara ya mastitis cyangwa amabere yanduye. (4) Ubushyuhe — inka ikunda ubushyuhe bwa 10—25°C. (5) Hitamo ubwoko bw'inka zitanga amata myinshi: Jersey, Friesian cyangwa inka zivanze (cross-breed). (6) Jya ujya inka zawe ku mugenzuzi w'amatungo (veterinary) buri kwezi. (7) Koresha ubwatsi burimo ibinyamisogwe byinshi nka Meyer grass, Rhodes grass cyangwa lucerne.",
     "RAB Dairy Production Guide; MINAGRI Livestock Advisory", "general inquiry"),

    ("Rwanda", "Kinyarwanda", "dairy",
     "Inka yanjye ifite amabere ababaza kandi amata yanjye aragwinya ndetse arimo ibishishima. Ni iki?",
     "Ibi ni mastitis — indwara y'amabere mu nka. (1) HITA uhamagara umugenzuzi w'amatungo (vet). (2) Kora isuku — karoza amabere y'inka mbere yo gukama. (3) Koresha amavuta ya teat dip nyuma yo gukama buri munsi. (4) Ntukame inka zose n'uruho rumwe — koresha uruho rutandukanye kuri buri nka. (5) Kama inka zifite mastitis ari zo za nyuma — utangirane n'iziza mbere. (6) Sukura ahantu inka zikamirwa buri munsi. (7) Niba inka igira ubushyuhe, ugomba umuti wa antibiotique — shaka ubufasha bw'umugenzuzi w'amatungo. (8) Jya uvura inka ikurikiranye — mastitis igaruka niba itavuwe neza.",
     "RAB Mastitis Control Guide; MINAGRI Veterinary Advisory", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "sorghum",
     "Amasaka yanjye afite utuntu tw'umukara nk'igishishima ku mpusu. Mbese iyi ni indwara?",
     "Uwo ni ugukanya kw'amasaka (sorghum smut — Sporisorium sorghi). (1) Kura ibiti byanduye mbere y'uko utwo tuntu tumeneka — bikomeye kuko utwo tuntu twogosha imyanda mu butaka. (2) Twika ibyo biti kure y'umurima. (3) Hitamo imbuto z'amasaka zihanganira indwara: 'Macia', 'Seredo' cyangwa 'Gadam'. (4) Mbere yo kubiba, shyiramo imbuto mu mazi y'ubushyuhe (52°C) ku minota 10. (5) Hinduranya ibihingwa — ntuhinge amasaka aho wayikoze umwaka ushize. (6) Ntukoreshe ifumbire ya azote nyinshi ku masaka.",
     "RAB Sorghum Guide; ICRISAT Smut Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "sorghum",
     "Amasaka yanjye aribwa n'inyoni mbere y'uko mpaka. Haracyari nk'amezi abiri nkura. Nkora iki?",
     "Inyoni zangiza amasaka cyane mu Rwanda. (1) Shyira ibikoresho birusha urusaku (scarecrows) — imizinga, amapora cyangwa ibikoresho by'icyuma bivuga. (2) Kora urusenge rw'imyaka mu murima — inyoni zifite ubwoba bw'imyaka. (3) Hitamo ubwoko bw'amasaka bufite impusu igoye — inyoni zitonona ubwoko nka 'Seredo'. (4) Saruza amasaka vuba ukiboneza — ntuyareke mu murima igihe kirekire. (5) Shorera mu murima abana cyangwa abakozi bo kurinda inyoni mu gihe cyo kwegeranya. (6) Tegura imitego y'inyoni — ariko ntukice inyoni zose kuko zimwe zifasha mu bindi bintu.",
     "RAB Sorghum Bird Control; ICRISAT Bird Management", "pest management"),

    ("Rwanda", "Kinyarwanda", "groundnut",
     "Ubunyobwa bwanjye bufite amababi y'umuhondo kandi imizi yabwo irimo utubuye tw'ijosi. Ni iki?",
     "Ibi ni indwara ya groundnut rosette virus. (1) Kura ibiti byanduye byose ukabitwike. (2) Hitamo imbuto z'ubunyobwa zihanganira rosette: 'Nyirahindurwa', 'Mfitego' cyangwa 'Serenut 4T'. (3) Ntukore ubunyobwa aho wabukoze umwaka ushize — hinduranya ibihingwa. (4) Shyira ibyatsi byumye (mulch) mu murima kugira ngo ubutaka butinyishe amazi. (5) Shyiramo ifumbire y'ibimera (compost) mbere yo gutera. (6) Ubunyobwa bukenera pH 6.0—6.5 by'ubutaka. Ohereza ubutaka bwawe mu kigo cy'ubuhinzi kugira ngo bapime pH.",
     "RAB Groundnut Guide; ICRISAT Rosette Management", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "tomato",
     "Inyanya zanjye zirababara kandi zifite ibara ry'umukara ku mpera. Mbese nzitabika iki?",
     "Ibi ni 'blossom-end rot' — ntabwo ari indwara ya virus ahubwo ni ikibazo cyo kubura calcium. (1) Ntukoreshe ifumbire ya azote nyinshi — izahagarika calcium. (2) Tegura amazi neza — inyanya zikenera amazi ahagaze neza (zitanyarara kandi zitinwe). (3) Shyira ibyatsi byumye (mulch) kugira ngo ubutaka butinyishe amazi. (4) Hitamo ubwoko bw'inyanya buhanganira ikibazo: 'Tengeru 97', 'Rio Grande' cyangwa 'Moneymaker'. (5) Shyiramo ibishishwa by'amagi (egg shells) cyangwa lime mu butaka kugira ngo wongere calcium. (6) Tegura ifumbire ya calcium mu mazi (1 tablespoon ya calcium nitrate mu litre 4 y'amazi) hanyuma uyicishe ku mizi buri cyumweru.",
     "RAB Tomato Production Guide; AVRDC Blossom-end Rot Advisory", "disease diagnosis"),

    ("Rwanda", "Kinyarwanda", "maize",
     "Ibigori byanjye byaranduye n'udukoko two mu butaka twaciye imizi. Hari igisubizo?",
     "Udukoko two mu butaka twica imizi y'ibigori ni 'cutworms' cyangwa 'rootworms'. (1) Shyira ibyatsi byumye (mulch) ku butaka — ibi bihagarika udukoko. (2) Kora imirongo izenguruka imisozi (contour ridges) kugira ngo udukoko tutanyeganyega. (3) Hitamo imbuto z'ibigori zikura vuba — iyo zikura vuba, udukoko ntitwongera kuzibangamira. (4) Ntukore ibigori aho wabikoze umwaka ushize — hinduranya ibihingwa. (5) Shyiramo ibishara by'ibiti bya neem (neem cake) mu butaka — neem ihagarika udukoko twinshi. (6) Niba udukoko ari twinshi cyane, shaka inama mu biro by'ubuhinzi ku bijyanye n'imiti.",
     "RAB Maize Soil Pest Guide; CIMMYT Rootworm Control", "pest management"),

    ("Rwanda", "Kinyarwanda", "cassava",
     "Nshaka gutera imiyege ariko simfite ibiti byiza. Nakwirakiza ibiti kugira ngo mbone umusaruro mwiza?",
     "Gutera imiyege ufite ibiti byiza ni ingenzi. (1) Hitamo ibiti by'imiyege biva mu biro by'ubuhinzi — aho bapima ko ntibizana indwara. (2) Hitamo ubwoko buhanganira indwara — TME 419, MM96/5280 cyangwa 'NASE 3'. (3) Ibiti bigomba kuba bya 6—8 cm mu nshinga, bifite amasabwa 5—6. (4) Mbere yo gutera, shyiramo ibiti mu mazi y'ubushyuhe (52°C) ku minota 10 — bigabanya indwara. (5) Tera imiyege mu gihe cy'imvura — herekana ko ubutaka bufite amazi ahagije. (6) Shyira ibyatsi byumye mu murima kugira ngo ubutaka butinyishe amazi ndetse n'udukoko tukagabanuka.",
     "RAB Cassava Planting Guide; IITA Cassava Propagation", "cultural practice"),

    ("Rwanda", "Kinyarwanda", "cotton",
     "Nshaka gutera ipamba ariko nta buhanga mfite. Ni gute nategura ubutaka?",
     "Gutegura ubutaka bw'ipamba ni ingenzi ku musaruro mwiza. (1) Hingura ubutaka bwawe mu bujinja bwa 20—30 cm — ipamba ikenera ubutaka bwose. (2) Ohereza ubutaka mu kigo cy'ubuhinzi kugira ngo bapime pH (ikiza ni 5.5—7.0) n'ibiribwa. (3) Shyiramo ifumbire y'ibimera cyangwa ifumbire y'inka mbere yo guhinga. (4) Hitamo imbuto z'ipamba zihanganira udukoko — RAB ifite ubwoko bwiza. (5) Tera imbuto mu gihe cy'imvura — ipamba ikenera ubushyuhe bwa 20—35°C. (6) Haga umwanya hagati y'imirongo: cm 75 hagati y'imirongo, cm 30 hagati y'ibiti. (7) Jya ukura ibyatsi bibisha mu murima — ipamba ntikunda guhangana n'ibyatsi.",
     "RAB Cotton Production Guide; MINAGRI Cotton Advisory", "cultural practice"),

    # ═══════════════ LUGANDA — Uganda (20 entries) ═══════════════
    ("Uganda", "Luganda", "beans",
     "Ebijanjaalo byange bifulumye amabala amatoosi n'ebikoola nabyo bifulumye kyenvu. Kola ki?",
     "Ebyo bye bimenyetso by'endwadde ya anthracnose mu bijanjaalo. (1) Ggya ebijanjaalo ebyo ebiriko ebibala olwo obikyokye — tobyasuula ku ttaka. (2) Tola embuto ezirina obusobozi okulwanyisa endwadde okuva mu ttendekero lya NARO oba mu ofiisi y'ebyobulimi. (3) Wola omusulo omulungi (mulch) okusobola okugema ebirime — endwadde z'ebikoola ziyitibwa mu taka. (4) Wonnonza ettaka: wewale okusimba ebijanjaalo mu ttaka lye wagulimu omwaka oguwedde. (5) Fuka ssabbuuni mu biseera eby'enkuba nnyingi okugoba endwadde: essabbuuni 10g mu lita 1 y'amazzi. (6) Tega ebijanjaalo mu biseera eby'enkuba enkalu — ebbala lyongera mu bunnyogovu.",
     "NARO Bean Production Guide; CIAT Anthracnose Management", "disease diagnosis"),

    ("Uganda", "Luganda", "beans",
     "Ebijanjaalo byange tebikula bulungi n'ebikoola bibadde bya kyenvu. Waliwo byange?",
     "Ebijanjaalo ebya kyenvu kiyinza okuba nga ttaka lirina obuzibu. (1) Ettaka lirina asidi myingi: gezaako okuteeka lime oba evvu lya nkye (2—3kg ku butanda). (2) Ebijanjaalo byetaaga obusumbi bwa azote wadde nga bikola azote ez'omu ttaka — naye singa ttaka lirina afo nyo oba linyonnyolebwa, zisobola okubulwa. (3) Oteeka empalira (mulch) okuyamba okukuumira ebiriisa n'amazzi. (4) Tonnonnyanga ttaka: teeka ebijanjaalo bw'omala ebbira (grass) oba lumonde — ekyo kiyamba okuzzaawo Azote. (5) Gezaako ettaka lyo mu ofiisi y'ebyobulimi — bakugamba ekitali kituufu.",
     "NARO Soil Fertility Guide; CIAT Bean Nutrition", "general inquiry"),

    ("Uganda", "Luganda", "maize",
     "Omuwogo gwange gukulira mutono ate ebikoola biriko ebibala bya kakonge (rust) era bigwa. Nnyonnyola?",
     "Ebibala bya kakonge ku bikoola by'omuwogo bya endwadde ya maize rust (Puccinia sorghi). (1) Ggya ebikoola ebyo ebiriko ebibala — byokya tobyasuula ku ttaka. (2) Yesimba omuwogo nga ttonnya (spacing): cm 75 wakati w'emirongo, cm 25 wakati w'emiti. (3) Tola embuto z'omuwogo ezirina obusobozi okulwanyisa endwadde okuva mu NARO. (4) Ku z'okuddamu okusimba, wewale okusimba omuwogo mu ttaka lye walimu. (5) Fuka omusulo (mulch) okuyamba okukuuma amazzi. (6) Oba omuwogo gweyongera okwonooneka, kozesa eddagala erikkirizibwa ofiisi y'ebyobulimi.",
     "NARO Maize Rust Guide; CIMMYT Rust Management", "disease diagnosis"),

    ("Uganda", "Luganda", "maize",
     "Ebikoola by'omuwogo gwange bibadde biriko obulabe obweru (white streak) era nga teguli Nsimbye mu ludda olumu. Kiki ekiriwo?",
     "Owo obulabe obweru ku bikoola by'omuwogo ye maize streak virus (MSV). (1) Kola okulwanyisa obuwuka obutono obweru (leafhoppers) obuleeta obulabe — obuwuka buno buba wansi w'ebikoola. (2) Ggya ebikoola ebiri obulabe byokye tobyasuula ku ttaka. (3) Tola embuto ezirina obusobozi okulwanyisa MSV — muli 'Longe 5', 'Longe 7' oba 'WH 505'. (4) Simba omuwogo nga wakati entongole (early planting) — kino kiyamba okukwata obuwuka nga bweyali butono. (5) Wola omusulo (mulch) okukendeeza obuwuka. (6) Tonnonnyanga omuwogo — goleqa n'ebimera ebirala nga ebijanjaalo.",
     "NARO MSV Management; CIMMYT Streak Virus Control", "disease diagnosis"),

    ("Uganda", "Luganda", "coffee",
     "Omwanyi gwange guliko ebikoola ebya kyenvu ebitono ate emikolo gye giri yadde si gya kweyama. Nkoze ki?",
     "Ono ayinza okuba akawuka ka leaf miner (Leucoptera spp.). (1) Ggya ebikoola ebyo ebikyenvu ebiriko amabala — byokye. (2) Tega obutimba (sticky traps) mu nnimiro — bukwata obuwuka obutono. (3) Kozesa sabbuuni n'obulago eri mu nsi (neem oil): litiro 1 y'amazzi, sabbuuni 5g, obulago bwa neem 5ml. (4) Simba emiti gy'ekisiibo (shade trees) nga musizi oba grevillea — omwanyi guyagala ekisiibo. (5) Kola okulonda ebirime (pruning) ekisobola okuleeta omukka nga emyaka. (6) Rwala ebimanyiddwa mu ofiisi y'ebyobulimi oba mu UCDA — bakugamba ekirala.",
     "UCDA Coffee Leaf Miner Guide; NARO Coffee Pest Advisory", "pest management"),

    ("Uganda", "Luganda", "coffee",
     "Ebibala by'omwanyi byange biriko ebifo ebyeru (white) ate nga bigwa wansi. Lwaki?",
     "Ebyo bye bimenyetso by'endwadde ya Coffee Berry Disease (CBD). (1) Ggya ebibala ebyo ebiriko ebyeru byokye tobyasuula ku ttaka. (2) Tola ebibala ebirongoofu okuva ku muti ogwabulijjo — totola ebiva wansi. (3) Simba ebika by'omwanyi ebirina obusobozi okulwanyisa CBD: ebya Ruiru 11, SL28 oba Batian. (4) Wonnonza ettaka: tosimba mwanyi mu ttaka lye walimu omwaka oguwedde. (5) Tega emiti gy'ekisiibo okugabanya obunnyogovu — kino kikendeeza CBD. (6) Oba endwadde yongera, kozesa eddagala eririna obutiti bwa copper okuva mu UCDA — wabula embeera, bakulembeza okugoberera eddagala.",
     "UCDA CBD Management; NARO Coffee Disease Control", "disease diagnosis"),

    ("Uganda", "Luganda", "banana",
     "Ebitooke byange biriko ebifo ebya kyenvu era amabala gabyo gabulijjo negalya. Nkoze ki?",
     "Ebyo ye ndwadde ya Black Sigatoka (Mycosphaerella fijiensis). (1) Ggya amabala gonna agaliko endwadde — bakola okukendeeza obukosefu. (2) Temu ebikoola ebiriko endwadde — byokya tobyasuula ku ttaka. (3) Tola obutaka bw'ebitooke okuva mu NARO oba ofiisi y'ebyobulimi — busobola okuba bulongoofu. (4) Wonnonza ettaka — tosimba bitooke mu ttaka lye walimu omwaka oguwedde. (5) Fuka omusulo (mulch) okuyamba okukendeeza amabala. (6) Tega eddagala eririna copper oba neem — kozesa bulijjo buli wiiki 2—3 mu biseera by'enkuba.",
     "NARO Sigatoka Management; IITA Banana Disease Guide", "disease diagnosis"),

    ("Uganda", "Luganda", "banana",
     "Ebitooke byange ebikekeddwa (matooke) tebirina buwangwa era nga bigwa wansi. Nnyonnyola?",
     "Ebitooke ebitabula buwangwa kiyinza okuba nga ettaka telirina ebiriisa ebyetaagisa. (1) Fuka omusulo (mulch) — kino kiyamba okukuumira amazzi n'okukendeeza omusana ogwokya. (2) Teeka empalira (compost) oba obusa bw'ente (2—3kg ku muti buli kkumi n'ebiri (12 weeks). (3) Nga kitooke kikaddiye, temulira (prune) — ggyako ebikoola ebikaddiye. (4) Tola obutaka bwa NARO obulina obusobozi obulungi bw'ekika: 'Mbwazirume', 'Nakyetengu', 'Enyeru', 'Kibuzi' oba 'FHIA-17'. (5) Tega ekifo ekiyitibwa 'de-suckering' — leka obutaka 3 ku muti ogwakusiba. (6) Fuka amazzi mu biseera eby'omusana — bitooke byetaaga amazzi okusobola okukula bulungi.",
     "NARO Matooke Production Guide; IITA Banana Nutrition", "cultural practice"),

    ("Uganda", "Luganda", "cassava",
     "Emuwogo gwange guliko ebikoola ebya kyenvu ate ntudde nga si gwa kusimba?",
     "Ono ayinza okuba endwadde ya Cassava Mosaic Disease (CMD). (1) Ggya emuwogo ogwo oguliko endwadde — gulye by'okya si kulowooza. (2) Tola ebibala by'emuwogo ebya NARO ebirina obusobozi okulwanyisa CMD: TME 419, NASE 14 oba MH95/0183. (3) Tega ettaka — wonnonza emuwogo ne bimera ebirala. (4) Kola okusimba emuwogo mu nsobi (ridges) okuleeta amazzi. (5) Tega obukodyo obulwanyisa obuwuka obweru (whiteflies) obuleeta CMD — kozesa neem oba sabbuuni. (6) Simba emuwogo nga kituuse (early planting) — n'ekyangu, emuwogo gisobola okukula nga bwegali obuwuka tebunazze.",
     "NARO Cassava Mosaic Guide; IITA CMD Control", "disease diagnosis"),

    ("Uganda", "Luganda", "cassava",
     "Emuwogo gwange nga guba wansi, guliko ebirenga (cracks) ate nga waliwo ekirungo ekibi. Lwaki?",
     "Ebirenga mu muwogo n'ekirungo ekibi bigenda mu ndwadde ya Cassava Brown Streak Disease (CBSD). (1) Temu emuwogo ogwo — oggyemu byona. (2) Tola ebibala by'emuwogo ebya NARO ebirina obusobozi okulwanyisa CBSD: NASE 14, NAROCASS 1 oba NASE 3. (3) Tonnonnyanga muwogo — wonnonza n'ebimera ebirala nga ebijanjaalo oba lumonde. (4) Tega obukodyo olw'okulwanyisa obuwuka obweru (whiteflies) — kozesa neem. (5) Tega emirundi okusimba mu biseera eby'enkuba — CBSD yongera mu bunnyogovu. (6) Simba emuwogo mu nsobi (ridges) ekisobola okuleeta amazzi.",
     "NARO CBSD Guide; IITA Cassava Brown Streak Control", "disease diagnosis"),

    ("Uganda", "Luganda", "groundnut",
     "Ebinyeebwa byange ebikoola biriko ebibala ebya kyenvu n'amabala. Kiki ekiriko?",
     "Ebyo bye bimenyetso bya leaf spot (Cercospora). (1) Ggya ebikoola ebyo ebya kyenvu — byokya. (2) Tega emirundi emirala — tosimba binyeebwa mu ttaka lye walimu omwaka oguwedde. (3) Tola embuto eza NARO ezirina obusobozi okulwanyisa leaf spot: 'Serenut 2', 'Serenut 3' oba 'Igola'. (4) Simba mu nsobi (ridges) okuleeta amazzi. (5) Kozesa omusulo (mulch) okukendeeza ebikoola ebya leaf spot — kino kikendeeza obunyogovu. (6) Oba endwadde eyongera, kozesa eddagala eririna copper oba neem — singa omanyi akatambi.",
     "NARO Groundnut Leaf Spot Management; ICRISAT Foliar Disease Guide", "disease diagnosis"),

    ("Uganda", "Luganda", "sweet potato",
     "Lumonde lwange nga lwaka, luliko obwongo (holes) ate nga luzimbala. Kiki ekyo?",
     "Obwongo mu lumonde ye ndwadde ya sweet potato weevil (Cylas formicarius). (1) Ggya lumonde olwo oluliko obwongo — lwokye. (2) Tola emitogo gya NARO ogulina obusobozi okwewala enkokerwa eno: 'NASPOT 5', 'NASPOT 7' oba 'NKA IIR'. (3) Wonnonza ettaka — tosimba lumonde mu ttaka lye walimu omwaka oguwedde. (4) Simba mu nsobi (ridges) ekisobola okuleeta amazzi. (5) Siba lumonde nga gukaddiye — guleke mu ttaka okumala ekiseera ekiwanvu lemera. (6) Tega eddagala nga neem oba sabbuuni — kyoka nga lwokya ttiro (hot pepper) ng'okola eddagala.",
     "NARO Sweet Potato Weevil Guide; CIP Weevil Management", "pest management"),

    ("Uganda", "Luganda", "sweet potato",
     "Lumonde lwange lulina amabala aga brown (brown spots) mu mubiri. Lwaki ndabika bwe'tyo?",
     "Amabala ga brown mu lumonde galaga endwadde ya Sweet Potato Virus Disease (SPVD) oba obutabi bwa potassium. (1) Tola emitogo gya NARO egirina obusobozi okwewala SPVD: 'NASPOT 1', 'NASPOT 5' oba 'NASPOT 10 O'. (2) Wonnonza ettaka — si simba lumonde mu ttaka lye walimu. (3) Tega omusulo (mulch) no kubyegeza omusana — kino kikendeeza obunyogovu. (4) Gezaako ettaka mu ofiisi y'ebyobulimi okunnyonnyola ebiriisa ebikosede. (5) Oba SPVD yongera, ggya lumonde olwo olwonna oluliko endwadde — lwokye.",
     "NARO SPVD Management; CIP Sweet Potato Virus Control", "disease diagnosis"),

    ("Uganda", "Luganda", "dairy",
     "Ente yange egira amata matono wadde nga ndiisa bulungi. Kiki ekiriko?",
     "Ente egira amata matono kiyinza okuba n'ensonga ez'enjawulo. (1) Amazzi — ente eyetaaga amazzi 40—60 litres buli lunaku. (2) Emmere — wadde ng'oliisa, ente eyetaaga omugattiko gw'ebiriisa (dairy meal) 2—3 kg buli lunaku. (3) Obusera obw'ebika (breed) — ente za Jersey ne Friesian zifulumya amata mangi okusinga endiirira. (4) Obulwadde — ente esobola okuba n'obulwadde bwa mastitis oba amabere g'ente. (5) Emyaka — ente ekaddiye egira amata matono. (6) Kola okuzzaako — ente egira amata mangi ng'ezzike (calving) nga tezinnaba. (7) Yita omusawo w'ebisolo (vet) okulaba oba ente yofu oba endwadde.",
     "NARO Dairy Production Guide; MAAIF Livestock Advisory", "general inquiry"),

    ("Uganda", "Luganda", "dairy",
     "Ente yange erina amabere agababaza era amata gali n'ebiremye (lumps). Kiki?",
     "Ono ye mastitis — endwadde y'amabere g'ente. (1) YITA omusawo w'ebisolo (vet) mangu. (2) Kola obulongoofu: kwoza amabere g'ente nga tonakama. (3) Kozesa eddagala lye 'teat dip' buli nga omaze okukama. (4) Tokamira zonna n'omukono gumu — kozesa omukono ogw'enjawulo ku buli nte. (5) Kama ente ezirina mastitis nga z'okusembayo — tangira n'ezirongoofu. (6) Kwoza ekifo w'okamira buli lunaku. (7) Oba ente erina omusujja (fever), egyetaaga eddagala lye antibiotics okuva eri omusawo w'ebisolo. (8) Kozesa enkola ey'okukama ente (milking hygiene) buli lunaku.",
     "NARO Mastitis Control; MAAIF Veterinary Advisory", "disease diagnosis"),

    ("Uganda", "Luganda", "maize",
     "Nsimbye omuwogo naye gugwa wansi nga guba n'ebikoola. Nkoze ki?",
     "Omuwogo ogugwa wansi kiyinza okuba nga ttaka lirina obutabi (nutrients) obutasaana. (1) Gezaako ettaka lyo mu ofiisi y'ebyobulimi. (2) Tega omusulo — kino kiyamba okukuumira amazzi. (3) Wonnonza ettaka: tosimba muwogo mu ttaka lyona. (4) Tola ebintu ebirongoofu okuva mu NARO: embuto z'omuwogo eza 'Longe 5', 'Longe 7' oba 'KH 500-33A'. (5) Oba endwadde yongera, kozesa eddagala eririna copper — singa omanyi akatambi. (6) Fuka ifumbire ey'enjawulo: teeka DAP 100 kg ku ekka, CAN 100 kg ku ekka buli kitundu.",
     "NARO Maize Production Guide; CIMMYT Maize Agronomy", "cultural practice"),

    ("Uganda", "Luganda", "tomato",
     "Ennyaanya zange ziriko ebifo ebya black (black spots) ku bikoola era nga zifa. Kiki?",
     "Ebyo bye bimenyetso by'endwadde ya early blight (Alternaria solani). (1) Ggya ebikoola ebyo ebiriko ebbala — byokye. (2) Tola embuto za NARO ezirina obusobozi okulwanyisa blight: 'Tengeru 97', 'Rio Grande' oba 'Money Maker'. (3) Wonnonza ettaka — tosimba nnyaanya mu ttaka lye walimu omwaka oguwedde. (4) Fuka omusulo — mukole nga waggulu kugira ngu amazzi galabire ewala ebikoola. (5) Nga endwadde yongera, kozesa eddagala eririna copper (kopo). (6) Tega akatambi k'okusimba — singa obadde osimba nnyaanya atali mu bbanga (greenhouse), ziba nga zikuumibwa obulungi.",
     "NARO Tomato Blight Guide; AVRDC Early Blight Control", "disease diagnosis"),

    ("Uganda", "Luganda", "cowpea",
     "Ebijanjaalo byange eby'enkobyo (cowpea) biriko obuwuka mu bikoola. Nkoze ki?",
     "Obuwuka mu bikoola by'enkobyo buba aphids oba thrips. (1) Kozesa sabbuuni n'amazzi (5g mu litre 1) obulwanyisa obuwuka. (2) Ggya ebikoola ebiriko obuwuka mu bikoola — byokya. (3) Tola embuto za NARO ezirina obusobozi okulwanyisa obuwuka. (4) Tega omusulo (mulch) okukendeeza obuwuka. (5) Wonnonza ettaka — tosimba nkobyo mu ttaka lye walimu. (6) Oba buwuka bungi, kozesa neem oil (5ml mu litre 1 y'amazzi) oba eddagala erikkirizibwa mu ofiisi y'ebyobulimi.",
     "NARO Cowpea Pest Management; IITA Cowpea IPM", "pest management"),

    ("Uganda", "Luganda", "rice",
     "Omucere gwange tegulira bulungi ate ameere galiko obwongo (holes). Kiki ekyo?",
     "Obwongo mu meere g'omucere bya rice weevils. (1) Tega omucere ogwo nga gunnnyogovu — wekebe omucere nga gukaddiye. (2) Nga omaze okukungula, yanike ku musana okumala obuwuka. (3) Teeka omucere mu 'airtight container' oba mu nsuwa ez'ekyuma. (4) Tega obuwuka bw'omucere nga tebunnayingira: teeka omucere mu freeez ku nnaku 7. (5) Tega ekifo w'ebikole — kibeerenga ekirongoofu, ekikaddiye, ate nga mulimu omukka omulungi. (6) Oba buwuka bungi, tolina okukozesa eddagala mu meere — kozesa ebikolwa eby'awaggulu gyokka.",
     "NARO Rice Storage Guide; AfricaRice Post-Harvest Advisory", "pest management"),

    ("Uganda", "Luganda", "sorghum",
     "Obulo bwange buliko obuweru (white) ku ntobo era nga bwakadde. Kiki?",
     "Obuweru ku ntobo y'obulo ye ndwadde ya sorghum smut. (1) Ggya obulo obwo obuliko obuweru — bwokye. (2) Tola embuto za NARO ezirina obusobozi okulwanyisa smut: 'Seredo', 'Macia' oba 'Gadam'. (3) Tega amazzi g'omuliro (52°C) ku min. 10 nga tonasimba. (4) Wonnonza ettaka — tosimba bulo mu ttaka lyona. (5) Simba obulo nga bweyali — obuweru bwongera mu budde obw'amazzi mangi. (6) Tega eddagala ly'embuto nga tonasimba — kozesa embeera z'embeera (seed dressing) okuva mu NARO.",
     "NARO Sorghum Smut Control; ICRISAT Smut Management", "disease diagnosis"),

    # ═══════════════ TWI — Ghana (20 entries) ═══════════════
    ("Ghana", "Twi", "cocoa",
     "Me kookoo dua no so nwumaa adurow ayɛ kɔkɔɔ na aduro no aba no anyini yie. Menya mmoa?",
     "Nwumaa adurow a ayɛ kɔkɔɔ no yɛ kookoo miridii (black pod disease — Phytophthora palmivora). (1) Twitwa nwumaa a anya yareɛ no nyinaa na hye no ogya — mfa nto fam. (2) Yiyi nwumaa no firi dua no so bere a aduro no anyini. (3) Twitwa nnua a ayɛ den (pruning) ma mframa ne owia tumi kɔ nnua no mu. (4) Dua nnua a ɛde nyinsa (shade trees) — kookoo pɛ nyinsa kakra. (5) Sɛ yareɛ no yɛ den, fa aduru a ɛyɛ afuw (copper-based fungicide) firi Cocoa Health and Extension Division (CHED). (6) Nsiesie nsateaa no — twetwe nwumaa a abu no firi ase. (7) Nnua mu hɔ ntew — twitwa mmoadoma a ayɛ den.",
     "CHED Black Pod Management; CRIG Cocoa Disease Guide", "disease diagnosis"),

    ("Ghana", "Twi", "cocoa",
     "Me kookoo nnua no ahoɔden nni mu na nwumaa no so nni mu. Nhaban no yɛ kɔkɔɔ. Asɛm bɛn?",
     "Kookoo ahoɔden a ɛnni mu ne nhaban kɔkɔɔ yɛ nsɛnkyerɛnne a nsanyareɛ (capsid/mirid bugs) akuta so. (1) Hwɛ nsateaa no yiye — sɛ wuhu nsanyareɛ a, twɛn kɔkɔɔbɔ (black ants) a wodi nsanyareɛ no. (2) Sɛ nsanyareɛ no dɔɔso a, fa aduru a wɔde sa nsanyareɛ (insecticide) firi CHED — nanso mfa nkɔso (neem) na kan. (3) Twitwa nhaban a ayɛ kɔkɔɔ no na hye wɔn. (4) Dua nnua a ɛde nyinsa — kookoo a ɛwɔ nyinsa mu nnya nsanyareɛ. (5) Fa nkɔso (neem) nsuo: nkɔso ngo 5ml wɔ nsuo 1 litre mu. (6) Hwɛ sɛ kookoo dua no nnya nnua a atwa ho ahyia (weeds) — yiyi wɔn. (7) Fa nsateaa ne nkɔso dwuma sɛ wopɛ — nanso sɛ nsanyareɛ no dɔɔso a, fa CHED aduru.",
     "CRIG Capsid Management; CHED Cocoa Pest Control", "pest management"),

    ("Ghana", "Twi", "cocoa",
     "Me kookoo nwumaa no so wɔ nsensene (swollen shoot) na nwumaa no nso sua. Yareɛ bɛn?",
     "Nsensene wɔ kookoo nwumaa ne nhaban sua yɛ Cocoa Swollen Shoot Virus Disease (CSSVD). (1) Sɛ wuhu dua bi a nsensene wɔ so no, twa na hye no ogya — CSSVD trɛ ntɛm. (2) Nsateaa a ɛde CSSVD ba yɛ mealybugs — tɔ melebọg a wɔwɔ nnua no so. (3) Dua nnua foforo a ɛwɔ CSSVD ho ban (tolerant varieties): CRIG te sɛ 'Tafo', 'Mercedes' ne 'Akate'. (4) Nkakrankakra yiyi mealybugs — fa nsuo ne samina (5g wɔ litre 1 mu) gu wɔn so. (5) Mmɛfa nnua a wɔyareɛ no mma firi wɔn so — CSSVD nam nnua so trɛ. (6) Fa ntadeɛ a ɛkyɛ (permit) firi CRIG ansaana woatɔ nnua foforo. (7) Kasa kyerɛ wo mfɛfo — CSSVD tumi sɛe afuw biara.",
     "CRIG CSSVD Management; CHED Swollen Shoot Control", "disease diagnosis"),

    ("Ghana", "Twi", "cocoa",
     "Me kookoo nwumaa no wɔ mmodoma a wɔwɔ mu (borer) na wɔsɛe nwumaa no. Dɛn na menyɛ?",
     "Mmodoma a wɔwɔ kookoo nwumaa mu no yɛ cocoa pod borer (Conopomorpha cramerella). (1) Twitwa nwumaa a mmodoma wɔ mu nyinaa na hye wɔn — mfa nto fam. (2) Fa nnua a atwa ho ahyia (mulch) to kookoo nnua ase — mmodoma pɛ awia. (3) Twitwa nnua no ma mframa ne owia tumi kɔ mu — borer nnya awia a ɛdɔɔso. (4) Dua nnua a ɛde nyinsa — borer tɔ nnua a ɛwɔ nyinsa mu. (5) Fa nkɔso (neem oil) 5ml wɔ nsuo 1 litre mu gu nwumaa so. (6) Hwɛ nwumaa no yiye bere biara — fa nwumaa a mmodoma wɔ mu yi firi afuw no mu.",
     "CRIG Cocoa Pod Borer Management; CHED Pest Advisory", "pest management"),

    ("Ghana", "Twi", "cocoa",
     "Me kookoo nhaban no so wɔ mmodoma (swollen) a wɔteɛ na nwumaa no nso sua. Onya a ɛso atɔ?",
     "Nhaban a wɔteɛ no yɛ nsɛnkyerɛnne a ɛkyerɛ sɛ nnua no nya nsuo kakra. (1) Hwɛ sɛ nsuo yɛ dɛ — kookoo pɛ nsuo nanso nsuo a ɛdɔɔso yɛ den. (2) Yiyi nnua a atwa ho ahyia (weeds) na ɛmfom nsuo no. (3) Fa nnua a asɛe (dead wood) firi afuw no mu. (4) Fa nnua a ɛde nyinsa to afuw no mu — ɛboaboa nsuo ano. (5) Aduro a ɛwɔ nsuo pii no, kɔ afuw a ɛwɔ bepɔw so kakra. (6) Hwɛ afuw no mframa ne owia a ɛkɔ mu — twitwa nnua a ayɛ den. (7) Sɛ nsɛnkyerɛnne no kɔ so a, kɔ CRIG hɔ na wɔbɛkyerɛ wo.",
     "CRIG Cocoa Water Management; CHED Cocoa Agronomy", "general inquiry"),

    ("Ghana", "Twi", "maize",
     "Me nkyene aba no nhaban so wɔ nsɔneɛ a ɛyɛ fitaa (white fungus) na ɛnyɛ yiye. Dɛn ne asɛm?",
     "Nsɔneɛ fitaa wɔ nkyene nhaban so yɛ powdery mildew. (1) Fa nsuo ne samina (5g wɔ litre 1 mu) gu nhaban no so. (2) Twitwa nhaban a ayare no na hye wɔn. (3) Fa nsuo pii mma afuw no mu — nsɔneɛ no pɛ nsuo. (4) Nkyene a wotumi dua a ɛwɔ ho ban: 'Obatanpa', 'Mamaba' ne 'Omankwa'. (5) Nsakraeɛ afuw: nkyene akyi no, dua mmoa bi te sɛ ntorodeɛ. (6) Sɛ nsɔneɛ no yɛ den a, fa fungicide a ɛyɛ copper firi MOFA hɔ.",
     "MOFA Maize Powdery Mildew Guide; CSRI Cereal Disease Control", "disease diagnosis"),

    ("Ghana", "Twi", "maize",
     "Me nkyene no abu fam na wɔn nsateaa (roots) ayɛ kɔkɔɔ. Nsuo pii nni hɔ. Asɛm ne dɛn?",
     "Nkyene a abu fam ne nsateaa kɔkɔɔ yɛ nsɛnkyerɛnne a nsateaayareɛ (root rot). (1) Twitwa nkyene a ayare no so na hye wɔn. (2) Fa nsuo kakra mma afuw no mu — nkyene pɛ nsuo nanso ɛnsɛ sɛ nsuo gvina. (3) Fa nkyene a wotumi dua wɔ bepɔw so (ridges) — nsuo ntumi ngyina. (4) Nsakraeɛ afuw: nkyene akyi no, dua mmoa bi. (5) Fa nnua a atwa ho ahyia (mulch) — ɛboa ma nsuo ngyina. (6) Nsaso (drainage) yɛ — twa asutene ma nsuo fa. (7) Kɔ MOFA hɔ ma wɔnkyerɛ wo nkyene aba pa.",
     "MOFA Maize Root Rot Guide; CSRI Root Disease Management", "disease diagnosis"),

    ("Ghana", "Twi", "cassava",
     "Me bankye no yare — nsateaa no ayɛ se nkuro (galls), nhaban no yɛ akokɔsradeɛ na aduro no sua. Mayɛ dɛn?",
     "Bankye a nsateaa no yɛ se nkuro ne nhaban akokɔsradeɛ yɛ Cassava Mosaic Disease (CMD). (1) Twa bankye a ayare no na hye wɔn — mfa nto fam. (2) Fa bankye nnua a ɛwɔ hɔ ban (CMD-resistant): 'Bankye Nkum', NASE 14, TME 419. (3) Mfa nnua firi afuw a ayare no. (4) Kae: fa nnua firi MOFA hɔ — wɔn na wɔde nnua a ɛwɔ hɔ ban. (5) Nsakraeɛ afuw: bankye akyi no, dua mmoa bi. (6) Fa nkɔso (neem) dwuma sɛ wuhu whiteflies — wɔna na wɔde CMD ba. (7) Kasa kyerɛ wo mfɛfo — bankye yare yi trɛ ntɛm.",
     "MOFA CMD Management; IITA Cassava Disease Control", "disease diagnosis"),

    ("Ghana", "Twi", "cassava",
     "Me bankye aduro no wɔ nsɔneɛ (brown spots) na ɛyɛ den sɛ mɛhye. Nkyene a ɛyɛ?",
     "Bankye nsɔneɛ a ɛyɛ den yɛ Cassava Brown Streak Disease (CBSD). (1) Twa bankye a ayare no na hye wɔn. (2) Nnua a ɛwɔ hɔ ban: Bankye Nkum, NASE 3, NASE 14. (3) Mfa nnua firi afuw a ayare no mma. (4) Fa nnua firi MOFA hɔ — wobenya nnua a wɔasiesie. (5) Nsakraeɛ afuw: bankye akyi no, dua mmoa bi. (6) Fa nkɔso dwuma — nsateaayare yi kɔ akyiri sɛ nsateaa no nnya uyareɛ. (7) Sɛ aduro no yɛ den dodo a, mfa nto fam — fa adwuma (gari/agbelima) firi bankye a ayare no mu.",
     "MOFA CBSD Management; IITA Brown Streak Control", "disease diagnosis"),

    ("Ghana", "Twi", "groundnut",
     "Me nkateɛ no nhaban so wɔ nsensene (spots) a ɛfiri (rust) na ɛyɛ akokɔsradeɛ. Mmoadoma?",
     "Nsensene a ɛfiri wɔ nkateɛ nhaban so yɛ groundnut rust (Puccinia arachidis). (1) Twitwa nhaban a ayare no na hye wɔn. (2) Nkateɛ a wotumi dua a ɛwɔ hɔ ban: 'Nkateɛ Nsono', 'Serenut 2'. (3) Nsakraeɛ afuw: nkateɛ akyi no, dua mmoa bi te sɛ bankye. (4) Fa nsateaa mu nsɛm — nkateɛ pɛ nsuo nanso ɛnsɛ sɛ nsuo gvina wɔ nhaban so. (5) Fa nsuo ne samina (5g wɔ litre 1 mu) gu nkateɛ so. (6) Sɛ nsɔneɛ no yɛ den a, fa fungicide a ɛyɛ copper firi MOFA hɔ.",
     "MOFA Groundnut Rust Control; ICRISAT Rust Management", "disease diagnosis"),

    ("Ghana", "Twi", "yam",
     "Me bayere no ntini a ɛwɔ fam no ayɛ kɔkɔɔ na abɔ. Yareɛ bɛn?",
     "Bayere ntini kɔkɔɔ a abɔ yɛ yam rot (Dry rot / Soft rot). (1) Twa bayere a ayare no na hye wɔn — mfa nto fam. (2) Mpɛ bayere wɔ asase koro so mfeɛ mmienu (2 years). (3) Hwɛ sɛ woyi nsuo firi afuw no mu — bayere pɛ nsuo nanso ɛnsɛ sɛ nsuo gvina. (4) Fa nnua a wɔakora (stored yam seed) na wotumi dua — mfa bayere a ayare firi afuw no mu. (5) Nkora bayere wɔ baabi a ɛhɔ yɛ hye ne mframa — ɔyareɛ no pɛ ɔhye ne nsuo. (6) Kɔ MOFA hɔ ma wɔnkyerɛ wo bayere pa a ɛwɔ hɔ ban.",
     "MOFA Yam Rot Management; IITA Yam Disease Guide", "disease diagnosis"),

    ("Ghana", "Twi", "yam",
     "Me bayere aduro no sua na nhaban no yɛ kɔkɔɔ. Asase no anya ahoɔden?",
     "Nhaban kɔkɔɔ ne aduro sua yɛ nsɛnkyerɛnne a asase no nni biribi (nutrient deficiency). (1) Fa asase no ma wɔnhwɛ wɔ MOFA hɔ — wɔbɛkyerɛ wo asɛm no. (2) Fa nantwie nsɛɛ (cow dung) ne nnua a asɛe (compost) to afuw no mu. (3) Fa NPK 15-15-15 aduru (100gm wɔ dua biara ase). (4) Nsakraeɛ afuw: bayere akyi no, dua bankye ne nkateɛ — ɛno de nti (nitrogen) ba. (5) Fa nnua a atwa ho ahyia (mulch) — ɛma asase no nya nsuo ne biribi. (6) Nsuo yɛ dɛ — bayere pɛ nsuo nanso ɛnsɛ sɛ nsuo gvina.",
     "MOFA Yam Soil Health Guide; IITA Yam Nutrition", "general inquiry"),

    ("Ghana", "Twi", "plantain",
     "Me boodoo no nhaban no ayɛ akokɔsradeɛ na ɛrenteɛ. Nsateaa no nso wɔ ahoɔden?",
     "Boodoo nhaban akokɔsradeɛ yɛ nsɛnkyerɛnne a nsuo nni hɔ kɛseɛ. (1) Fa nsuo pii ma — boodoo pɛ nsuo nanso ɛnsɛ sɛ nsuo gvina. (2) Fa nnua a atwa ho ahyia (mulch) to ase — ɛma nsuo ngyina. (3) Nsakraeɛ hɔ aduro: NPK (100gm wɔ dua biara ase). (4) Fa abusua boodoo (suckers) a ɛwɔ ahoɔden — Mfa boodoo firi afuw a ayare no mu. (5) Twitwa nhaban a ayɛ kɔkɔɔ na ɛmfom nsuo no. (6) Fa nsuo ne samina (5g wɔ litre 1 mu) gu nhaban so sɛ wuhu nsateaa. (7) Hwɛ sɛ boodoo nnya nsateaa te sɛ weevils — fa neem dwuma.",
     "MOFA Plantain Water Management; IITA Plantain Advisory", "cultural practice"),

    ("Ghana", "Twi", "plantain",
     "Me boodoo nwumaa no so wɔ nsateaa (black) na aduro no nso nnyini. Mmoadoma bɛn?",
     "Nsateaa tuntum wɔ boodoo nwumaa so yɛ plantain weevil (Cosmopolites sordidus). (1) Twitwa boodoo a nsateaa wɔ so na hye wɔn — weevil no bɛwu. (2) Fa boodoo firi baabi a ayare no mma. (3) Hwɛ sɛ woyi boodoo a ayare firi afuw no mu. (4) Fa nkɔso (neem) dwuma: nkɔso ngo 5ml wɔ nsuo 1 litre mu gu nsateaa no so. (5) Nsakraeɛ afuw: boodoo akyi no, dua nkyene ne mmoa — weevil no ntumi ntena asase koro so. (6) Fa nnua a atwa ho ahyia (mulch) — weevil pɛ nsuo nanso mmoa no boa ma wɔkɔ. (7) Kɔ MOFA hɔ ma wɔnkyerɛ wo boodoo pa.",
     "MOFA Plantain Weevil Management; IITA Weevil Control", "pest management"),

    ("Ghana", "Twi", "okra",
     "Me nkruma nhaban no so wɔ nsateaa fɛtɛɛ (whitefly) na aduro no nso sua. Aduru bɛn?",
     "Nsateaa fɛtɛɛ wɔ nkruma so yɛ whiteflies. (1) Fa nsuo ne samina (5g wɔ litre 1 mu) gu wɔn so — ɛno kum whiteflies. (2) Hwɛ sɛ woyi nhaban a nsateaa dɔɔso wɔ so. (3) Fa nkɔso ngo (5ml wɔ litre 1 mu) dwuma — nkɔso kum whiteflies a ɛnyɛ den. (4) Nsakraeɛ afuw: nkruma akyi no, dua nkateɛ ne mmoa — whiteflies ntumi ntena. (5) Twitwa nhaban a nsateaa wɔ so na fa firi afuw no mu. (6) Fa nnua a ɛwɔ hɔ ban — kɔ MOFA hɔ ma wɔkyerɛ wo nkruma a ɛwɔ ahoɔden.",
     "MOFA Okra Whitefly Management; AVRDC Whitefly Control", "pest management"),

    ("Ghana", "Twi", "pepper",
     "Me mako no nhaban no sɛe na ɛyɛ kɔkɔɔ. Mako no nso tɔ fam (drop). Dɛn?",
     "Mako a ɛtɔ fam ne nhaban kɔkɔɔ yɛ nsɛnkyerɛnne a blossom-end rot ne fungal disease. (1) Fa nsuo pii ma na ɛnsɛ sɛ nsuo gvina — mako pɛ nsuo a ɛkɔ so. (2) Fa nsuo ne samina (5g wɔ litre 1 mu) gu nhaban no so. (3) Fa NPK ne calcium (eggshells) to asase no mu — blossom-end rot firi calcium a nni hɔ. (4) Twitwa mako a atɔ fam no na fa firi afuw no mu. (5) Fa nnua a atwa ho ahyia (mulch) — ɛma nsuo ngyina. (6) Nsakraeɛ afuw: mako akyi no, dua nkruma ne nkateɛ. (7) Sɛ ɔyareɛ no kɔ so a, fa fungicide a ɛyɛ copper firi MOFA hɔ.",
     "MOFA Pepper Disease Guide; AVRDC Pepper Management", "disease diagnosis"),

    ("Ghana", "Twi", "tomato",
     "Me ntoosi nwumaa no so wɔ nsateaa (small worms) na ɛsɛe nwumaa no. Nkumaa?",
     "Nsateaa a ɛwɔ ntoosi nwumaa so yɛ tomato fruitworm (Helicoverpa armigera). (1) Twitwa ntoosi a nsateaa wɔ mu na hye wɔn. (2) Fa nkɔso ngo (5ml wɔ nsuo 1 litre mu) gu ntoosi no so. (3) Fa nsuo ne samina gu nhaban no so — nsateaa ntumi ntena nhaban a samina wɔ so. (4) Nsakraeɛ afuw: ntoosi akyi no, dua nkruma ne nkateɛ. (5) Fa nnua a ɛwɔ hɔ ban te sɛ 'Tengeru 97', 'Rio Grande'. (6) Hwɛ ntoosi no yiye — sɛ wuhu nsateaa, yi wɔn ansa. (7) Kɔ MOFA hɔ ma wɔnkyerɛ wo ntoosi pa.",
     "MOFA Tomato Fruitworm Guide; AVRDC Fruitworm Control", "pest management"),

    ("Ghana", "Twi", "cowpea",
     "Me nkruma (cowpea) nhaban so wɔ nsateaa a ɛyɛ tuntum ne akokɔsradeɛ. Mmoadoma?",
     "Nsateaa a ɛyɛ tuntum ne akokɔsradeɛ wɔ nkruma so yɛ aphids ne thrips. (1) Fa nsuo ne samina (5g wɔ litre 1 mu) gu wɔn so. (2) Fa nkɔso ngo (5ml wɔ litre 1 mu) dwuma. (3) Twitwa nhaban a nsateaa dɔɔso wɔ so na hye wɔn. (4) Nsakraeɛ afuw: nkruma akyi no, dua nkyene ne ntoosi. (5) Fa nnua a ɛwɔ hɔ ban: kɔ MOFA hɔ ma wɔnkyerɛ wo nkruma a ɛwɔ ahoɔden. (6) Sɛ nsateaa no dɔɔso a, fa insecticidal soap firi MOFA hɔ.",
     "MOFA Cowpea Pest Management; IITA Cowpea IPM", "pest management"),

    ("Ghana", "Twi", "groundnut",
     "Me nkateɛ aduro no wɔ nkateɛ a ɛyɛ huam (aflatoxin) na ɛnyɛ dɛ sɛ mɛdi. Yɛn na yɛanya?",
     "Nkateɛ a ɛyɛ huam no yɛ aflatoxin — no mu yareɛ (fungus) a ɛba sɛ nkateɛ no nnyini yiye. (1) Yan (sun-dry) nkateɛ no yiye ansa na wode akora. (2) Nkora wɔ baabi a ɛhɔ yɛ hye ne mframa — aflatoxin pɛ nsuo ne ɔhye. (3) Mfa nkateɛ a wɔayi firi afuw no ntena ase kyɛ. (4) Nyi nkateɛ no firi asase no mu bere a aduro no anyini — mfa nkyɛ. (5) Fa nkateɛ no gu nkora mu a ɛyɛ mframa (baskets) na ɛnyɛ plastik. (6) Kɔ MOFA hɔ sɛ wopɛ nkateɛ a ɛyɛ papa (seed treatment).",
     "MOFA Aflatoxin Control; ICRISAT Aflatoxin Management", "general inquiry"),

    # ═══════════════ KANURI — Nigeria (7 entries) ═══════════════
    ("Nigeria", "Kanuri", "groundnut",
     "Njiwa dala ganyam ndu ga jili sorom alama yetana kambu be. Nya karfu?",
     "Alama mabe ganyam ji kambu sorom (leaf spot). Kambu yaye awo laaro karo liiro: (1) Kare ganyam mabe kambu yaye am nyi baade. (2) Ku ganyam late nalama tiyara A.A. (3) Kare ganyande raadu (rotate) — ku njiwa baade tando laaro. (4) Kare ganyam ndi raduguma na funti juwu (1.5-2 feet) — ndu kambu yaye tilo. (5) Dala Nyi (neem oil 5ml/funtun 1) re kambu yaye jiiro. (6) Ku shetto kalibe A.A. ma dala kambu yaye fungicide (copper) jiiro.",
     "Nigerian Agricultural Extension Groundnut Pest Guide; ICRISAT Leaf Spot Control", "disease diagnosis"),

    ("Nigeria", "Kanuri", "sorghum",
     "Ngawu dala dabe kamba kasuwa karo kambu be. Nzaku?",
     "Kambu mabe ngawu dabe kamba kasuwa yaye dabe yaye ndi (sorghum smut). (1) Kare ngawu mabe kambu yaye am shettobe baade. (2) Ku ngawu raadu ma nyi ngawu tando laaro. (3) Kare ngawu late ma fungicide jiiro: copper-based oba seed dressing firi ADP hɔ. (4) Kare ngawu 'Seredo', 'Macia' oba 'Gadam'. (5) Kare ngawu ndi raduguma ma nyi funti juwu. (6) Nsuwu karo — ngawu gonya nsuwu pilla (early) ma ku gaba.",
     "ADP Sorghum Smut Control; ICRISAT Smut Management", "disease diagnosis"),

    ("Nigeria", "Kanuri", "millet",
     "Margo dala tsa karo yeri yaye firo firo konyi. Nya?",
     "Tsa karo yeri yaye firo firo konyi yaye downy mildew. (1) Kare margo mabe yaye am nyi baade — mfa nto fam. (2) Ku margo raadu — ku mfa margo tando laaro. (3) Kare margo late ma wulu (seed dressing) firi ADP hɔ. (4) Kare margo 'Ex-Borno', 'LCIC 9702' oba 'SOSAT-C88'. (5) Nsuwu karo — margo gonya nsuwu pilla ma wulu laaro. (6) Sɛ njiwa futo re, kare fungicide (mancozeb) karo.",
     "ADP Millet Downy Mildew Control; ICRISAT Millet Disease Guide", "disease diagnosis"),

    ("Nigeria", "Kanuri", "cowpea",
     "Nganye dala nzaku yaye kambu yaye am kare so. Nya tso?",
     "Nganye nzaku yaye kambu yaye am kare so yaye cowpea aphids. (1) Shetto kalibe A.A. ma dala maye baade. (2) Ku dala neem oil (5ml wɔ nsuwun 1 litre) re kambu yaye jiiro. (3) Kare nganye raadu — mfa nganye tando laaro. (4) Kare nganye 'IT 90K-59', 'IT 97K-499-35' oba 'Kanannado'. (5) Nyi kambu mabe aphid yaye am kare so. (6) Ku dala sabuni (5g wɔ nsuwun 1 litre) re jiiro.",
     "ADP Cowpea Aphid Control; IITA Cowpea Pest Management", "pest management"),

    ("Nigeria", "Kanuri", "beans",
     "Dala nalama mabe tsa yaye kambu yaye. Nya ya?",
     "Tsa yaye kambu yaye mabe dala (beans) yaye anthracnose. (1) Kare dala mabe kambu yaye am nyi baade. (2) Ku dala raadu ma nyi tando laaro. (3) Kare dala late ma fungicide (copper-based) firi ADP hɔ. (4) Nsuwu futo re — ɛnsɛ sɛ nsuwu nyi kambu yaye jiiro. (5) Kare dala mabe gonya pilla — ndu tsa yaye tilo. (6) Ku wo late ma 'Compost' oba 'NPK' to asase re.",
     "ADP Bean Anthracnose Guide; CIAT Bean Disease Control", "disease diagnosis"),

    ("Nigeria", "Kanuri", "groundnut",
     "Ganyam dala dabe yaye kambu yaye am shetto kaaro. Nya karfu?",
     "Dabe yaye kambu yaye mabe ganyam ji yaye rosette virus. (1) Kare ganyam mabe dabe yaye am nyi baade. (2) Ku ganyam raadu — mfa tando laaro. (3) Kare ganyam 'Serenut 4T', 'Nyirahindurwa' oba 'Mfitego'. (4) Nyi aphids yaye baade — wɔna ndu virus yaye re karo. (5) Ku dala neem oil karo. (6) Nyi kare ganyam ndi raduguma ma nyi funti juwu.",
     "ADP Groundnut Rosette Control; ICRISAT Rosette Management", "disease diagnosis"),

    ("Nigeria", "Kanuri", "sorghum",
     "Ngawu dala nzaku karo yeri yaye firo konyi. Nya?",
     "Yeri yaye firo konyi yaye loose smut. (1) Kare ngawu mabe yaye am nyi baade. (2) Ku ngawu late ma wulu (seed dressing) karo. (3) Kare ngawu 'Seredo', 'Macia' oba 'Gadam'. (4) Nsuwu karo — ngawu pilla gonya. (5) Ku ngawu raadu ma nyi tando laaro. (6) Nyi kare wulu wɔ nsuwun (52°C) min. 10 — ndu yaye kum.",
     "ADP Sorghum Loose Smut Guide; ICRISAT Smut Control", "disease diagnosis"),

    # ═══════════════ TIV — Nigeria (7 entries) ═══════════════
    ("Nigeria", "Tiv", "yam",
     "Iyo m sule a kwagh u tsung u venda a kpue. U nyor?",
     "Kpue iyo m sule a kwagh u tsungu venda yô, a kwagh u yam dry rot. (1) Nyor iyo a ie gbenda a ve sha iyô. (2) Hema iyo sha ahar, kpa gba a shin iyôngo. (3) Nyor iyo a sô a kiriki a soo kpa gba la kpa— iyo hembe mnger u ngu ashighe kpishi. (4) Nyor anyom a ahar sha u ngu a ngise. (5) Hange iyo na gbaa li a moughul sha anyam or u ahar. (6) Kôngo or u ahar (ADP) ne iwe iyo i sôn a lu cii.",
     "ADP Yam Rot Advisory; IITA Yam Disease Guide", "disease diagnosis"),

    ("Nigeria", "Tiv", "rice",
     "Ikyer m a de or u a gba sha inja. Or u bom u ior?",
     "Or u bom u iyer a de or u a gba sha inja yô, a kwagh u rice blast. (1) Nyor ikyer a de kwagh u bom la kpue a ve sha iyô. (2) Hema ikyer a ahar a ve tindi— i twer sha amban moughul. (3) Nyor ikyer a aôndo: 'FARO 44', 'FARO 52' oba 'SIPI 692033'. (4) Hema ikyer u game— icigh u yô a door u game. (5) Hema ikyer a wase a gbenda sha iyôngo. (6) Hema a or u ahar (ADP) ne iwe mbu u hange kwagh u bom la.",
     "ADP Rice Blast Control; AfricaRice Blast Management", "disease diagnosis"),

    ("Nigeria", "Tiv", "rice",
     "Ikyer m a de or u bom u tseen kwagh u imo. Ngu kwagh u soo?",
     "Kwagh u tseen zwa ikyer u ngu a wase la moughul yô, a kwagh u u tsee moughul (iron toxicity). (1) Hema ikyer m a wangen ne a wase. (2) Nyor iyôngo ikyer a kpishi— tsee wase la kpishi la zwa. (3) Nyor ikyer 'FARO 61' oba 'FARO 67' a wase tseen shighe. (4) Hema kwagh u or u ahar ne a zwa moughul la a lu. (5) Nyor ikyer u yange u game ga. (6) Kôngo or u ahar (ADP) ne iwe i sôn a lu ra.",
     "ADP Rice Iron Toxicity Guide; AfricaRice Iron Management", "disease diagnosis"),

    ("Nigeria", "Tiv", "cassava",
     "Ikyu m sule a kwagh u taver u fegh yô, kpa ikyu la a viir. Annyom u soo?",
     "Ikyu u taver fegh la a viir yô, a kwagh u Cassava Brown Streak Disease. (1) Nyor ikyu u taver fegh la cii a ve sha iyô. (2) Nyor ikyu i sôn a viir ga: TME 419, NASE 14 oba NAROCASS 1. (3) Nyor ikyu u game ga— ikyua kpar sha ahar nyom ma to. (4) Ghô ikyu u mba or u vihin (whitefly) sha ikyu— nda kpar kwagh u a viir la. (5) Nyor ikyu raadu— i gbenda yough la a soo kpa ha. (6) Kôngo or u ahar ne iwe ikyu i sôn a viir ga.",
     "ADP Cassava CBSD Guide; IITA Brown Streak Management", "disease diagnosis"),

    ("Nigeria", "Tiv", "groundnut",
     "Ikyura m sule a kwagh u kpue u or u hemen. Kpa ikyura la a er sha ahar?",
     "Kpue ku ikyura yô a kwagh u aflatoxin— ikyura u kpue u or u hemen u soo. (1) Nyor ikyura a ahar sha iyôngo— na yan wa. (2) Hema ikyura sha ahar a kpa soo— aflatoxin kpa wase moughul ya. (3) Nyor ikyura sha ayu a or u ahar (sacks) a wase u ngu. (4) Nyor ikyura a game— ne wase moughul la a viir. (5) Ghô ikyura u game ga a ikyôngo— ikyura u game la ngu a viir. (6) Nyor ikyura raadu: ikyura a nyi ibunde a wase u soo la.",
     "ADP Groundnut Aflatoxin Control; ICRISAT Aflatoxin Management", "general inquiry"),

    ("Nigeria", "Tiv", "beans",
     "Ikyura m (beans) sule a kwagh u kumbu a ve sha. Annyom?",
     "Kwagh u kumbu a ve sha m ikyura yô, a kwagh u bean beetle. (1) Nyor ikyura u kumbu la a ve sha iyô. (2) Nyor ikyura la sha ahar a wase— i twer sha a kati. (3) Nyor ikyura u game ga sha iyôngo—ne yo tumen ikyura la. (4) Hema ikyura la sha ahar shin sun (2 sun) ne ikyua a kpa. (5) Nyor ikyura a 'airtight container' la ne ater u zi. (6) Kôngo or u ahar (ADP) ne iwe i sôn a lu ra.",
     "ADP Bean Beetle Control; CIAT Bean Storage Guide", "pest management"),

    ("Nigeria", "Tiv", "yam",
     "Iyo m sule a kwagh u taver yô. Kpa iyo m zungwa ben. Annyom?",
     "Iyo u ngu zungwa u soo yô, a kwagh u virus oba a kwagh u or u ahar (nutrients). (1) Nyor iyo a or u ahar (ADP) ne a lu a zungwa ga. (2) Hema iyo raadu— i gbenda yough la a soo kpa. (3) Nyor iyo i sôn a taver yô ga: 'TDr 89/02665', 'TDr 95/18544'. (4) Hema iyo a game—i yange icigh u la ye shighe. (5) Nyor iyo sha ahar a wase (compost) u soo. (6) Hema or u ahar ne a lu a ishima ne iwe mba u taver la.",
     "ADP Yam Virus Guide; IITA Yam Disease Management", "disease diagnosis"),

    # ═══════════════ IBIBIO — Nigeria (7 entries) ═══════════════
    ("Nigeria", "Ibibio", "cassava",
     "Idiọk mi ekedi usụn udia, ediwak iyak ke ubọk. Nso idiọk emi?",
     "Idiọk emi edi Cassava Mosaic Disease (CMD). (1) Tutụ idiọk emi ekemede enyene utom — yak afiak. (2) Da idiọk emi osụkụkọt inọ CMD: TME 419, NASE 14 oba MM96/5280. (3) Mmọfiọk idiọk ke ufọk nwed (ADP) — mmọ ama ekemede ndinọ fi idiọk emi anam idap. (4) Kọpọ idiọk emi — mmenye idiọk ke isọn̄ emi mbon ekụkọ. (5) Da ikọ (neem oil 5ml ke liter 1) — whiteflies ndien emi ekemede ndinam CMD. (6) Sụkọ mme ufọknwed (extension agents) — mmọ ekemede ndinọ fi ibet.",
     "ADP Cassava Mosaic Control; IITA CMD Guide", "disease diagnosis"),

    ("Nigeria", "Ibibio", "cassava",
     "Idiọk mi ọkọdọk ebot (brown spots) ke ubọk ye okụk. Nso?",
     "Ebot ke ubọk ye okụk edi Cassava Brown Streak Disease (CBSD). (1) Tutụ idiọk emi ekemede enyene utom — yak afiak. (2) Da idiọk emi osụkọkọt: NASE 14, NAROCASS 1. (3) Mben̄e idiọk emi — kọpọ ke mme idiọk emi ekpedi. (4) Da ikọ (neem) inọ whiteflies — mmọ edi mme ndien CBSD. (5) Kọpọ idiọk ke isọn̄ emi ekededi — kọpọ ke isọn̄ emi mbon ekụkọ. (6) Sụkọ ofiisi ikpọ (ADP) — mmọ ekemede ndinọ fi udia.",
     "ADP CBSD Management; IITA Brown Streak Control", "disease diagnosis"),

    ("Nigeria", "Ibibio", "oil palm",
     "Eyop mi oyom ndinam ekpri mmọ (fruits), ediwak nsinsi ke udia. Nso?",
     "Nsinsi ke udia eyop edi palm weevil. (1) Tutụ eyop emi enyene nsinsi — yak afiak. (2) Mbre eyop mi — da udia emi mbon ekụkọ. (3) Da udia emi osụkọkụt (tolerant varieties) ke ofiisi ikpọ (ADP). (4) Da ikọ (neem oil) ke udia eyop — nsinsi edi ndien. (5) Kọpọ udia eyop — mmenye nsinsi ke esịt. (6) Sụkọ ADP inọ ibet — mmọ ekemede ndinọ fi udia emi osụkọkọt.",
     "ADP Oil Palm Weevil Guide; NIFOR Oil Palm Pest Control", "pest management"),

    ("Nigeria", "Ibibio", "oil palm",
     "Eyop mi ofụk (fruit) ikọdọk bot. Nso ntak?",
     "Nso ke (fruit) ebot ke eyop eyedi ganoderma butt rot oba fruit rot. (1) Tutụ eyop emi enyene utom — yak. (2) Mbre udia eyop mi — da udia emi mbon ekụkọ. (3) Da udia emi osụkọkụt ganoderma — ofiisi NIFOR ekemede ndinọ fi. (4) Nsio eyop emi mbon ekụkọ ke udia emi ekededi. (5) Mben̄e udia eyop — kọpọ ke isọn̄ emi ekedebiat. (6) Sụkọ NIFOR oba ADP inọ ibet ikpọ.",
     "ADP Oil Palm Disease Guide; NIFOR Ganoderma Control", "disease diagnosis"),

    ("Nigeria", "Ibibio", "plantain",
     "Ayaba mi ikọdọk bot (spots) ke udi ye mme n̄wed. Nso okụkọde?",
     "Bot ke udi ye mme n̄wed ayaba edi Black Sigatoka. (1) Tutụ n̄wed emi enyene bot — yak afiak. (2) Da ayaba emi osụkọkụt ke ofiisi (ADP). (3) Da ikọ (neem oil 5ml/liter) — bot edi ndien. (4) Kọpọ ayaba emi — mmenye bot ke udia. (5) Mbre udia — da udia emi ekededi mbon ekụkọ. (6) Sụkọ ofiisi ikpọ inọ ibet.",
     "ADP Plantain Sigatoka Guide; IITA Black Sigatoka Control", "disease diagnosis"),

    ("Nigeria", "Ibibio", "pepper",
     "Nsama mi ikọdọk nsinsi ke udi ye mme n̄wed. Ediwak ndien. Nso ntak?",
     "Nsinsi ke udi nsama edi aphids oba thrips. (1) Da nsama emi mbon ekụkọ — kụt ke esịt obụkidem. (2) Da ikọ (neem) ke udi ye mme n̄wed. (3) Kọpọ nsama emi — mmenye aphids. (4) Da nsama emi osụkọkụt — ofiisi ikpọ ekemede ndinọ fi. (5) Mbre udia — da udia emi ekededi mbon ekụkọ. (6) Sụkọ ADP inọ ibet ikpọ ke nsinsi.",
     "ADP Pepper Pest Guide; AVRDC Pepper IPM", "pest management"),

    ("Nigeria", "Ibibio", "beans",
     "Idiọk mi ekedi usụn udia. Ama ntak idiọk emi?",
     "Idiọk emi ekekemede ndinam ntak (yield loss) edi anthracnose. (1) Da idiọk emi osụkọkụt ke ofiisi ikpọ. (2) Kọpọ ke isọn̄ — mmenye idiọk ke isọn̄ emi ekededi. (3) Da fungicide a copper — sụkọ ADP ibet. (4) Kọpọ idiọk emi — tutụ emi enyene bot. (5) Mbre udia — da udia emi ekededi mbon ekụkọ. (6) Da n̄wed ke ofiisi ikpọ — mmọ ekemede ndinọ fi udia emi osụkọkụt.",
     "ADP Bean Anthracnose Guide; CIAT Bean Disease Control", "disease diagnosis"),

    # ═══════════════ BEANS — Across regions (15 entries) ═══════════════
    ("Kenya", "Kikuyu", "beans",
     "Mbaa ciiria njaria iri na twana twa kahiga ikinyi-ini. Ni ugwati atia?",
     "Twana twa kahiga ikinyi-ini ni weevils. (1) Ananga mbaa ciiria—iga na mwaki. (2) Ananga mbaa ciiria na riua—ciume wega. (3) Ikara mbaa ciiria na container-ini ya kutaga heho. (4) Ikara mbaa ciiria refrigerator-ini (7 days)—ni kuura twana twa kahiga. (5) Ti kuhanda mbaa ciiria handu hamwe mwaka gukiraniria. (6) Uria ofisa wa ugwati (extension officer)—ana kuhona.",
     "KALRO Bean Storage Guide; CIAT Weevil Control", "pest management"),

    ("Kenya", "Kikuyu", "beans",
     "Mbaa ciiria iri na marua mathwaro na ithondekiaga wega. Ni ugwati?",
     "Marua mathwaro ni anthracnose. (1) Ananga mbaa ciiria iria iri na marua—iga. (2) Handa mbaa ciiria iria iciaraga na ugwati—KALRO nayo. (3) Handa mbaa ciiria handu hangi mwaka uyu—tigana na handu ha mwaka muthiru. (4) Tega fungicide ya copper (KALRO nayo). (5) Tiga guthia (overhead watering)—thiaga na thitha (drip). (6) Ananga mbaa ciiria iria iri na ugwati na mwaki.",
     "KALRO Bean Anthracnose Guide; CIAT Anthracnose Management", "disease diagnosis"),

    ("Tanzania", "Swahili", "beans",
     "Maharagwe yangu yana madoa meusi na majani yananyauka. Nifanyeje?",
     "Madoa meusi kwenye maharagwe ni ugonjwa wa anthracnose. (1) Ondoa mimea yote iliyoathirika na uichome. (2) Panda mbegu za maharagwe zinazostahimili ugonjwa — kutoka KALRO au ofisi ya kilimo. (3) Zungusha mazao — usipande maharagwe kwenye shamba moja msimu baada ya msimu. (4) Tumia dawa ya shaba (copper-based fungicide) baada ya kupata ushauri kutoka ofisa kilimo. (5) Panda maharagwe kwenye matuta (ridges) ili kuzuia maji kusimama. (6) Epuka kumwagilia kutoka juu — tumia umwagiliaji kwa njia ya matone (drip irrigation).",
     "KALRO Bean Anthracnose Guide; CIAT Disease Management", "disease diagnosis"),

    ("Tanzania", "Swahili", "beans",
     "Maharagwe yangu yana wadudu wadogo kwenye maganda. Yaweza kuwa nini?",
     "Wadudu wadogo kwenye maganda ya maharagwe ni bean pod borers au thrips. (1) Ondoa maganda yaliyoathirika na uyachome. (2) Panda aina za maharagwe zinazostahimili wadudu — kutoka ofisi ya kilimo. (3) Tumia mchafu wa neem (neem oil 5ml kwa lita 1 ya maji). (4) Zungusha mazao — usipande maharagwe mara kwa mara kwenye shamba moja. (5) Weka matandazo (mulch) kuzuia wadudu. (6) Wasiliana na ofisa kilimo kwa ushauri zaidi.",
     "KALRO Bean Pest Guide; IITA Bean IPM", "pest management"),

    ("Ethiopia", "Amharic", "beans",
     "ባቄላዬ ላይ ቡናማ ነጠብጣቦች አሉ ቅጠሎቹም ደርቀዋል። ምን ችግር ነው?",
     "ቡናማ ነጠብጣቦች የባቄላ አንትራክኖዝ (anthracnose) በሽታ ሊሆን ይችላል። (1) የታመሙትን ተክሎች አውጥተህ አቃጥላቸው። (2) በሽታን የሚቋቋም የባቄላ ዘር ምረጥ — ወደ ግብርና ቢሮ ሂድ። (3) ሰብል አዙር — ባቄላ በተመሳሳይ ማሳ ዘርተህ አትተው። (4) የነም (neem) ዘይት ተጠቀም (5ml በ1 ሊትር ውሃ)። (5) አትክልቱ ላይ ውሃ አታፍሰስ — ውሃ የሚረጭ ቱቦ ተጠቀም። (6) ለተጨማሪ እርዳታ የግብርና ባለሙያውን አነጋግር።",
     "EIAR Bean Disease Guide; CIAT Anthracnose Management", "disease diagnosis"),

    ("Ethiopia", "Amharic", "beans",
     "ባቄላዬ በደንብ አያድግም ቅጠሎቹም ጠማማ ናቸው። ምንድነው?",
     "ቅጠሎቹ ጠማማ መሆን የቫይረስ በሽታ (Bean Common Mosaic Virus) ምልክት ነው። (1) የታመሙትን ተክሎች አውጥተህ አቃጥላቸው። (2) ቫይረሱን የሚቋቋም ዘር ተጠቀም — ከግብርና ቢሮ አግኝ። (3) አፊድ (aphids) ቫይረሱን ያስተላልፋል — ነም ዘይት ተጠቀም። (4) ሰብል አዙር። (5) የታመሙ ተክሎችን አውጥተህ አቃጥላቸው። (6) ለተጨማሪ እርዳታ ወደ ግብርና ቢሮ ሂድ።",
     "EIAR Bean Virus Guide; CIAT BCMV Control", "disease diagnosis"),

    ("India", "Punjabi", "beans",
     "ਮੇਰੀ ਫਲੀਆਂ (beans) ਦੇ ਪੱਤਿਆਂ 'ਤੇ ਭੂਰੇ ਧੱਬੇ ਹਨ ਅਤੇ ਫਲੀਆਂ ਸੁੱਕ ਰਹੀਆਂ ਹਨ। ਕੀ ਕਰਾਂ?",
     "ਭੂਰੇ ਧੱਬੇ ਐਂਥ੍ਰੈਕਨੋਜ਼ (anthracnose) ਰੋਗ ਦੇ ਲੱਛਣ ਹਨ। (1) ਪ੍ਰਭਾਵਿਤ ਪੌਦਿਆਂ ਨੂੰ ਪੁੱਟ ਕੇ ਸਾੜ ਦਿਓ। (2) ਰੋਗ-ਰੋਧਕ ਬੀਜ ਵਰਤੋ — ਖੇਤੀਬਾੜੀ ਦਫ਼ਤਰ ਤੋਂ ਲਵੋ। (3) ਫਸਲੀ ਚੱਕਰ ਅਪਣਾਓ — ਹਰ ਸਾਲ ਇੱਕੋ ਖੇਤ ਵਿੱਚ ਫਲੀਆਂ ਨਾ ਬੀਜੋ। (4) ਨੀਮ ਦਾ ਤੇਲ (neem oil 5ml/ਲੀਟਰ) ਵਰਤੋ। (5) ਸਿੰਜਾਈ ਦੌਰਾਨ ਪੱਤਿਆਂ 'ਤੇ ਪਾਣੀ ਨਾ ਪੈਣ ਦਿਓ। (6) ਕਾਪਰ-ਆਧਾਰਿਤ ਫ਼ੰਜੀਸਾਈਡ ਵਰਤਣ ਲਈ ਖੇਤੀਬਾੜੀ ਅਧਿਕਾਰੀ ਨਾਲ ਸਲਾਹ ਕਰੋ।",
     "Punjab Agriculture Bean Disease Guide; CIAT Anthracnose Control", "disease diagnosis"),

    ("India", "Punjabi", "beans",
     "ਫਲੀਆਂ (beans) ਵਿੱਚ ਕੀੜੇ (weevils) ਪੈ ਗਏ ਹਨ। ਸਟੋਰ ਕਰਨ ਦਾ ਸਹੀ ਤਰੀਕਾ?",
     "ਫਲੀਆਂ ਵਿੱਚ ਕੀੜੇ (weevils) ਭੰਡਾਰਨ ਦੀ ਸਮੱਸਿਆ ਹੈ। (1) ਫਲੀ ਨੂੰ ਧੁੱਪ ਵਿੱਚ ਚੰਗੀ ਤਰ੍ਹਾਂ ਸੁਕਾਓ। (2) ਕੀੜੇ-ਮਾਰ ਦਵਾਈ (neem oil) ਨਾਲ ਫਲੀ ਦਾ ਇਲਾਜ ਕਰੋ। (3) ਫਲੀ ਨੂੰ ਹਵਾ-ਬੰਦ ਡੱਬੇ (airtight container) ਵਿੱਚ ਰੱਖੋ। (4) ਫਲੀ ਨੂੰ ਫ੍ਰੀਜ਼ਰ ਵਿੱਚ 7 ਦਿਨ ਰੱਖੋ — ਕੀੜੇ ਮਰ ਜਾਣਗੇ। (5) ਸਟੋਰ ਵਿੱਚ ਸਫ਼ਾਈ ਰੱਖੋ। (6) ਪੁਰਾਣੇ ਕੀੜੇ ਵਾਲੇ ਡੱਬੇ ਨਾ ਵਰਤੋ — ਨਵੇਂ ਸਾਫ਼ ਡੱਬੇ ਵਰਤੋ।",
     "Punjab Agriculture Bean Storage Guide; CIAT Weevil Control", "pest management"),

    ("India", "Tamil", "beans",
     "என் பீன்ஸ் (beans) செடிகளில் பழுப்பு நிற புள்ளிகள் உள்ளன. என்ன பிரச்சனை?",
     "பழுப்பு நிற புள்ளிகள் ஆந்த்ராக்னோஸ் (anthracnose) நோயின் அறிகுறி. (1) நோயுற்ற செடிகளை பிடுங்கி எரித்து விடுங்கள். (2) நோயை எதிர்க்கும் விதைகளைப் பயன்படுத்துங்கள் — வேளாண்மை அலுவலகத்தில் கிடைக்கும். (3) பயிர் சுழற்சி மேற்கொள்ளுங்கள் — ஒரே நிலத்தில் ஒவ்வொரு வருடமும் பீன்ஸ் பயிரிட வேண்டாம். (4) வேப்ப எண்ணெய் (neem oil 5ml/லிட்டர்) பயன்படுத்துங்கள். (5) இலைகளில் நீர் படாமல் பார்த்துக்கொள்ளுங்கள். (6) செப்பு கலந்த பூஞ்சைக் கொல்லி (copper fungicide) பற்றி வேளாண்மை அதிகாரியை அணுகுங்கள்.",
     "TNAU Bean Disease Guide; CIAT Anthracnose Management", "disease diagnosis"),

    ("India", "Tamil", "beans",
     "பீன்ஸ் (beans) வித்துகளில் புழுக்கள் (weevils) உள்ளன. எப்படி சேமிப்பது?",
     "பீன்ஸில் புழுக்கள் சேமிப்பின் போது ஏற்படும் பொதுவான பிரச்சனை. (1) வித்துகளை நன்றாக வெயிலில் உலர்த்துங்கள். (2) வேப்ப எண்ணெய் (neem oil) தடவுங்கள். (3) காற்றுப் புகாத பாத்திரத்தில் (airtight container) சேமியுங்கள். (4) 7 நாட்கள் ஃப்ரீஸரில் வையுங்கள் — புழுக்கள் இறந்துவிடும். (5) சேமிப்பு அறையை சுத்தமாக வையுங்கள். (6) பாதிக்கப்பட்ட பழைய வித்துகளைப் பயன்படுத்த வேண்டாம்.",
     "TNAU Bean Storage Guide; CIAT Post-Harvest Guide", "pest management"),

    ("India", "Hindi", "beans",
     "मेरी फलियों (beans) में कीड़े लग गए हैं। बचाने का तरीका?",
     "फलियों में कीड़े (weevils) भंडारण की आम समस्या है। (1) फलियों को धूप में अच्छी तरह सुखाएं। (2) नीम का तेल (neem oil 5ml/लीटर) लगाएं। (3) एयरटाइट कंटेनर में रखें। (4) 7 दिन फ्रीज़र में रखें — कीड़े मर जाएंगे। (5) भंडारण कक्ष को साफ रखें। (6) पुराने कीड़े वाले कंटेनर का उपयोग न करें। कृषि अधिकारी से सलाह लें।",
     "ICAR Bean Storage Guide; CIAT Post-Harvest Management", "pest management"),

    ("India", "Hindi", "beans",
     "फलियों (beans) के पत्तों पर भूरे धब्बे और फलियाँ सूख रही हैं। क्या करें?",
     "भूरे धब्बे एंथ्रेक्नोज़ (anthracnose) रोग के लक्षण हैं। (1) प्रभावित पौधों को उखाड़ कर जला दें। (2) रोग-प्रतिरोधी बीज का उपयोग करें — कृषि विभाग से प्राप्त करें। (3) फसल चक्र अपनाएं — हर साल एक ही खेत में फलियाँ न लगाएं। (4) नीम तेल का छिड़काव करें (5ml प्रति लीटर पानी)। (5) सिंचाई के दौरान पत्तियों पर पानी न गिराएं। (6) तांबा-आधारित फफूंदनाशक के लिए कृषि अधिकारी से सलाह लें।",
     "ICAR Bean Anthracnose Guide; CIAT Disease Control", "disease diagnosis"),

    ("Kenya", "Luo", "beans",
     "Oganda m okethore e keno. Ang'o ma anyalo timo mondo okikethre?",
     "Oganda okethore e keno en chandruok maduong'. (1) Riambo oganda e chieng' ka osechok — mondo oneg ondiegi. (2) Kan oganda e 'airtight containers' — ma ondiegi ok nyal donjo e iye. (3) Keto oganda e 'freezer' kuom ndalo 7 — onego tong' gik. (4) Bilo oganda gi neem oil — ondiegi ok hero neem. (5) Tim nyono ni kar keno otwo, ler, to yamo donjoe maber. (6) Dhi ir ofisa mar kilimo mondo okonyi gi kit oganda ma chiegni ohinyi.",
     "KALRO Bean Storage Guide; CIAT Weevil Management", "pest management"),

    ("Tanzania", "Swahili", "beans",
     "Maharagwe yangu yamekosa rutuba na majani yanageuka manjano. Nisaidie?",
     "Majani kugeuka manjano ni ishara ya ukosefu wa nitrojeni au maji mengi. (1) Chukua sampuli ya udongo kwa ofisa wa kilimo. (2) Tumia mbolea ya asili (compost/mavi ya kuku) kuongeza rutuba. (3) Hakikisha shamba lina mifereji mizuri — maharagwe hayapendi maji kusimama. (4) Panda maharagwe kwenye matuta (ridges). (5) Zungusha mazao — panda maharagwe kwa msimu mmoja, panda mahindi au viazi msimu unaofuata. (6) Tumia mbegu za maharagwe zinazostahimili hali mbaya ya udongo kutoka ofisi ya kilimo.",
     "KALRO Bean Soil Health Guide; CIAT Bean Nutrition", "cultural practice"),

    ("Kenya", "Luo", "beans",
     "Oganda mara odongo maber to koro osechako bedo matar, it bende olokore. Ang'o?",
     "Oganda matar gi it olokore nyiso ni nitie tuo mar virus (BCMV) kata chandruok mar lowo. (1) Kel sampul mar it oganda gi lowo ir ofisa mar kilimo mondo gine. (2) Tim nyono gi oganda ma ok mak tuo — many kit machiegni gi KALRO. (3) Ne ane ka nitie aphids — gin e gikelo tuo mar virus. (4) Dhi ir ofisa mar kilimo mondo okonyi gi fungicide ma owinjore. (5) Puodh cham kinyoro — kik ipidh oganda kamoro pile.",
     "KALRO Bean BCMV Guide; CIAT Virus Management", "disease diagnosis"),

    # ═══════════════ SUNFLOWER — Across regions (12 entries) ═══════════════
    ("Tanzania", "Swahili", "sunflower",
     "Alizeti zangu zina majani yanayokauka na maua madogo. Nifanyeje?",
     "Alizeti yenye majani kukauka na maua madogo inaweza kuwa na ukosefu wa maji au virutubisho. (1) Alizeti haipendi maji mengi lakini inahitaji unyevu. Weka matandazo (mulch). (2) Chukua sampuli ya udongo kwa ofisa wa kilimo. (3) Tumia mbolea ya NPK (kijiko kimoja kwa mmea) wakati wa kupanda. (4) Panda aina za alizeti zinazostahimili ukame: 'Hysun 33', 'PAN 7351' au 'Record'. (5) Panda alizeti kwenye matuta (ridges) — mizizi inahitaji hewa. (6) Weka nafasi: cm 75 kati ya mistari, cm 30 kati ya mimea.",
     "TARI Sunflower Guide; ICRISAT Sunflower Agronomy", "cultural practice"),

    ("Tanzania", "Swahili", "sunflower",
     "Alizeti zangu zina wadudu wakula maua na mbegu. Wadudu gani?",
     "Wadudu wanaokula maua na mbegu za alizeti ni sunflower head borer (Helicoverpa armigera). (1) Ondoa maua yaliyoathirika na uyachome. (2) Panda mapema kabla ya wadudu kuwa wengi. (3) Tumia neem oil (5ml kwa lita 1) kunyunyiza maua. (4) Zungusha mazao — usipande alizeti mara kwa mara. (5) Aina zinazostahimili: 'PAN 7031', 'Hysun 38'. (6) Kwa mashambulizi makubwa, wasiliana na ofisa kilimo kwa dawa za kibiashara.",
     "TARI Sunflower Pest Guide; ICRISAT Head Borer Control", "pest management"),

    ("Tanzania", "Swahili", "sunflower",
     "Alizeti zangu zina kutu (rust) kwenye majani. Tiba gani?",
     "Kutu kwenye majani ya alizeti ni ugonjwa wa sunflower rust (Puccinia helianthi). (1) Ondoa majani yaliyoathirika na uyachome. (2) Panda aina za alizeti zinazostahimili kutu: 'Hysun 39', 'PAN 7031'. (3) Zungusha mazao — usipande alizeti kwenye shamba moja msimu kwa msimu. (4) Tumia fungicide ya shaba (copper) baada ya ushauri wa ofisi ya kilimo. (5) Panda alizeti mapema wakati wa mvua. (6) Ondoa magugu — magugu hueneza kutu.",
     "TARI Sunflower Rust Guide; ICRISAT Rust Management", "disease diagnosis"),

    ("India", "Punjabi", "sunflower",
     "ਮੇਰੇ ਸੂਰਜਮੁਖੀ (sunflower) ਦੇ ਫੁੱਲ ਛੋਟੇ ਹਨ ਅਤੇ ਬੀਜ ਨਹੀਂ ਪੈ ਰਹੇ। ਕੀ ਕਰਾਂ?",
     "ਸੂਰਜਮੁਖੀ ਦੇ ਛੋਟੇ ਫੁੱਲ ਅਤੇ ਬੀਜ ਨਾ ਪੈਣਾ ਪਰਾਗਣ (pollination) ਦੀ ਸਮੱਸਿਆ ਹੈ। (1) ਸੂਰਜਮੁਖੀ ਦੇ ਨੇੜੇ ਸ਼ਹਿਦ ਦੀਆਂ ਮੱਖੀਆਂ ਰੱਖੋ — ਇਹ ਪਰਾਗਣ ਵਿੱਚ ਮਦਦ ਕਰਦੀਆਂ ਹਨ। (2) ਕੀੜੇ-ਮਾਰ ਦਵਾਈਆਂ ਫੁੱਲ ਆਉਣ ਸਮੇਂ ਨਾ ਵਰਤੋ — ਇਹ ਮਿੱਤਰ ਕੀੜਿਆਂ ਨੂੰ ਮਾਰਦੀਆਂ ਹਨ। (3) ਪਾਣੀ ਦੀ ਕਮੀ — ਫੁੱਲ ਆਉਣ ਸਮੇਂ ਸੂਰਜਮੁਖੀ ਨੂੰ ਕਾਫ਼ੀ ਪਾਣੀ ਚਾਹੀਦਾ ਹੈ। (4) ਬੀਜਣ ਦਾ ਸਮਾਂ ਸਹੀ ਰੱਖੋ — ਫਰਵਰੀ-ਮਾਰਚ। (5) NPK ਖਾਦ (10:20:10) ਵਰਤੋ। (6) ਕਿਸਾਨ ਸਲਾਹ ਕੇਂਦਰ ਤੋਂ ਸਲਾਹ ਲਓ।",
     "Punjab Agriculture Sunflower Guide; ICRISAT Pollination Guide", "general inquiry"),

    ("India", "Punjabi", "sunflower",
     "ਸੂਰਜਮੁਖੀ (sunflower) ਦੇ ਪੱਤਿਆਂ 'ਤੇ ਗੂੜ੍ਹੇ ਭੂਰੇ ਧੱਬੇ ਹਨ। ਬਿਮਾਰੀ?",
     "ਗੂੜ੍ਹੇ ਭੂਰੇ ਧੱਬੇ Alternaria blight ਦੇ ਲੱਛਣ ਹਨ। (1) ਪ੍ਰਭਾਵਿਤ ਪੱਤਿਆਂ ਨੂੰ ਤੋੜ ਕੇ ਸਾੜ ਦਿਓ। (2) ਰੋਗ-ਰੋਧਕ ਕਿਸਮਾਂ ਵਰਤੋ: 'PSFH 118', 'PSFH 167'। (3) ਬੀਜ ਨੂੰ ਬੀਜਣ ਤੋਂ ਪਹਿਲਾਂ ਗਰਮ ਪਾਣੀ (52°C) ਵਿੱਚ 10 ਮਿੰਟ ਪਕਾਓ। (4) ਕਾਪਰ-ਆਧਾਰਿਤ ਫ਼ੰਜੀਸਾਈਡ ਵਰਤੋ — ਕਿਸਾਨ ਸਲਾਹ ਕੇਂਦਰ ਤੋਂ ਸਲਾਹ ਲਓ। (5) ਫਸਲੀ ਚੱਕਰ — ਹਰ ਸਾਲ ਇੱਕੋ ਖੇਤ ਵਿੱਚ ਨਾ ਬੀਜੋ। (6) ਪਾਣੀ ਪੱਤਿਆਂ 'ਤੇ ਨਾ ਪੈਣ ਦਿਓ — ਤੁਪਕਾ ਸਿੰਚਾਈ (drip irrigation) ਵਰਤੋ।",
     "Punjab Agriculture Sunflower Blight Guide; ICRISAT Alternaria Control", "disease diagnosis"),

    ("India", "Hindi", "sunflower",
     "सूरजमुखी (sunflower) के फूल छोटे हैं और बीज नहीं बन रहे। क्या करें?",
     "छोटे फूल और बीज न बनना परागण (pollination) की समस्या है। (1) खेत के पास मधुमक्खी के छत्ते रखें — ये परागण में मदद करते हैं। (2) फूल आने पर कीटनाशक का प्रयोग न करें — यह मित्र कीटों को मारता है। (3) फूल आने पर पानी की कमी न होने दें। (4) NPK खाद (10:20:10) का प्रयोग करें। (5) सही समय पर बुवाई करें — फरवरी-मार्च। (6) कृषि अधिकारी से सलाह लें।",
     "ICAR Sunflower Guide; ICRISAT Pollination Guide", "general inquiry"),

    ("India", "Hindi", "sunflower",
     "सूरजमुखी (sunflower) के पत्तों पर भूरे धब्बे हैं। रोग का नाम?",
     "भूरे धब्बे Alternaria blight के लक्षण हैं। (1) प्रभावित पत्तियों को तोड़कर जला दें। (2) रोग-प्रतिरोधी किस्मों का प्रयोग करें: 'PSFH 118', 'KBSH 53'। (3) बीज को गर्म पानी (52°C) में 10 मिनट उपचारित करें। (4) तांबा-आधारित फफूंदनाशक का प्रयोग — कृषि अधिकारी से सलाह लें। (5) फसल चक्र अपनाएं। (6) पत्तियों पर पानी न गिराएं — ड्रिप सिंचाई का प्रयोग करें।",
     "ICAR Sunflower Blight Guide; ICRISAT Alternaria Control", "disease diagnosis"),

    ("Kenya", "Luo", "sunflower",
     "Chieng' mara mara (sunflower) ok onyiso kithe maber. Ang'o?",
     "Chieng' mara ma ok onyiso kithe nyalo bedo ni cham ok oyudomo maber. (1) Pidh chieng' mara e lowo ma yamo donjoe maber — chieng' mara ok hero pi mochung'. (2) Ti gi NPK manyien (10:20:10) — kijiko achiel kuom yien ka ipidho. (3) Ket chieng' mara e lowo ma ok ne oseri gi chieng' mara mokwongo. (4) Pidh chieng' mara ka ochako chwiri (March-April) mondo oyud pi maber. (5) Ri e kinde kod chieng' mara — 75cm e kinde, 30cm e kinde mag yien. (6) Dhi ir ofisa mar kilimo.",
     "KALRO Sunflower Guide; ICRISAT Sunflower Agronomy", "cultural practice"),

    ("Kenya", "Luo", "sunflower",
     "Chieng' mara nigi tuo ma rachar e it kod e wigi. Ang'o ma anyalo timo?",
     "Tuo ma rachar e it chieng' mara en rust (Puccinia helianthi). (1) Golo it ma tuo oko ma iwang'gi. (2) Pidh chieng' mara ma ok mak tuo: 'Hysun 39'. (3) Puodh cham kinyoro — kik ipidh chieng' mara kamoro pile. (4) Ti gi fungicide ma ofisa mar kilimo osenyiso. (5) Pidh chieng' mara e ndalo maber mondo oyud pi maber. (6) Golo lum oko e puodho — lum kelo tuo.",
     "KALRO Sunflower Rust Guide; ICRISAT Rust Control", "disease diagnosis"),

    ("Ethiopia", "Amharic", "sunflower",
     "የሱፍ አበባዬ (sunflower) አበባዎች ትንሽ ናቸው ዘርም አይፈጠርም። ምን ችግር ነው?",
     "የአበባ መጠን አነስተኛ መሆን እና ዘር አለመፈጠር የአበባ ውርስ (pollination) ችግር ነው። (1) በማሳ አጠገብ የማር ንቦችን ያስቀምጡ — ንቦች ለአበባ ውርስ ይረዳሉ። (2) አበባ በሚወጣበት ጊዜ ፀረ-ነፍሳት አይጠቀሙ። (3) ውሃ አይጉደል — ሱፍ አበባ በአበባ ጊዜ ብዙ ውሃ ያስፈልገዋል። (4) NPK ማዳበሪያ ተጠቀሙ። (5) ወቅቱን ጠብቀው ይዝሩ — የካቲት ወር (ፌብሩዋሪ)። (6) ለተጨማሪ እርዳታ የግብርና ባለሙያውን ያነጋግሩ።",
     "EIAR Sunflower Guide; ICRISAT Pollination Advisory", "general inquiry"),

    ("Ethiopia", "Amharic", "sunflower",
     "የሱፍ አበባዬ (sunflower) ቅጠሎች ላይ ቡናማ ነጠብጣቦች አሉ። በሽታ?",
     "ቡናማ ነጠብጣቦች Alternaria blight በሽታ ነው። (1) የታመሙ ቅጠሎችን አውጥተህ አቃጥላቸው። (2) በሽታን የሚቋቋሙ ዝርያዎች: 'KBSH 53', 'PSFH 118'። (3) ዘሩን በሙቅ ውሃ (52°C) ለ10 ደቂቃ አከም (seed treatment)። (4) የነም (neem) ዘይት ተጠቀም (5ml በ1 ሊትር ውሃ)። (5) ሰብል አዙር። (6) ቅጠሎች ላይ ውሃ እንዳይወርድ አድርግ — drip irrigation ተጠቀም።",
     "EIAR Sunflower Blight Guide; ICRISAT Alternaria Control", "disease diagnosis"),

    ("Nigeria", "Hausa", "sunflower",
     "Furen rana (sunflower) na ganye suna yin launin ruwan kasa. Cutace ne?",
     "Launin ruwan kasa a ganyen furen rana cutace ne na Alternaria blight. (1) Cire ganyen da suka kamu da cutar — kona su. (2) Yi amfani da iri masu jurewa cutar: 'KBSH 53', 'PSFH 118'. (3) Yi maganin iri da ruwan zafi (52°C) na mintuna 10 kafin shuka. (4) Yi amfani da mai na neem (neem oil 5ml/lita). (5) Juya amfanin gona — kada a shuka furen rana a gona guda kowace shekara. (6) Tuntuɓi jami'in noma don ƙarin shawara.",
     "NAERLS Sunflower Guide; ICRISAT Alternaria Management", "disease diagnosis"),

    # ═══════════════ DAIRY — Across regions (12 entries) ═══════════════
    ("Kenya", "Luo", "dairy",
     "Dhiang'a ok nyal nyuolo nanga. Ang'o ma timo?",
     "Dhiang' ma ok nyal nyuolo nyalo bedo gi chandruok moro. (1) Kel dhiang' ir ng'al moro mar le (vet). (2) Riti gi dhiang' maber — miye chiemo maber, pi mathoth. (3) Nyaka dhiang' bed gi ng'wno maber — ka dhiang' nen gi remo, biyo vet. (4) Ket dhiang' kod rwodhi (bull) kata ti gi AI (insemination) — vet nyiso kaka. (5) Sukuru dhiang' ka osebedo gi tuo. (6) Dhiang' ma tek tek inyalo ng'iewo — dhiang' Nyando (Jersey) chiegni nyuolo nanga.",
     "KALRO Dairy Breeding Guide; DVS Cattle Reproduction", "general inquiry"),

    ("Kenya", "Luo", "dairy",
     "Nyang'a (calf) kata nyathi dhiang' ok dwaro metho mi kata chiemo. Ang'o?",
     "Nyang'a ma ok dwaro chiemo nyalo bedo gi tuo. (1) Ne ane ka nyathi dhiang' (calf) nigi tuo — kel ir vet. (2) Miye pi maler, chiemo maber. (3) Ket nyathi dhiang' kar ma otwo, ma yamo donjoe, to piny ok ng'ich. (4) Riti kod nyathi dhiang' kaka midwaro — sukuru kar otwo pile. (5) Kokwo (colostrum) ema onego mi nyathi dhiang' bang' nyuolo — en chiwo teko. (6) Ka nyathi dhiang' ok metho bang' 12 hours, biyo vet.",
     "KALRO Calf Rearing Guide; DVS Calf Health Advisory", "general inquiry"),

    ("Kenya", "Kikuyu", "dairy",
     "Ng'ombe yakwa ndĩrĩ kũhaica mũceere. Ngĩkwo?",
     "Ng'ombe ndĩrĩ kũhaica mũceere no gũtũmwo nĩ indo ingĩ. (1) Rekereria vet — no kũrĩ na ndwari mũciĩ. (2) Rĩa (feed) wega: nyeki njaa, dairy meal 2-3 kg mũthenya. (3) Mai (water) maingĩ: ng'ombe yũyaga mai 40-60 litres mũthenya. (4) Ng'ombe no ĩrĩ na mastitis — rekereria vet. (5) Rĩa na maũndu marĩa marĩ na protini nyingĩ — lucerne, Rhodes grass. (6) Tiga gũtema (stress) — ndwari ĩthekagia mũceere.",
     "KALRO Dairy Production Guide; DVS Milk Advisory", "general inquiry"),

    ("Kenya", "Kikuyu", "dairy",
     "Ng'ombe yakwa nĩ ĩrĩ na magego ma gũthinia na mũcinga. Nĩ ndwari?",
     "Magego ma gũthinia na mũcinga nĩ mastitis. (1) ITA vet oka — ndwari ĩno ĩregana. (2) Theria (clean) mara nyonĩ cia ng'ombe mbere ya gũthinia. (3) Tuma teat dip thutha wa gũthinia buri mũthenya. (4) Ndũkathinie na moko makwa na ng'ombe ciothe — tuma moko ma mũciĩrĩrĩ. (5) Thinia ng'ombe iria irĩ mastitis ciagĩrĩrĩo — tangira na iria njega. (6) Theria handũ ha gũthinia buri mũthenya. (7) Ng'ombe ĩngĩkorwo ĩrĩ na mwaki (fever), vet nĩegũtuma antibiotics.",
     "KALRO Mastitis Control; DVS Veterinary Guide", "disease diagnosis"),

    ("Tanzania", "Swahili", "dairy",
     "Ng'ombe wangu ana maziwa machache. Nini sababu?",
     "Ng'ombe kuwa na maziwa machache kuna sababu nyingi. (1) Chakula — ng'ombe anahitaji nyasi bora na unga wa maziwa (dairy meal) 2-3 kg kwa siku. (2) Maji — ng'ombe anahitaji maji 40-60 lita kwa siku. (3) Afya — angalia kama ng'ombe ana mastitis au ugonjwa mwingine. (4) Aina (breed) — ng'ombe wa Friesian na Jersey wana maziwa mengi. (5) Umri — ng'ombe wakubwa wana maziwa machache. (6) Msimu — ng'ombe ana maziwa mengi baada ya kuzaa. (7) Piga simu daktari wa mifugo (vet) kwa ushauri zaidi.",
     "TALIRI Dairy Guide; DVS Milk Production Advisory", "general inquiry"),

    ("Tanzania", "Swahili", "dairy",
     "Ng'ombe wangu ana uvimbe kwenye kiwele (udder). Nifanyeje?",
     "Uvimbe kwenye kiwele ni mastitis. (1) PIGA SIMU daktari wa mifugo (vet) haraka. (2) Kama ng'ombe — safisha kiwele kabla ya kukama. (3) Tumia teat dip baada ya kukama (kila siku baada ya kukama). (4) Usikame kwa mikono yote — tumia kitambaa tofauti kwa kila ng'ombe. (5) Kama kwanza ng'ombe wenye afya — kisha ng'ombe wenye mastitis. (6) Safisha eneo la kukama kila siku. (7) Kama ng'ombe ana homa, anahitaji antibiotics — daktari wa mifugo atatoa dawa.",
     "TALIRI Mastitis Control; DVS Veterinary Guide", "disease diagnosis"),

    ("India", "Punjabi", "dairy",
     "ਮੇਰੀ ਗਾਂ (cow) ਦਾ ਦੁੱਧ ਘੱਟ ਹੋ ਗਿਆ ਹੈ। ਕੀ ਕਰਾਂ?",
     "ਗਾਂ ਦਾ ਦੁੱਧ ਘੱਟ ਹੋਣ ਦੇ ਕਈ ਕਾਰਨ ਹਨ। (1) ਖੁਰਾਕ — ਗਾਂ ਨੂੰ ਹਰਾ ਚਾਰਾ, 2-3 ਕਿਲੋ ਦੁੱਧਣੀ ਖੁਰਾਕ (dairy meal) ਪ੍ਰਤੀ ਦਿਨ ਦਿਓ। (2) ਪਾਣੀ — ਗਾਂ ਨੂੰ 40-60 ਲਿਟਰ ਪਾਣੀ ਪ੍ਰਤੀ ਦਿਨ ਚਾਹੀਦਾ ਹੈ। (3) ਸਿਹਤ — mastitis ਜਾਂ ਹੋਰ ਬੀਮਾਰੀ। (4) ਨਸਲ — Friesian, Gir, Sahiwal ਨਸਲਾਂ ਵਧੀਆ ਦੁੱਧ ਦਿੰਦੀਆਂ ਹਨ। (5) ਸਮਾਂ — ਬੱਚਾ ਦੇਣ ਤੋਂ ਬਾਅਦ ਦੁੱਧ ਵਧਦਾ ਹੈ। (6) ਪਸ਼ੂ ਡਾਕਟਰ (vet) ਨੂੰ ਬੁਲਾਓ — ਉਹ ਪੂਰੀ ਜਾਂਚ ਕਰ ਸਕਦਾ ਹੈ।",
     "NDDB Dairy Guide; ICAR Dairy Advisory", "general inquiry"),

    ("India", "Punjabi", "dairy",
     "ਗਾਂ (cow) ਦੇ ਥਣ (udder) ਵਿੱਚ ਸੋਜ (swelling) ਹੈ। ਇਲਾਜ?",
     "ਥਣ ਵਿੱਚ ਸੋਜ mastitis ਦੇ ਲੱਛਣ ਹਨ। (1) ਪਸ਼ੂ ਡਾਕਟਰ (vet) ਨੂੰ ਤੁਰੰਤ ਬੁਲਾਓ। (2) ਦੁੱਧ ਦੁਹਾਉਣ ਤੋਂ ਪਹਿਲਾਂ ਥਣ ਨੂੰ ਧੋਵੋ। (3) ਦੁੱਧ ਦੁਹਾਉਣ ਤੋਂ ਬਾਅਦ 'teat dip' ਵਰਤੋ (ਹਰ ਵਾਰ)। (4) ਹਰ ਗਾਂ ਲਈ ਵੱਖਰਾ ਤੌਲੀਆ ਵਰਤੋ। (5) ਪਹਿਲਾਂ ਤੰਦਰੁਸਤ ਗਾਵਾਂ, ਫਿਰ ਬੀਮਾਰ ਗਾਂ — ਦੁੱਧ ਦੁਹੋਵੋ। (6) ਸਫਾਈ (hygiene) ਦਾ ਧਿਆਨ ਰੱਖੋ। (7) ਜੇ ਗਾਂ ਨੂੰ ਬੁਖਾਰ (fever) ਹੈ, antibiotics ਜ਼ਰੂਰੀ — vet ਨਾਲ ਸਲਾਹ ਕਰੋ।",
     "NDDB Mastitis Guide; ICAR Veterinary Advisory", "disease diagnosis"),

    ("India", "Hindi", "dairy",
     "मेरी गाय (cow) का दूध कम हो गया है। क्या करें?",
     "दूध कम होने के कई कारण हैं। (1) खुराक — हरा चारा, 2-3 किलो डेयरी मील प्रतिदिन। (2) पानी — गाय को 40-60 लिटर पानी प्रतिदिन चाहिए। (3) स्वास्थ्य — mastitis या अन्य बीमारी। (4) नस्ल — Sahiwal, Gir, Friesian बेहतर दूध देती हैं। (5) समय — बच्चा देने के बाद दूध बढ़ता है। (6) पशु चिकित्सक (vet) को बुलाएं।",
     "NDDB Dairy Guide; ICAR Livestock Advisory", "general inquiry"),

    ("India", "Hindi", "dairy",
     "गाय (cow) के थन (udder) में सूजन (swelling) है। इलाज?",
     "थन में सूजन mastitis का लक्षण है। (1) पशु चिकित्सक (vet) को तुरंत बुलाएं। (2) दूध निकालने से पहले थन धोएं। (3) दूध निकालने के बाद 'teat dip' का प्रयोग करें (हर बार)। (4) हर गाय के लिए अलग तौलिया प्रयोग करें। (5) पहले स्वस्थ गाय, फिर बीमार गाय का दूध निकालें। (6) स्वच्छता का ध्यान रखें। (7) बुखार (fever) होने पर antibiotics ज़रूरी — vet से सलाह लें।",
     "NDDB Mastitis Control; ICAR Veterinary Guide", "disease diagnosis"),

    ("Ethiopia", "Amharic", "dairy",
     "ላሜ (cow) ወተቷ ጠፋ። ምን ማድረግ አለብኝ?",
     "ላም ወተቷ መጥፋት ብዙ ምክንያቶች አሉት። (1) አመጋገብ — ሳር፣ የወተት ምግብ (dairy meal) 2-3 ኪሎ በቀን። (2) ውሃ — ላም 40-60 ሊትር ውሃ በቀን ያስፈልጋታል። (3) ጤና — mastitis ወይም ሌላ በሽታ። (4) ዝርያ — Friesian፣ Jersey እና አካባቢው ዝርያዎች። (5) እንስሳት ሐኪም (vet) ይደውሉ።",
     "EIAR Dairy Guide; MoA Livestock Advisory", "general inquiry"),

    ("Ethiopia", "Amharic", "dairy",
     "ላሜ (cow) ጡቷ (udder) አበጠ (swelling)። መድሀኒት?",
     "የጡት እብጠት mastitis ነው። (1) እንስሳት ሐኪም (vet) ወዲያው ይደውሉ። (2) ከማጠብ በፊት ጡትን ያጽዱ (wash)። (3) ከወተት ከወጡ በኋላ 'teat dip' ይጠቀሙ (በየቀኑ)። (4) ለእያንዳንዱ ላም የተለየ ፎጣ (towel) ይጠቀሙ። (5) መጀመሪያ ጤናማ ላሞች፣ በኋላ mastitis ያለባትን ላም ያጥቡ። (6) ንጽህና ይጠብቁ። (7) ላም ትኩሳት (fever) ካለባት አንቲባዮቲክስ ያስፈልጋል — የእንስሳት ሐኪሙን ያነጋግሩ።",
     "EIAR Mastitis Control; MoA Veterinary Advisory", "disease diagnosis"),

    # ═══════════════ MALAWI — Region boost (12 entries) ═══════════════
    ("Malawi", "English", "maize",
     "My maize has purple leaves and stunted growth. What is the problem?",
     "Purple leaves in maize indicate phosphorus deficiency (purpling) or maize streak virus. (1) Purple from phosphorus deficiency: apply DAP fertilizer (1 tablespoon per plant). (2) Test your soil at the agricultural office — they'll confirm pH and nutrients. (3) If leaves have white/yellow streaks instead, it's maize streak virus (MSV) carried by leafhoppers. (4) For MSV, remove affected plants and burn them. (5) Plant MSV-resistant varieties: 'SC 403', 'PAN 691', 'DK 777'. (6) Rotate crops — don't plant maize in the same field next season. Contact your extension officer (Department of Agricultural Research Services).",
     "DARS Maize Production Guide; CIMMYT Streak Virus Control", "disease diagnosis"),

    ("Malawi", "English", "maize",
     "My maize cobs have rotten tips and mouldy grains. What causes this?",
     "Rotten cob tips and mouldy grains are caused by ear rot (Fusarium or Aspergillus). (1) Harvest maize as soon as it's ready — don't leave cobs in the field too long. (2) Dry maize thoroughly on a clean surface (not bare ground). (3) Store grains in clean, dry, airtight containers. (4) Remove any mouldy cobs immediately — don't mix with healthy ones. (5) Apply recommended fungicide (copper-based) if problem persists. (6) Next season, plant varieties with better husk cover: 'SC 403', 'MH 30'. Contact your extension officer.",
     "DARS Maize Post-Harvest Guide; CIMMYT Ear Rot Control", "disease diagnosis"),

    ("Malawi", "English", "groundnut",
     "My groundnut leaves have orange spots and the plants are dying. What to do?",
     "Orange spots on groundnut leaves are rust (Puccinia arachidis). (1) Remove and burn affected leaves. (2) Plant resistant varieties: 'CG 7', 'Chalimbana', 'JL 24'. (3) Rotate crops — don't plant groundnuts in the same field for 2 years. (4) Space plants properly (30cm between rows, 15cm between plants) for air circulation. (5) Use neem oil spray (5ml per litre water). (6) If severe, apply copper-based fungicide — consult extension officer. Contact Department of Agricultural Research Services.",
     "DARS Groundnut Rust Guide; ICRISAT Rust Management", "disease diagnosis"),

    ("Malawi", "English", "groundnut",
     "My groundnut seeds taste bitter and have dark spots inside. Problem?",
     "Bitter tasting groundnuts with dark spots likely have aflatoxin contamination. (1) Dry groundnuts thoroughly in the sun before storage. (2) Store in a cool, dry, well-ventilated place. (3) Don't store groundnuts for more than 3-4 months. (4) Remove any discoloured or shrivelled nuts. (5) Apply lime to soil (2-3 kg per plot) before next planting. (6) Plant early maturing varieties: 'CG 7', 'ICGV 90704'. Test your soil at DARS office.",
     "DARS Aflatoxin Guide; ICRISAT Aflatoxin Control", "general inquiry"),

    ("Malawi", "English", "cassava",
     "My cassava leaves are curling and the roots are small. What's wrong?",
     "Curling leaves and small roots indicate Cassava Mosaic Disease (CMD). (1) Remove and burn all affected plants immediately. (2) Get clean cassava cuttings from the agricultural office (Bwanje Valley Farm or DARS). (3) Plant CMD-resistant varieties: 'Sauti', 'Mbundumali', 'Tumaini'. (4) Control whiteflies — they spread CMD. Use neem oil spray (5ml/litre). (5) Rotate: don't plant cassava in the same field next year. (6) Plant early — whiteflies increase late in the season. Contact your extension officer.",
     "DARS Cassava CMD Guide; IITA Cassava Disease Management", "disease diagnosis"),

    ("Malawi", "English", "cassava",
     "My cassava has brown streaks inside the roots and tastes bitter. Help?",
     "Brown streaks inside cassava roots with bitter taste is Cassava Brown Streak Disease (CBSD). (1) Remove and burn all affected plants — do NOT use for cuttings. (2) Get disease-free cuttings from DARS or Bwanje Valley Farm. (3) Plant CBSD-tolerant varieties: 'Mbundumali', 'Sauti', 'Nkhwangwa'. (4) Control whiteflies with neem oil (5ml/litre). (5) Don't plant cassava in the same field for at least one season. (6) Inform neighbouring farmers — CBSD spreads quickly. Contact extension officer.",
     "DARS CBSD Management; IITA Cassava Brown Streak Advisory", "disease diagnosis"),

    ("Malawi", "English", "beans",
     "My beans have brown spots on leaves and the pods are rotting. Disease?",
     "Brown spots on leaves and rotting pods is anthracnose. (1) Remove and burn all affected plants. (2) Plant resistant bean varieties: 'Napilira' (MS 5), 'Makwacha' (MS 6), 'Chimbamba'. (3) Rotate — don't plant beans in the same field next season. (4) Use neem oil spray (5ml/litre). (5) Plant in raised ridges for drainage. (6) Apply copper-based fungicide if severe — consult extension officer at DARS.",
     "DARS Bean Anthracnose Guide; CIAT Bean Disease Management", "disease diagnosis"),

    ("Malawi", "English", "beans",
     "My harvested beans have small holes and weevils inside. How to store?",
     "Small holes and weevils in stored beans is bean weevil (Acanthoscelides obtectus). (1) Sun-dry beans thoroughly before storage. (2) Mix with neem leaves or neem oil (5ml/kg). (3) Store in airtight containers. (4) Put beans in freezer for 7 days to kill weevils. (5) Clean storage area thoroughly. (6) Don't reuse old infested containers. Contact extension officer for resistant varieties.",
     "DARS Bean Storage Guide; CIAT Post-Harvest Advisory", "pest management"),

    ("Malawi", "English", "sweet potato",
     "My sweet potato vines are wilting and the tubers have holes. What?",
     "Wilting vines and holes in tubers is sweet potato weevil (Cylas formicarius). (1) Remove and destroy all infested plants. (2) Plant weevil-resistant varieties: 'Mafuta', 'Machinga', 'Tanzania'. (3) Plant on ridges for good drainage. (4) Harvest early — don't leave tubers in the ground too long. (5) Rotate — don't plant sweet potato in the same field next season. (6) Apply neem oil around stems. Contact DARS extension officer.",
     "DARS Sweet Potato Weevil Guide; CIP Weevil Management", "pest management"),

    ("Malawi", "English", "groundnut",
     "My groundnuts are producing poorly and the soil looks tired. What now?",
     "Poor groundnut yield and tired soil indicates soil depletion. (1) Test soil at DARS — they'll tell you what's missing. (2) Apply compost or well-rotted manure (2-3 kg per square metre). (3) Apply NPK (15:15:15) at 50g per plant. (4) Rotate groundnuts with maize and beans to restore nutrients. (5) Plant cover crops (sunn hemp, mucuna) after harvest to improve soil. (6) Plant improved varieties: 'CG 7', 'JL 24', 'ICGV 90704'. Contact extension officer.",
     "DARS Soil Health Guide; ICRISAT Groundnut Agronomy", "cultural practice"),

    ("Malawi", "English", "maize",
     "Maize stems are breaking and there are caterpillars inside. What pest?",
     "Caterpillars inside broken maize stems is maize stem borer (Busseola fusca). (1) Cut and burn all infested stems. (2) Plant early — before borer numbers increase. (3) Rotate with non-cereal crops (beans, groundnuts). (4) Plant tolerant varieties: 'SC 403', 'MH 30'. (5) Apply neem oil (5ml/litre) directly into stem funnels. (6) For heavy infestation, contact extension officer for approved insecticide. Use neem-based solutions first.",
     "DARS Maize Stem Borer Guide; CIMMYT Borer Management", "pest management"),

    ("Malawi", "English", "sorghum",
     "Sorghum heads have mould and the seeds are black. Problem?",
     "Black mould on sorghum heads is grain mould (Fusarium/Aspergillus). (1) Harvest sorghum promptly when ready. (2) Dry heads thoroughly on a clean surface. (3) Store in dry, well-ventilated containers. (4) Plant resistant varieties: 'Pilira 1', 'Pilira 2', 'Macia'. (5) Remove mouldy heads immediately — don't mix with healthy ones. (6) Rotate crops. Contact DARS extension officer for seed treatment options.",
     "DARS Sorghum Mould Guide; ICRISAT Grain Mould Control", "disease diagnosis"),

    # ═══════════════ ADDITIONAL GAPS (15 entries) ═══════════════
    ("Kenya", "Swahili", "tea",
     "Chai yangu ina majani ya rangi ya kijani na madoa ya kahawia. Inaweza kuwa nini?",
     "Madoa ya kahawia kwenye chai ni ugonjwa wa blister blight (Exobasidium vexans). (1) Chuma majani yalioathirika na uyachome. (2) Panda chai kwenye mwinuko mkubwa (elevation) — chai ya juu hupata tatizo dogo. (3) Ondoa magugu na kuhakikisha hewa inapita miongoni mwa vichaka. (4) Tumia dawa ya shaba (copper fungicide) baada ya ushauri wa ofisa kilimo. (5) Panda aina za chai zinazostahimili: 'TRFK 301/4', 'TRFK 306/1'. (6) Wasiliana na KALRO au ofisi ya chai (Tea Board) kwa ushauri zaidi.",
     "KALRO Tea Blister Blight Guide; TRFK Disease Advisory", "disease diagnosis"),

    ("Kenya", "Swahili", "tea",
     "Chai yangu inakauka na majani yanageuka nyekundu. Nini?",
     "Majani nyekundu na kukauka kwa chai ni ugonjwa wa 'red rust' (Cephaleuros virescens). (1) Hii ni mwani (algae) na sio kuvu — haitaji dawa kali. (2) Ondoa majani yaliyoathirika na uyachome. (3) Hakikisha miti ina hewa ya kutosha — panda chai kwa nafasi ya cm 120 kati ya safu. (4) Weka matandazo (mulch) ili kupunguza unyevu kwenye majani. (5) Tumia neem oil (5ml kwa lita 1). (6) Wasiliana na KALRO au TRFK kwa ushauri zaidi.",
     "KALRO Tea Red Rust Guide; TRFK Algae Management", "disease diagnosis"),

    ("Tanzania", "Swahili", "tea",
     "Chai yangu haitoi majani mengi na inaonekana dhaifu. Nifanyeje?",
     "Chai dhaifu yenye majani machache inahitaji ukarabati. (1) Chukua sampuli ya udongo kwa ofisi ya kilimo. (2) Tumia mbolea ya chai iliyopendekezwa (NPK tea fertilizer) — 50g kwa kichaka baada ya kunya. (3) Kata (prune) chai kwa kina cha cm 50-60 kufanya vichaka kuwa vichanga. (4) Ondoa magugu — magugu huchukua rutuba. (5) Weka matandazo (mulch) kwa kutumia nyasi au majani. (6) Panda miti ya kivuli kama grevillea — chai inafanya vizuri kwenye kivuli kidogo. Wasiliana na TARI.",
     "TARI Tea Management Guide; TRFK Tea Agronomy", "cultural practice"),

    ("Ghana", "Twi", "maize",
     "Me nkyene no anyini yie nso nwumaa no so nni bi. Asem?",
     "Nkyene a ayɛ dena nwumaa nni so no botae ne pollination. (1) Fa nkyene pii dua wɔ baabi koro so — wobenya nnua pii a wɔyɛ no. (2) Mfa nnua a ɛkyekye nwura (herbicides) adwuma wɔ mmaeberɛ mu — ɛno kum mmodoma a wodi afuw no ho dwumadie. (3) Nsuo a ɛdɔɔso ma nkyene ntumi nyini. Fa nkyene a ɛwɔ hɔ ban: 'Obatanpa', 'Mamaba'. (4) Fa NPK kɔ afuw no mu (100kg/hekta). (5) Hwɛ wɔ berɛ a nkyene rekɔ mmaeberɛ mu — sɛ nsuo nni hɔ a, fa nsuo gu. (6) Kɔ MOFA hɔ ma wɔnkyerɛ wo nkyene aba pa.",
     "MOFA Maize Pollination Guide; CSRI Maize Agronomy", "general inquiry"),

    ("Rwanda", "Kinyarwanda", "rice",
     "Umuceli wanjye urahindagurika, amababi yera umuhondo, kandi ibiti byawo biroroshye. Ni iki gitari?",
     "Ibi ni indwara ya rice blast (Pyricularia oryzae). (1) Kura ibiti byanduye byose ukabitwike. (2) Hitamo imbuto z'umuceli zihanganira blast: 'FARO 44', 'FARO 52', 'SIPI 692033'. (3) Tega murima amahuriro (drainage) — umuceli ukunda amazi ariko si menshi cyane. (4) Ntukoreshe ifumbire ya azote nyinshi — izagabanya ubudahangarwa bw'umuceli. (5) Hinduranya ibihingwa — ntuhinge umuceli aho wawukozee. (6) Ohereza amababi y'umuceli mu kigo cy'ubuhinzi kugira ngo bamenye neza indwara.",
     "RAB Rice Blast Guide; AfricaRice Blast Management", "disease diagnosis"),

    ("Uganda", "Luganda", "cotton",
     "Pamba yange teliika bulungi era n'ebikoola bya kyenvu. Kiki ekiriwo?",
     "Pamba nga teliika bulungi n'ebikoola bya kyenvu kiyinza okuba ettaka lirina obutabi obutasaana. (1) Gezaako ettaka lyo mu ofiisi y'ebyobulimi okumanya ebiriisa ebikosede. (2) Tega ifumbire ya NPK (20:10:10) — 50g ku muti. (3) Tola embuto za NARO ezirina obusobozi obulungi: 'NTA 88-6', 'BAR 7/80', 'BPA 75'. (4) Wonnonza ettaka — tosimba pamba mu ttaka lyona. (5) Fuka omusulo (mulch) okukuumira amazzi. (6) Kola okulonda ebirime (pruning) okuleeta omukka omulungi. [Kontakta Ofiisi y'ebyobulimi wangelowooze.]",
     "NARO Cotton Production Guide; MAAIF Cotton Advisory", "cultural practice"),

    ("India", "Tamil", "cotton",
     "என் பருத்தி (cotton) செடிகளில் பச்சை புழுக்கள் (green bollworms) உள்ளன. என்ன செய்வது?",
     "பச்சை புழுக்கள் பருத்தியின் முக்கிய பூச்சி (Helicoverpa armigera). (1) பாதிக்கப்பட்ட காய்களை பறித்து எரித்து விடுங்கள். (2) வேப்ப எண்ணெய் (neem oil 5ml/லிட்டர்) தெளியுங்கள். (3) மஞ்சள் பொறிகள் (yellow sticky traps) வைத்து பூச்சிகளை கவர்ந்து பிடியுங்கள். (4) பயிர் சுழற்சி செய்யுங்கள் — மக்காச்சோளம், பீன்ஸ் ஆகியவற்றுடன் மாற்றிப் பயிரிடுங்கள். (5) 'Bt cotton' வகைகளை பயிரிடுங்கள் — இவை புழு எதிர்ப்புத் திறனுடையவை. (6) அதிகமான பாதிப்பு இருந்தால், வேளாண்மை அதிகாரியை அணுகி உரிய பூச்சிக்கொல்லியை பயன்படுத்துங்கள்.",
     "TNAU Cotton Bollworm Guide; ICAR Cotton IPM", "pest management"),

    ("Kenya", "Luo", "coffee",
     "Niti onego timo gi bura (pruning) mag yien kahawa? Nyalo konyo ang'o?",
     "Bura mag yien kahawa (coffee pruning) en gima ber ahinya. (1) Buro konyo yien kahawa mondo gigol nyak mathoth. (2) Golo yien motwo, ma tuo, kata motwo e wi yien. (3) We yien matin 3-4 magi gin gi teko e wi yien. (4) Tim buro e kinde mag dwi (bang' keyo) — ka piny ok ng'ich. (5) Konyre gi nyiso ni yie yudo yamo e iye. (6) Yien ma oser buro maber gikelo nyak 20-30% moloyo ma ok oburo. Dhi ir ofisa mar kilimo mondo onyisi kaka iburo maber.",
     "KALRO Coffee Pruning Guide; UCDA Coffee Agronomy", "cultural practice"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) ላይ ቡናማ ነጠብጣብ አለ። በሽታ ነው?",
     "በጤፌ ላይ ቡናማ ነጠብጣብ የራስጦኒያ ጭቃ (Rust) በሽታ ነው። (1) የታመሙ ተክሎችን አውጥተህ አቃጥላቸው። (2) በሽታን የሚቋቋሙ ዝርያዎችን ተጠቀም: 'Quncho', 'DZ-Cr-37', 'DZ-01-354'። (3) ዘሩን ከመዝራት በፊት በሙቅ ውሃ (52°C) ለ10 ደቂቃ አከም። (4) ሰብል አዙር — በተመሳሳይ ማሳ ጤፌ እና ስንዴ ተለዋጭ አትዝራ። (5) የነም (neem) ዘይት ተጠቀም (5ml በ1 ሊትር ውሃ)። (6) ለተጨማሪ እርዳታ ወደ ግብርና ቢሮ ሂድ።",
     "EIAR Teff Rust Guide; MoA Teff Disease Advisory", "disease diagnosis"),

    ("Ethiopia", "Amharic", "teff",
     "ጤፌ (teff) እያደገ በደንብ አይደለም። ምን ማድረግ አለብኝ?",
     "ጤፌ በደንብ ካላደገ ብዙ ምክንያቶች አሉት። (1) ዘሩ በሽታን የሚቋቋም ይሁን — 'Quncho' ወይም 'DZ-Cr-37' ይምረጡ። (2) አፈሩን ይላኩ — ምን ንጥረ-ነገር እንደጎደለ ይወቁ። (3) NPK ማዳበሪያ (100 ኪሎ በሄክታር) ይጠቀሙ። (4) ዘሩን በቆራጥ (broadcasting) ይዝሩ — 25 ኪሎ በሄክታር። (5) አረም ይንከባከቡ — ጤፌ ከአረም ጋር ይቸገራል። (6) ወቅቱን ይምረጡ — የክረምት መጀመሪያ ላይ ይዝሩ። የግብርና ባለሙያውን ያነጋግሩ።",
     "EIAR Teff Production Guide; MoA Teff Agronomy", "cultural practice"),

    ("Nigeria", "Yoruba", "sunflower",
     "Odidẹ (sunflower) mi ko so eso daradara. Kini iṣoro?",
     "Odidẹ ti ko so eso daradara nitori pollination kiko. (1) Fi awọn apata oyin (beehives) nitosi oko — oyin n ran lọwọ pollination. (2) Ma lo insecticide nigbati odidẹ ba n ta — eyi n pa awọn kòkòrò ọ̀rẹ́. (3) Odidẹ nilo omi pupọ nigbati o ba n ta eso. (4) Lo NPK ajile (10:20:10). (5) Gbin ni akoko ti o tọ — Kínní sí Márí. (6) Kan si oṣiṣẹ iṣẹ-ogbin fun imọran diẹ sii.",
     "NAERLS Sunflower Guide; ICRISAT Pollination Advisory", "general inquiry"),

    ("Nigeria", "Hausa", "beans",
     "Wake na suna da tsutsotsi a ciki. Yadda za a ajiye su?",
     "Tsutsotsi a cikin wake (weevils) matsala ce ta ajiya. (1) Bushe wake da rana sosai kafin a adana. (2) Gama da mai na neem (neem oil 5ml/lita). (3) Ajiye a cikin kwandon da iska ba ta shiga (airtight container). (4) Saka wake a injin daskarewa (freezer) na kwanaki 7 — tsutsotsi za su mutu. (5) Tsabtace wurin ajiya sosai. (6) Tuntuɓi jami'in noma don samun iri masu jurewa tsutsotsi.",
     "NAERLS Bean Storage Guide; CIAT Post-Harvest Advisory", "pest management"),

    ("India", "Punjabi", "cotton",
     "ਕਪਾਹ (cotton) ਦੀਆਂ ਫਲੀਆਂ ਵਿੱਚ ਸੁੰਡੀ (bollworm) ਲੱਗ ਗਈ ਹੈ। ਇਲਾਜ?",
     "ਫਲੀ ਸੁੰਡੀ (bollworm) ਕਪਾਹ ਦਾ ਵੱਡਾ ਕੀੜਾ ਹੈ। (1) ਪ੍ਰਭਾਵਿਤ ਫਲੀਆਂ ਨੂੰ ਤੋੜ ਕੇ ਸਾੜ ਦਿਓ। (2) ਨੀਮ ਦਾ ਤੇਲ (neem oil 5ml/ਲੀਟਰ) ਛਿੜਕੋ। (3)ਪੀਲੇ ਚਿਪਚਿਪੇ ਜਾਲ (yellow sticky traps) ਲਗਾਓ। (4) ਫਸਲੀ ਚੱਕਰ — ਕਪਾਹ ਤੋਂ ਬਾਅਦ ਮੱਕੀ, ਬੀਨਜ਼ ਬੀਜੋ। (5) BT ਕਪਾਹ ਦੀਆਂ ਕਿਸਮਾਂ ਬੀਜੋ। (6) ਜੇ ਸੁੰਡੀ ਜ਼ਿਆਦਾ ਹੈ, ਕਿਸਾਨ ਸਲਾਹ ਕੇਂਦਰ (Agriculture Officer) ਤੋਂ ਸਲਾਹ ਲਓ।",
     "Punjab Agriculture Cotton Bollworm Guide; ICAR Cotton IPM", "pest management"),

    # ═══════════════ EXTRA GAPS (5 entries) ═══════════════
    ("Rwanda", "Kinyarwanda", "maize",
     "Nshaka kumenya uko ntegura imbuto z'ibigori mbere yo gutera. Ni gute?",
     "Gutegura imbuto z'ibigori ni ingenzi. (1) Hitamo imbuto ziva mu nzego z'ubuhinzi — aho zigenzuwe neza. (2) Mbere yo gutera, shyiramo imbuto mu mazi y'ubushyuhe (52°C) ku minota 10 — bigabanya indwara. (3) Tega ifumbire ya DAP (1 tablespoon) mu murongo mbere yo gutera. (4) Tera imbuto mu bujinja bwa 3—5 cm. (5) Haga umwanya hagati y'imirongo: cm 75, hagati y'ibiti: cm 30. (6) Tera mu gihe cy'imvura — igori rikenera amazi mu gukura.",
     "RAB Maize Planting Guide; CIMMYT Maize Agronomy", "cultural practice"),

    ("Uganda", "Luganda", "coffee",
     "Nnyinyonyola enkola y'okulonda ebirime (pruning) mu mwanyi?",
     "Okulonda ebirime mu mwanyi kikola omusaruro omulungi. (1) Ggya ebikoola ebikaddiye, ebiriko endwadde n'ebya kikazi. (2) Tega emikolo 3—4 emirongoofu ku muti ogwakusiba. (3) Ggya omuti ogwayitirira (suckers) — mwanyi guba n'omuti ogutali mu bbanga. (4) Kola okulonda mu biseera eby'enkuba enkalu — mwanyi guyagala okutemwa nga watono. (5) Tega omuti okuva waggulu: 50—60 cm okuva waggulu. (6) Enkola ennungi ey'okulonda ebirime yongera omusaruro ku 20—30%. KONTKTA UCDA oba ofiisi y'ebyobulimi.",
     "UCDA Coffee Pruning Guide; NARO Coffee Agronomy", "cultural practice"),

    ("Tanzania", "Swahili", "groundnut",
     "Karanga zangu zina majani ya njano. Nini sababu?",
     "Majani ya njano kwenye karanga yanaweza kuwa na sababu mbalimbali. (1) Ukosefu wa chuma (iron) — karanga hupenda udongo wenye pH 6.0—6.5. (2) Maji mengi — karanga haipendi maji kusimama; hakikisha mifereji mizuri. (3) Ugonjwa wa rosette virus — katika hali hii, ondoa mimea yote iliyoathirika na uichome. (4) Panda aina zinazostahimili: 'Serenut 4T', 'Serenut 5'. (5) Chukua sampuli ya udongo kwa ofisa wa kilimo. (6) Zungusha mazao — usipande karanga mara kwa mara kwenye shamba moja.",
     "TARI Groundnut Guide; ICRISAT Groundnut Nutrition", "disease diagnosis"),

    ("Nigeria", "Kanuri", "groundnut",
     "Ganyam dala tsa yaye kambu yaye am kare so. Nya karfu?",
     "Tsa yaye kambu yaye mabe ganyam ji yaye groundnut rosette virus. (1) Kare ganyam mabe kambu yaye am nyi baade. (2) Ku ganyam raadu — mfa ganyam tando laaro. (3) Kare ganyam 'Serenut 4T', 'Yarkwa', oba 'Nyirahindurwa'. (4) Nyi aphids baade — wɔna ndu virus yaye re. (5) Kare fungicide (copper-based) wɔ ADP she karo. (6) Ku dala neem oil (5ml/lita) re aphids karo.",
     "ADP Groundnut Rosette Control; ICRISAT Rosette Management", "disease diagnosis"),

    ("Kenya", "Kikuyu", "maize",
     "Mbeca ciakwa iri na rangi tunyu na itigakura wega. Ni ugwati atia?",
     "Rangi tunyu na kugira gutikure wega ni ugwati wa nitrogen deficiency. (1) Tega mbolea ya CAN kana DAP (kijiko kimwe harĩ muti). (2) Tuma thithi ya tiri (soil sample) KALRO — makaamenya kĩrĩa gĩathaawe. (3) Tega matira (mulch) — nĩgũteithia kũmenyera ũnyũũ. (4) Handa mbeca iria irĩ na ugwati wa gũtigana: 'H614', 'H6213'. (5) Tiga ũhanda mbeca handu hamwe mwaka na mwaka — gũcagania mĩgunda nĩ kwega. (6) Tega ifumbire ya compost — nĩgũteithia tiri. Uria ofisa wa ugwati (extension officer).",
     "KALRO Maize Nitrogen Guide; CIMMYT Soil Fertility", "disease diagnosis"),
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
print(f"Generated {len(new_entries)} new entries")
errors = []
for i, e in enumerate(new_entries):
    try:
        assert e["id"].startswith("agri-"), f"Bad ID: {e['id']}"
        assert len(e["question"]) > 10, f"Question too short at idx {i}: {len(e['question'])}"
        assert len(e["question"]) < 600, f"Question too long at idx {i}: {len(e['question'])}"
        assert len(e["answer"]) > 50, f"Answer too short at idx {i}: {len(e['answer'])}"
        assert len(e["answer"]) < 2500, f"Answer too long at idx {i}: {len(e['answer'])}"
        assert len(e["source"]) > 10, f"Source too short at idx {i}"
    except AssertionError as ex:
        errors.append(str(ex))

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for err in errors[:10]:
        print(f"  - {err}")
else:
    print("Validation: PASS (all entries OK)")

# ── Stats ───────────────────────────────────────────────────────────
from collections import Counter
regions = Counter(e["region"] for e in new_entries)
dialects = Counter(e["dialect"] for e in new_entries)
crops = Counter(e["crop"] for e in new_entries)
print(f"\nRegions: {dict(regions)}")
print(f"Dialects: {dict(dialects)}")
print(f"Crops: {dict(crops.most_common())}")

# ── Merge ───────────────────────────────────────────────────────────
merged = existing + new_entries
with open(DATASET_PATH, "w") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

old_total = len(existing)
new_total = len(merged)
print(f"\nMerged: {old_total} → {new_total} entries (+{new_total - old_total})")
print(f"Saved to {DATASET_PATH}")

# ── Post-merge stats ────────────────────────────────────────────────
r2 = Counter(e["region"] for e in merged)
d2 = Counter(e["dialect"] for e in merged)
c2 = Counter(e["crop"] for e in merged)
print(f"\n=== POST-MERGE ===")
for r, n in r2.most_common():
    print(f"  {r:15s}: {n:4d}")
print(f"  {'TOTAL':15s}: {len(merged):4d}")
print(f"\nPost-merge dialects:")
for d, n in d2.most_common():
    print(f"  {d:20s}: {n:4d}")
print(f"\nCrops:")
for c, n in c2.most_common():
    print(f"  {c:20s}: {n:4d}")
