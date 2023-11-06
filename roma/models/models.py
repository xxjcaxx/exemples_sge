# -*- coding: utf-8 -*-
import builtins

import bs4.builder
from odoo import models, fields, api
import math
from odoo.exceptions import ValidationError
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

noms_romans = ["Abronius", "Abudius", "Aburius", "Accius", "Accoleius", "Acerronius", "Acilius", "Aconius", "Actorius", "Acutius", "Adginnius", "Aebutius", "Aedinius", "Aelius", "Aemilius", "Aerelius", "Afinius", "Afranius", "Agnanius", "Agorius", "Albanius", "Albatius", "Albinius", "Albius", "Albinovanus", "Albucius", "Alburius", "Alfenus", "Alfius", "Allectius", "Allienus", "Amafinius", "Amatius", "Amblasius", "Ambrosius", "Ampius", "Amplas", "Ampudius", "Amusanus", "Ancharius", "Anicius", "Anisinus", "Anisius", "Annaeus", "Anneius", "Annius", "Anquirinnius", "Antistius", "Antius", "Antonius", "Apisius", "Aponius", "Appianius", "Appius", "Appuleius", "Apronius", "Apustius", "Aquillius", "Aquinius", "Arellius", "Arennius", "Arminius", "Arpineius", "Arrecinus", "Arrius", "Arruntius", "Arsinius", "Articuleius", "Artorius", "Arvenius", "Asconius", "Asellius", "Asinius", "Asvillius", "Ateius", "Aternius", "Ateronius", "Atius", "Atilius", "Atinius", "Atrius", "Attius", "Atzicius", "Auconius", "Auctorius", "Audasius", "Aufeius", "Aufidius", "Aulius", "Aurelius", "Aurius", "Aurunculeius", "Ausonius", "Autrodius", "Autronius", "Avianus", "Avidius", "Avienus", "Avilius", "Avius", "Axius", "Babrius", "Baebius", "Balonius", "Balventius", "Bantius", "Barbatius", "Barrius", "Barsius", "Bavius", "Bellicius", "Bellienus", "Bellius", "Betilienus", "Betitius", "Betucius", "Betuus", "Bicleius", "Blandius", "Blandonius", "Blossius", "Boionius", "Bruttius", "Bucculeius", "Burbuleius", "Burrienus", "Butronius", "Caecilius", "Caecina", "Caecius", "Caedicius", "Caelius", "Caeparius", "Caepasius", "Caerellius", "Caesellius", "Caesennius", "Caesetius", "Caesius", "Caesonius", "Caesulenus", "Caetronius", "Calavius", "Calesterna", "Calidius", "Calpurnius", "Calumeius", "Calvenus", "Calventius", "Calvisius", "Camaronius", "Campatius", "Canidius", "Caninius", "Canius", "Cantilius", "Cantius", "Canuleius", "Canutius", "Capienus", "Carfulenus", "Carisius", "Caristanius", "Caristicus", "Carius", "Carpinatius", "Carrinas", "Carsicius", "Carteius", "Carvilius", "Casperius", "Cassius", "Castricius", "Castrinius", "Catabronius", "Catienus", "Catilius", "Catius", "Cavinnius", "Ceionius", "Centenius", "Ceppuleius", "Cerenius", "Cervilius", "Cervonius", "Cestius", "Cicereius", "Cilnius", "Cincius", "Cispius", "Classidius", "Claudius", "Cloelius", "Cluentius", "Clutorius", "Cluvius", "Cocceius", "Coelius", "Cominius", "Communius", "Concessius", "Condetius", "Consentius", "Considius", "Consius", "Coponius", "Cordius", "Corfidius", "Cornelius", "Cornificius", "Coruncanius", "Cosconius", "Cossinius", "Cossutius", "Cotius", "Cottius", "Crassicius", "Crastinus", "Cremutius", "Crepereius", "Critonius", "Cupiennius", "Curiatius", "Curius", "Curtilius", "Curtius", "Cusinius", "Cuspius", "Decidius", "Decimius", "Decitius", "Decius", "Decumenus", "Dellius", "Dercullius", "Desticius", "Dexius", "Didius", "Digitius", "Dillius", "Distubuanus", "Domitius", "Dubius", "Duccius", "Duilius", "Duratenus", "Durmius", "Duronius", "Ebetius", "Eggius", "Egilius", "Egnatius", "Egnatuleius", "Egrilius", "Elvius", "Ennius", "Epidius", "Eppius", "Equitius", "Eranius", "Erucius", "Evasius", "Fabius", "Fabricius", "Fadenus", "Fadius", "Faenius", "Falcidius", "Falerius", "Faminius", "Fannius", "Farsuleius", "Faucius", "Favonius", "Festinius", "Fidiculanius", "Firmius", "Flaminius", "Flanus", "Flavinius", "Flavius", "Flavoleius", "Flavonius", "Floridius", "Florius", "Floronius", "Fonteius", "Foslius", "Fufetius", "Fuficius", "Fufidius", "Fufius", "Fulcinius", "Fulginas", "Fulvius", "Fundanius", "Furius", "Furnius", "Gabinius", "Gagilius", "Galerius", "Gallius", "Gargonius", "Gavius", "Geganius", "Gellius", "Geminius", "Genucius", "Gessius", "Glicius", "Granius", "Gratidius", "Gratius", "Haterius", "Hedusius", "Heius", "Helvidius", "Helvius", "Herennius", "Herennuleius", "Herminius", "Hirrius", "Hirtius", "Hirtuleius", "Hisseius", "Horatius", "Hordeonius", "Hortensius", "Hosidius", "Hostilius", "Hostius", "Humidius", "Iallius", "Iasidius", "Iccius", "Icilius", "Ignius", "Ingenius", "Insteius", "Istacidius", "Iteius", "Iturius", "Janius", "Javolenus", "Jucundius", "Julius", "Juncius", "Junius", "Justinius", "Juventius", "Laberius", "Labienus", "Lacerius", "Laecanius", "Laelius", "Laenius", "Laetilius", "Laetorius", "Lafrenius", "Lamponius", "Laronius", "Lartius", "Latinius", "Lavinius", "Lemonius", "Lentidius", "Lepanius", "Lepidius", "Levissatius", "Libellius", "Libertius", "Liburnius", "Licinius", "Ligarius", "Limisius", "Litrius", "Livinius", "Livius", "Lollius", "Longinius", "Loreius", "Lucceius", "Lucienus", "Lucilius", "Lucius", "Lucretius", "Lurius", "Luscidius", "Luscius", "Lusius", "Lutatius", "Maccius", "Maccienus", "Macrinius", "Macrobius", "Maecenas", "Maecilius", "Maecius", "Maelius", "Maenas", "Maenius", "Maevius", "Magius", "Mallius", "Mamercius", "Mamilius", "Manilius", "Manlius", "Mannaius", "Marcius", "Marius", "Martinius", "Matienus", "Matinius", "Matius", "Matrinius", "Mattavius", "Matuius", "Maximius", "Memmius", "Menenius", "Menius", "Mercatorius", "Mescinius", "Messienus", "Messius", "Mestrius", "Metilius", "Metonius", "Mettius", "Milonius", "Mimesius", "Minatius", "Minicius", "Minidius", "Minius", "Minucius", "Moderatius", "Modius", "Mucimeius", "Mucius", "Multillius", "Mummius", "Munatius", "Munius", "Murrius", "Mussidius", "Mustius", "Mutilius", "Mutius", "Naevius", "Nasennius", "Nasidienus", "Nasidius", "Nautius", "Neratius", "Nercius", "Nerfinius", "Nerius", "Nessinius", "Nesulna", "Nigidius", "Nimmius", "Ninnius", "Nipius", "Nonius", "Norbanus", "Novellius", "Novercinius", "Novius", "Numerius", "Numicius", "Numisius", "Numitorius", "Nummius", "Numoleius", "Numonius", "Nunnuleius", "Nymphidius", "Obellius", "Obultronius", "Occius", "Oclatinius", "Oclatius", "Ocratius", "Octavenus", "Octavius", "Ofanius", "Ofatulenus", "Ofilius", "Ogulnius", "Ollius", "Opellius", "Opetreius", "Opimius", "Opisius", "Opiternius", "Oppidius", "Oppius", "Opsidius", "Opsilius", "Opsius", "Oranius", "Orbicius", "Orbilius", "Orbius", "Orchius", "Orcivius", "Orfidius", "Orfius", "Orosius", "Oscius", "Ostorius", "Otacilius", "Ovidius", "Ovinius", "Paccius", "Paciaecus", "Pacidius", "Pacilius", "Paconius", "Pactumeius", "Pacuvius", "Paldius", "Palfurius", "Palpellius", "Pantuleius", "Papinius", "Papirius", "Papius", "Pascellius", "Pasidienus", "Pasidius", "Passienus", "Patulcius", "Pedanius", "Pedius", "Peducaeus", "Peltrasius", "Percennius", "Perperna", "Persius", "Pescennius", "Petillius", "Petreius", "Petronius", "Petrosidius", "Pidius", "Pilius", "Pinarius", "Pinnius", "Pisentius", "Pitisedius", "Placidius", "Plaetorius", "Plaguleius", "Plancius", "Plarius", "Plautius", "Pleminius", "Plinius", "Ploticius", "Pluticius", "Poetelius", "Pollius", "Pompeius", "Pompilius", "Pomponius", "Pomptinus", "Pompuledius", "Pontidius", "Pontificius", "Pontilienus", "Pontilius", "Pontius", "Popaedius", "Popidius", "Poppaeus", "Porcius", "Porsina", "Postumius", "Postumulenus", "Potitius", "Praecilius", "Praeconius", "Prastinius", "Precius", "Priscius", "Procilius", "Proculeius", "Propertius", "Publicius", "Puccasius", "Publilius", "Pupius", "Pusonius", "Quartinius", "Quartius", "Queresius", "Quinctilius", "Quinctius", "Quinquaius", "Quirinius", "Rabirius", "Rabonius", "Rabuleius", "Racectius", "Racilius", "Raecius", "Ragonius", "Rammius", "Ranius", "Rasinius", "Reconius", "Reginius", "Remmius", "Rennius", "Resius", "Ricinius", "Romanius", "Romilius", "Roscius", "Rubellius", "Rubrenus", "Rubrius", "Rufinius", "Rufius", "Rufrius", "Rullius", "Rupilius", "Rusonius", "Rusticelius", "Rustius", "Rutilius", "Sabellius", "Sabidius", "Sabinius", "Sabucius", "Saenius", "Saevonius", "Safinius", "Sagarius", "Salienus", "Sallustius", "Salonius", "Saltius", "Saltorius", "Salvidienus", "Salvidius", "Salvius", "Salvienus", "Samacius", "Samientus", "Sammius", "Sanquinius", "Sariolenus", "Sarius", "Sarrenius", "Satellius", "Satrienus", "Satrius", "Sattius", "Saturius", "Saturninius", "Saufeius", "Scaevilius", "Scaevinius", "Scaevius", "Scalacius", "Scandilius", "Scantinius", "Scantius", "Scaptius", "Scatidius", "Scetanus", "Scoedius", "Scribonius", "Scuilius", "Scutarius", "Seccius", "Secundinius", "Secundius", "Sedatius", "Segulius", "Seius", "Selicius", "Sellius", "Sempronius", "Sennius", "Sentius", "Seppienus", "Seppius", "Septicius", "Septimius", "Septimuleius", "Septueius", "Sepullius", "Sepunius", "Sergius", "Serius", "Sertorius", "Servaeus", "Servenius", "Servilius", "Servius", "Sestius", "Severius", "Sextilius", "Sextius", "Sibidienus", "Sicinius", "Silicius", "Silius", "Silvius", "Simplicius", "Simplicinius", "Sinicius", "Sinnius", "Sinuleius", "Sisenna", "Sittius", "Socellius", "Sollius", "Sornatius", "Sosius", "Sotidius", "Spedioleius", "Spedius", "Spellius", "Splattius", "Spurilius", "Spurinna", "Spurius", "Staberius", "Staius", "Stallius", "Statilius", "Statinius", "Statioleius", "Statius", "Statorius", "Statrius", "Steius", "Stellius", "Stenius", "Stertinius", "Stlabillenus", "Stlaccius", "Stlammius", "Stlarius", "Strabonius", "Subrius", "Successius", "Suedius", "Suellius", "Suetonius", "Suettius", "Suilius", "or", "Suillius", "Sulpicius", "Summianius", "Surdinius", "Tadius", "Talepius", "Talius", "Tampius", "Tanicius", "Tannonius", "Tanusius", "Tapsenna", "Tariolenus", "Taronius", "Tarpeius", "Tarquinius", "Tarquitius", "Tarrutenius", "Tarutius", "Tatius", "Tattius", "Taurius", "Tebanus", "Tecusenus", "Tedisenus", "Teditius", "Tedius", "Teiustius", "Terefrius", "Terrasidius", "Terentilius", "Terentius", "Tertinius", "Tertius", "Tesitanus", "Tetricius", "Tetrinius", "Tettidius", "Tettienus", "Tettius", "Thoranius", "Thorius", "Tiburtius", "Ticinius", "Tifernius", "Tigellius", "Tigidius", "Tilioficiosus", "Tillius", "Tineius", "Titanius", "Titedius", "Titinius", "Titioleius", "Titius", "Tittidienus", "Tittienus", "Tittius", "Titucius", "Tituculenus", "Titulenus", "Titurius", "Titurnius", "Togonius", "Traius", "Tranquillius", "Traulus", "Trausius", "Travinius", "Travius", "Trebanius", "Trebatius", "Trebellienus", "Trebellius", "Trebicius", "Trebius", "Trebulanus", "Trebonius", "Tremellius", "Triarius", "Triccius", "Trisimpedius", "Tritius", "Truttedius", "Tuccius", "Tudicius", "Tullius", "Turallasius", "Turciacus", "Turcilius", "Turbonius", "Turcius", "Turionius", "Turius", "Turpilius", "Turranius", "Turselius", "Tursidius", "Turullius", "Tuscenius", "Tuscilius", "Tussanius", "Tussidius", "Tuticanus", "Tuticius", "Tutilius", "Tutinius", "Tutius", "Tutorius", "Ulentinius", "Ulpius", "Umberius", "Umbilius", "Umbirius", "Umboleius", "Umbonius", "Umbrenus", "Umbricius", "Umbrius", "Umbrilius", "Umerius", "Ummidius", "Urbanius", "Urbicius", "Urbinius", "Urgulanius", "Ursius", "Urseius", "Urvinius", "Ussinus", "Utilius", "Valerius", "Varenus", "Varinius", "Varisidius", "Varius", "Vatinius", "Vecilius", "Vedius", "Vedodius", "Vegetius", "Velanius", "Velius", "Velleius", "Vemnasius", "Ventidius", "Venuleius", "Vequasius", "Veranius", "Verbisius", "Verecundius", "Vergilius", "Verginius", "Verres", "Verrius", "Vesiculanus", "Vesnius", "Vesonius", "Vespasius", "Vestius", "Vestorius", "Vestricius", "Vestrius", "Vetilius", "Vettius", "Veturius", "Vibenius", "Vibidius", "Vibius", "Vibulliacus", "Vibullius", "Vicirius", "Victorinius", "Victorius", "Victricius", "Viducius", "Vigilius", "Villius", "Vinicius", "Vinius", "Vipsanius", "Vipstanus", "Viridius", "Virius", "Visellius", "Vistilius", "Vitellius", "Vitedius", "Vitrasius", "Vitruvius", "Vivanius", "Voconius", "Volcacius", "Volnius", "Volscius", "Volturcius", "Volumnius", "Volusenna", "Volusenus", "Volusius", "Vorenius", "Vulius", "Vulpius"]
cognoms_romans = ["Abercius", "Abito", "Absens", "Abundantius", "Abundius", "Abundus", "Aburianus", "Acacius", "Acaunus", "Acceptus", "Achaica", "Achaicus", "Acidinus", "Aciliana", "Acilianus", "Aculeo", "Acutianus", "Acutus", "Adauctus", "Adelphius", "Adiutor", "Adranos", "Adventus", "Aeacus", "Aebutus", "Aedesius", "Aelianus", "Aemiliana", "Aequa", "Aequitas", "Aemilianus", "Aeserninus", "Aeternitas", "Aetius", "Afer", "Afra", "Africana", "Africanus", "Afrinus", "Agaptus", "Agatopus", "Agelastus", "Agilis", "Agorix", "Agricola", "Agrippa", "Agrippianus", "Agrippina", "Agrippinillus", "Agrippinus", "Ahala", "Ahenobarbus", "Albanianus", "Albanus", "Albillus", "Albina", "Albinianus", "Albinius", "Albinus", "Albucillus", "Albucius", "Albus", "Alcimus", "Alethius", "Alienus", "Allectus", "Aluredes", "Alypius", "Amabilis", "Amandianus", "Amandinus", "Amandus", "Amans", "Amantillus", "Amantius", "Amarantus", "Amator", "Amatus", "Ambrosius", "(d", "Fabia)", "Amor", "Amphion", "Ampliatus", "Anatolius", "Andronicus", "Angelus", "Annaeanus", "Annianus", "Animaequitas", "Anniolus", "Antias", "Antius", "Antiquus", "Antistianus", "Antonianus", "Antonillus", "Antoninus", "Anulinus", "Anullinus", "Apelles", "Apelliana", "Apellinus", "Aper", "Apollinaris", "Apollonarius", "Apollonius", "Appianillus", "Appianus", "Appuleianus", "Aprilis", "Aprillus", "Aprinus", "Apronianus", "Apronillus", "Aprulla", "Apuleianus", "Aquila", "Aquilianus", "Aquilinus", "Aquillianus", "Arator", "Aratus", "Arcadius", "Arcanus", "Arcavius", "Archarius", "Arius", "Armiger", "Arminus", "Arnobius", "Arpagius", "Arrianus", "Arruntianus", "Arruntius", "Artorianus", "Arulenus", "Arvina", "Asellio", "Asellus", "Asiaticus", "Asina", "Asinianus", "Asper", "Asprenas", "Asprenus", "Assanius", "Atianus", "Atilianus", "Atratinus", "Atta", "Attianus", "Attianillus", "Atticianus", "Atticillus", "Atticinus", "Atticus", "Attilianus", "Auctillus",  "Auctoritas","Auctus", "Audaios", "Audax", "Audens", "Aufidianus", "Augendus", "Augur", "Augurinus", "Augurius", "Augustalis", "Augustanus", "Augustinus", "Augustus", "Aurelianus", "Aurelius", "Aureolus", "Aurunculeianus", "Auruncus", "Ausonius", "Auspex", "Auspicatus", "Auxentius", "Auxientius", "Auxiliaris", "Auxilius", "Avienus", "Aviola", "Avitianus", "Avitillus", "Avitus", "Baebianus", "Balbillus", "Balbinus", "Balbus", "Bambalio", "Bamballio", "Banquerius", "Barba", "Barbarus", "Barbatus", "Barbillus", "Barbula", "Baro", "Bassianus", "Bassinus", "Bassus", "Bato", "Belenus", "Belisarius", "Beatus", "Bellator", "Bellicianus", "Bellicus", "Bellus", "Benedictus", "Benignus", "Bestia", "Betto", "Bibaculus", "Bibulus", "Bitucus", "Blaesillus", "Blaesus", "Blandinus", "Blandus", "Blasius", "Blossianus", "Bodenius", "Boethius", "Boetius", "Bolanus", "Bonifatius", "Bonosus", "Bonus", "Bradua", "Briccius", "Bricius", "Briktius", "Britannicus", "Britius", "Brixius", "Brocchillus", "Brocchus", "Bromidus", "Bruccius", "Brucetus", "Bruscius", "Bruttianus", "Brutus", "Bubo", "Bubulcus", "Buca", "Buccio", "Bulbus", "Bulla", "Burcanius", "Burrus", "Caecilianus", "Caecina", "Caecinianus", "Caedicianus", "Caelianus", "(d", "Verginia)", "Caelinus", "Caecus", "Caelestinus", "Caelestius", "Caelianus", "Caelinus", "Caelistis", "Caepio", "Caerellius", "Caesar", "Caesennianus", "Caesianus", "Caesonianus", "Caesoninus", "Caianillus", "Caianus", "Calacicus", "Calamus", "Calaritanus", "Calatinus", "Calavianus", "Caldus", "Calenus", "Calerus", "Caletus", "Calidianus", "Callidianus", "Callisunus", "Calogerus", "Calpurnianus", "Calpurnis", "Calvinus", "Calvisianus", "Calvus", "Camerinus", "Camerius", "Camillus", "Campanianus", "Campanus", "Campester", "Candidianus", "Candidillus", "Candidinus", "Candidus", "Canianus", "Canidianus", "Canina", "Caninianus", "Cantaber", "Capella", "Capito", "Capitolinus", "Capra", "Caprarius", "Capreorus", "Caracturus", "Carantus", "Carbo", "Carinus", "Carius", "Carnifex", "Carus", "Carvilianus", "Casca", "Cassianillus", "Cassianus", "Castinus", "Castorius", "Castus", "Catianus", "Catilina", "Cato", "Catonius", "Cattianus", "Catuarus", "Catullinus", "Catullus", "Catulus", "Catus", "Caudex", "Caudinus", "Celatus", "Celer", "Celerianus", "Celerinus", "Celsillus", "Celsinillus", "Celsinus", "Celsus", "Cenaeus", "Cencius", "Censor", "Censorinillus", "Censorinus", "Censorius", "Centumalus", "Cerialis", "Cerinthus", "Certinus", "Certus", "Cerularius", "Cervianus", "Cervidus", "Cethegus", "Chlorus", "Christianus", "Cicada", "Cicatricula", "Cicero", "Cico", "Cicurinus", "Cicurius", "Cimber", "Cincinnatus", "Cinna", "Cinnianus", "Cita", "Cittinus", "Civilis", "Clarentius", "Clarianus", "Clarus", "Classicianus", "Classicus", "Claudianus", "Claudillus", "Claudus", "Clemens", "Clementianus", "Clementillus", "Clementinus", "Clodianus", "Clodus", "Cocceianus", "Cocles", "Coelianus", "Coelinus", "Cogitatus", "Colias", "Collatinus", "Colonus", "Columbanus", "Columella", "Coma", "Comes", "Comitianus", "Comitinus", "Commidius", "Commidus", "Commius", "Commodus", "Concessianus", "Concessus", "Congrio", "Constans", "Constantillus", "Constantinus", "Constantius", "Coranus", "Corbulo", "Corculum", "Cordillus", "Cordus", "Coriolanus", "Cornelianus", "Cornicen", "Cornix", "Cornutus", "Corvinus", "Corvus", "Cosmas", "Cossus", "Cotentinus", "Cotta", "Crassillus", "Crassus", "Cremutius", "Crescens", "Crescentianus", "Crescentillus", "Crescentina", "Crescentinus", "Crescentius", "Creticus", "Crispianus", "Crispinianus", "Crispinillus", "Crispinus", "Crispus", "Crito", "Crotilo", "Crus", "Cucuphas", "Culleolus", "Cullio", "Cumanus", "Cunctator", "Cunobarrus", "Cupitianus", "Cupitus", "Curianus", "Curio", "Cursor", "Curtianus", "Curvus", "Cyprianus", "Dacianus", "Dacicus", "Dacius", "Dalmaticus", "Dalmatius", "Dama", "Damascius", "Damasippus", "Damasus", "Damianus", "Dannicus", "Dardanius", "Dardanus", "Dativus", "Datus", "Decembris", "Decianus", "Deciminus", "Decimus", "Decmitius", "Decor", "Decoratus", "Densus", "Dentatus", "Denter", "Dento", "Desideratus", "Desiderius", "Dexion", "Dexippus", "Dexter", "Dextrianus", "Diadematus", "Dianilla", "Didianus", "Didicus", "Didymus", "Dido", "Dignillus", "Dignissimus", "Dignitas", "Dignus", "Diligens", "Dio", "Diocletianus", "Dioscourides", "Disertus", "Dives", "Docilis", "Docilinus", "Docilus", "Dolabella", "Dolens", "Dominicus", "Domitianus", "Domitillus", "Donatianus", "Donatillus", "Donatus", "Donicus", "Dorotheus", "Dorso", "Dorsuo", "Dotalis", "Draco",  "Drusilla""known", "attested?", "Drusus", "Dubitatius", "Duilianus", "Dulcis", "Dulcitius", "Durio", "Durus", "Eborius", "Eburnus", "Ecdicius", "Eclectus", "Efficax", "Egbuttius", "Egnatianus", "Egnatillus", "Elegans", "Elerius", "Eliphas", "Elpidius", "Elvorix", "Emeritus", "Encratis", "Ennecus", "Ennodius", "Eonus", "Eparchius", "Epidianus", "Epimachus", "Epiphanius", "Epolonius", "Erasinus", "Esdras", "Esquilinus", "Equinus", "Etruscillus", "Etruscus", "Eucherius", "Eudomius", "Eudoxius", "Eugenius", "Eugenus", "Eulogius", "Eumenius", "Eunapius", "Euphemius", "Eurysaces", "Eustachius", "Eustacius", "Eustathius", "Eustochius", "Eutherius", "Evodius", "Excingus", "Exoratus", "Exoriens", "Exsupereus", "Extricatus", "Exuperans", "Exuperantius", "Exuperatus", "Exupereus", "Faber", "Fabianus", "Fabiolus", "Fabricianus", "Fabullianus", "Fabullus", "Facilis", "Facundinus", "Facundus", "Fadus", "Fagus", "Falco", "Falconillus", "Falx", "Fama", "Familiaris", "Fastidius", "Farus", "Fatalis", "Faustillus", "Faustinianus", "Faustinus", "Faustus", "Faventinus", "Favonianus", "Favor", "Favorinus", "Felicianus", "Felicissimus", "Felicitas", "Felicius", "Felissimus", "Felix", "Ferentinus", "Ferox", "Ferreolus", "Festianus", "Festivus", "Festus", "Fidelis", "Fidenas", "Fides", "Fidus", "Figulus", "Fimbria", "Fimus", "Firmianus", "Firmillus", "Firminianus", "Firminillus", "Firminus", "Firmus", "Flaccianus", "Flaccillus", "Flaccinator", "Flaccinus", "Flaccus", "Flamen", "Flaminianus", "Flaminillus", "Flamininus", "Flamma", "Flavianillus", "Flavianus", "Flavillus", "Flavinus", "Flavus", "Florens", "Florentianus", "Florentillus", "Florentinus", "Florentius", "Florianus", "Floridus", "Florillus", "Florinus", "Florus", "Flos", "Fonteianus", "Fontinalis", "Forianus", "Formica", "Fortio", "Fortis", "Fortunatianus", "Fortunatus", "Fraucus", "Frequens", "Frequentianus", "Frequentillus", "Frequentinus", "Frigidianus", "Frontalis", "Frontillus", "Frontinianus", "Frontinus", "Fronto", "Frontonianus", "Frontonillus", "Fructuosus", "Fructus", "Frugi", "Frugius", "Frumentius", "Fufianus", "Fulgentius", "Fullo", "Fullofaudes", "Fulvianillus", "Fulvianus", "Fulvillus", "Fulvus", "Fundanus", "Furianus", "Fuscianillus", "Fuscianus", "Fuscillus", "Fuscinillus", "Fuscinus", "Fuscus", "Gabinianus", "Gabinillus", "Gabinus", "Gaetulicus", "Gaianillus", "Gaianus", "Gala", "Galarius", "Galba", "Galenus", "Galerus", "Gallicanus", "Gallicus", "Gallienus", "Gallio", "Gallus", "Galvisius", "Garilianus", "Garrulus", "Gaudens", "Gaudentianus", "Gaudentius", "Gavianus", "Gavros", "Gelasius", "Gellianus", "Gemellianus", "Gemellinus", "Gemellus", "Geminianus", "Geminus", "Generidus", "Genesius", "Genialis", "Gennadius", "Gentilis", "Germanicus", "Germanus", "Jovinianus", "Geta", "Getha", "Glabrio", "Globulus", "Gluvias", "Glycia", "Gordianus", "Gordio", "Gorgonius", "Gracchanus", "Gracchus", "Gracilis", "Graecinus", "Granianus", "Granillus", "Gratianus", "Gratidianus", "Gratillus", "Gratinianus", "Gratinus", "Gratus", "Grattianus", "Gregorius", "Grumio", "Gryllus", "Grypus", "Gualterus", "Gurges", "Gutta", "Habitus", "Hadrianus", "Hardalio", "Hasta", "Helvianus", "Hemina", "Herculanus", "Herculius", "Herennianus", "Herennius", "Herenus", "Herma", "Hermias", "Hermina", "Hesychius", "Hiberus", "Hibrida", "Hilarianus", "Hilarillus", "Hilarinus", "Hilario", "Hilaris", "Hilarius", "Hilarus", "Hipparchus", "Hirpinius", "Hirrus", "Homullus", "Honoratianus", "Honoratus", "Honorinus", "Horatianus", "Horatius", "Hortensianus", "Hortensis", "Hortensus", "Hostilianus", "Humilus", "Iacomus", "Ianuarius", "Iavolenus", "Imbrex", "Imperiosus", "Impetratus", "Indaletius", "Indus", "Ingeniosus", "Ingenuillis", "Ingenuus", "Ingenvinus", "Innocens", "Inregillensis", "Iocundus", "Iovianus", "Iovinianus", "Iovinus", "Iovius", "Irenaeus", "Isatis", "Isauricus", "Isaurus", "Isidorus", "Ismarus", "Italicus", "Iuba", "Iucundianus", "Iucundillus", "Iucundinus", "Iucundus", "Iulianus", "Iulillus", "Iuliolus", "Iulius", "Iulus", "Iuncinus", "Iuncus", "Iunianus", "Iunillus", "Iunior", "Iustianus", "Iustillus", "Iustinianus", "Iustinus", "Iustus", "Iuvenalis", "Iuvenis", "Iuventianus", "Iuventinus", "Labienus", "Labeo", "Laberianus", "Lactantius", "Lactuca", "Lacticinus", "Laeca", "Laelianus", "Laenas", "Laetillus", "Laetinianus", "Laetus", "Laevillus", "Laevinus", "Laevus", "Lamia", "Lanatus", "Larcianus", "Lartianus", "Largus", "Lateranus", "Latinus", "Latro", "Laurentinus", "Laurentius", "Laurinus", "Laurus", "Leddicus", "Lentullus", "Lentulus", "Leo", "Leontius", "Lepidianus", "Lepidillus", "Lepidinus", "Lepidus", "Lepontus", "Leporinus", "Lepos", "Libanius", "Liberalis", "Liberius", "Libo", "Licinianus", "Licinus", "Ligur", "Ligus", "Ligustinus", "Limetanus", "Linus", "Litorius", "Littera", "Litumaris", "Livianus", "Livigenus", "Livillus", "Lollianus", "Longillus", "Longinianus", "Longinillus", "Longinus", "Longus", "Lovernianus", "Lovernius", "Lucanus", "Lucianus", "Lucidus", "Lucifer", "Lucilianus", "Lucillianus", "Lucillus", "Lucinus", "Luciolus", "Lucretianus", "Luctacus", "Lucullus", "Lunaris", "Luonercus", "Lupercillus", "Lupercus", "Lupicinus", "Lupinus", "Lupulus", "Lupus", "Lurco", "Lurio", "Luscinus", "Luscus", "Lusianus", "Lustricus", "Lutatianus", "Maccalus", "Macer", "Macerinus", "Macrinianus", "Macrinillus", "Macrinus", "Macro", "Macrobius", "Mactator", "Maecenus", "Maecianus", "Magnentius", "Magnianus", "Magnillus", "Magnus", "Magunnus", "Maior", "Maius", "Malchus", "Malleolus", "Mallianus", "Mallus", "Maltinus", "Maluginensis", "Mamercinus", "Mamercus", "Mamertinus", "Mamilianus", "Mamma", "Mammula", "Mancinus", "Manilianus", "Manlianus", "Mansuetus", "Marcallas", "Marcellianus", "Marcellinus", "Marcellus", "Marcialis", "Marcianus", "Margarita", "Marianillus", "Marianus", "Marinianus", "Marinus", "Maritialis", "Maritimus", "Marius", "Maro", "Marsallas", "Marsicus", "Marsus", "Marsyas", "Martialis", "Martianus", "Martinianus", "Martinus", "Martius", "Martyrius", "Marullinus", "Marullus", "Masavo", "Masculus", "Materninus", "Maternus", "Matho", "Maturinus", "Maturus", "Mauricius", "Maurinus", "Mauritius", "Maurus", "Maxentius", "Maximianus", "Maximillianus", "Maximillus", "Maximinus", "Maximus", "Medullinus", "Megellus", "Meletius", "Melissus", "Melito", "Melitus", "Mellitus", "Melus", "Meminianus", "Memmianus", "Memor", "Mento", "Mercator", "Mercurialis", "Mercurinus", "Merenda", "Merula", "Messala", "Messalinus", "Messianus", "Messor", "Metellinus", "Metellus", "Metilianus", "Metunus", "Micianus", "Mico", "Milo", "Milonius", "Minervalis", "Minervinus", "Minianus", "Minicianus", "Minucianus", "Moderatillus", "Moderatus", "Modestinus", "Modestus", "Modianus", "Molacus", "Momus", "Montanillus", "Montanus", "Mordanticus", "Mucianus", "Mugillanus", "Munatianus", "Muncius", "Murena", "Mus", "Musa", "Musca", "Musicus", "Nabor", "Naevianus", "Naevolus", "Narcissus", "Narses", "Nasica", "Naso", "Natalianus", "Natalinus", "Natalis", "Natalius", "Natta", "Nepos", "Nepotianus", "Naucratius", "Nazarius", "Nectaridus", "Nelius", "Nemesianus", "Nemnogenus", "Neneus", "Nennius", "Nepos", "Nepotillus", "Neptunalis", "Nero", "Nertomarus", "Nerva", "Nicasius", "Nicetius", "Nigellus", "Niger", "Nigidianus", "Nigrianus", "Nigrinus", "Ninnianus", "Niraemius", "Nobilior", "Noctua", "Nolus", "Nonianus", "Norbanianus", "Noricus", "Noster", "Novanus", "Novation", "Novellianus", "Novellus", "Novianus", "Numerianus", "Nummus", "Obsequens", "Oceanus", "Ocella", "Octavillus", "Octobrianus", "Oculatus", "Ofella", "Olennius", "Olympicus", "Opilio", "Opimianus", "Opis", "Oppianicus", "Oppianus", "Optatillus", "Optatus", "Ordius", "Orestes", "Orestillus", "Orientalis", "Orientius", "Orissus", "Orontius", "Ostorianus", "Otacilianus", "Otho", "Pacatianus", "Pacatus", "Pachomius", "Pacilus", "Pacuvianus", "Paenula", "Paetillus", "Paetinus", "Paetus", "Palicanus", "Palma", "Pammachius", "Pamphilius", "Panaetius", "Pansa", "Pantensus", "Pantera", "Panthera", "Papianus", "Papinianus", "Papirianus", "Papus", "Paratus", "Pardus", "Parmensis", "Parnesius", "Pastor", "Paterculus", "Paternianus", "Paternus", "Patiens", "Patricius", "Paulinus", "Paullinus", "Paullus/Paulus", "Pavo", "Pelagius", "Pennus", "Pera", "Peregrinus", "Perennis", "Perpetuus", "Persicus", "Pertacus", "Pertinax", "Pervincianus", "Pervincus", "Petasius", "Peticus", "Petilianus", "Petillianus", "Petro", "Petronax", "Petronianus", "Petronillus", "Petronius", "Petrus", "Philippus", "Philo", "Philus", "Photius", "(d", "Herennia)", "Pictor", "Pilatus", "Pilus", "Pinarianus", "Pinnus", "Piso", "Pitio", "Pius", "Placidianus", "Placidinus", "Placidus", "Plancianus", "Plancinus", "Plancus", "Planta", "Plautianus", "Plautillus", "Plautinus", "Plautis", "Plautus", "Pleminianus", "Plinianus", "Plotianus", "Plotillus", "Plotinus", "Plotus", "Pollianus", "Pollienus", "Pollio", "Pollus/Polus", "Polybius", "Pompeianus", "Pompilianus", "Pompolussa", "Pomponianus", "Pomponillus", "Pontianus", "Ponticillus", "Ponticus", "Poplicola", "Porcellus", "Porcianus", "Porcina", "Porcus", "Porphyrius", "Posca", "Postumianus", "Postuminus", "Postumus", "Potens", "Potentinus", "Potestas", "Potitianus", "Potitus", "Praenestinus", "Praesens", "Praetextatus", "Praetextus", "Prilidianus", "Primanus", "Primianus", "Primillus", "Primulus", "Primus", "Priscianus", "Priscillianus", "Priscillus", "Priscinus", "Priscus", "Privatus", "Privernas", "Probatus", "Probianus", "Probillus", "Probinus", "Probus", "Processus", "Proceus", "Proclus", "Proculianus", "Proculinus", "Proculus", "Procus", "Procyon", "Promptus", "Prontinus", "Profuturus", "Propertius", "Propinquus", "Prosperus", "Protacius", "Proteus", "Protus", "Provincialis", "Proximillus", "Proximus", "Prudens", "Prudentillus", "Publianus", "Publicianus", "Publicola", "Publicus", "Publilianus", "Pudens", "Pudentianus", "Pudentillus", "Pudentius", "Pulcher", "Pulcherius", "Pulex", "Pullus", "Pulvillus", "Pupianus", "Pupus", "Purpureo", "Pusinnus", "Pusio", "Quadratillus", "Quadratus", "Quartillus", "Quartinus", "Quarto", "Quartus", "Quietus", "Quintianus", "Quintilianus", "Quintillanius", "Quintillus", "Quintinus", "Quintus", "Quiricus", "Quirinalis", "Rabirianus", "Raeticus", "Ramio", "Ravilla", "Rebilus", "Reburrinus", "Reburrus", "Receptus", "Rectus", "Regillensis", "Regillianus", "Regillus", "Reginus", "Regulianus", "Regulus", "Remigius", "Remus", "Renatus", "Repentinus", "Respectillus", "Respectus", "Restitutus", "Rex", "Rhesus", "Ripanus", "Robustus", "Rogatianus", "Rogatillus", "Rogatus", "Rogelius", "Romanillus", "Romanus", "Romulianus", "Romulus", "Roscianus", "Rufianus", "Rufillus", "Rufinianus", "Rufinillus", "Rufinus", "Rufrianus", "Rufus", "Ruga", "Rullianus", "Rullus", "Ruricius", "Rusca", "Ruso", "Russus", "Rusticus", "Rutilianus", "Sabaco", "Sabellius", "Sabinianus", "Sabinillus", "Sabinus", "Saccus", "Sacerdos", "Saenus", "Salinator", "Sallustianus", "Salonianus", "Saloninus", "Salvianus", "Salvillus", "Salvinus", "Sanctinus", "Sanctus", "Sandilianus", "Sanga", "Sarimarcus", "Saserna", "Satullus", "Saturnalis", "Saturninus", "Saunio", "Saverrio", "Saxo", "Scaeva", "Scaevola", "Scapula", "Scaro", "Scarpus", "Scato", "Scaurus", "Schlerus", "Scipio", "Scribonianus", "Scrofa", "Sebastianus", "Secundianus", "Secundillus", "Secundinus", "Secundus", "Securus", "Sedatus", "Sedulus", "Segestes", "Seianus", "Sempronianus", "Senator", "Seneca", "Senecianus", "Senecio", "Senilianus", "Senilis", "Senna", "Senopianus", "Septimianus", "Septimillus", "Septimus", "Serapion", "Serenus", "Sergianus", "Sergillus", "Seronatus", "Serranus", "Sertorianus", "Servanus", "Servatius", "Servilianus", "Sestianus", "Sestinus", "Severlinus", "Severianus", "Severillus", "Severinus", "Severus", "Seuso", "Sextianus", "Sextilianus", "Sextillianus", "Sextillus", "Sextinus", "Sextus", "Siculus", "Sidonius", "Sigilis", "Silanus", "Silianus", "Silo", "Silus", "Silvanus", "Silvester", "Silvianus", "Silvillus", "Silvinus", "Silvia", "Silvius", "Similis", "Simo", "Simplex", "Simplicianus", "Simplicius", "Siricius", "Siricus", "Sisenna", "Sisinnius", "Sita", "Solinus", "Sollemnis", "Solon", "Solus", "Sophus", "Soranus", "Sorex", "Sorio", "Sospes", "Sotericus", "Sparsus", "Spartacus", "Spectatillus", "Spectatus", "Spendius", "Speratus", "Spinther", "Spurinna", "Squillus", "Statius", "Stellio", "Stilo", "Stichus", "Stolo", "Strabo", "Structus", "Suavis", "Subulo", "Suburanus", "Successianus", "Successus", "Sudrenus", "Sulca", "Sulinus", "Sulla", "Sulpicianus", "Super", "Superbus", "Superianus", "Superstes", "Superus", "Sura", "Surdus", "Surinus", "Surius", "Surus", "Symmachus", "Symphorianus", "Synistor", "Synnodus", "Tacitianus", "Tacitus", "Taenaris", "Tancinus", "Tanicus", "Tantalus", "Tarcisius", "Tarquinianus", "Tatianus", "Taurillus", "Taurinus", "Taurus", "Tegula", "Telesinus", "Tenax", "Terentianus", "Terentillus", "Tertianus", "Tertinus", "Tertiolus", "Tertius", "Tertullianus", "Tertullus", "Tetricus", "Tettianus", "Thrasea", "Thurinus", "Tiberianus", "Tiberillus", "Tiberinus", "Tibullus", "Tiburs", "Tigris", "Tiro", "Titianus", "Titillus", "Titinianus", "Titiolus", "Torquatus", "Toxotius", "Traianus", "Trailus", "Tranio", "Tranquillinus", "Tranquillus", "Trebellianus", "Trebonianus", "Tremerus", "Tremorinus", "Tremulus", "Trenico", "Triarius", "Tricipitinus", "Trifer", "Trigeminus", "Trimalchio", "Trinus", "Trio", "Trogus", "Trypho", "Tubero", "Tubertus", "Tubulus", "Tuccianus", "Tuditanus", "Tullianus", "Turbo", "Turibius", "Turpilianus", "Turpilinus", "Turrinus", "Tuscillus", "Tuscus", "Tuticanus", "Ulpianus", "Ulpiolus", "Umbrianus", "Umbrinus", "Ummidianus", "Urbanillus", "Urbanus", "Urbicus", "Urgulanianus", "Urgulanillus", "Ursianus", "Ursinianus", "Ursillus", "Ursinus", "Ursulus", "Ursus", "Vala", "Valens", "Valentianus", "Valentillus", "Valentinian", "Valentinus", "Valerianus", "Valerillus", "(d", "Quinctia)", "Varialus", "Varianus", "Varro", "Varus", "Vatia", "Vaticanus", "Vatinianus", "Vedrix", "Velikov", "Vegetus", "Vejento", "Velocianus", "Velox", "Venantianus", "Venantius", "Venator", "Venter", "Venustinus", "Venustus", "Verax", "Verecundus", "Vergilianus", "Verginianus", "Verinus", "Verissimus", "Veritas", "Verna", "Verres", "Verrucosus", "Verullus", "Verus", "Vespa", "Vespasianus", "Vespillo", "Vestinus", "Vetranio", "Vettianus", "Vettillus", "Vettonianus", "Veturianus", "Vetus", "Viator", "Vibennis", "Vibianus", "Vibidianus", "Vibillus", "Vibulanus", "Vicanus", "Victor", "Victorianus", "Victoricus", "Victorinus", "Victorius", "Victricius", "Vigilantius", "Vincentius", "Vindex", "Vindicianus", "Vinicianus", "Vipsanianus", "Virgilianus", "Virgula", "Virginianus", "Viridio", "Virilis", "Viscellinus", "Vitalianus", "Vitalinus", "Vitalis", "Vitellianus", "Vitulus", "Vitus", "Vivianus", "Vocula", "Volumnianus", "Volusianus", "Volusus", "Vopiscus", "Voluptas", "Zeno", "Zenodotus", "Zethos", "Zosimus"]

