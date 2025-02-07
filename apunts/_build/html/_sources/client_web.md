**Pàgina principal: [Odoo](Odoo "wikilink")**

En la secció de la vista i de l\'herència en la vista hem pogut
modificar la forma en que [Odoo](Odoo "wikilink") mostra o gestiona la
base de dades amb el client web. La gestió de la vista es limita a crear
trees, forms, kanbans\... Els creadors d\'Odoo recomanen utilitzar
aquestes vistes sempre que es puga. No obstant, de vegades volem fer
alguna cosa més personalitzada. Si volem personalitzar a baix nivell
l\'aparença i funcionament del client web, deguem entendre bé cóm
funciona.

Les pàgines web més simples són estàtiques. Però en el moment que
necessitem accedir a una base de dades, necessitem un llenguatge de
programació de servidor que obtinga les dades i les envie al navegador
web. Fins a Odoo 6, el backend creava html complet i l\'enviava al
client. Després van entendre que això sobrecarrega al servidor amb
aspectes més relacionats amb la vista.

El Odoo actual carrega un client complet a la web, que es comunica amb
missatges breus i concrets amb el servidor. Missatges en JSON que sols
tenen dades o ordres a executar. Cada vegada que refresquem el navegador
web, està enviant-se un programa de client complet, però quan entrem a
un menú, sols s\'envia un missatge JSON demanant unes dades i es rep un
altre amb una llista de les dades a mostrar pel client. Opcionalment,
s\'envía el xml de la vista, el qual serà interpretat pel client per
mostrar correctament les dades.

-   Si volem veure tot el que el servidor rep o envia al client, podem
    arrancar el servici amb l\'opció \--log-level=debug_rpc.

El client web és una **SPA (Single Page Application)**, a l\'estil
d\'altres frameworks coneguts com Angular, va creant i destruint
elements de la interfície contínuament. Aquests elements són, entre
altre coses, Widgets.

Si volem saber modificar a baix nivell el client web, necessitem saber
prou de Javascript, de JQuery, BootStrap i altres, amés de HTML5.

En Odoo, es proporcionen tres clients web diferenciats, però que,
internament, funcionen amb el mateix framework. Aquest són el **web
client** que és el backend on es treballa en les dades, el **website**
que és la pàgina web pública i el **point of sale**, que és per al punts
de venda.

Quan ens referim a crear mòduls per al client, generalment ens referim a
fer canvis subtils en l\'apariència o comportament de la web.
Reflexionem sobre el tipus de modificació que necessitem:

-   Un canvi menor en l\'apariència: Afegir algunes regles CSS.
-   Un canvi estétic o de comportament de la manera en que es visualitza
    un field: Afegir HTML, CSS i Javascript a un **Widget**.
-   Un canvi en la manera en la que un field enmagatzema o recupera les
    dades: Modificació del Javascript del Widget i de la part del model
    o el controlador Javascript de la vista.
-   Un canvi en la manera de mostrar un recordset sencer: Crear una
    vista.
-   Fer una web des de 0 amb les dades d\'Odoo: Utilitzar els [Web
    controllers](https://www.odoo.com/documentation/12.0/reference/http.html#reference-http-controllers)

# Arquitectura del client web {#arquitectura_del_client_web}

![Arquitectura MVC](Mvc_client.png "Arquitectura MVC"){width="312"} El
**WebClient** d\'Odoo es construeix amb mòduls, de la mateixa manera que
els mòduls per al \'servidor\'. Sols que en els mòduls per ampliar el
client web es modifiquen altres arxius més que els típics dels models de
python o els xml de la vista.

L\'arquitectura és **MVC** internament. És a dir, Odoo té un model (ORM
sobre PostgresSQL), un controlador (Mètodes de Python) i una vista (El
client Web definit en el servidor amb XML) i el propi client web també
té un model (Les peticions Ajax al servidor amb JSON i la interpretació
d\'aquestes), un controlador (Funcions Javascript per a gestionar
aquestes dades) i una vista (El renderitzat dels elements web al
navegador). Com que Javascript és un llenguatge que deixa fer de tot, no
tenim perquè respectar aquesta arquitectura, però els nostres mòduls han
de poder ser mantinguts i cal que aprofiten al màxim els recursos que el
client web ja ens proporciona, per tant, intentarem programar el menys
possible i aprofitar tot el que ja té el client.

Els mòduls principal del client web depenen del mòdul **web**, que
proporciona el nucli del client web. Els altres complementen a aquest.
Hi ha mòduls que específicament es diuen, per exemple, **web_kanban**,
que amplien la web. Però en realitat qualsevol mòdul ho pot fer. El
mòdul web conté tot el HTML i Javascript necessari per a que els altres
mòduls de la web funcionen.

Per modificar el client web cal proporcional HTML, xml, CSS, Javascript
i imatges. Això ha d\'estar en el directori **static** del mòdul:

-   static/src/js : the JavaScript files
-   static/src/css : the CSS files
-   static/src/xml : the HTML template files
-   static/img : pictures used in templates or CSS
-   static/libs : JS libraries needed by the module

El server no manipula aquesta informació, però la processa en certa
manera i l\'envia a client.

```{=mediawiki}
{{nota|Com que els CSS i JS no són processades pel servidor, no cal reiniciar el servidor per veure els canvis, sols refrescar el navegador. Això no sempre funciona, ja que el servidor pot ser que no processe els assets o que la cau del navegador no actualitze el JS o el XML.}}
```
# Enviant el client al navegador {#enviant_el_client_al_navegador}

Cada vegada que refresquem, s\'envia el client sencer. Això vol dir
molts CSS, moltes línies de Javascript de molt fitxers distints i molt
de HTML i XML. Per evitar saturar la xarxa, el servidor fa una
compressió de totes eixes dades de la següent manera:

-   Tots els CSS i Javascript són concatenats en un sol fitxer. La
    concatenació s\'ordena per dependències entre mòduls.
-   El Javascript és minimitzat llevant espais i refactoritzant les
    variables per noms més curts.
-   Una web HTML molt simple sols amb l\'enllaç als CSS i Javascript és
    enviada al client.
