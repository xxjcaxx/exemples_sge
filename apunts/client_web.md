# Client Web

En la secció de la vista i de l\'herència en la vista hem pogut
modificar la forma en que `Odoo` mostra o gestiona la
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

> Si volem veure tot el que el servidor rep o envia al client, podem arrancar el servici amb l\'opció \--log-level=debug_rpc.

El client web és una **SPA (Single Page Application)**, a l\'estil
d\'altres frameworks coneguts com Angular o React, va creant i destruint
elements de la interfície contínuament. Aquests elements són, entre
altre coses, Widgets.

Si volem saber modificar a baix nivell el client web, necessitem saber
prou de Javascript, de JQuery, BootStrap i altres, amés de HTML5.

Amb Odoo, es proporcionen tres clients web diferenciats, però que, internament, funcionen amb el mateix framework. Aquest són el **web client** que és el "backoffice" utilitzat pel empleats de l'empresa, el **website** que és la pàgina web pública i el **point of sale**, que és per al punts de venda.

Quan ens referim a crear mòduls per al client, generalment ens referim a
fer canvis subtils en l\'apariència o comportament de la web.

Reflexionem sobre el tipus de modificació que necessitem:

- Un canvi menor en l\'apariència: Afegir algunes regles CSS.
- Un canvi estétic o de comportament de la manera en que es visualitza un field: Afegir HTML, CSS i Javascript a un **Widget**.
- Un canvi en la manera en la que un field enmagatzema o recupera les dades: Modificació del Javascript del Widget i de la part del model o el controlador Javascript de la vista.
- Un canvi en la manera de mostrar un recordset sencer: Crear una  vista.
- Fer una web des de 0 amb les dades d\'Odoo: Utilitzar els [Web
    controllers](https://www.odoo.com/documentation/12.0/reference/http.html#reference-http-controllers)

## Arquitectura del client web

El **WebClient** d\'Odoo es construeix amb mòduls, de la mateixa manera que
els mòduls per al \'servidor\'. Sols que en els mòduls per ampliar el
client web es modifiquen altres arxius a banda dels típics dels models de
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

Els mòduls principals del client web depenen del mòdul **web**, que
proporciona el nucli del client web. Els altres complementen a aquest.
Hi ha mòduls que específicament es diuen, per exemple, **web_kanban**,
que amplien la web. Però en realitat qualsevol mòdul ho pot fer. El
mòdul web conté tot l'HTML i Javascript necessari per a que els altres
mòduls de la web funcionen.

Per modificar el client web cal proporcional HTML, xml, CSS, Javascript
i imatges. Això ha d\'estar en el directori **static** del mòdul:

- static/src/js : the JavaScript files
- static/src/css : the CSS files
- static/src/xml : the HTML template files
- static/img : pictures used in templates or CSS
- static/libs : JS libraries needed by the module

El server no manipula aquesta informació, però la processa en certa
manera i l\'envia a client.

```{tip}
Com que els CSS i JS no són processades pel servidor, no cal reiniciar el servidor per veure els canvis, sols refrescar el navegador. Això no sempre funciona, ja que el servidor pot ser que no processe els assets o que la cau del navegador no actualitze el JS o el XML.
```

## Enviant el client al navegador

Cada vegada que refresquem, s\'envia el client sencer. Això vol dir
molts CSS, moltes línies de Javascript de molt fitxers distints i molt
d'HTML i XML. Per evitar saturar la xarxa, el servidor fa una
compressió de totes eixes dades de la següent manera:

- Tots els CSS i Javascript són concatenats en un sol fitxer. La
    concatenació s\'ordena per dependències entre mòduls.
- El Javascript és minimitzat llevant espais i refactoritzant les
    variables per noms més curts.
- Una web HTML molt simple sols amb l\'enllaç als CSS i Javascript és
    enviada al client.
- Tot es comprimeix en gzip pel server per reduir l\'enviament. El
    navegador és capaç de descomprimir.

Tot això fa difícil de fer debug amb el client. Per això es recomana
ficar **?debug=1** a la URL per demanar que no minimitze.

### Els Assets

El client d\'Odoo és molt complex i necessita tindre Javascript, HTML i
CSS de molts fitxers distints. Gestionar això permetent que qualsevol
puga fer un mòdul per afegir més implica una gestió d\'aquests enllaços
més automàtica. Per això han creat principalment tres **bundles** en XML
que no són més que una col·lecció de links a Javascript o CSS. Aquests
tenen l\'estructura d\'un Template QWeb i els més comuns són:

- **web.assets_common**: amb les coses comuns.
- **web.assets_backend**: Amb les coses específiques del Backend.
- **web.assets_frontend**: Amb les coses de la web pública.

 Si volem afegir fitxers a un asset en odoo, s\'ha d\'afegir al manifest:

```python
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

> Aquesta és la manera general d'afegir funcionalitats o estils. Però tal vegada el nostre widget no necessita ser carregat sempre i estem afegint una càrrega constant a la xarxa. Per això pot ser interessant afegir la llibreria sols quan es crea el widget en temps d'execució. Odoo proporciona formes de carrega llibreries i CSS de forma dinàmica (lazyload en Qweb template engine).

Documentació sobre els assets: <https://www.odoo.com/documentation/master/developer/reference/frontend/assets.html>

#### Afegir CSS al nostre mòdul

Abans d\'entrar en la creació de Widgets, pot ser interessant observar
cóm els **bundles** es poden ampliar d\'una forma simple per modificar o
afegir CSS.

El primer és crear el css en
**/`<modul>`/static/src/css/`<modul>`.css**. En el nostre cas, sols fem un per a fer la lletra mès menuda:

``` css
.reserves_tree { font-size:0.8em;}
```

Després afegim el css al bundle **assets_backend**:

```python
'assets': {
    'web.assets_backend': [
        'web/static/src/xml/**/*',
    ],
},
```

I per últim, sols cal utilitzar la classe css:

``` xml
<field name="bookings" limit="10" class="reserves_tree">
```

## Arquitectura dels mòduls en Javascript

De la mateixa manera que hem vist per introduir un CSS personalitzat en
Odoo, es pot introduir un Javascript. Aquest serà afegit al final del
bundle i serà executat pel navegador.

Odoo té molt de Javascript ja funcionant i podem interferir. Però el major problema és que no sabem molt bé qué s\'està executant en cada moment. Javascript és un llenguatge que
treballa molt de forma asíncrona. Això permet que es puga carregar part
de la web mentres una altra part ja està funcionant. Aquesta asincronia
fa que no es puga predir fàcilment en quin ordre es carregarà o
executarà tot. Totes les aplicacions web complexes tenen que solucionar
eixos problemes. Javascript té un ecosistema de biblioteques molt divers
i no tots treballen de la mateixa manera, de fet, molts han solventat
carències del llenguatge amb tècniques de programació i biblioteques.
Aques és el cas dels mòduls. Odoo gestiona la complexitat del seu
Javascript amb mòduls i dependències d\'altres mòduls. Per això no és
tan simple con afegir un parell d\'instruccions Jquery per modificar una
part del DOM, ja que no podem saber si està carregada o quan es
carregarà. Abans de fer partxes que solucionen mal els problemes, cal
estudiar cóm ho fa Odoo.

```{tip}
Els mòduls simplifiquen la programació de les webs grans. Els mòduls oculten la complexitat de la programació de les distintes parts lògiques d’un programa. Els mòduls ofereixen una interfície en la que interactuen amb la resta de mòduls. Un programa modular és més fàcilment ampliable i reutilitzable.
En els mòduls cal aconseguir tindre la major independència al aconseguit el menor '''acoblament''' i la major '''cohesió'''. L’acoblament és la excessiva dependència d’un mòdul respecte a altres i la cohesió és la íntima relació entre els elements interns del mòdul. [https://developer.mozilla.org/es/docs/Web/JavaScript/Introducci%C3%B3n_a_JavaScript_orientado_a_objetos]
```
<https://www.odoo.com/documentation/15.0/developer/reference/frontend/framework_overview.html>

Odoo suporta tres maneres de fer codi Javascript:

- Sense mòduls (No recomanable)
- Amb mòduls natius ES6.
- Amb el seu propi sistema de mòduls (En versions antigues)

### Utilitzar mòduls natius ES6 en Odoo

La documentació oficial recomana fer els nous mòduls d\'aquesta manera.

``` javascript
import { someFunction } from './file_b';

export function otherFunction(val) {
    return someFunction(val + 3);
}
```

# OWL

Moltes pàgines web SPA com és Odoo estan fetes en un framework de
Javascript, ja que el manteniments dels components, els hooks, la
reactivitat o la comunicació amb el servidor són complicats i és
innecessari fer-ho sempre. Alguns dels frameworks són: Angular, Vue,
React...

Odoo té el seu propi, i a partir de la versió 14 es diu OWL i es
desenvolupa per separat, sempre pensant en que siga la base dels nous
elements de la web en Odoo. En Odoo 14 el sistema antic i OWL poden
conviure. Al 16 tots els fields i vistes adopten el nou framework.

```{tip}
La primera pregunta que un desenvolupador web es fa al veure que Odoo està desenvolupant el seu framework és perquè no utilitzen Angular, Vue o React o qualsevol altre framework madur. Els desenvolupadors d'Odoo la responen en cada article: Necessiten que siga més lleugera, adaptada totalment a Odoo i no dependre d'altres. Semblen bons motius i si tenen raó o no es veurà en les pròximes versions. 
```

OWL és un framework web menut (\<20KB) que té els elements d\'un
framework modern:

- Un sistema declaratiu de components
- Un sistema de reactivitat basat en Hooks.
- Per defecte té un mode concurrent.
- Un store per a l\'estat del programai
- Un Router.
- Un sistema de plantilles amb QWeb.
- Al contrari que en versions anteriors, OWL aprofita la sintaxi ES6
    per a les classes.
- Un virtual DOM amb renderització asíncrona.

En la [documentació oficial d\'OWL](https://github.com/odoo/owl) quasi no menciona cóm integrar-lo en Odoo. Això és perquè OWL aspira a ser un framework independent i poder ser utilitzat per a quasevol cosa. En la realitat, ha sigut desenvolupat pensant en Odoo i quasi sols s'utilitza en projectes relacionats.

> Quan desenvolupem per a Odoo en OWL cal tenir en compte que Odoo afegeix a OWL alguns objectes propis, com una estructura estàndard de `props`, el concepte de `Widget`, registres ja predefinits i moltes coses més. 

Abans de continuar cal preguntar-se què es vol aconseguir o què podem aconseguir amb OWL:
- Crear una web completa sense relació amb Odoo.
- Crear una web completa que tinga com a backend Odoo (no té molta
    diferència de l\'anterior)
- Fer una secció en la web o el backend d\'Odoo.
- Fer una vista, un menú, un widget nou per a Odoo.

Aquest manual es centra sobretot en l\'última opció i anem a començar
per ella.

## Crear un component d\'Odoo en OWL

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
//Importar els elements del framework
import { Component, xml, useState, mount } from "@odoo/owl";

// Crear el component que hereta de Component d'OWL
class MyComponent extends Component {
    static template = xml`
        <div t-on-click="increment">
            <t t-esc="state.value">
        </div>
    `;

    // La funció setup és on s'inicialitza el component, no deuriem utilitzar constructor.
    setup() {
        this.state = useState({ value: 1 });
    }

    increment() {
        this.state.value++;
    }
}

// La forma de cridar a la funció xml en tagged templates 
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates

MyComponent.template = xml`<button t-on-click="increment">  
Click Me! [<t t-esc="state.value"/>]
</button>`;
```

El problema és que ara no és fàcil integrar el component en la vista d'Odoo, ja que es necessita donar d'alta un Widget o ampliar les vistes.

De moment, podem provar si funciona amb aquest codi que després llevarem:

```javascript
document.addEventListener("DOMContentLoaded", function () {
    const el = document.createElement("div");
    document.body.appendChild(el);
    mount(MyComponent, el);
});
```

> El codi anterior és símplement un exemple tret de la documentació d'Odoo. Té un problema de disseny i és que la plantilla `xml` deuria estar en un fitxer a banda i ser referenciada per a poder estar en un asset, poder ser traduida i ser més eficient.

## Modificar components en OWL

<https://codingdodo.com/owl-in-odoo-14-extend-and-patch-existing-owl-components/>

## Crear nous Widgets en OWL

La paraula `Widget` es considera obsoleta en Odoo amb OWL, ara cal dir `Components`. No obstant, al crear forms o trees, encara posem `widget=`, per tant, podem entendre al Widget com un component capaç de mostrar o editar dades dins de les vistes. 

> Cal dir que els Widgets són l'única manera actualment de clavar components personalitzats en `form`, `tree` o `search`, ja que aquestes vistes no accepten plantilles `Qweb`. En les vistes `form` sols s'accepta `XML` amb `fields` que poden tenir `widgets`. No obstant, en Kanban i altres més manuals sí es poden utilitzar.

Per crear nous Widgets podem fer-los de 0 o extendre un existent.


### Crear un Widget molt simple

Aquest és un codi mínim que funciona per crear un widget:

```javascript
import { Component, xml, useState, mount } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import {registry} from "@web/core/registry";
export class CodeField extends Component {
    static props = {...standardFieldProps}
    setup() {
        this.formattedValue = this.props.record.data[this.props.name];
    }
}
CodeField.template = xml`<pre t-esc="formattedValue" class="bg-primary text-white p-3 rounded"/>`;
registry.category("fields").add("codefield", {
    component: CodeField,
});
```

Per utilitzar el widget:

```xml
<field name="code" widget="codefield"/>
```

Aquest field sols és de lectura i mostra el codi dins d'un `<pre>` blau. És interessant perquè arreplega el seu valor de `props` i perquè pot ser utilitzat com a Widget. A continuació anem a aprofuncir un poc més i a fer Widgets i components més complexos.

### Props

Com en React o Vue, OWL permet que els components tinguen una propietat estàtica anomenada `props` (properties). Serveix per a comunicar al component les seues dades.

https://github.com/odoo/owl/blob/master/doc/reference/props.md 

Com que el pare ha de saber quin nom posar al props, hi ha uns amb un nom per defecte que funcionen específicament per a Odoo: `standardFieldProps`. Amés, es poden crear nous dins de l'objecte `static props` del component. D'aquesta manera, fem components (Widgets) compatibles amb les vistes (components pares) ja existents. 

Els props poden ser valors estàtics, poden ser referències a objectes per ser dinàmics i reactius o poden ser referències a funcions. Els components pares els poden assignar de la següent manera:

```javascript  
class Child extends Component {
  static template = xml`<div><t t-esc="props.a"/><t t-esc="props.b"/></div>`;
}

class Parent extends Component {
  static template = xml`<div><Child a="state.a" b="'string'"/></div>`;
  static components = { Child };
  state = useState({ a: "fromparent" });
}
```

## Crear noves vistes en OWL

<https://codingdodo.com/odoo-javascript-101-classes-and-mvc-architecture/>
<https://codingdodo.com/odoo-15-javascript-reference/>

## Hooks en OWL

<https://www.cybrosys.com/blog/hooks-in-odoo-owl-framework>

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