def name_generator():
    random.shuffle(noms_romans)
    random.shuffle(cognoms_romans)
    return noms_romans[0]+" "+cognoms_romans[0]

class player(models.Model):
     _name = 'roma.player'
     _description = 'Players of Roma Aeterna Game'

     name = fields.Char(required=True)
     avatar = fields.Image(max_width=200, max_height=200)
     citicens = fields.One2many('roma.citicen','player')

     def generate_citicen(self):
         for p in self:
             templates = self.env['roma.template'].search([]).ids
             random.shuffle(templates)
             cities = self.env['roma.city'].search([]).ids
             random.shuffle(cities)
             citicen = p.citicens.create({
                 "name": name_generator(),
                 "avatar": self.env['roma.template'].browse(templates[0]).image_small,
                 "player": p.id,
                 "hierarchy": "1",
                 "city": cities[0]
             })


class city(models.Model):
    _name = 'roma.city'
    _description = 'Cities'

    name = fields.Char(required=True)
    level = fields.Selection([('1','Villa'),('2','Oppidum'),('3','Urbs')], required=True, default='1')
    forum_level = fields.Integer()
    # Desbloca la capacitat de tindre magisters, consul o dictador
    thermae_level = fields.Integer()
    theater_level = fields.Integer()
    circus_level = fields.Integer()
    temple_level = fields.Integer()
    # Els deus ajuden a la lealtat i en la resta de coses

    health = fields.Float()
    loyalty = fields.Float()
    gods = fields.Integer()

    metal = fields.Float(default=1000)
    gold = fields.Float(default=100)
    food = fields.Float(default=10000)

    buildings = fields.One2many('roma.building','city')
    citicens = fields.One2many('roma.citicen','city')
    units = fields.One2many('roma.unit','city')

    def generate_unit(self):
        for c in self:
            if len(c.buildings.filtered(lambda b: b.soldiers_production > 0)) > 0:
                time_to_train = 80/sum(c.buildings.mapped('soldiers_production'))
                self.env['roma.unit'].create({
                    "name" : "Generated Saeculum",
                    "city" : c.id,
                    "type": "1",
                    "legionaries" : 60,
                    "equites" : 20,
                    "training" : 0,
                    "time_to_train": time_to_train
                })

    @api.constrains('gods')
    def _check_gods(self):
        for c in self:
            if c.gods > c.temple_level:
                raise ValidationError("You cannot have more than %s gods" % c.temple_level)
            if c.gods < 0:
                raise ValidationError("You cannot have less than 0 gods")

    def update_resources(self):
        for c in self.search([]):
            metal = c.metal
            gold = c.gold
            food = c.food
            for b in c.buildings:
                metal += b.metal_production
                gold += b.gold_production
                food += b.food_production
            c.write({"metal": metal,"gold": gold,"food": food})


