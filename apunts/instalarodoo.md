# Instal·lar Odoo

Odoo pot ser instal·lat en qualsevol sistema
operatiu. No obstant, es desenvolupa pensant en Ubuntu o Debian i és el
sistema en el que anem a treballar.

Odoo, en esencia, és un servidor web fet en python que es connecta amb
una base de dades postgreSQL. Hi ha moltes maneres d\'instal·lar Odoo,
de les més avançades que són descarregar per *git* el repositori i fer
que arranque a l\'inici a les més simples que són desplegar un
**docker** amb tot funcionant. [Manual technical training
Odoo](https://github.com/odoo/technical-training/tree/12.0-99-sysadmin).

## Instal·lar en Debian i Ubuntu

Abans de res, cal preparar un poc el sistema:

En el cas de Ubuntu o Debian, que és el que ens interessa,
Odoo proporciona uns repositoris anomenats
**Nightly**, que poden ser afegits al **sources.list** per instal·lar de
manera automàtica tot. Aquests respositoris són actualitzats cada nit.
Per tant, és possible que al llarg del temps, algunes funcions o arxius
canvien si actualitzem.

En principi tot ha de funcionar com diuen en els manuals, però si tenim
que utilitzar utf-8 per l\'idioma, tenim que fer algunes coses abans.

Abans de res, es possible que Debian o ubuntu no tinga bé els
**locales**. Es pot fer en:

     # dpkg-reconfigure locales

I seleccionar els de es_ES i el de UTF8 per defecte. Cal eixir de sessió
i tornar a entrar.

Si dpkg-reconfigure no mostra un asistent, pots fer:

     # locale-gen "es_ES.UTF-8"
     # dpkg-reconfigure locales

Enllaç als repositoris: <https://nightly.odoo.com/>

I com en el propi manual diu, es pot fer tot en aquests comandaments (el
primer si estem en Debian):

     # sudo apt-get install ca-certificates
     # wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
     # echo "deb http://nightly.odoo.com/17.0/nightly/deb/ ./" >> /etc/apt/sources.list
     # apt-get update && apt-get install odoo

Aquests comandaments el que fan és instal·lar els certificats que els
navegadors o, en aquest cas, wget necessiten per admetre HTTPS, a
continuació, descarrega el certificat, afegeix el repositori i instal·la
l\'Odoo.

A continuació, cal anar a la direcció en el navegador:

    http://<ip o url>:8069

[Asciinema del procés](https://asciinema.org/a/122875).

## Configuració de la ruta dels mòduls

Com que la instalació d\'Odoo crea lúsuari **odoo**, que és el que tenim
que utilitzar per al desenvolupament, anem a donar-li una contrasenya:

    $ sudo passwd odoo
    $ sudo usermod -s /bin/bash odoo

```{admonition} Atenció
:class: warning
 
A partir d'aquest moments, tots els comandaments s'han de fer amb l'usuari odoo.
```
La configuració del servidor Odoo té una opció que es diu
**addons-path**. Nosaltres poden afegir més rutes per als nostres addons
personalitzats. Es pot deixar de manera definitiva en el fitxer de
configuració o iniciar el servidor indicant quina és la ruta dels
addons:

     $ odoo -d demodb --addons-path="<ruta>"

Si volem que quede guardat de manera definitiva, cal afegit **\--save**
al comandament. Els comandaments són queda, per tant:

     $ mkdir /var/lib/odoo/modules
     $ odoo scaffold proves /var/lib/odoo/modules
     $ odoo --addons-path="/var/lib/odoo/modules,/usr/lib/python3/dist-packages/odoo/addons" --save

```{admonition} Nota
:class: tip
 
L'opció --save guarda la configuració en $HOME/.odoorc, que és un fitxer per a l'usuari odoo. Si volem que siga per a tots els usuaris que puguen executar el servidor odoo, es pot ficar en el fixter de /etc/odoo
```
## Depurar Odoo

Per crear mòduls o vorer els problemes que estan passant, cal llegir els
fitxers de log, però hi ha una manera més eficient de fer-ho. Si
observem el comandament que, realment, està executant odoo:

`python3 /usr/bin/odoo --config /etc/odoo/odoo.conf --logfile /var/log/odoo/odoo-server.log`

Podem observar que diu que \--logofile va a un fitxer. Si parem el
servici amb:

     # systemctl stop odoo
    o
     # /etc/init.d/odoo stop

Podem iniciar sessió amb l\'usuari odoo (cal fer que puga iniciar sessió
en Linux) i executar:

     odoo --config /etc/odoo/odoo.conf

D\'aquesta manera, en temps real, va apareguent els missatges que dona
el servidor.

Si volem, amés, actualizar un mòdul al arrancar, podem especificar quina
base de dades i quin mòdul a actualitzar:

     odoo --config /etc/odoo/odoo.conf -u mòdul -d empresa

Pot ser que el nostre usuari odoo tinga una configració personalitzada.
En aquest cas, cal fer, per exemple:

     $ odoo --config /var/lib/odoo/.odoorc -d empresa -u modul

De fet, una vegada fet el \--save, cada vegada que cridem al comandament
**odoo** busca el .odoorc al directori personal de l\'usuari. Per tant,
sols cal fer:

     $ odoo -d empresa -u modul

Amés, podem modificar el nivell de log amb l\'opció \--log-level, per
exemple: \--log-level=debug

[Asccinema amb tots els passos per
depurar.](https://asciinema.org/a/122901)

Per saber més, pots anar a l\'ajuda:

     $ odoo --help

O a aquesta web:
<https://www.odoo.com/documentation/12.0/reference/cmdline.html>


### Millorar l\'eixida de Log

Per afegir als nostres mètodes una eixida de log i facilitar la
depuració, es pot utilitzar el api de Odoo:

Al principi del fitxer .py:

``` python
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)
```

Per dins de les funcions:

``` python
    _logger.debug("Use _logger.debug for debugging purposes, nothing else.")
    _logger.info("Use _logger.info for information messages. This is used for notifying about something important.")
    _logger.warning("Use _logger.warning for minor issues, which will not crash your module.")
    _logger.error("Use _logger.error to report a failed operation.")
    _logger.critical("Use _logger.critical for critical message: when this goes off the module will not work anymore.")
    #Want to include data from your field? Pass it along in the context, get it from the pool or from the dict.
    _logger.critical("The name '" + str(record.get('name')) + "' is not okay for us!")
```

### Opcions de log {#opcions_de_log}

Per defecte, Odoo llança el seu log a un fitxer a **/var/log/odoo/**,
però es pot fer que envía a un altre fitxer amb **\--log-file=LOGFILE**.

Si volem més detall en determinats accions d\'Odoo, podem afegir al
comandament les següents opcions:

-   **\--log-request**: Mostra les peticions **RPC** (remote procedure
    call) fetes per l\'http des del client.
-   **\--log-response**: Mostra el contingut de la resposta que dona el
    servidor a les peticions anteriors. Molt útil per saber què està
    enviant i cóm ho interpreta el client.
-   **\--log-web**: Dona més detalls de totes les peticions GET o POST
    que es donen a la web.
-   **\--log-sql**: Mostra el sql que llança al servidor PostgreSQL.
    Aquesta opció ens ajuda a entendre cóm funciona el ORM.
-   **\--log-level=LOG_LEVEL**

`                       specify the level of the logging. Accepted values:`\
`                       ['info', 'debug_rpc', 'warn', 'test', 'critical',`\
`                       'debug_sql', 'error', 'debug', 'debug_rpc_answer',`\
`                       'notset'].`

### Preparar l\'entorn de treball per a SGE 

```{admonition} Nota
:class: tip
 
Aquesta ajuda és per que, com a alumnes, vos prepareu correctament per poder programar de manera cómoda en Odoo. No obstant, es poden traure idees per al treball professional o en altres entorns
```
-   Instal·lar el contenidor o la màquina virtual Ubuntu Server
-   Crear un usuari per poder accedir fàcilment per SSH les primeres
    vegades i que no siga Odoo.
-   Accedir amb eixe usuari per SSH, fer-se root i instal·lar Odoo
    segons els manuals anteriors.
-   Crear una empresa amb dades de demo en la web d\'Odoo.
-   Fer que l\'usuari Odoo tinga shell i fer que es puga accedir a ell
    per [SSH](SSH "wikilink") sense contrasenya des del vostre equip. (
    usermod -s /bin/bash odoo )
-   Fer-se un compte i un projecte en Github.
-   Crear el directori modules i configurar Odoo per utilitzar aquest
    quant s\'inicie en \'mode depuració\'.
-   Sincronitzar el directori modules en el Github personal.
-   Instal·lar ngrok per poder accedir des de remot al contenidor.
-   Configurar el navegador d\'arxius per accedir per SSH i editar amb
    el teu editor preferit.
-   Entrar en el navegador d\'arxius a *altres ubicacions* i escriure
    <ssh://odoo@>`<ip>`{=html}
    -   Ens mostrarà un directori que podem afegir com a favorit del
        navegador d\'arxius.
    -   El directori real on l\'ha muntat
        **[gvfs](https://es.wikipedia.org/wiki/GVFS)** és
        **/run/user/`<usuari>`{=html}/gvfs/sftp:host=`<ip>`{=html},user=odoo/var/lib/odoo**
        o **\~/.gvfs/**
    -   Podem afegir aquest directori real com a lloc de projecte per al
        programa **PyCharm**.
    -   PyCharm també té una terminal que pot entrar per SSH.
-   Una alternativa al navegador d\'arxius és connectar per sshfs:
     
     sshfs odoo@10.100.23.100:/var/lib/odoo ./odoo/


### Debug mode

Odoo permet entrar en mode debug amb **\--debug**.

També es pot importar la bibliteca **pdb** i col·locar un *trace* en el
codi que ens interessa:

``` python
    import pdb
    ...
    pdb.set_trace()
```

Una vegada dins, es poden utilitzar els comandaments de pdb:
<https://docs.python.org/3/library/pdb.html>

## Posar en producció

<https://www.odoo.com/documentation/17.0/administration/install/deploy.html?highlight=workers>

### Odoo per HTTPS

El servidor Odoo per defecte dona la seua web pel port 8069 i en HTTP
sense capa de seguretat SSL.

Per fer que tinga eixa seguretat, necessitem utilitzar un servidor web
que faça de proxy i proporcione la connectivitat per HTTPS.

Situació inicial:

`  ------------             ------------`\
`  |          |         8069|          |`\
`  |  Client  |<----------->| Server   | `\
`  |          |             | Odoo     |`\
`  ------------             ------------`

Situació que busquem:

`  ------------             --------------------`\
`  |          |         443 |                  |`\
`  |  Client  |<----------->| Nginx <--┐       |`\
`  |          |             |          |       |`\
`  ------------             |          |8069   |`\
`                           |          v       |`\
`                           |        ------    |`\
`                           |        |Odoo|    |`\
`                           |        ------    |`\
`                           --------------------`

Tots els servicis que utilitzen SSL necessiten un certificat. En una
situació ideal, tenim un certificat signat per una entitat
certificadora. Si no, tenim que crear en nostre autosignat.

[tutorial del
certificat](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04)

    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/odoo-selfsigned.key -out /etc/ssl/certs/odoo-selfsigned.crt
    Generating a 2048 bit RSA private key
    ...........................................................................................................+++
    ...........................................................................................+++
    writing new private key to '/etc/ssl/private/odoo-selfsigned.key'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:ES
    State or Province Name (full name) [Some-State]:Valencia
    Locality Name (eg, city) []: Xàtiva
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:
    Organizational Unit Name (eg, section) []:
    Common Name (e.g. server FQDN or YOUR name) []: nom o domini
    Email Address []: correu@servidor.com

A continuació cal configurar el https en Nginx per a fer de proxy en
Odoo. [manual
oficial](https://www.odoo.com/documentation/9.0/setup/deploy.html#https)

En /etc/odoo.conf:

     proxy_mode = True 

En /etc/nginx/sites-enabled/odoo.conf:

    #odoo server
    upstream odoo {
     server 127.0.0.1:8069;
    }
    upstream odoochat {
     server 127.0.0.1:8072;
    }
    # S'han definit els upstream a localhost i als port determinats

    # http -> https (totes les peticions per HTTP se reformulen a HTTPS)
    server {
       listen 80;
       server_name _;                            
       # Si tinguerem nom de domini el ficariem, en altre cas: _
       rewrite ^(.*) https://$host$1 permanent;
    }

    server {
     listen 443;
     server_name _;
     # La _ perquè en l'exemple no tenim domini, com dalt
     proxy_read_timeout 720s;
     proxy_connect_timeout 720s;
     proxy_send_timeout 720s;

     # Add Headers for odoo proxy mode
     proxy_set_header X-Forwarded-Host $host;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
     proxy_set_header X-Real-IP $remote_addr;

     # SSL parameters
     ssl on;
     ssl_certificate /etc/ssl/certs/odoo-selfsigned.crt;
     ssl_certificate_key /etc/ssl/private/odoo-selfsigned.key ;
     # IMPORTANT: ficar bé les rutes dels certificats
     ssl_session_timeout 30m;
     ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
     ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
     ssl_prefer_server_ciphers on;

     # log
     access_log /var/log/nginx/odoo.access.log;
     error_log /var/log/nginx/odoo.error.log;

     # Redirect requests to odoo backend server
     location / {
       proxy_redirect off;
       proxy_pass http://odoo;
     }
     location /longpolling {
         proxy_pass http://odoochat;
     }

     # common gzip
     gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;
     gzip on;
    }

També cal esborrar el **default** de sites-enables de nginx o
modificar-lo per a que no afecte al port 80 d\'Odoo.

Ara es reinicien tanmt Odoo com nginx

## En Docker {#en_docker}

Aquest manual està originalment escrit per a Ubuntu 18.04

[Documentació
oficial](https://www.odoo.com/documentation/11.0/setup/install.html#setup-install-docker)
[Article sobre Docker i
Odoo](http://falconsolutions.cl/todo-sobre-de-docker-y-odoo-erp/)

En Docker és molt sencill desplegar Odoo, tan sols fa falta aquests
comandaments:

    # apt install docker.io
    # docker run -d --restart="always" -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo --name db postgres:9.4
    # docker run --restart="always" -p 8069:8069 --name odoo --link db:db -t odoo
    # docker stop odoo
    # docker start -a odoo

El primer comandament instal·la el servei Docker. El segon instal·la un
docker PostgreSQL amb una base de dades anomenada *odoo* i de
contrasenya odoo. El tercer crea un docker Odoo vinculat a l\'anterior
base de dades. Per entrar sols cal anar a la **direcció de
l\'amfitrió:8069** ja que el comandament indica que es redireccione per
\[Iptables\] el port 8069 al del contenidor.

Resultat d\'iptables:

    # iptables -L
    Chain INPUT (policy ACCEPT)
    target     prot opt source               destination         

    Chain FORWARD (policy ACCEPT)
    target     prot opt source               destination         
    DOCKER-USER  all  --  anywhere             anywhere            
    DOCKER-ISOLATION  all  --  anywhere             anywhere            
    ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
    DOCKER     all  --  anywhere             anywhere            
    ACCEPT     all  --  anywhere             anywhere            
    ACCEPT     all  --  anywhere             anywhere            

    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination         

    Chain DOCKER (1 references)
    target     prot opt source               destination         
    ACCEPT     tcp  --  anywhere             172.17.0.3           tcp dpt:8069

    Chain DOCKER-ISOLATION (1 references)
    target     prot opt source               destination         
    RETURN     all  --  anywhere             anywhere            

    Chain DOCKER-USER (1 references)
    target     prot opt source               destination         
    RETURN     all  --  anywhere             anywhere           

Si fem **ctrl-C** eixim sense parar el contenidor. si volem tornar a
entrar per veure els errors:

    # docker attach odoo

**Creació de mòduls**

Per a fer els nostres mòduls podem crear-los en un directori fora del
docker i executar-lo d\'aquesta manera:

    # docker run -v /path/to/addons:/mnt/extra-addons -p 8069:8069 --name odoo --link db:db -t odoo

Mentre estem fent nous mòduls, necessitem reiniciar el servici i
arrancar-lo actualitzant un mòdul. Primer deguem parar el docker,
després iniciar-lo indicant que vols entrar a la consola i finalment
actualitzar el mòdul.

    # docker stop odoo
    # docker start -a odoo
    # docker exec odoo odoo --config /etc/odoo/odoo.conf -u nommodul -d nombasededades -r odoo -w odoo --db_host 172.17.0.2 --db_port 5432

**Creació de mòduls, mètode 1**

Com es veu, el últim comandament és un poc complicat. Per tant, anem a
fer les coses totalment bé. Per a aixó necessitem un fitxer propi de
configuració d\'Odoo al que anomenarem **odoo.conf**. Podem utilitzar
aquesta plantilla:

    # docker exec odoo cat /etc/odoo/odoo.conf > odoo.conf

El que s\'ha fet és copiar el fitxer que té el docker per defecte. Si
l\'analitzem, no diu bé on està la base de dades, ja que aquesta
informació la passem amb el paràmetre **\--link** del **docker run**.
Nosaltres tenim que crear un directori i ficar dins el fitxer, editar-lo
i afegir aquesta informació:

    db_user = odoo
    db_password = odoo
    db_host = 172.17.0.2
    db_port = 5432

Ara ja podem arrancar el contenidor amb tot:

    # docker stop odoo
    # docker run --volumes-from odoo -v /home/jose/modules/:/mnt/extra-addons -v /home/jose/config/:/etc/odoo -p 8069:8069 --name odoo2 --link db:db -t odoo

Observem que tenim un directori per als nostres mòduls, un altre amb el
fitxer de configuració, la redirecció del port, el nom del nou mòdul,
l\'enllaç a la base de dades i el tipus de container.

Per últim, mentre tenim en marxa el servei, en una altra terminal podem
executar:

    # docker exec odoo odoo -u nommodul -d nombasededades

**Creació de mòduls, mètode 2**

El mètode anterior suposa l\'execució d\'un **docker run** molt complex.
Per evitar equivocar-nos, podem per un [docker
compose](https://docs.docker.com/compose/) com aquest:

    version: '2'
    services:
      db:
        container_name: db
        image: postgres:9.4
        network_mode: bridge
        environment:
          - POSTGRES_PASSWORD=odoo
          - POSTGRES_USER=odoo
          - PGDATA=/var/lib/postgresql/data/pgdata
        volumes:
          - odoo-db-data:/var/lib/postgresql/data/pgdata
      odoo:
        container_name: odoo
        image: odoo
        network_mode: bridge
        depends_on:
          - db
        ports:
          - "8069:8069"
        volumes:
          - odoo-web-data:/var/lib/odoo
          - /home/jose/config:/etc/odoo
          - /home/jose/modules:/mnt/extra-addons

    volumes:
      odoo-web-data:
      odoo-db-data:

Observem que declarem dos servicis i el **odoo** depen del **db**. També
cal dir quina xarxa utilitzen i la resta de dades que posem normalment
en el **run**.

Això ha d\'estar en un directori dins d\'un fitxer anomenat
**docker-compose.yml** i sols cal executar cada vegada:

    # docker-compose up

Cal dir que. d\'aquesta manera, el servici es para quan fem ctrl+c, per
tant, per a actualitzar un mòdul podem executar el docker exec en una
alta terminal.

**Altres coses**

Per a llançar més dockers amb odoo:

    # docker run -p 8070:8069 --name odoo2 --link db:db -t odoo
    # docker run -p 8071:8069 --name odoo3 --link db:db -t odoo

Si volem entrar en la base de dades postgreSQL per a fer coses
manualment, podem executar:

    # docker exec -ti db psql -U odoo
    # docker exec -ti db psql -U postgres

Executem el comandament psql de forma interactiva i amb l\'usuari odoo.
L\'usuari postgres és l\'administrador.

## Creació de una base de dades

```{admonition} Atenció
:class: tip

En general no cal fer aquest pas i és recomanable fer la base de dades per la interfície web.
```
En l\'usuari de odoo, creem una base de dades i li apliquem l\'esquema
de dades de Odoo:

     $ createdb --encoding=UTF-8 --template=template0 testdb
     $ odoo -d testdb

Aixó crea una base de dades amb les dades de prova per començar a
treballar.

Per defecte, l\'usuari serà admin amb contrasenya admin.

[Comandaments bàsics de
postgreSQL](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546)

## Errors documentats

```{admonition} Atenció
:class: tip

**Important** Abans de fer aquests comandaments, consulteu el final del
fitxer de log, generalment en /var/log/odoo/odoo-server.log
```
### Error amb el rol Odoo

Si apareix un error similar a:

`OperationalError: FATAL:  no existe el rol «odoo»`\
`OperationalError: FATAL:  role "odoo" does not exist`

Cal fer el comandament:

     su - postgres -c "createuser -s odoo"

Això crea l\'usuari odoo amb permís de superusuari (-s)

### Error amb UTF-8 

Moltes vegades, al instal·lar, no configura el template0 de la base de
dades en utf-8.
[1](http://www.postgresql.org/docs/9.3/static/manage-ag-templatedbs.html)

Es soluciona esborrant i tornant a crear la base de dades template1
utilitzant la codificació UTF8.
[2](https://gist.github.com/ffmike/877447)

     # su postgres
     $ psql
     postgres=# update pg_database set datallowconn = TRUE where datname = 'template0';
     postgres=# \c template0
     template0=# update pg_database set datistemplate = FALSE where datname = 'template1';
     template0=# drop database template1;
     template0=# create database template1 with template = template0 encoding = 'UTF8';
     template0=# update pg_database set datistemplate = TRUE where datname = 'template1';
     template0=# \c template1
     template1=# update pg_database set datallowconn = FALSE where datname = 'template0';

Pot ser que no es cree el cluster de postgresql. Primer cal reconfigurar
els locales y després:

     pg_createcluster 9.4 main --start

### Recuperar la contrasenya de l\'administrador

**De l\'administrador d\'un base de dades:** Dins de la base de dades:

     update res_users set password='test' where login='admin';

**De l\'administrador d\'Odoo**

Si no pots administrar o crear noves bases de dades, cal modficar la
línia **admin_passwd** de /etc/odoo/odoo.conf o .odoorc, depenent quin
fitxer de configuració estem utilitzant.

### Problemes en els repositoris oficials d\'ubuntu

En el cas de l\'IES, els repositoris oficials no funcionen bé per alguna
interferència amb els de Lliurex. Cal canviar-los. Per exemple per els
de Caliu. Una manera és entrar en **vim** i executar aquest comandament:

     :%s_http://archive.ubuntu.com/ubuntu_http://ftp.udc.es/ubuntu/_         

(Utilitzem \_ en compte de / en la subtitució perquè la / ja està en les
URL.)

### No connecta amb PostgreSQL 

Pot ser perquè no está el servici en funcionament.

     service postgresql [restart,start,stop,status]         

En cas de que falle, podem veure el log:

     cat /var/log/postrgresql/(versio)...        

De vegades la base de dades queda corrupta. Es pot intentar recuperar
amb:

     su - postgres -c '/usr/lib/postgresql/12/bin/pg_resetwal -f /var/lib/postgresql/12/main'

Si s\'han perdut dades, no són molt importants o tenim còpia de
seguretat, tal vegada cal eliminar la base de dades de la empresa que no
funciona:

     postgres$ psql
     psql> drop database <base de dades>;

## Enllaços

-   [Video de instalar Odoo
    manualmente](https://www.youtube.com/watch?v=IPjqbwA814Q).
-   [Video de configurar Odoo como
    servicio](https://www.youtube.com/watch?v=36XolOPbOFI).
-   [Vídeo de Copias de
    seguridad](https://www.youtube.com/watch?v=AvMXfYAD0PA).
