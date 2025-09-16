<!-- omit in toc -->
# ¡Contribuye a la librería ESCatastroLib!

Antes de nada, ¡gracias por tomarte el tiempo para contribuir al proyecto! 🇪🇸🏞️

> Recordamos que tenemos un [Código de conducta](CODE_OF_CONDUCT.md) que aplicamos aquí

Se fomenta y valora todo tipo de contribuciones. Consulta la [Tabla de contenidos](#table-of-contents) para conocer las diferentes formas de ayudar y los detalles sobre cómo el equipo de este proyecto las gestiona. Por favor, asegúrate de leer la sección correspondiente antes de hacer tu contribución. Nos facilitará la tarea al equipo de mantenimiento y facilitará la experiencia a todos los implicados. La comunidad espera vuestras contribuciones. 🎉

> Y si te gusta el proyecto, pero no tienes tiempo para contribuir, no pasa nada. Hay otras formas sencillas de apoyar el proyecto y mostrar tu apoyo, que también nos alegrarían mucho:
> - Dale una estrella al proyecto
> - Postea sobre él en Mastodon, Bluesky...
> - Menciona este proyecto en el léame de tu proyecto
> - Menciona el proyecto en las quedadas locales y díselo a tus amigos/colegas

<!-- omit in toc -->
## Tabla de contenidos
- [Tengo una pregunta](#tengo-una-pregunta)
- [Me gustaría aportar algo](#me-gustaría-aportar-algo)
  - [Si veo un Bug, ¿cómo lo reporto?](#si-veo-un-bug-cómo-lo-reporto)
  - [Sugiriendo mejoras](#sugiriendo-mejoras)
  - [Tu primera Contribución](#tu-primera-contribución)
    - [Haciendo funcionar a la librería](#haciendo-funcionar-a-la-librería)
    - [Para hacer los cambios](#para-hacer-los-cambios)
    - [Subiendo a GitHub](#subiendo-a-github)
  - [Mejorando la documentación](#mejorando-la-documentación)
- [Guías de estilo](#guías-de-estilo)
  - [Mensajes para commits](#mensajes-para-commits)
- [Únete al proyecto](#únete-al-proyecto)



## Tengo una pregunta

> Si quieres hacer una pregunta, suponemos que has leído la [Documentación](https://github.com/IvanitiX/ESCatastroLib). disponible anteriormente

Antes de plantear una pregunta, es mejor que busques las [Cuestiones](https://github.com/IvanitiX/ESCatastroLib/issues) existentes que te puedan ayudar. En caso de que hayas encontrado un tema adecuado y sigas necesitando aclaraciones, puedes escribir tu pregunta en esa cuestión. También es aconsejable buscar respuestas en Internet primero si el tema está más alejado del ámbito del proyecto

Si luego sigues sintiendo la necesidad de hacer una pregunta y necesitas una aclaración, te recomendamos hacer lo siguiente:

- Abre una [incidencia](https://github.com/IvanitiX/ESCatastroLib/issues/new).
- Proporciona todo el contexto que puedas sobre lo que te está ocurriendo.
- Proporciona las versiones del proyecto y de la plataforma (Python, Pip...), dependiendo de lo que parezca relevante.

Nos encargaremos de la incidencia lo antes posible.

<!--
You might want to create a separate issue tag for questions and include it in this description. People should then tag their issues accordingly.

Depending on how large the project is, you may want to outsource the questioning, e.g. to Stack Overflow or Gitter. You may add additional contact and information possibilities:
- IRC
- Slack
- Gitter
- Stack Overflow tag
- Blog
- FAQ
- Roadmap
- E-Mail List
- Forum
-->

## Me gustaría aportar algo

> ### Un aviso legal <!-- omit in toc -->
> Al contribuir a este proyecto, debes aceptar que eres el autor del 100% del contenido, que tienes los derechos necesarios sobre el mismo y que el contenido que aportas pueda ser proporcionado bajo la licencia del proyecto.

### Si veo un Bug, ¿cómo lo reporto?

<!-- omit in toc -->
#### Antes de enviar un Bug Report

Un buen reporte de errores no debería hacer que otros tuvieran que buscarte para obtener más información. Por lo tanto, te pedimos que investigues con cuidado, recojas información y describas el problema con todo detalle en tu informe. Por favor, completa los siguientes pasos por adelantado para ayudarnos a solucionar cualquier posible fallo lo antes posible.

- Asegúrate de que estás utilizando la última versión.
- Determina si tu error es realmente un bug y no un error por tu parte, por ejemplo, por utilizar componentes/versiones de entorno incompatibles (asegúrate de haber leído la [documentación](https://github.com/IvanitiX/ESCatastroLib). Si estás buscando soporte, puede que quieras comprobar [esta sección](#tengo-una-pregunta)).
- Para ver si otros usuarios han experimentado (y potencialmente ya han resuelto) el mismo problema que tienes, comprueba si no existe ya un informe de error para tu fallo o error en el [bug tracker](https://github.com/IvanitiX/ESCatastroLib/issues?q=label%3Abug).
- Asegúrate también de buscar en Internet (incluyendo Stack Overflow, aunque va a ser raro) para ver si los usuarios fuera de la comunidad de GitHub han discutido el problema.
- Recoge información sobre el fallo:
  - Traceback de la ejecución
  - Sistema operativo, plataforma y versión (Windows, Linux, macOS, x86, ARM)
  - Versión del intérprete, compilador, SDK, entorno de ejecución, gestor de paquetes, dependiendo de lo que parezca relevante.
  - Posiblemente la entrada y la salida
  - ¿Puedes reproducir el problema de forma fiable? ¿Y puedes reproducirlo también con versiones anteriores?


<!-- omit in toc -->
#### ¿Cómo subo un buen Bug Report?

> Nunca debes informar sobre problemas de seguridad, vulnerabilidades o errores que incluyan información sensible en el rastreador de problemas, o en cualquier otro lugar en público. Los errores sensibles deben enviarse por correo electrónico a <IvanVR@protonmail.com>.
<!-- You may add a PGP key to allow the messages to be sent encrypted as well. -->

Utilizamos GitHub Issues para hacer un seguimiento de los fallos y errores. Si te encuentras con un problema en el proyecto:

- Abre una [incidencia](https://github.com/IvanitiX/ESCatastroLib/issues/new). (Como no podemos estar seguros en este momento de si se trata de un error o no, te pedimos que no hables todavía de un bug y que no etiquetes el problema).
- Explica el comportamiento que esperarías y el comportamiento real.
- Por favor, proporciona todo el contexto posible y describe los *pasos de reproducción* que otra persona puede seguir para recrear el problema por su cuenta. Esto suele incluir tu código. Para un buen informe de errores, debes aislar el problema y crear un caso de prueba reducido.
- Proporciona la información que has recogido en la sección anterior.

Una vez presentada:

- El equipo del proyecto etiquetará el problema como corresponde.
- Un miembro del equipo intentará reproducir el problema con los pasos que hayas proporcionado. Si no hay pasos de reproducción o no hay una manera obvia de reproducir el problema, el equipo te pedirá esos pasos y marcará el problema como `needs-repro`. Los errores con la etiqueta `needs-repro` no se tratarán hasta que se reproduzcan.
- Si el equipo es capaz de reproducir el problema, se marcará como `needs-fix`, así como posiblemente otras etiquetas (como `urgent`), y el problema se dejará para ser [implementado por alguien](#tu-primera-contribución).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->


### Sugiriendo mejoras

Esta sección explica cómo enviar una sugerencia de mejora para el la librería, **incluyendo características completamente nuevas y pequeñas mejoras en la funcionalidad existente**. Siguiendo estas directrices ayudará a los mantenedores y a la comunidad a entender tu sugerencia y a encontrar sugerencias relacionadas.

<!-- omit in toc -->
#### Antes de sugerir una mejora...

- Asegúrate de que estás utilizando la última versión.
- Lee detenidamente la [documentación](https://github.com/IvanitiX/ESCatastroLib) y averigua si la funcionalidad ya está cubierta, quizá por una configuración individual.
- Realiza una [búsqueda](https://github.com/IvanitiX/ESCatastroLib/issues) para ver si la mejora ya ha sido sugerida. Si es así, añade un comentario a la cuestión existente en lugar de abrir una nueva.
- Averigua si tu idea encaja con el alcance y los objetivos del proyecto. Depende de ti hacer un argumento sólido para convencer a los desarrolladores del proyecto de las ventajas de esta función. Ten en cuenta que queremos funciones que sean útiles para la mayoría de nuestros usuarios y no sólo para un pequeño subconjunto. Si sólo te diriges a una minoría de usuarios, considera la posibilidad de escribir una biblioteca de complementos/plugins para adapatarlo a la librería.

<!-- omit in toc -->
#### ¿Cómo envío una buena sugerencia de mejora?

Las sugerencias de mejora se registran como [Issues de GitHub](https://github.com/IvanitiX/ESCatastroLib/issues).

- Utiliza un **título claro y descriptivo** para identificar la sugerencia.
- Proporciona una **descripción paso a paso de la mejora sugerida** con tantos detalles como sea posible.
- Describe el comportamiento actual y explica qué comportamiento esperabas ver en su lugar y por qué. En este punto también puede decir qué alternativas no le funcionan.
- Puedes **incluir capturas de pantalla y grabaciones** que te ayuden a demostrar los pasos o a señalar la parte con la que está relacionada la sugerencia. Puedes usar herramientas como [OBS Studio](https://obsproject.com/) para ello.
- **Explica por qué esta mejora sería útil** para la mayoría de los usuarios de la librería Voice Assistant. También puedes señalar los otros proyectos que lo resolvieron mejor y que podrían servir de inspiración.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Tu primera Contribución
<!-- TODO
include Setup of env, IDE and typical getting started instructions?

-->
#### Haciendo funcionar a la librería
Una vez hayas descargado el código, podrás usar Hatch para:
- Crear el entorno de pruebas (hatch env)
- Hacer tests (con hatch test o hatch --test-all, que incluye las versiones de la 3.8 a la 3.13)
- Construir un paquete en local (con hatch build)
#### Para hacer los cambios
Los cambios a las clases las podréis hacer en los ficheros de `models`, y las funciones de apoyo, en los de `utils`.

#### Subiendo a GitHub
A la hora de subir a GitHub hay muchos archivos que se han generado en el transcurso del desarrollo. Es normal, pero si intentas subirlos a GitHub va a explotar. para ello, sólo sube los archivos `.py` del código, y cualquier documentación que hayas hecho. Sigue las recomendaciones para poner un buen mensaje de commit [aquí](#mensajes-para-commits) y una vez subido, haz una Pull Request

### Mejorando la documentación
<!-- TODO
Updating, improving and correcting the documentation

-->

Sabemos que la documentación puede ser más bien cortita, pero necesaria para poder usar y mejorar a la librería, paso a paso.

Por ello te recomendamos algunos puntos para poder hacer una buena documentación:
- Si estás haciendo código, documenta el proceso donde creas que no se pueda entender algo.
- Documenta qué hace cada clase, cada método y el fichero en general. Eso permite la autogeneración de código en una gran medida, y hace más fácil que otra persona entienda lo que haces.
- Si vas a hacer nuevos módulos para adaptar al flujo principal, redacta un archivo de Markdown con el flujo que sigue para poder interactuar con el proyecto. Sería un plus si además aportas diagramas de flujo (puedes usar herramientas como Draw.io)

## Guías de estilo
### Mensajes para commits
Para tener un buen commit, hay que hacerse entender. Por ello es recomendable seguir estos puntos para que podamos aceptarte esa Pull Request:
- El principio del mensaje debe tener unas palabras especiales que nos ubiquen qué tipo de cambio es:
  - `[Fix]` indica un arreglo.
  - `[Enhancement]` indica una mejora.
  - `[Typo]` indica un cambio por errores tipográficos en alguna frase.
  - `[Docs]` indica la adición o modificación de la documentación
  - `[Dep-Update]` indica que se han anotado las actualizaciones las dependencias de la librería para la instalación
  - `[Experimental]` indica que se ha hecho un cambio sustancial en el funcionamiento de la librería y necesita ser probado primero.
  -  `[Adapter]` indica que se ha prgramado un adaptador para usarse en el flujo principal de la librería.
- El resto del mensaje principal del commit deberá ser un resumen (en español o inglés) de los cambios (ej: *Añadida interacción para convertir las coordenadas / Addded interacion to convert coordinates*). Sé conciso y no te pases de 50-60 caracteres.
- Puedes añadir un mensaje más largo con los cambios más pormenorizados. Por ejemplo:
 ```
 + Añadida nueva funcion para ...
 = Modificada la lista de acciones
 ```
Recomendamos que pongas una lista de cambios y un icono distinto según si has añadido(+), modificado (=) o eliminado (-) código.

## Únete al proyecto
<!-- TODO -->
Al ser un proyecto con sólo una persona, toda ayuda que se quiera prestar será bien recibida. Si te interesa, escríbeme a <IvanVR@protonmail.com> con el asunto `ESCatastroLib | (Asunto)` y hablamos. Puede que en un futuro me aventure a crear un canal de Telegram/Discord si somos más.  

<!-- omit in toc -->
## Atribuciones
Esta guía está basada en una traducción de **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!