class citicen(models.Model):
    _name = 'roma.citicen'
    _description = 'Important Citicen'

    name = fields.Char(required=True)
    avatar = fields.Image(max_width=200, max_height=200)
    player = fields.Many2one('roma.player', required=True)
    hierarchy = fields.Selection([('1','Equites'),('2','Patricius'),('3','Magister'),('4','Potestas'),('5','Consul'),('6','Dictator')],required=True)
    # Sols pot haver un cónsul o un Dictador. Sols hi ha dictador en situació de guerra. Sols hi ha un potestas, que tria als magister
    # A partir de magister pots tindre legios
    # A partir de potestas pots controlar el senat
    # A partir de consul pots tindre dictador i més d'una legio
    # Tindre dictador millora molt el rendiment en batalles però es perd en lealtat, salut i producció
    city = fields.Many2one('roma.city',required=True)

    @api.constrains('hierarchy')
    def _check_hierarchy(self):
        for c in self:
           print('a')

class building_type(models.Model):
    _name = 'roma.building_type'
    _description = 'Type of buildings'

    name = fields.Char()
    food_production = fields.Float()
    soldiers_production = fields.Float()
    gold_production = fields.Float()
    metal_production = fields.Float()
    icon = fields.Image(max_width=200, max_height=200)

class building(models.Model):
    _name = 'roma.building'
    _description = 'Buildings of the cities'

    name = fields.Char(compute='_get_name')
    type = fields.Many2one('roma.building_type',required=True)
    city = fields.Many2one('roma.city',required=True)
    level = fields.Integer(default=1)
    food_production = fields.Float(compute='_get_productions')
    soldiers_production = fields.Float(compute='_get_productions')
    gold_production = fields.Float(compute='_get_productions')
    metal_production = fields.Float(compute='_get_productions')
    icon = fields.Image(related='type.icon')
    @api.depends('type','level')
    def _get_productions(self):
        for b in self:
            b.food_production = b.type.food_production+ b.type.food_production * math.log(b.level)
            b.soldiers_production =  b.type.soldiers_production+b.type.soldiers_production * math.log(b.level)
            b.gold_production =  b.type.gold_production+b.type.gold_production * math.log(b.level)
            b.metal_production = b.type.metal_production+b.type.metal_production * math.log(b.level)

    @api.depends('type','city')
    def _get_name(self):
        for b in self:
            b.name = 'undefined'
            if b.type and b.city:
                b.name = b.type.name +" "+ b.city.name +" "+ str(b.id)