-   Tot es comprimeix en gzip pel server per reduir l\'enviament. El
    navegador és capaç de descomprimir.

Tot això fa difícil de fer debug amb el client. Per això es recomana
ficar **?debug=1** a la URL per demanar que no minimitze.

# Els [Assets](https://www.odoo.com/documentation/15.0/developer/reference/frontend/assets.html) {#els_assets}

El client d\'Odoo és molt complex i necessita tindre Javascript, HTML i
CSS de molts fitxers distints. Gestionar això permetent que qualsevol
puga fer un mòdul per afegir més implica una gestió d\'aquests enllaços
més automàtica. Per això han creat principalment tres **bundles** en XML
que no són més que una col·lecció de links a Javascript o CSS. Aquests
tenen l\'estructura d\'un Template QWeb i els més comuns són:

-   **web.assets_common**: amb les coses comuns.
-   **web.assets_backend**: Amb les coses específiques del Backend.
-   **web.assets_frontend**: Amb les coses de la web pública.

Si volem afegir fitxers a un asset en **odoo fins al 14**, sols cal
heretar el XML com fem en l\'[Herència en la
vista](Odoo#Her.C3.A8ncia_en_la_vista "wikilink"):

``` xml
<template id="assets_backend" name="helpdesk assets" inherit_id="web.assets_backend">
    <xpath expr="//script[last()]" position="after">
        <link rel="stylesheet" href="/helpdesk/static/src/less/helpdesk.less"/>
        <script type="text/javascript" src="/helpdesk/static/src/js/helpdesk_dashboard.js"></script>
    </xpath>
</template>
```

Observem que afegeix coses al Asset del Backend, concretament al final.
`{{nota|Aquesta és la manera general d'afegir funcionalitats o estils. Però tal vegada el nostre widget no necessita ser carregat sempre i estem afegint una càrrega constant a la xarxa. Per això pot ser interessant afegir la llibreria sols quan es crea el widget en temps d'execució. Odoo proporciona formes de carrega llibreries i CSS de forma dinàmica (lazyload en Qweb template engine). }}`{=mediawiki}

En cas de ser en **Odoo 15**, s\'ha d\'afegir al manifest:

``` python
'assets': {
    'web.assets_backend': [
        'web/static/src/xml/**/*',
    ],
    'web.assets_common': [
        'web/static/lib/bootstrap/**/*',
        'web/static/src/js/boot.js',
        'web/static/src/js/webclient.js',
    ],
    'web.qunit_suite_tests': [
        'web/static/src/js/webclient_tests.js',
    ],
},
```

## Afegir CSS al nostre mòdul {#afegir_css_al_nostre_mòdul}

Abans d\'entrar en la creació de Widgets, pot ser interessant observar
cóm els **bundles** es poden ampliar d\'una forma simple per modificar o
afegir CSS.

El primer és crear el css en
**/`<modul>`{=html}/static/src/css/`<modul>`{=html}.css**. En el nostre
cas, sols fem un per a fer la lletra mès menuda:

``` css
.reserves_tree { font-size:0.8em;}
```

Després creem un template per afegir el CSS al bundle
**assets_backend**:

``` xml
<template id="assets_backend" name="reserves assets" inherit_id="web.assets_backend">
    <xpath expr="//script[last()]" position="after">
        <link rel="stylesheet" href="/reserves/static/src/css/reserves.css"/>
    </xpath>
</template>
```

I per últim, sols cal utilitzar la classe css:

``` xml
<field name="bookings" limit="10" class="reserves_tree">
```

# Arquitectura dels mòduls en Javascript {#arquitectura_dels_mòduls_en_javascript}

De la mateixa manera que hem vist per introduir un CSS personalitzat en
Odoo, es pot introduir un Javascript. Aquest serà afegit al final del
bundle i serà executat pel navegador. No obstant, el Javascript no és
tan simple de desenvolupar. Odoo té molt de Javascript ja funcionant i
podem interferir. Però el major problema és que no sabem molt bé qué
s\'està executant en cada moment. Javascript és un llenguatge que
treballa molt de forma asíncrona. Això permet que es puga carregar part
de la web mentres una altra part ja està funcionant. Aquesta asincronia
fa que no es puga predir fàcilment en quin ordre es carregarà o
executarà tot. Totes les aplicacions web complexes tenen que solucionar
eixos problemes. Javascript té un ecosistema de biblioteques molt divers
i no tots treballen de la mateixa manera, de fet, molt han solventat
carències del llenguatge amb tècniques de programació i biblioteques.
Aques és el cas dels mòduls. Odoo gestiona la complexitat del seu
Javascript amb mòduls i dependències d\'altres mòduls. Per això no és
tan simple con afegir un parell d\'instruccions Jquery per modificar una
part del DOM, ja que no podem saber si està carregada o quan es
carregarà. Abans de fer partxes que solucionen mal els problemes, cal
estudiar cóm ho fa Odoo.

```{=mediawiki}
{{nota|Els mòduls simplifiquen la programació de les webs grans. Els mòduls oculten la complexitat de la programació de les distintes parts lògiques d’un programa. Els mòduls ofereixen una interfície en la que interactuen amb la resta de mòduls. Un programa modular és més fàcilment ampliable i reutilitzable.
En els mòduls cal aconseguir tindre la major independència al aconseguit el menor '''acoblament''' i la major '''cohesió'''. L’acoblament és la excessiva dependència d’un mòdul respecte a altres i la cohesió és la íntima relació entre els elements interns del mòdul. [https://developer.mozilla.org/es/docs/Web/JavaScript/Introducci%C3%B3n_a_JavaScript_orientado_a_objetos]}}
```
<https://www.odoo.com/documentation/15.0/developer/reference/frontend/framework_overview.html>

Odoo suporta tres maneres de fer codi Javascript:

-   Sense mòduls (No recomanable)
-   Amb mòduls natius ES6.
-   Amb el seu propi sistema de mòduls:

## Mòduls JS segons Odoo {#mòduls_js_segons_odoo}

Javascript fins a ES6 no tenia una manera definida de fer mòduls. Per
tant, cada programador utilitzaba un patró de disseny diferent. En Odoo
han optat per utilitzar una tècnica anomenada AMD (Asynchronous Module
Definition), de manera similar a com ho fa la biblioteca **require.js**.
Odoo utilitza una única variable global anomenada **odoo** que conté una
referència a cada funció de cada mòdul web. Per tant, per definir una
funció deguem observar aquest exemple:

``` javascript
// in file a.js
odoo.define('module.A', function (require) {  
    "use strict";
    var A = ...;
    return A;
});

// in file b.js
odoo.define('module.B', function (require) {
    "use strict";
    var A = require('module.A');
    var B = ...; // something that involves A
    return B;
});
```

```{=mediawiki}
{{nota|La tècnica d’utilitzar una funció com a mòdul és anomenada '''patró mòdul''' i aconsegueix que les variables definides dins de la funció es comporten com a variables '''privades''' i sols es puga accedir a les variables i mètodes '''públics''' definits en el '''return''' de la funció.}}
```
El mètode **odoo.define** accepta tres arguments:

-   **moduleName**: El nom del mòdul. Es recomana seguir la mateixa
    sintaxi que en els models de la programació en python.
-   **dependencies**: (opcional) Es tracta d\'una llista d\'strings amb
    els noms d\'altres mòduls dels que depen.
-   **function**: L\'últim argument és una funció que defineix el mòdul
    i que retorna la classe o un array de les classes definides. Aquesta
    funció accepta com a argument la funció **require**, que és
    l\'encarregada d\'obtindre altres objectes del **namespace** del
    Javascript.

Per tant, un mòdul de client web en Odoo és el resultat de la funció
define() de la classe global Odoo, la qual necessita el nom del mòdul,
dependències i una funció que retorne una variable o un diccionari de
variables. Aquestes variables són les classes que exporta el mòdul.

```{=mediawiki}
{{nota|Si es pot traure una analogía amb el backend python d'Odoo, el require() és com el '''self.env[]''' i permet delarar dependències sense necessitat de saber l'ordre en que carrega tot. }}
```
Hi ha una altra manera de cridar a la funció define i és ficant els
mòduls dels que depèn com a segon argument:

``` javascript
odoo.define('module.Something', ['module.A', 'module.B'], function (require) {
    "use strict";

    var A = require('module.A');
    var B = require('module.B');

    // some code
});
```

Si alguna cosa falla, el client pot donar aquests missatges d\'error:

-   Missing dependencies: These modules do not appear in the page. It is
    possible that the JavaScript file is not in the page or that the
    module name is wrong
-   Failed modules: A javascript error is detected
-   Rejected modules: The module returns a rejected Promise. It (and its
    dependent modules) is not loaded.
-   Rejected linked modules: Modules who depend on a rejected module
-   Non loaded modules: Modules who depend on a missing or a failed
    module

## Utilitzar mòduls natius ES6 en Odoo {#utilitzar_mòduls_natius_es6_en_odoo}

La documentació oficial recomana fer els nous mòduls d\'aquesta manera.
No obstant, Odoo els transformarà en el seu sistema de mòduls al fer el
bundle. Per això cal afegir un comentari en la primera línia:

``` javascript
/** @odoo-module **/
import { someFunction } from './file_b';

export function otherFunction(val) {
    return someFunction(val + 3);
}
```

Això té algunes limitacions en la sintaxi de les exportacions que està
[documentada en la documentació
oficial](https://www.odoo.com/documentation/15.0/developer/reference/frontend/javascript_modules.html#limitations).
Si hi ha alguna cosa realment complicada, recomanen continuar utilitzant
el mètode d\'Odoo que és el que, en realitat, és transpilat.

# OWL

Moltes pàgines web SPA com és Odoo estan fetes en un framework de
Javascript, ja que el manteniments dels components, els hooks, la
reactivitat o la comunicació amb el servidor són complicats i és
innecessari fer-ho sempre. Alguns dels frameworks són: Angular, Vue,
React\...

Odoo té el seu propi, i a partir de la versió 14 es diu OWL i es
desenvolupa per separat, sempre pensant en que siga la base dels nous
elements de la web en Odoo. En Odoo 14 el sistema antic i OWL poden
conviure, però s\'espera que OWL siga adoptat completament en el futur.
De fet en Odoo 15 diuen que el core de la web ja està totalment reescrit
en OWL, amés de la vista graph, per exemple. Per al 16 es preveu que
tots els fields i vistes adopten el nou framework.

```{=mediawiki}
{{nota| La primera pregunta que un desenvolupador web es fa al veure que Odoo està desenvolupant el seu framework és perquè no utilitzen Angular, Vue o React o qualsevol altre framework madur. Els desenvolupadors d'Odoo la responen en cada article: Necessiten que siga més lleugera, adaptada totalment a Odoo i no dependre d'altres. Semblen bons motius i si tenen raó o no es veurà en les pròximes versions. }}
```
OWL és un framework web menut (\<20KB) que té els elements d\'un
framework modern:

-   Un sistema declaratiu de components
-   Un sistema de reactivitat basat en Hooks.
-   Per defecte té un mode concurrent.
-   Un store per a l\'estat del programai
-   Un Router.
-   Un sistema de plantilles amb QWeb.
-   Al contrari que en versions anteriors, OWL aprofita la sintaxi ES6
    per a les classes.
-   Un virtual DOM amb renderització asíncrona.

En la [documentació oficial d\'OWL](https://github.com/odoo/owl) quasi
no menciona cóm integrar-lo en Odoo.

Abans de continuar cal preguntar-se què es vol aconseguir o què podem
aconseguir amb OWL:

-   Crear una web completa sense relació amb Odoo.
-   Crear una web completa que tinga com a backend Odoo (no té molta
    diferència de l\'anterior)
-   Fer una secció en la web o el backend d\'Odoo.
-   Fer una vista, un menú, un widget nou per a Odoo.

Aquest manual es centra sobretot en l\'última opció i anem a començar
per ella.

## Crear un component d\'Odoo en OWL {#crear_un_component_dodoo_en_owl}

Abans de començar, cal fer l\'estructura de directoris i fitxers i un
xml per afegir el nostre Javascript al bundle:

``` python
  'assets': {
    'web.assets_backend': [
        'provesowl/static/src/js/component.js',
        'provesowl/static/src/css/component.css',
    ],
```

En la ruta especificada farem el fitxer **components.js** i el css.

Els components en OWL estan basats en classes ES6 o en el seu sistema
modular. Com que sembla que recomanen el sistema de classes, anem a
fer-ho ja d\'aquesta manera en l\'exemple. En components.js afegim
aquest codi:

``` javascript
/** @odoo-module **/

const { useState } = owl.hooks;  // Object destructuring per treue el que necessitem
const { xml } = owl.tags;
const { Component } = owl;   // Com es veu, owl està disponible en l'espai de noms del bundle per a que es puga accedir fàcilment.


class MyComponent extends Component {
    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
    }
}

// La forma de cridar a la funció xml en tagged templates 
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates

MyComponent.template = xml`<button t-on-click="changeText">  
Click Me! [<t t-esc="state.value"/>]
</button>`;
```

## Modificar components en OWL {#modificar_components_en_owl}

<https://codingdodo.com/owl-in-odoo-14-extend-and-patch-existing-owl-components/>

## Crear nous Widgets en OWL {#crear_nous_widgets_en_owl}

## Crear noves vistes en OWL {#crear_noves_vistes_en_owl}

<https://codingdodo.com/odoo-javascript-101-classes-and-mvc-architecture/>
<https://codingdodo.com/odoo-15-javascript-reference/>

## Hooks en OWL {#hooks_en_owl}

<https://www.cybrosys.com/blog/hooks-in-odoo-owl-framework>

# Classes Javascript en Odoo {#classes_javascript_en_odoo}

En Javascript no hi ha una manera estàndard tampoc de crear classes,
però proporciona mecanismes per simular l\'efecte. Odoo utilitza la
tècnica de [John
Resig](https://johnresig.com/blog/simple-javascript-inheritance/).
Cridanta al mètode **extend()** d\'una classe.

``` javascript
var Class = require('web.Class');

var Animal = Class.extend({
    init: function () {
        this.x = 0;
        this.hunger = 0;
    },
    move: function () {
        this.x = this.x + 1;
        this.hunger = this.hunger + 1;
    },
    eat: function () {
        this.hunger = 0;
    },
});
```

El mètode extend() agafa un diccionari amb una llista de funcions i
atributs. Podem crear tants atributs com funcions necessitem, podem
sobreescriure atributs i mètodes de la classe pare i cridar a mètodes de
la classe pare amb **this.\_super.apply(this, arguments);**

Aquestes són les técniques que utilitzen en Odoo per a les classes:

-   Les classes es defineixen heretant de Class o d\'alguna de les seves
    filles.
-   extend() s\'utilitza per heretar d\'una classe, com a paràmetre
    accepta objectes (o diccionaris que és el mateix).
-   init() actua com a constructor.
-   include() permet modificar classes (monkey patch)
-   Quan utilitzem extend() o include(), cada mètode que es redefineix
    pot utilitzar this.\_super() per accedir a la implementació
    original.

**Més sobre classes en Javascript/Odoo:**

```{=html}
<div class="toccolours mw-collapsible mw-collapsed" style="overflow: hidden;">
```
Per fer herència:

``` javascript
var Animal = require('web.Animal');

var Dog = Animal.extend({
    move: function () {
        this.bark();
        this._super.apply(this, arguments);
    },
    bark: function () {
        console.log('woof');
    },
});

var dog = new Dog();
dog.move()
```

També es pot mesclar l\'herencia de varies classes:

``` javascript
var Animal = require('web.Animal');
var DanceMixin = {
    dance: function () {
        console.log('dancing...');
    },
};

var Hamster = Animal.extend(DanceMixin, {
    sleep: function () {
        console.log('sleeping');
    },
});
```

Una altra cosa que es pot fer és ampliar una classe existent amb
**include**

``` javascript
var Hamster = require('web.Hamster');

Hamster.include({
    sleep: function () {
        this._super.apply(this, arguments);
        console.log('zzzz');
    },
});
```

```{=html}
</div>
```
[Manual Oficial Javascript
Reference](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html)
[technical training](https://github.com/gdeb/technical-training) [Video
Odoo JS Framework (2017)](https://www.youtube.com/watch?v=u-6aLi1oqcw)
[Video JS Framework (2018)](https://www.youtube.com/watch?v=e3YOpQBJL_A)

# Widgets personalitzats {#widgets_personalitzats}

![Esquema recomanat per comunicar widgets entre sí.
([1](https://www.odoo.com/es_ES/slides/slide/the-odoo-js-framework-569))](Odoocomunicacionscomponentesjs.png "Esquema recomanat per comunicar widgets entre sí. (1)"){width="400"}
`{{nota|A partir d'Odoo 9, el client web ha canviat substancialment. Aixì que no podem fiar-nos de tutorial basats en aquest. De fet, el propi manual oficial d'Odoo no està actualitzat i no funciona. }}`{=mediawiki}

El Widget és la manera que té Odoo de mostrar les dades i gestionar-les
de forma estàndard en tota la interfície.

La classe Widget és una de les més importants en el framework Javascript
d\'Odoo i està definida en el mòdul **web.Widget** concretament en
**widget.js**. Els widgets tenen algunes capacitats interessants:

-   Es poden establir relacions pare/fill entre els widgets per mesclar
    i afegir funcionalitats.
-   Tenen un **cicle de vida** que permet, per exemple, destruir els
    widgets fills quan es destrueix el pare.
-   Es renderitzen amb QWeb. La classe widget té una funció anomenada
    **renderElement** que crea el html i l\'inserta en el lloc indicat
    de la web. Aquesta funció primer consulta el **template**, que és un
    atribut de la classe i està definit en un xml amb el llenguatge
    QWeb. Si no hi ha template, dins del codi javascript de la funció
    **start:**, per exemple, es pot insertar html amb el llenguatge de
    JQuery.
-   Tenen funcions per interactuar amb l\'exterior. Per exemple, quan
    modifiquem el valor d\'un **widget field**, aquest informa cap a
    dalt de la modificació i aquesta és enregistrada per ser enviada a
    la base dades si cal.

```{=mediawiki}
{{nota|Els desenvolupadors d'Odoo han fet que els widgets no siguen els que gestionen les seues dades. Per obtindrer-les, el model de la vista demanarà les dades a la base de dades i el controlador demanarà a la vista que renderitze el widget amb el valor obtingut de la base de dades. Per escriure en la base de dades, el widget sols envia un trigger que és arreplegat pels pares cap a dalt fins que arriba al controlador que li demana al model que envíe les dades al servidor.}}
```
La comunicació entre widgets es produeix amb **events** si és d\'un
widget fill a un pare i amb **funcions públiques** si és d\'un pare a un
fill. Quan un widget pare inicialitza un widget fill, el fill no ha de
confiar en que el pare li proporcione les dades, sino que ha de ser
inicialitzat en tot el que necessita per a funcionar.

Quan es recarrega la web sencera, es demana a **/web/webclient/qweb** i
aquest descarrega totes les **templates** que necessita. Aquesta és una
de les descàrregues més pesades (\~200Kb) ja que conté quasi totes les
plantilles de tota la interfície. De vegades no necessitem aquesta
plantilla més que en un lloc molt concret i no volem saturar la xarxa
més. Aleshores podem demanar la descàrrega en temps de inicialització
del widget amb **xmlDependencies**:

``` javascript
    template: 'some.template',
    xmlDependencies: ['/myaddon/path/to/my/file.xml'], 
```

## Widgets Fields {#widgets_fields}

Quasi tot el que es mostra en la interfície web està format per Widgets.
Per tant, hi ha de moltes maneres. Alguns són elements bàsics de la
interfície. Altres contenen informació de la base de dades, altres són
elements interactius entre altres widgets\... Com que hi ha tanta
varietat, la classe Widget s\'ha ampliat amb herència per a simplificar
la programació. Per exemple, els widgets que són **fields** hereten tots
d\'una classe filla de widget anomenada **AbstractField**. Si volem fer
un Widget per a mostrar un field d\'un manera diferent, hem de heretar
de AbstractField. És més, probablement podem heretar d\'un widget més
concret, per exemple **FieldChar**.

Aquest missatge està en el .js que defineix el **AbstractField** i
explica les particularitats dels Widgets que són per a Fields:

    /**
     * This is the basic field widget used by all the views to render a field in a view.
     * These field widgets are mostly common to all views, in particular form and list
     * views.
     *
     * The responsabilities of a field widget are mainly:
     * - render a visual representation of the current value of a field
     * - that representation is either in 'readonly' or in 'edit' mode
     * - notify the rest of the system when the field has been changed by
     *   the user (in edit mode)
     *
     * Notes
     * - the widget is not supposed to be able to switch between modes.  If another
     *   mode is required, the view will take care of instantiating another widget.
     * - notify the system when its value has changed and its mode is changed to 'readonly'
     * - notify the system when some action has to be taken, such as opening a record
     * - the Field widget should not, ever, under any circumstance, be aware of
     *   its parent.  The way it communicates changes with the rest of the system is by
     *   triggering events (with trigger_up).  These events bubble up and are interpreted
     *   by the most appropriate parent.
     *
     * Also, in some cases, it may not be practical to have the same widget for all
     * views. In that situation, you can have a 'view specific widget'.  Just register
     * the widget in the registry prefixed by the view type and a dot.  So, for example,
     * a form specific many2one widget should be registered as 'form.many2one'.
     *
     * @module web.AbstractField
     */

Com diu el propi comentari, els widgets field no són responsables de les
seues dades. Quan un usuari les modifica, aquests informen cap a dalt
(**\_setValue**). Els fields tampoc són responsables de carregar les
dades. Els widgets tenen una funció **init:** que rep un paràmetre
anomenat **record** que és un objecte que representa el record obtingut
pel client web. Aquest record té, entre altres coses, els valors de cada
field. La funció **init:** de **AbstractField** guarda el seu valor en
**this.value**.

Els Widget tenen un cicle de vida en el que s\'executen una serie de
funcions:

-   **init**: On es crea el widget, aquesta funció agafa les dades i
    crea l\'estructura del widget. Cal dir que les dades ja estan en el
    client. El widget agafa el paràmetre **record** que rep el init de
    **AbstractField** i selecciona les dades que corresponen al seu
    field. Aquesta funció és síncrona, és a dir, no es pot utilitzar per
    demanar coses al servidor.
-   **willStart**: Funció **asíncrona** cridada abans d\'insertar en el
    DOM. Si es necessita demanar alguna cosa al servidor, ha de ser en
    aquest moment, ja que encara no està el widget dibuixat.
-   **start**: On s\'inicia el widget. Ací podem afegir contingut o
    modificar l\'aspecte. També és una funció **asíncrona** i pot
    retornar una **promise**.
-   **render**: El client web executa aquesta funció per mostrar o
    actualitzar el widget.
-   **destroy**: Quan és eliminat pel client web. Aquesta funció pot
    eliminar el widgets fills o fer alguna cosa abans de ser eliminat.

Tots els widgets tenen una variable anomenada **\$el** o símplement
**el** que conté l\'element del DOM en format objecte JQuery on comença
el widget. Per defecte, a falta de una plantilla, és un **div** buit.

Arbre genealòlic dels widgets fields:

`AbstractField`\
`   |`\
`   --> LinkButton `\
`   --> FieldBoolean`\
`       |`\
`       --> BooleanToggle`\
`   --> FieldToggleBoolean`\
`   --> PriorityWidget`\
`   --> AttachmentImage`\
`   --> StateSelectionWidget`\
`   --> FavoriteWidget`\
`   --> LabelSelection`\
`   --> FieldBooleanButton`\
`   --> PercentPie`\
`   --> ProgressBar`\
`   --> JournalDashboardGraph`\
`   --> FieldDomain`\
`   --> DebouncedField (Per a fields que es modifiquen moltes vegades)`\
`   |    |`\
`   |    --> AceEditor`\
`   |    --> InputField `\
`   |        |`\
`   |        --> FieldChar, FieldText`\
`   |        --> FieldDate, FieldDatetime`\
`   |        --> FieldMonetary`\
`   |        --> FieldEmail`\
`   |        --> UrlWidget`\
`   |        --> NumericField `\
`   |            |`\
`   |            --> FieldInteger`\
`   |            --> FieldFloat`\
`   |                |`\
`   |                --> FieldFloatTime, FieldFloatFactor, FieldFloatToggle, FieldPercentage`\
`   --> AbstracFieldBinary`\
`       |`\
`       --> FieldBinaryImage`\
`       --> FieldBinaryFile`\
`           |`\
`           --> FieldPDFViewer`

La millor manera de saber fer fields widgets és mirar exemples. Els
següents exemples tenen comentaris per explicar qué està passant:

**Exemple de Widget field simple: Widget comptador:**

```{=html}
<div class="toccolours mw-collapsible mw-collapsed" style="overflow: hidden;">
```
``` javascript
console.log('Creacio del widget');
odoo.define('model.module', function(require) {
    "use strict";
var FieldInteger = require('web.basic_fields').FieldInteger; 
    /* web.basic_fields defineix la majoría dels fields
     * no relacionals. Podem veure els que té vejent el final
     * del fitxer /web/static/src/js/fields/basic_fields.js
     * */
var contador = FieldInteger.extend({
    //template: 'contador_template', en aquest cas no fa falta template
    events: _.extend({},FieldInteger.prototype.events, {
        'click': '_onClick',
    }),
    _renderReadonly: function () {
        this._super.apply(this,arguments);
        // render en  mode sols lectura; _renderEdit
    },
    start: function() {  
        return this._super.apply(this,arguments);
    },
    init: function() { //inizialització amb valors
        this._super.apply(this,arguments);
     // console.log(arguments)
     // arguments d'init AbstractField: 
     // init: function (parent, name, record, options)
    },
    _onClick: function () {
    this.value++;
     /**
      *Fragment del mètode _setValue de AbstractField:
      *
     * this method is called by the widget, to change its value and to notify
     * the outside world of its new state.  This method also validates the new
     * value.  Note that this method does not rerender the widget, it should be
     * handled by the widget itself, if necessary.
     *
     * @private
     * @param {any} value
     * @param {Object} [options]
     * @param {boolean} [options.doNotSetDirty=false] if true, the basic model
     *   will not consider that this field is dirty, even though it was changed.
     *   Please do not use this flag unless you really need it.  Our only use
     *   case is currently the pad widget, which does a _setValue in the
     *   renderEdit method.
     * @param {boolean} [options.notifyChange=true] if false, the basic model
     *   will not notify and not trigger the onchange, even though it was changed.
     * @param {boolean} [options.forceChange=false] if true, the change event will be
     *   triggered even if the new value is the same as the old one
     * @returns {Deferred}
     */
    this._setValue(this._formatValue(this.value),{forceChange:true});
        // Si no fem el forceChange no actualitza el field.
        // El _formatValue transforma string en Integer si fora el cas.
    this._render(); // Cal actualitzar el valor
    },
});
    var fieldRegistry = require('web.field_registry');
    fieldRegistry.add('contador', contador); // Son cal fer widget="contador" en un field Integer
    return contador;
});
```

```{=html}
</div>
```
**Exemple de Widget field complex: Widget galeria:**

```{=html}
<div class="toccolours mw-collapsible mw-collapsed" style="overflow: hidden;">
```
Aquest widget fa ús del [RPC](Odoo#RPC "wikilink") per carregar en temps
de renderitzat unes imatges. En aquest cas no està seguint les
recomanacions de Odoo que diuen que el field no deuria gestionar les
seues dades. Per fer millor el que fa el field el recomanable és fer una
vista. No obstant, per a estudiar és molt interessant i planteja la
dificultat afegida d\'un field *x2many*.

``` javascript
/*
Aquest widget mostra una galeria de fotos sempre que tinga un field binary anomenat 'photo_small'. 
La galeria no és editable ni interactiva.
*/
console.log('Creacio del widget galeria');
odoo.define('cine.galeria', function(require) {
    "use strict";
var AbstractField = require('web.AbstractField'); 
    /* Ens basem en la classe abstracta 
     * del fitxer /web/static/src/js/fields/abstract_field.js
     * */
var core = require('web.core');
var qweb = core.qweb; // Necessari per cridar al render
var utils = require('web.utils'); // per a la imatge
var photo = 'photo_small';  // El nom que té el field de la foto per defecte.

var galeria = AbstractField.extend({
    className: 'o_field_m2m_galeria', // classe CSS
    supportedFieldTypes: ['many2many','many2one'], // Suporta M2m i M2o
    galeria_template: 'galeria_template', 
    /*
     *  template: Definició de la plantilla Qweb
     *  Recordem que tots els templates estan en el client 
     *  perquè els demana amb web/webclient/qweb
     *
     *  En aquest cas utilitzem galeria_template perquè no volem que l'utilitze
     *  dirèctament, sino cridar al qweb.render amb paràmetre.
     */
   fieldsToFetch: {   // Els fields que va a demanar el widget del model. 
       // Sols demana els que diu aquesta llista. Es pot observar en el debug del navegador.
       // https://gitlab.merchise.org/merchise/odoo/commit/eafa14d3bc16e7212000d0c9c30a3ed922395574?view=inline
        display_name: {type: 'char'},
       // [photo]: {type: 'binary'},
       /*
        * Aquesta línia està comentada perquè l'interpreta abans de ser carregat el field. 
        * Per tant, no pot fer ús del atribut 'image_field' de la vista i sempre utilitza el valor inicial
        * de la variable photo. fieldsTofech és interpretat per data_manager.js al carregar la vista sencera, no el widget.
        */
    },
    placeholder: "/web/static/src/img/placeholder.png", // Imatge en cas de no tindre imatge
    willStart: function(){  // Aquesta funció és asíncrona, per tant, pot servir per carregar dades des del servidor.
    
        var self = this;  // Com que anem a cridar a funcions, el this serà diferent dins i cal fer una variable independent.

        var res = this._rpc({           
        model: this.value.model,   // El model demanat per el field
                method: 'read',        // Demana el mètode python read
                args: [this.value.res_ids, [photo,'display_name']],   // En aquest cas, enviem com a arguments els ids demanats i el nom dels fields demanats.
                context: this.record.getContext(),   // El context
                }).then(function (result) {       
                if (result.length === 0) {
                    console.log('no trobat');
                }
         var i;
                for(let i of result) {
            var url = self.placeholder; // En cas de no tindre url
            if (i[photo]) {
            url = 'data:image/png;base64,' + i[photo];
                }
                i.url= url;
        }
        self.record.dataLoaded = { elements: result, readonly: self.mode === "readonly"}; // El render espera aquest objecte
        });
        return res;  // res és un 'promise' de jquery, ja que segurament el rpc no acaba abans que la funció. 
                     // La funció que el cride ha de fer un $.when per esperar a que acabe la 'promise' i les dades estiguen carregades.
    
    },
    start: function() { 
    var p = this.$el.append('<p>Widget Galeria</p>');
        // ^ línia sols per provar cóm es poden afegir coses al widget en start 
        // (no es veurà, ja que sols funciona amb el render per defecte)
        return $.when(p, this._super.apply(this,arguments)); // $.when espera a l'inserció 
    },
    init: function(parent, name, record, options) { //inizialització amb valors
        photo = record.fieldsInfo[options.viewType][name].image_field //La manera d'extraure el valor d'un atribut 
                                                                  // En el field de la vista
        this._super.apply(this,arguments);
    },
    
    _LoadGaleria: function(){
    console.log('Load Galeria');
    },

/*
 *La següent funció modifica els datos que s'envien al render afegint el base64 al raw de la imatge.
 Com que no ha carregat la imatge en fieldsTofetch, cal fer un _rpc per a carregar-la en el moment del render. 
 Aquesta, no és la millor solució i per això està comentada, perquè carrega les dades cada vegada que es renderitza.
 La solució correcta és fer-ho en el willStart que ja actua de forma asíncrona.
 * */
    _getRenderGaleriaContext: function () {
        // var elements = this.value ? _.pluck(this.value.data, 'data') : []; 
        // _.pluck() és una funció de underscore.js una biblioteca javascript que també
        // utilitza Odoo. pluck és l'equivalent a mapped() en python.
        // En aquest cas, de la llista sols volem un array amb la clau data de cadascun.
        /*var self = this;  // Com que anem a cridar a funcions, el this serà diferent dins i cal fer una variable independent.
        var res = this._rpc({           
        model: this.value.model,   // El model demanat per el field
                method: 'read',        // Demana el mètode python read
                args: [this.value.res_ids, [photo,'display_name']],   // En aquest cas, enviem com a arguments els ids demanats i el nom dels fields demanats.
                context: this.record.getContext(),   // El context
                }).then(function (result) {       
                if (result.length === 0) {
                    console.log('no trobat');
                }
         var i;
                for(let i of result) {
            var url = self.placeholder; // En cas de no tindre url
            if (i[photo]) {
            url = 'data:image/png;base64,' + i[photo];
                }
                i.url= url;
        }
        self.record.dataLoaded = { elements: result, readonly: self.mode === "readonly"}; // El render espera aquest objecte
        });
        return res;  // res és un 'promise' de jquery, ja que segurament el rpc no acaba abans que la funció. 
                     // La funció que el cride ha de fer un $.when per esperar a que acabe la 'promise' i les dades estiguen carregades. */
    },

    _renderReadonly: function () {
        this._renderGaleria();
    },
    _renderEdit: function () {
        this._renderGaleria();
    },
    _renderGaleria: function () {
        var self = this;
            $.when(this._getRenderGaleriaContext()).done(function(){
            //this.$el.html(qweb.render(this.tag_template, this._getRenderTagsContext()));
            self.$el.html(qweb.render(self.galeria_template, self.record.dataLoaded));
        });
        /*
         *qweb.render() és una funció que accepta una template i un context en el que estan les 
         variables que en template necessita. En aquest cas enviem elements i l'opcio de readonly
         * */
    },
});
    var fieldRegistry = require('web.field_registry');
    fieldRegistry.add('m2m_galeria', galeria); // Son cal fer widget="m2m_galeria" en un field m2m o o2m
    return galeria;
});
```

```{=html}
</div>
```
## RPC

Observem el mètode **\_fetchRecord()** de
**/web/static/src/js/views/basic/basic_model.js**.

``` javascript
    _fetchRecord: function (record, options) {
        var self = this;
        options = options || {};   
        var fieldNames = options.fieldNames || record.getFieldNames(options);
        fieldNames = _.uniq(fieldNames.concat(['display_name']));   // Als fields afegir Display_name, que sempre fa falta
        return this._rpc({   // El mètode _rpc 
                model: record.model,   // El model demanat 
                method: 'read',        // Demana el mètode de l'ORM read, pot ser qualsevol de l'ORM o del model.
                args: [[record.res_id], fieldNames],   // En aquest cas, enviem com a arguments 
                                                      //el id demanat i el nom dels fields demanats.
                context: _.extend({}, record.getContext(), {bin_size: true}),   // El context
            })
            .then(function (result) {       
                if (result.length === 0) {
                    return $.Deferred().reject();
                }
                result = result[0];
                record.data = _.extend({}, record.data, result);
            })
            .then(function () {
                self._parseServerData(fieldNames, record, record.data);  //transforma les dades per al javascript
            })
            .then(function () {   
                return $.when(   // Com que és una vista, ha de demanar tots els records dels fields x2Many i demés.
                    self._fetchX2Manys(record, options),
                    self._fetchReferences(record, options)
                ).then(function () {
                    return self._postprocess(record, options);
                });
            });
    },
```

**\_rpc** és una funció que ejecuta un **service** Ajax. Odoo incorpora
el concepte de **service** per centralitzar la comunicació entre
elements del programa. El que retorna és un objecte **promise** com els
de **JQuery**. Això perment utilitzar la funció **\$.when** i
**\$.then** per esperar a que es carregue.

<https://stackoverflow.com/questions/45049996/how-can-i-create-a-simple-widget-in-odoo10>

<https://github.com/odoo/odoo/wiki/Javascript-coding-guidelines>

[video A Single Page](https://www.youtube.com/watch?v=H-iFhOh1tOE) [Codi
del video](https://github.com/dbo-odoo/odoo-js-demo)

# Qweb Templates {#qweb_templates}

Si volem tindre un html personalitzat en el nostre widget, cal escriure
en un XML la plantilla. S\'utilitza el llenguatge **QWeb**. Aquestes
plantilles permeten al Javascript renderitzar un Widget.

Quan el client arranca, es realitza un **rpc** a /web/webclient/qweb.
Aquest té una llista de totes les plantilles definides en tots el mòduls
instal·lats. Aquestes plantilles estan en la entrada **qweb** del
**\_\_manifest\_\_.py**. Quan a carregat aquestes plantilles ja pot
començar a renderitzar els elements de la web.

En **\_\_manifest.py\_\_**:

``` javascript
 'qweb': [
        "static/src/xml/widgets.xml",
    ],
```

Això funciona prou bé, però si és un widget no molt demanat, estem
creant molt de tràfic innecessari. Per això, es pot utilitzar la
variable **xmlDependencies** que carregarà les dependències sols quan
arranque el widget:

``` javascript
var Widget = require('web.Widget');

var Counter = Widget.extend({
    template: 'some.template',
    xmlDependencies: ['/myaddon/path/to/my/file.xml'],
    ...
});
```

Les plantilles en QWeb permeten personalitzar el html resultant. Els
fitxers XML que contenen les plantilles han de tindre la següent
estructura:

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="modul.template" xml:space="preserve">

</templates>
```

I dins, etiquetes **`<t t-name>`{=html}**:

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="contador_template" xml:space="preserve">
<t t-name="galeria_template">
    <t t-foreach="elements" t-as="el">
        <span t-attf-class="galeria"  t-att-data-index="el_index" t-att-data-id="el.id">
        <img class="img img-responsive" t-att-src='url' />
            <span t-if="!readonly" class="fa fa-times o_delete"/>
        </span>
    </t>
</t>
</templates>
```

Si volem tindre un html personalitzat en el nostre widget, tenim moltes
opcions:

-   Podem **no tindre un template** i generar tot el html en el codi
    Javascript al mètode **\_renderEdit i \_renderReadonly**. Això es
    pot fer amb el mètode **this.\$el.html()**.
-   Podem tindre un **QWeb bàsic** amb divs i altres etiquetes en
    classes i ids. Aleshores els mètodes de **\_render..** poden indicar
    què va en cada lloc amb **this.\$(\'div\').html()** un per un.
-   Si la plantilla QWeb és complexa i té ifs o foreachs, es té que fer
    ús del mètode **qweb.render(plantillaQWeb, Elements)** on la
    plantilla és el nom de la plantilla i **Elements** és un diccionari
    amb els valors que es tenen que mostrar.

# Vistes Personalitzades {#vistes_personalitzades}

Les vistes en Odoo són un **widget** més encarregat de mostrar la
informació en la finestra sencera. Aquest widget cridarà a tots els que
composen la vista. Cada vista agafa un **XML** en el camp anomenat
**arch**, uns paràmetres i unes dades i renderitzar un model.

Les vistes en el Javascript tenen també el **MVC**. El arxiu i classe
**view** defineix la vista i carrega el MVC, de manera que està l\'arxiu
**model, controller i renderer**. El renderer representa la V en el
model-vista-controlador.

Per tant, la vista Javascript:

1.  Instància una vista amb el **arch**, **fields** i paràmetres.
2.  Crida al mètode **getController** en la instància de la vista, açò
    retorna un controlador amb uns subwidgets anomenats **renderer** i
    **model**.
3.  Afegeix el controlador a la web.
4.  Una vegada afegit el controlador, la classe **view** no és
    necessària.

```{=mediawiki}
{{nota| Es recomana estudiar l'arxiu: odoo/addons/web/static/src/js/views/abstract_view.js }}
```
El **controlador**, dins del Javascript, s\'encarrega de servir els
esdeveniments que arriven dels fills i del model/renderer i cridar als
mètodes apropiats. Tot el que té a veure amb la relació entre el
renderer/model amb el servidor l\'ha de fer el controlador.

El **model** és més un concepte de la part del servidor, però en el
client, guarda la informació a mostrar, les modificacions a les dades
pasen pel model. El model no és un widget, ja que no ha de ser
renderitzat, però pot notificar al seu pare llançant **events**. El
model hereta de **web.Class**

El **renderer** sols ha de dibuixar en el navegador el widget de la
vista.

En general, les vistes han d\'heretar de **BasicView**.

[Create a View (2018)](https://www.youtube.com/watch?v=SIoljYJhTqk)

[OWL, el nou framework per a Odoo 14](https://github.com/odoo/owl)

[tutorial
complet](https://www.oocademy.com/v14.0/tutorial/introduction-to-owl-87#-Adding-our-first-component)

[2](https://www.fatalerrors.org/a/odoo14-odoo-web-library-owl.html)

[3](https://www.cybrosys.com/blog/hooks-in-odoo-owl-framework)

<https://www.youtube.com/watch?v=IrcQf4hgjtw>

Enllaços: <https://github.com/odoo/owl>
<https://odoo.github.io/owl/playground/>
<https://medium.com/cybrosys/introduction-to-odoo-owl-framework-29cbe9111919>
<https://www.odoo.com/es_ES/forum/ayuda-1/blogs-or-websites-available-for-owl-odoo-web-library-for-odoo-v14-to-learn-from-the-scratch-168365>
<https://www.youtube.com/watch?v=HSer89uSnoM&list=PL1-aSABtP6ABc8HP_02IuC9lUHESnUJM1&index=11>
