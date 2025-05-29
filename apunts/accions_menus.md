## Accions i menús

Diagrama de cóm es comporta el client web quan carrega Odoo per primera vegada i cóm crida a un action i carrega les vistes i les dades (records)

<!-- 
sequenceDiagram
    participant N as Navegador Web
    participant O as Servidor Odoo

    N->>O: GET / (port 8069)
    O->>N: index.html (bàsic)
    N->>O: GET JS i CSS QWeb 
    Note right of O: Crear els assets
    O->>N: Assets (JS i CSS) Templates

    Note left of N: Inicia Client Web

    N->>O: POST Load Views
    Note right of O: ir.ui.view
    O->>N: arch + json amb fields
    Note left of N: Polsem un menú

    N->>O: POST Load Action
    Note right of O: ir.ui.action
    O->>N: Definició de l'action

    N->>O: POST Load Views (per l'action)
    O->>N: Totes les vistes i fields

    N->>O: POST Search Read
    Note right of O: Select i compute
    O->>N: Json amb els records

    Note left of N: Analitza fields necessaris
    Note left of N: Renderitza la vista amb els records
-->

<div>
<svg aria-roledescription="sequence" role="graphics-document document" style="overflow: hidden; max-width: 100%; touch-action: none; user-select: none;" xmlns="http://www.w3.org/2000/svg" width="100%" id="graph-1" height="100%" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"><defs><symbol height="24" width="24" id="computer"><path d="M2 2v13h20v-13h-20zm18 11h-16v-9h16v9zm-10.228 6l.466-1h3.524l.467 1h-4.457zm14.228 3h-24l2-6h2.104l-1.33 4h18.45l-1.297-4h2.073l2 6zm-5-10h-14v-7h14v7z" transform="scale(.5)"></path></symbol></defs><defs><symbol clip-rule="evenodd" fill-rule="evenodd" id="database"><path d="M12.258.001l.256.004.255.005.253.008.251.01.249.012.247.015.246.016.242.019.241.02.239.023.236.024.233.027.231.028.229.031.225.032.223.034.22.036.217.038.214.04.211.041.208.043.205.045.201.046.198.048.194.05.191.051.187.053.183.054.18.056.175.057.172.059.168.06.163.061.16.063.155.064.15.066.074.033.073.033.071.034.07.034.069.035.068.035.067.035.066.035.064.036.064.036.062.036.06.036.06.037.058.037.058.037.055.038.055.038.053.038.052.038.051.039.05.039.048.039.047.039.045.04.044.04.043.04.041.04.04.041.039.041.037.041.036.041.034.041.033.042.032.042.03.042.029.042.027.042.026.043.024.043.023.043.021.043.02.043.018.044.017.043.015.044.013.044.012.044.011.045.009.044.007.045.006.045.004.045.002.045.001.045v17l-.001.045-.002.045-.004.045-.006.045-.007.045-.009.044-.011.045-.012.044-.013.044-.015.044-.017.043-.018.044-.02.043-.021.043-.023.043-.024.043-.026.043-.027.042-.029.042-.03.042-.032.042-.033.042-.034.041-.036.041-.037.041-.039.041-.04.041-.041.04-.043.04-.044.04-.045.04-.047.039-.048.039-.05.039-.051.039-.052.038-.053.038-.055.038-.055.038-.058.037-.058.037-.06.037-.06.036-.062.036-.064.036-.064.036-.066.035-.067.035-.068.035-.069.035-.07.034-.071.034-.073.033-.074.033-.15.066-.155.064-.16.063-.163.061-.168.06-.172.059-.175.057-.18.056-.183.054-.187.053-.191.051-.194.05-.198.048-.201.046-.205.045-.208.043-.211.041-.214.04-.217.038-.22.036-.223.034-.225.032-.229.031-.231.028-.233.027-.236.024-.239.023-.241.02-.242.019-.246.016-.247.015-.249.012-.251.01-.253.008-.255.005-.256.004-.258.001-.258-.001-.256-.004-.255-.005-.253-.008-.251-.01-.249-.012-.247-.015-.245-.016-.243-.019-.241-.02-.238-.023-.236-.024-.234-.027-.231-.028-.228-.031-.226-.032-.223-.034-.22-.036-.217-.038-.214-.04-.211-.041-.208-.043-.204-.045-.201-.046-.198-.048-.195-.05-.19-.051-.187-.053-.184-.054-.179-.056-.176-.057-.172-.059-.167-.06-.164-.061-.159-.063-.155-.064-.151-.066-.074-.033-.072-.033-.072-.034-.07-.034-.069-.035-.068-.035-.067-.035-.066-.035-.064-.036-.063-.036-.062-.036-.061-.036-.06-.037-.058-.037-.057-.037-.056-.038-.055-.038-.053-.038-.052-.038-.051-.039-.049-.039-.049-.039-.046-.039-.046-.04-.044-.04-.043-.04-.041-.04-.04-.041-.039-.041-.037-.041-.036-.041-.034-.041-.033-.042-.032-.042-.03-.042-.029-.042-.027-.042-.026-.043-.024-.043-.023-.043-.021-.043-.02-.043-.018-.044-.017-.043-.015-.044-.013-.044-.012-.044-.011-.045-.009-.044-.007-.045-.006-.045-.004-.045-.002-.045-.001-.045v-17l.001-.045.002-.045.004-.045.006-.045.007-.045.009-.044.011-.045.012-.044.013-.044.015-.044.017-.043.018-.044.02-.043.021-.043.023-.043.024-.043.026-.043.027-.042.029-.042.03-.042.032-.042.033-.042.034-.041.036-.041.037-.041.039-.041.04-.041.041-.04.043-.04.044-.04.046-.04.046-.039.049-.039.049-.039.051-.039.052-.038.053-.038.055-.038.056-.038.057-.037.058-.037.06-.037.061-.036.062-.036.063-.036.064-.036.066-.035.067-.035.068-.035.069-.035.07-.034.072-.034.072-.033.074-.033.151-.066.155-.064.159-.063.164-.061.167-.06.172-.059.176-.057.179-.056.184-.054.187-.053.19-.051.195-.05.198-.048.201-.046.204-.045.208-.043.211-.041.214-.04.217-.038.22-.036.223-.034.226-.032.228-.031.231-.028.234-.027.236-.024.238-.023.241-.02.243-.019.245-.016.247-.015.249-.012.251-.01.253-.008.255-.005.256-.004.258-.001.258.001zm-9.258 20.499v.01l.001.021.003.021.004.022.005.021.006.022.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.023.018.024.019.024.021.024.022.025.023.024.024.025.052.049.056.05.061.051.066.051.07.051.075.051.079.052.084.052.088.052.092.052.097.052.102.051.105.052.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.048.144.049.147.047.152.047.155.047.16.045.163.045.167.043.171.043.176.041.178.041.183.039.187.039.19.037.194.035.197.035.202.033.204.031.209.03.212.029.216.027.219.025.222.024.226.021.23.02.233.018.236.016.24.015.243.012.246.01.249.008.253.005.256.004.259.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.021.224-.024.22-.026.216-.027.212-.028.21-.031.205-.031.202-.034.198-.034.194-.036.191-.037.187-.039.183-.04.179-.04.175-.042.172-.043.168-.044.163-.045.16-.046.155-.046.152-.047.148-.048.143-.049.139-.049.136-.05.131-.05.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.053.083-.051.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.05.023-.024.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.023.01-.022.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.127l-.077.055-.08.053-.083.054-.085.053-.087.052-.09.052-.093.051-.095.05-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.045-.118.044-.12.043-.122.042-.124.042-.126.041-.128.04-.13.04-.132.038-.134.038-.135.037-.138.037-.139.035-.142.035-.143.034-.144.033-.147.032-.148.031-.15.03-.151.03-.153.029-.154.027-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.01-.179.008-.179.008-.181.006-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.006-.179-.008-.179-.008-.178-.01-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.027-.153-.029-.151-.03-.15-.03-.148-.031-.146-.032-.145-.033-.143-.034-.141-.035-.14-.035-.137-.037-.136-.037-.134-.038-.132-.038-.13-.04-.128-.04-.126-.041-.124-.042-.122-.042-.12-.044-.117-.043-.116-.045-.113-.045-.112-.046-.109-.047-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.05-.093-.052-.09-.051-.087-.052-.085-.053-.083-.054-.08-.054-.077-.054v4.127zm0-5.654v.011l.001.021.003.021.004.021.005.022.006.022.007.022.009.022.01.022.011.023.012.023.013.023.015.024.016.023.017.024.018.024.019.024.021.024.022.024.023.025.024.024.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.052.11.051.114.051.119.052.123.05.127.051.131.05.135.049.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.044.171.042.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.022.23.02.233.018.236.016.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.012.241-.015.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.048.139-.05.136-.049.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.051.051-.049.023-.025.023-.024.021-.025.02-.024.019-.024.018-.024.017-.024.015-.023.014-.023.013-.024.012-.022.01-.023.01-.023.008-.022.006-.022.006-.022.004-.021.004-.022.001-.021.001-.021v-4.139l-.077.054-.08.054-.083.054-.085.052-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.044-.118.044-.12.044-.122.042-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.035-.143.033-.144.033-.147.033-.148.031-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.009-.179.009-.179.007-.181.007-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.007-.179-.007-.179-.009-.178-.009-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.031-.146-.033-.145-.033-.143-.033-.141-.035-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.04-.126-.041-.124-.042-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.051-.093-.051-.09-.051-.087-.053-.085-.052-.083-.054-.08-.054-.077-.054v4.139zm0-5.666v.011l.001.02.003.022.004.021.005.022.006.021.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.024.018.023.019.024.021.025.022.024.023.024.024.025.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.051.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.043.171.043.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.021.23.02.233.018.236.017.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.013.241-.014.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.049.139-.049.136-.049.131-.051.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.049.023-.025.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.022.01-.023.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.153l-.077.054-.08.054-.083.053-.085.053-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.048-.105.048-.106.048-.109.046-.111.046-.114.046-.115.044-.118.044-.12.043-.122.043-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.034-.143.034-.144.033-.147.032-.148.032-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.024-.161.024-.162.023-.163.023-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.01-.178.01-.179.009-.179.007-.181.006-.182.006-.182.004-.184.003-.184.001-.185.001-.185-.001-.184-.001-.184-.003-.182-.004-.182-.006-.181-.006-.179-.007-.179-.009-.178-.01-.176-.01-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.023-.162-.023-.161-.024-.159-.024-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.032-.146-.032-.145-.033-.143-.034-.141-.034-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.041-.126-.041-.124-.041-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.048-.105-.048-.102-.048-.1-.05-.097-.049-.095-.051-.093-.051-.09-.052-.087-.052-.085-.053-.083-.053-.08-.054-.077-.054v4.153zm8.74-8.179l-.257.004-.254.005-.25.008-.247.011-.244.012-.241.014-.237.016-.233.018-.231.021-.226.022-.224.023-.22.026-.216.027-.212.028-.21.031-.205.032-.202.033-.198.034-.194.036-.191.038-.187.038-.183.04-.179.041-.175.042-.172.043-.168.043-.163.045-.16.046-.155.046-.152.048-.148.048-.143.048-.139.049-.136.05-.131.05-.126.051-.123.051-.118.051-.114.052-.11.052-.106.052-.101.052-.096.052-.092.052-.088.052-.083.052-.079.052-.074.051-.07.052-.065.051-.06.05-.056.05-.051.05-.023.025-.023.024-.021.024-.02.025-.019.024-.018.024-.017.023-.015.024-.014.023-.013.023-.012.023-.01.023-.01.022-.008.022-.006.023-.006.021-.004.022-.004.021-.001.021-.001.021.001.021.001.021.004.021.004.022.006.021.006.023.008.022.01.022.01.023.012.023.013.023.014.023.015.024.017.023.018.024.019.024.02.025.021.024.023.024.023.025.051.05.056.05.06.05.065.051.07.052.074.051.079.052.083.052.088.052.092.052.096.052.101.052.106.052.11.052.114.052.118.051.123.051.126.051.131.05.136.05.139.049.143.048.148.048.152.048.155.046.16.046.163.045.168.043.172.043.175.042.179.041.183.04.187.038.191.038.194.036.198.034.202.033.205.032.21.031.212.028.216.027.22.026.224.023.226.022.231.021.233.018.237.016.241.014.244.012.247.011.25.008.254.005.257.004.26.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.022.224-.023.22-.026.216-.027.212-.028.21-.031.205-.032.202-.033.198-.034.194-.036.191-.038.187-.038.183-.04.179-.041.175-.042.172-.043.168-.043.163-.045.16-.046.155-.046.152-.048.148-.048.143-.048.139-.049.136-.05.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.05.051-.05.023-.025.023-.024.021-.024.02-.025.019-.024.018-.024.017-.023.015-.024.014-.023.013-.023.012-.023.01-.023.01-.022.008-.022.006-.023.006-.021.004-.022.004-.021.001-.021.001-.021-.001-.021-.001-.021-.004-.021-.004-.022-.006-.021-.006-.023-.008-.022-.01-.022-.01-.023-.012-.023-.013-.023-.014-.023-.015-.024-.017-.023-.018-.024-.019-.024-.02-.025-.021-.024-.023-.024-.023-.025-.051-.05-.056-.05-.06-.05-.065-.051-.07-.052-.074-.051-.079-.052-.083-.052-.088-.052-.092-.052-.096-.052-.101-.052-.106-.052-.11-.052-.114-.052-.118-.051-.123-.051-.126-.051-.131-.05-.136-.05-.139-.049-.143-.048-.148-.048-.152-.048-.155-.046-.16-.046-.163-.045-.168-.043-.172-.043-.175-.042-.179-.041-.183-.04-.187-.038-.191-.038-.194-.036-.198-.034-.202-.033-.205-.032-.21-.031-.212-.028-.216-.027-.22-.026-.224-.023-.226-.022-.231-.021-.233-.018-.237-.016-.241-.014-.244-.012-.247-.011-.25-.008-.254-.005-.257-.004-.26-.001-.26.001z" transform="scale(.5)"></path></symbol></defs><defs><symbol height="24" width="24" id="clock"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.848 12.459c.202.038.202.333.001.372-1.907.361-6.045 1.111-6.547 1.111-.719 0-1.301-.582-1.301-1.301 0-.512.77-5.447 1.125-7.445.034-.192.312-.181.343.014l.985 6.238 5.394 1.011z" transform="scale(.5)"></path></symbol></defs><defs><marker orient="auto-start-reverse" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="7.9" id="arrowhead"><path d="M -1 0 L 10 5 L 0 10 z"></path></marker></defs><defs><marker refY="4.5" refX="4" orient="auto" markerHeight="8" markerWidth="15" id="crosshead"><path d="M 1,2 L 6,7 M 6,2 L 1,7" stroke-width="1pt" style="stroke-dasharray: 0px, 0px;" stroke="#000000" fill="none"></path></marker></defs><defs><marker orient="auto" markerHeight="28" markerWidth="20" refY="7" refX="15.5" id="filled-head"><path d="M 18,7 L9,13 L14,7 L9,1 Z"></path></marker></defs><defs><marker orient="auto" markerHeight="40" markerWidth="60" refY="15" refX="15" id="sequencenumber"><circle r="6" cy="15" cx="15"></circle></marker></defs><g id="viewport-20250529144425758" class="svg-pan-zoom_viewport" transform="matrix(0.6925618648529053,0,0,0.6925618648529053,486.3194885253906,31.850482940673828)" style="transform: matrix(0.692562, 0, 0, 0.692562, 486.32, 31.8505);"><g><rect class="actor actor-bottom" ry="3" rx="3" name="O" height="65" width="150" stroke="#666" fill="#eaeaea" y="1053" x="310"></rect><text class="actor actor-box" alignment-baseline="central" dominant-baseline="central" style="text-anchor: middle; font-size: 16px; font-weight: 400;" y="1085.5" x="385"><tspan dy="0" x="385">Servidor Odoo</tspan></text></g><g><rect class="actor actor-bottom" ry="3" rx="3" name="N" height="65" width="150" stroke="#666" fill="#eaeaea" y="1053" x="0"></rect><text class="actor actor-box" alignment-baseline="central" dominant-baseline="central" style="text-anchor: middle; font-size: 16px; font-weight: 400;" y="1085.5" x="75"><tspan dy="0" x="75">Navegador Web</tspan></text></g><g><line name="O" stroke="#999" stroke-width="0.5px" class="actor-line 200" y2="1053" x2="385" y1="65" x1="385" id="actor1"></line><g id="root-1"><rect class="actor actor-top" ry="3" rx="3" name="O" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="310"></rect><text class="actor actor-box" alignment-baseline="central" dominant-baseline="central" style="text-anchor: middle; font-size: 16px; font-weight: 400;" y="32.5" x="385"><tspan dy="0" x="385">Servidor Odoo</tspan></text></g></g><g><line name="N" stroke="#999" stroke-width="0.5px" class="actor-line 200" y2="1053" x2="75" y1="65" x1="75" id="actor0"></line><g id="root-0"><rect class="actor actor-top" ry="3" rx="3" name="N" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="0"></rect><text class="actor actor-box" alignment-baseline="central" dominant-baseline="central" style="text-anchor: middle; font-size: 16px; font-weight: 400;" y="32.5" x="75"><tspan dy="0" x="75">Navegador Web</tspan></text></g></g><style>#graph-1{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#graph-1 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#graph-1 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#graph-1 .error-icon{fill:#552222;}#graph-1 .error-text{fill:#552222;stroke:#552222;}#graph-1 .edge-thickness-normal{stroke-width:1px;}#graph-1 .edge-thickness-thick{stroke-width:3.5px;}#graph-1 .edge-pattern-solid{stroke-dasharray:0;}#graph-1 .edge-thickness-invisible{stroke-width:0;fill:none;}#graph-1 .edge-pattern-dashed{stroke-dasharray:3;}#graph-1 .edge-pattern-dotted{stroke-dasharray:2;}#graph-1 .marker{fill:#333333;stroke:#333333;}#graph-1 .marker.cross{stroke:#333333;}#graph-1 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#graph-1 p{margin:0;}#graph-1 .actor{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#graph-1 text.actor&gt;tspan{fill:black;stroke:none;}#graph-1 .actor-line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);}#graph-1 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#graph-1 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#graph-1 #arrowhead path{fill:#333;stroke:#333;}#graph-1 .sequenceNumber{fill:white;}#graph-1 #sequencenumber{fill:#333;}#graph-1 #crosshead path{fill:#333;stroke:#333;}#graph-1 .messageText{fill:#333;stroke:none;}#graph-1 .labelBox{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#graph-1 .labelText,#graph-1 .labelText&gt;tspan{fill:black;stroke:none;}#graph-1 .loopText,#graph-1 .loopText&gt;tspan{fill:black;stroke:none;}#graph-1 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);}#graph-1 .note{stroke:#aaaa33;fill:#fff5ad;}#graph-1 .noteText,#graph-1 .noteText&gt;tspan{fill:black;stroke:none;}#graph-1 .activation0{fill:#f4f4f4;stroke:#666;}#graph-1 .activation1{fill:#f4f4f4;stroke:#666;}#graph-1 .activation2{fill:#f4f4f4;stroke:#666;}#graph-1 .actorPopupMenu{position:absolute;}#graph-1 .actorPopupMenuPanel{position:absolute;fill:#ECECFF;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#graph-1 .actor-man line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#graph-1 .actor-man circle,#graph-1 line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;stroke-width:2px;}#graph-1 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g></g><g><rect class="note" height="39" width="150" stroke="#666" fill="#EDF2AE" y="219" x="410"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="224" x="485"><tspan x="485">Crear els assets</tspan></text></g><g><rect class="note" height="39" width="157" stroke="#666" fill="#EDF2AE" y="316" x="-107"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="321" x="-28"><tspan x="-28">Inicia Client Web</tspan></text></g><g><rect class="note" height="39" width="150" stroke="#666" fill="#EDF2AE" y="413" x="410"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="418" x="485"><tspan x="485">ir.ui.view</tspan></text></g><g><rect class="note" height="39" width="150" stroke="#666" fill="#EDF2AE" y="510" x="-100"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="515" x="-25"><tspan x="-25">Polsem un menú</tspan></text></g><g><rect class="note" height="39" width="150" stroke="#666" fill="#EDF2AE" y="607" x="410"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="612" x="485"><tspan x="485">ir.ui.action</tspan></text></g><g><rect class="note" height="39" width="153" stroke="#666" fill="#EDF2AE" y="848" x="410"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="853" x="487"><tspan x="487">Select i compute</tspan></text></g><g><rect class="note" height="39" width="228" stroke="#666" fill="#EDF2AE" y="945" x="-178"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="950" x="-64"><tspan x="-64">Analitza fields necessaris</tspan></text></g><g><rect class="note" height="39" width="304" stroke="#666" fill="#EDF2AE" y="994" x="-254"></rect><text dy="1em" class="noteText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="999" x="-102"><tspan x="-102">Renderitza la vista amb els records</tspan></text></g><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="80" x="229">GET / (port 8069)</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="113" x2="381" y1="113" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="128" x="232">index.html (bàsic)</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="161" x2="79" y1="161" x1="384"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="176" x="229">GET JS i CSS QWeb</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="209" x2="381" y1="209" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="273" x="232">Assets (JS i CSS) Templates</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="306" x2="79" y1="306" x1="384"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="370" x="229">POST Load Views</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="403" x2="381" y1="403" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="467" x="232">arch + json amb fields</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="500" x2="79" y1="500" x1="384"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="564" x="229">POST Load Action</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="597" x2="381" y1="597" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="661" x="232">Definició de l'action</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="694" x2="79" y1="694" x1="384"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="709" x="229">POST Load Views (per l'action)</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="742" x2="381" y1="742" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="757" x="232">Totes les vistes i fields</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="790" x2="79" y1="790" x1="384"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="805" x="229">POST Search Read</text><line marker-end="url(#arrowhead)" style="fill: none;" stroke="none" stroke-width="2" class="messageLine0" y2="838" x2="381" y1="838" x1="76"></line><text dy="1em" class="messageText" style="font-size: 16px; font-weight: 400;" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="902" x="232">Json amb els records</text><line marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" style="stroke-dasharray: 3px, 3px; fill: none;" y2="935" x2="79" y1="935" x1="384"></line></g></svg>
</div>


    +----------------------+                            +----------------------+
    |                      | GET / al port 8069         |                      |
    |    Navegador Web     +--------------------------> |    Servidor Odoo     |
    |                      |                            |                      |
    +----------------------+  index.html (bàsic)        |                      |
    |  Enllaços a JS i CSS <----------------------------+                      |
    +----------------------+                            |                      |
    |                      | GET JS i CSS  Qweb         +----------------------+
    |                      +----------------------------> Crea els Assets      |
    |                      |                            +----------------------+
    +----------------------+ CSS i JS ASSETS Templates  |                      |
    | Inicia Client Web    <----------------------------+                      |
    +----------------------+                            |                      |
    |                      | POST Load Views            +----------------------+
    |                      +----------------------------> ir.ui.view           |
    |                      | arch i json amb els fields |                      |
    |                      +<---------------------------+                      |
    |                      |                            +----------------------+
    +----------------------+ POST load action           +----------------------+
    |  Pulsem un menú      +----------------------------> ir.ui.action         |
    +----------------------+ Definició de l'action      |                      |
    |                      <----------------------------+                      |
    | l'Action necessita   |                            +----------------------+
    | vistes               | POST Load Views            |                      |
    |                      +---------------------------->  ir.ui.view          |
    |                      | Totes les vistes i fields  |                      |
    | El client analitza   <----------------------------+                      |
    | quins field necessita| POST Search read           +----------------------+
    +---------------------------------------------------> Selecciona i computa |
    |                      | Json amb els records       | el fields            |
    |El client renderitza  <---------------------------------------------------+
    |la vista amb els      |                            |                      |
    |records               |                            |                      |
    +----------------------+                            +----------------------+

El client web de Odoo conté uns menús dalt i a l\'esquerra. Aquests
menús, al ser accionats mostren altres menús i les pantalles del
programa. Quant pulsem en un menú, canvia la pantalla perquè hem fet una
[acció](https://www.odoo.com/documentation/12.0/reference/actions.html).

Una acció bàsicament té:

- **type**: El tipus d\'acció que és i cóm l\'acció és interpretada.
    Quan la definim en el XML, el type no cal especificar-lo, ja que ho
    indica el model en que es guarda.
- **name**: El nom, que pot ser mostrat en la pantalla o no. Es
    recomana que siga llegible per els humans.

Les accions i els menús es declaren en fitxers de dades en XML o
dirèctament si una funció retorna un diccionari que la defineix. Les
accions poden ser cridades de tres maneres:

- Fent clic en un menú.
- Fent clic en botons de les vistes (han d\'estar connectats amb
    accions).
- Com accions contextuals en els objectes.

D\'aquesta manera, el client web pot saber quina acció ha d\'executar si
rep alguna d\'aquestes coses:

- **false**: Indica que s\'ha de tancar el diàleg actual.
- **Una string**: Amb l\'etiqueta de **l\'acció de client** a
    executar.
- **Un número**: Amb el ID o external ID de l\'acció a trobar a la
    base de dades.
- **Un diccionari**: Amb la definició de l\'acció, aquesta no està ni
    en XML ni en la base de dades. En general, és la manera de cridar a
    un action al finalitzar una funció.

### Accions tipus *window*

Les accions *window* són un record més (**ir.actions.act_window**). No
obstant, els menús que les criden, tenen una manera més ràpida de ser
declarats amb una etiqueta **menuitem**:

``` xml
<record model="ir.actions.act_window" id="action_list_ideas">
    <field name="name">Ideas</field>
    <field name="res_model">idea.idea</field>
    <field name="view_mode">tree,form</field>
</record>
<menuitem id="menu_ideas" parent="menu_root" name="Ideas" sequence="10"
          action="action_list_ideas"/>
```

```{tip}
Les accions han de ser declarades al XML abans que els menús que les accionen. 
```

```{tip}
El que hem vist en esta secció és la definició d'una acció en un XML com a part de la vista, però una acció no és més que una forma còmoda d'escriure moltes coses que farà el client en javascript per demanar alguna cosa al servidor. Els actions separen i simplifiquen el desenvolupament de la interfície d'usuari que és el client web. Un menú o botó en html acciona una funció javascript que en principi no sap el que fer. Aquesta demana que es carregue la definició del seu action. Una vegada carregada la definició, queda clar tot el que ha de demanar (les vistes, context, dominis, vistes search, lloc on carregar-ho tot...) aleshores demana les vistes i amb ajuda de les vistes i els fields, demana els records que són les dades a mostrar. Per tant, un action és la definició sense programar javascript de coses que ha de fer el javascript. Odoo permet declarar actions com a resposta de funcions. Aquestes actions no estan en la base de dades, però són enviades igualment al client i el client fa en elles el mateix que en un action que ell ha demanat. Un exemple d'això són els actions que retornen els botons dels wizards. De fet, podem fer que un botó torne un action i, per tant, obrir una vista diferent. 
```

Aquest exemple és una funció cridada per un botó que retorna un action:

``` python
    @api.multi    # Molt important que siga multi.
    def create_comments(self):
       clients=self.env['reserves.bookings'].search([('checking_day','<',fields.Date.today()),('room.hotel','=',self.id)]).mapped('client').ids
       print(clients)
       if len(clients)>0:
        print(clients)
        random.shuffle(clients)
        comment = self.env['reserves.comments'].create({'hotel':self.id,'client':clients[0],'stars':str(random.randint(1,5))})
        return {
    'name': 'Comment',
    'view_type': 'form',
    'view_mode': 'form',
    'res_model': 'reserves.comments',
    'res_id': comment.id,
    #'view_id': self.env.ref('reserves.comments_form').id,
    'type': 'ir.actions.act_window',
    'target': 'current',
         }
```

Observem que li pasem el model i el res_id per a que puga obrir un
formulari amb el comentari creat.

Aquest és el json que rep el client després de cridar al botó:

``` javascript
{
   "jsonrpc":"2.0",
   "id":878622456,
   "result":{
      "name":"Comment",
      "view_mode":"form",
      "res_model":"reserves.comments",
      "res_id":20,
      "type":"ir.actions.act_window",
      "target":"current",
      "flags":{ },
      "views":[[false,"form"]]
   }
}
```

Ara el client pot demanar un formulari i el record corresponent al model
*reserves.comments* i el id *20*.

Anem a veure en detall tots els fields que tenen aquestes accions:

- **res_model**: El model del que mostrarà les vistes.
- **views**: Una llista de parelles en el ID de la vista i el tipus.
    En cas de que no sabem el ID de la vista, podem ficar **false** i
    triarà o crearà una per defecte. Observem l\'exemple anterior, on en
    la declaració de l\'acció no s\'especifica aquest field, però el
    client si acaba rebent-lo amb
    **\"views\":**. La llista
    de vistes la trau automàticament amb la funció
    **[fields_view_get()](https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.models.Model.fields_view_get)**.
- **res_id**: (Opcional) Si es va a mostrar un form, indica la ID del
    record que es va a mostrar.
- **search_view_id**: (Opcional) Se li pasa (id, name) on id
    respresenta el ID de la vista search que es mostrarà.
- **target**: (Opcional) El destí del action. Per defecte és en la
    finestra actual (**current**), encara que pot ser a tota la pantalla
    (**full_screen**) o en un diàleg o *pop-up* (**new**) o **main** en
    cas de voler que es veja en la finestra actual sense les
    *breadcrumbs*, el que vol dir que elimina el rastre d\'on vé
    l\'acció.
- **context**: (Opcional)Informació addicional.
- **domain**: (Opcional) Aplica un filtre als registres que es demanaran a la base de dades.
- **limit**: (Opcional) Per defecte 80, és la quantitat de records que
    mostrar en la vista tree.
- **auto-search**: (Opcional) En cas de que necessitem una búsqueda
    només carregar la vista.

Exemples d\'Actions declarades en python:

``` python
# Action per obrir arbre i form:
{
    "type": "ir.actions.act_window",
    "res_model": "res.partner",
    "views": [[False, "tree"], [False, "form"]],
    "domain": [["customer", "=", true]],
}
# Action sols per a form en un id específic.
{
    "type": "ir.actions.act_window",
    "res_model": "product.product",
    "views": [[False, "form"]],
    "res_id": a_product_id,
    "target": "new",
}
# Action que ja està en la base de dades:
       action = self.env.ref('terraform.new_building_type_action_window').read()[0]
       return action
```

Quan guardem una action en la base de dades, normalment definint-la com
un XML, tenim aquest altres fields:

- **view_mode**: Lista separada per comes de les vistes que ha de
    mostrar. Una vegada el servidor va a enviar aquest action al client,
    amb açò generarà el field **views**.
- **view_ids**: Una llista d\'objectes de vista que permet definir la
    vista de la primera part de **views**. Aquesta llista és un
    Many2many amb les vistes i la taula intermitja es diu
    **ir.actions.act_window.view**.
- **view_id**: Una vista específica a afegir a **views**.

Per tant, si volem definir les vistes que volem que mostre el action,
podem omplir els camps anteriors. El servidor observa la llista de
**view_ids** i afegeix el **view_id**. Si no ompli tot el definit en
**view_mode**, acaba d\'omplir el field **views** (el que envía als
clients) amb (False,`<tipus>`). Exemple de cóm especificar una
vista en un action:

``` python
<field name="view_ids" eval="[(5, 0, 0),(0, 0, {'view_mode': 'tree', 'view_id': ref('tree_external_id')}),(0, 0, {'view_mode': 'form', 'view_id': ref('form_external_id')}),]" />
```

En els fitxers de dades, aquesta sintaxi és per a modificar fields Many2many. El **(5,0,0)** per
a desvincular les possibles vistes. El **(0,0,`<record>`{=html})** per
crear un nou record i vincular-ho. En aquest cas, crea un record amb els
dos fields necessaris, el tipus de vista i el External ID de la vista a
vincular.

Això també es pot fer més explícitament insertant records en **ir.actions.act_window.view**.

### Accions tipus URL {#accions_tipus_url}

Aquestes accions símplement obrin un URL. Exemple:

``` python
{
    "type": "ir.actions.act_url",
    "url": "http://odoo.com",
    "target": "self",     # Target pot ser self o new per reemplaçar el contingut de la pestanya del navegador o obrir una nova.
}
```

### Accions tipus Server {#accions_tipus_server}

Les accions tipus server funcionen en un model base i poden ser
executades automàticament o amb el menú contextual d\'acció que es veu
dalt en la vista.

Les accions que pot fer un server action són:

- Executar un **codi python**. Amb un bloc de codi que serà executat
    al servidor.
- Crear un **nou record**.
- **Escriure** en un record existent.
- Executar **varies accions**. Per poder executar varies accions
    server.

Com es pot veure al codi de les server action:

``` python
 state = fields.Selection([
        ('code', 'Execute Python Code'),
        ('object_create', 'Create a new Record'),
        ('object_write', 'Update the Record'),
        ('multi', 'Execute several actions')], string='Action To Do',
        default='object_write', required=True,
        help="Type of server action. The following values are available:\n"
             "- 'Execute Python Code': a block of python code that will be executed\n"
             "- 'Create': create a new record with new values\n"
             "- 'Update a Record': update the values of a record\n"
             "- 'Execute several actions': define an action that triggers several other   

 server actions\n"
             "- 'Send Email': automatically send an email (Discuss)\n"
             "- 'Add Followers': add followers to a record (Discuss)\n"
             "- 'Create Next Activity': create an activity (Discuss)")
```

Permet executar codi en el servidor. És una acció molt genèrica que pot,
inclús retornar una acció tipus window. Les accions tipus server són una
forma més genèrica del que fa el button tipus **object**.

Vejem un exemple:

``` xml
<record model="ir.actions.server" id="print_instance">
    <field name="name">Res Partner Server Action</field>
    <field name="model_id" ref="model_res_partner"/>
    <field name="state">code</field>
    <field name="code">
        raise Warning(model._name)
    </field>
</record>
```

En l\'exemple anterior podem veure les característiques bàsiques:

- **ir.action.server**: El nom del model on es guardarà.
- **model_id**: És l\'equivalent a **res_model** en les accions tipus
    window. Es tracta del model sobre el que treballarà l\'action.
- **code**: Troç de codi que executarà. Pot ser un python complex o el
    nom d\'un mètode que ja tinga el model.

El servidor rebrà del client la ordre d\'executar eixe action. Eixa
ordre és un **Json** en el que sols es diu la **action_id** del action i
el context. Dins del context, tenim coses com els **active_id,
active_ids** o el **active_model**. El servidor executa sobre eixe model
el codi que diu l\'action. En l\'exemple anterior, simplement diu una
alerta.

El codi del action server pot definir una variable anomenada **action**
que retornarà al client la seguent acció a executar. Aquesta pot ser
window, això pot servir per refescar la pàgina o enviar a una altra.
Exemple:

``` xml
<record model="ir.actions.server" id="print_instance">
    <field name="name">Res Partner Server Action</field>
    <field name="model_id" ref="model_res_partner"/>
    <field name="state">code</field>
    <field name="code">
        if object.some_condition():
            action = {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": model._name,
                "res_id": object.id,
            }
    </field>
</record>
```

Però no sempre s\'utilitza l\'etiqueta **code**. Això depen d\'una altra
anomenada **state** que pot tindre el tipus d\'acció de servidor. Estan
disponibles els següents valors:

- **code** : Executar codi Python\': un bloc de codi Python que serà
    executat. En el cas d\'utilitzar code, el codi té accés a algunes
    variables específiques:
  - **env**: *Enviroment* d\'Odoo en el que l\'action s\'executa.
  - **model**: Model en que s\'executa. Es tracta d\'un
        **recordset** buit.
  - **record**: El registre en que s\'executa l\'acció.
  - **records**: Recordset de tots els registres en que s\'executa
        l\'acció (si es cridada per un tree, per exemple)
  - **time, datetime, dateutil, timezone** Bilioteques Python útils
        (**són python pures, no d\'odoo**)
  - **log(message, level=\'info\')**: Per enviar missatges al log.
  - **Warning** per llançar una excepció amb **raise**.
  - **action={\...}** per llançar una acció.
- **object_create**: Crear o duplicar un nou registre: crea un nou
    registre amb nous valors, o duplica un d\'existent a la base de
    dades
- **object_write**: Escriure en un registre: actualitza els valors
    d\'un registre
- **multi**: Executar diverses accions: defineix una acció que llança
    altres diverses accions de servidor
- **followers**: Afegir seguidors: afegeix seguidors a un registre
    (disponible a Discuss)
- **email**: Enviar un correu electrònic: envia automàticament un
    correu electrònic (disponible a email_template)

Exemple complet de action tipus server. (No fa res útil, però es pot
veure cóm s\'utilitza tot):

``` xml
    <record model="ir.actions.server" id="escoleta.creaar_dia_menjador">
    <field name="name">Creacio de un dia de menjador a partir d'una plantilla d'alumnes</field>
    <field name="model_id" ref="model_escoleta_menjador"/>
    <field name="state">code</field>
    <field name="code">
for r in records:
     fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     env['escoleta.menjador_day'].create({'name':fecha,'day':r.id})
     log('creat dia menjador',level='info')
     for s in r.students:
      log('creat alumne',level='info')
      env['escoleta.student_day'].create({'name':str(s.name)+" "+str(fecha),'student':s.id,'menjador_day':r.id})
action = {
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "escoleta.menjador_day",
         }

    </field>
    <field name="binding_model_id" ref="escoleta.model_escoleta_menjador"/>
</record>
```

L\'exemple anterior mostra cóm podem crear un action server i executar
coses complexes en el servidor sense modificar el codi python del model.
Però açò té varis inconvenients: El primer és que estem desplaçant la
tasca del controlador a la vista o a una part en mig entre la vista i el
controlador. El segon inconvenient és que és més complicat escriure codi
python dins d\'un XML sense equivocar-se en la indentació. I el
inconvenient més important és que no tenim accés a totes les funcions
del ORM i biblioteques útils d\'Odoo del controlador. Per tant, és
recomanable crear una funció en el model i cridar-la:

``` xml
    <record model="ir.actions.server" id="escoleta.creaar_dia_menjador">
    <field name="name">Creacio de un dia de menjador a partir d'una plantilla d'alumnes</field>
    <field name="model_id" ref="model_escoleta_menjador"/>
    <field name="state">code</field>
    <field name="code">
action=model.crear_dia_menjador()      # Assignar el resultat de la funció a action per refrescar la web
    </field>
    <field name="binding_model_id" ref="escoleta.model_escoleta_menjador"/>
</record>
```

Codi de la funció:

``` python
    def crear_dia_menjador(self):                            
        # En el XML era records i en el python cal extraurer els records de active_ids                             
        records = self.browse(self._context.get('active_ids'))                            
        for r in records:
         # Ja es pot treballar millor en dates gràcies a la biblioteca 'fields'
         fecha = fields.Datetime.now()                                                               
         self.env['escoleta.menjador_day'].create({'name':fecha,'day':r.id})              
         for s in r.students:
           self.env['escoleta.student_day'].create({'name':str(s.name)+" "+str(fecha),'student':s.id,'menjador_day':r.id})
        return {                                                  
                # En el XML era action i ací fa falta que retorne el diccionari per assignar-lo a action
                "type": "ir.actions.act_window",                                          
                "view_mode": "tree",                                                      
                "res_model": "escoleta.menjador_day",                                     
         }      
```

### *Domains* en les *actions*

En Odoo, el concepte de **domain** o domini està en varis llocs, encara
que el seu funcionament sempre és el mateix. Es tracta d\'un criteri de
búsqueda o filtre sobre un model. La sintaxi dels domains és como veurem
en aquest exemple:

``` python
# [(nom_del_field, operador , valor)] 
['|',('gender','=','male'),('gender','=','female')]
```

Com es veu, cada condició va entre parèntesis amb el mon del field i el
valor desitjat entre cometes si és un *string* i amb l\'operador entre
cometes i tot separat per comes. Les dues condicions tenen un **\|**
dabant, que significa la **O** lògica. Està dabant per utilitzar la
[notació polaca
inversa](https://es.wikipedia.org/wiki/Notaci%C3%B3n_polaca_inversa).

Un action en domain treu vistes per als elements del model que
coincideixen en les condicions del domini. El domain és trauit per el
model en un *where* més a la consulta SQL. Per tant, al client no li
arriben mai els registres que no pasen el filtre. Els *domains* en les vistes search el funcionament en la
part del model és igual, ja que no ejecuta un action, però fa la mateixa
petició javascript.

Exemple de domain en action:

``` xml
    <record id="action_employee" model="ir.actions.act_window">
        <field name="name">Employee Male or Female</field>
        <field name="res_model">employee.employee</field>
        <field name="view_type">form</field>
        <field name="view_mode">tree,form</field>
                <field name="domain">['|',('gender','=','male'),('gender','=','female')]</field>
    </record>
```

### Actions per a molts records

Quan estem observant un tree, podem veure dalt uns menús desplegables
que mostren varies accions que es poden fer als records seleccionats del
tree. Com ara eliminar o duplicar. Nosaltres podem crear noves accions
que estaran ahí dalt.

Fins ara hem vist accions que s\'executen al polsar un menú o un botó.
El menú està declarat explícitament i el botó també. Les accions sols
són una manera de dir-li al client web cóm ha de demanar les coses i cóm
ha de mostrar-les. El client web de Odoo genera moltes part de
l\'interfície de manera automàtica. En el cas que ens ocupa, el client
web atén a un action demanat pel menú lateral, aquest mostra un tree en
la finestra corresponent. Però en la definició del tree, sols està la
part de les dades. Dalt del tree, el client web mostra una barra de
búsqueda i uns menús desplagables **dropdown**. Aquest menú és generat
pel client amb la llista d\'accions vinculades al model que està
mostrant.

Lamanera més senzilla de vincular un action al menú de dalt és amb aquests
fields que ara tenen les actions:

- **binding_type**: Per defecte és de tipus **action**, però pot ser
    **action_form_only** per mostrar un formulari o **report** per
    generar un report.
- **binding_model_id**: Aquest field serveix per vincular l\'action al
    menú de dalt de les vistes d\'eixe model.

Exemple tret del codi d\'Odoo 11:

``` xml
 <record id="action_view_sale_advance_payment_inv" model="ir.actions.act_window">
  <field name="name">Invoice Order</field>
  <field name="type">ir.actions.act_window</field>
  <field name="res_model">sale.advance.payment.inv</field>
  <field name="view_type">form</field>
  <field name="view_mode">form</field>
  <field name="target">new</field>
  <field name="groups_id" eval="[(4,ref('sales_team.group_sale_salesman'))]"/>
  <field name="binding_model_id" ref="sale.model_sale_order" />
</record>
```

Exemple per a accions tipus server:

``` xml
<record id="action_server_learn_skill" model="ir.actions.server">
    <field name="name">Learning</field>
    <field name="type">ir.actions.server</field>
    <field name="model_id" ref="your_module_folder_name.model_your_model" />
    <field name="binding_model_id" ref="module_folder_name.model_your_target_model" />
    <field name="state">code</field>
    <field name="code">model.action_learn()</field>
</record>
```

Per saber més de les actions, podem estudiar el codi:
[1](https://github.com/odoo/odoo/blob/18.0/odoo/addons/base/models/ir_actions.py)