class unit(models.Model):
    _name = 'roma.unit'
    _description = 'Group of soldiers'

    name = fields.Char()
    city = fields.Many2one('roma.city')
    type = fields.Selection([('1','Saeculum'),('2','Cohortis'),('3','Legio')])
    #  1 Centuria 80 soldats
    # 2 Cohortis 6 centuries
    # 3 Legio 10 cohortes
    legionaries = fields.Integer()
    equites = fields.Integer()
    parent_unit = fields.Many2one('roma.unit')
    units = fields.One2many('roma.unit','parent_unit')
    training = fields.Float(default=1)
    time_to_train = fields.Float(default=0)
    total_soldiers = fields.Integer(compute='_get_total_soldiers')

    @api.depends('legionaries','equites','units')
    def _get_total_soldiers(self):
        print(self)
        for unit in self:
            total = unit.legionaries + unit.equites
            for subunit in unit.units:
                total = total + subunit.total_soldiers
            unit.total_soldiers = total
    def update_train(self):
        for u in self.search([('time_to_train','>',0)]):
            u.time_to_train = u.time_to_train - 1
            if u.time_to_train <= 0:
                u.training += 1



class template(models.Model):
    _name = 'roma.template'
    _description = 'Template Images'

    name = fields.Char()
    type = fields.Char()
    image = fields.Image(max_width=400, max_height=400)
    image_small = fields.Image(related="image", string="ismall", max_width=200, max_height=200)
    image_thumb = fields.Image(related="image", string="ithumb", max_width=100, max_height=100)


class battle(models.Model):
    _name = 'roma.battle'
    _description = 'Battles'

    name = fields.Char()
    start = fields.Datetime(default = lambda self: fields.Datetime.now())
    end = fields.Datetime(compute = '_get_data_end')
    total_time = fields.Integer(compute = '_get_date_end')
    remaining_time = fields.Char(compute = '_get_date_end')
    progress = fields.Float(compute='_get_date_end')
    city1 = fields.Many2one('roma.city', domain="[('id','!=',city2)]")
    city2 = fields.Many2one('roma.city', domain="[('id','!=',city1)]")
    units1 = fields.Many2many('roma.unit', domain="[('city','=',city1),('training','>',0)]")


    def update_battles(self):
        for b in self.search([]):
            if fields.Datetime.now() > b.end:
                print(b.name)


    @api.depends('start')
    def _get_data_end(self):
        for b in self:
            date_start = fields.Datetime.from_string(b.start)
            date_end = date_start + timedelta(hours = 2)
            b.end = fields.Datetime.to_string(date_end)
            b.total_time = (date_end - date_start).total_seconds()/60
            remaining = relativedelta(date_end,datetime.now())
            b.remaining_time = str(remaining.hours)+":"+str(remaining.minutes)+":"+str(remaining.seconds)
            passed_time = (datetime.now()-date_start).total_seconds()
            b.progress = (passed_time*100)/(b.total_time*60)
            if b.progress > 100:
                b.progress = 100
                b.remaining_time = '00:00:00'


    @api.constrains('city1','city2')
    def _check_cities(self):
        for b in self:
            if b.city1.id == b.city2.id:
                raise ValidationError("One city can attack itself")

    @api.constrains('city1', 'units1')
    def _check_units(self):
        for b in self:
            for u in b.units1:
                if u.city.id != b.city1.id:
                    raise ValidationError("All units have to be from city 1")
                if u.training < 1:
                    raise ValidationError("All units have to be trained")