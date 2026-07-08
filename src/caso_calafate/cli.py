"""La interfaz de terminal del juego.

Todo lo "visual" vive acá: paneles, colores, streaming de texto, parseo de
comandos. El grafo no sabe que existe una terminal — solo recibe jugadas y
devuelve estado — así que esta capa se puede reescribir entera (¿una web?
¿un bot de Telegram?) sin tocar el motor.

La división de responsabilidades por turno es:

1. El CLI parsea lo que tipeó el jugador.
2. Si es una jugada (pregunta o acusación), invoca el grafo con la acción.
3. El CLI muestra lo que el grafo devolvió (streaming incluido).

Los comandos informativos (/pistas, /caso, ...) no invocan el grafo: leen el
estado actual con ``grafo.get_state()`` — el checkpointer guarda la partida y
cualquiera con el ``thread_id`` puede consultarla.
"""


from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from caso_calafate.caso import CASO_CALAFATE, Caso, Sospechoso
from caso_calafate.grafo import construir_grafo
from caso_calafate.llm import crear_motores, texto_de

console = Console()

AYUDA = """\
[bold]/sospechosos[/bold]        quiénes son y qué dicen haber hecho
[bold]/hablar <nombre>[/bold]    elegir a quién interrogar (después escribí tu pregunta y Enter)
[bold]/pistas[/bold]             tu libreta de pistas descubiertas
[bold]/caso[/bold]               releer el briefing del caso
[bold]/acusar <nombre>[/bold]    señalar al culpable — cierra la partida, tenés UNA oportunidad
[bold]/ayuda[/bold]              este mensaje
[bold]/salir[/bold]              abandonar el caso

Todo lo que escribas sin barra es una pregunta para el sospechoso elegido."""


def main() -> None:
    """Punto de entrada del comando ``detective`` (ver [project.scripts] en pyproject)."""
    load_dotenv()  # lee el .env del directorio actual, si existe

    try:
        actor, analista, nombre_motor = crear_motores()
    except Exception as error:  # API key ausente, proveedor mal escrito, etc.
        _mostrar_error_de_motor(error)
        return

    grafo = construir_grafo(CASO_CALAFATE, actor, analista)
    # El thread_id identifica LA partida dentro del checkpointer. Acá usamos
    # uno fijo porque cada proceso es una partida nueva (MemorySaver vive en
    # RAM); con un checkpointer persistente, cambiarlo permitiría retomar
    # partidas guardadas.
    config = {"configurable": {"thread_id": "partida"}}

    _mostrar_briefing(CASO_CALAFATE)
    console.print(f"[dim]Motor: {nombre_motor} · Escribí /ayuda para ver los comandos.[/dim]\n")
    if nombre_motor == "fake":
        console.print(
            "[yellow]⚠ Modo fake: sin LLM real. Las respuestas son enlatadas y las "
            "pistas se revelan solas — sirve para probar la mecánica.[/yellow]\n"
        )
    _bucle(grafo, config, CASO_CALAFATE)


def _bucle(grafo, config: dict, caso: Caso) -> None:
    """El loop principal: leer → parsear → jugar/mostrar, hasta que la partida cierre."""
    seleccionado: Sospechoso | None = None

    while True:
        estado = grafo.get_state(config).values  # {} antes del primer turno
        restantes = caso.max_preguntas - estado.get("preguntas_usadas", 0)

        try:
            entrada = Prompt.ask(_etiqueta(restantes, seleccionado)).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]El caso queda abierto. Hasta la próxima, detective.[/dim]")
            return

        if not entrada:
            continue

        if entrada.startswith("/"):
            comando, _, resto = entrada.partition(" ")
            terminado = _ejecutar_comando(
                comando.lower(), resto.strip(), grafo, config, caso, estado
            )
            if terminado:
                return
            # /hablar es el único comando que cambia a quién interrogamos.
            if comando.lower() == "/hablar":
                seleccionado = caso.buscar_sospechoso(resto) or seleccionado
            continue

        # Sin barra: es una pregunta para el sospechoso seleccionado.
        if seleccionado is None:
            console.print(
                "Primero elegí a quién interrogar: [bold]/hablar <nombre>[/bold] "
                "(mirá [bold]/sospechosos[/bold])."
            )
            continue
        if restantes <= 0:
            console.print(
                "[red]Se te acabó el tiempo: el directorio exige un nombre.[/red] "
                "Cerrá el caso con [bold]/acusar <nombre>[/bold]."
            )
            continue
        _turno_interrogatorio(grafo, config, caso, seleccionado, entrada)


def _ejecutar_comando(
    comando: str, resto: str, grafo, config: dict, caso: Caso, estado: dict
) -> bool:
    """Ejecuta un comando con barra. Devuelve True si la partida terminó."""
    match comando:
        case "/ayuda" | "/help":
            console.print(Panel(AYUDA, title="Comandos", border_style="blue"))
        case "/caso":
            _mostrar_briefing(caso)
        case "/sospechosos":
            _mostrar_sospechosos(caso)
        case "/pistas":
            _mostrar_pistas(caso, estado)
        case "/hablar":
            sospechoso = caso.buscar_sospechoso(resto)
            if sospechoso is None:
                console.print(
                    f"No encuentro a «{resto}». Probá con [bold]/sospechosos[/bold]."
                )
            else:
                console.print(
                    f"\nAhora interrogás a [bold {sospechoso.color}]{sospechoso.nombre}[/], "
                    f"{sospechoso.cargo}. Escribí tu pregunta y Enter.\n"
                )
        case "/acusar":
            sospechoso = caso.buscar_sospechoso(resto)
            if sospechoso is None:
                console.print(
                    f"¿Acusar a quién? No encuentro a «{resto}». "
                    "Usá [bold]/acusar <nombre>[/bold]."
                )
                return False
            confirmacion = Prompt.ask(
                f"¿Acusar a [bold {sospechoso.color}]{sospechoso.nombre}[/]? "
                "Es tu ÚNICA oportunidad",
                choices=["s", "n"],
                default="n",
            )
            if confirmacion != "s":
                console.print("[dim]Sabia prudencia. Seguí investigando.[/dim]")
                return False
            _turno_acusacion(grafo, config, caso, sospechoso)
            return True
        case "/salir":
            console.print("[dim]El caso queda abierto. Hasta la próxima, detective.[/dim]")
            return True
        case _:
            console.print(f"No conozco el comando {comando}. Probá [bold]/ayuda[/bold].")
    return False


# ── Jugadas (acá se invoca el grafo) ─────────────────────────────────────────


def _turno_interrogatorio(
    grafo, config: dict, caso: Caso, sospechoso: Sospechoso, pregunta: str
) -> None:
    """Un turno de pregunta: invoca el grafo en modo streaming y muestra todo.

    ``stream_mode="messages"`` hace que el grafo emita cada pedacito de texto
    que genera cualquier LLM interno, junto con metadata de QUÉ nodo lo generó.
    Filtramos por el nodo "interrogar" para mostrar solo la voz del sospechoso
    (el analista también es un LLM, pero trabaja en silencio).
    """
    jugada = {
        "accion": "interrogar",
        "sospechoso_actual": sospechoso.id,
        "pregunta": pregunta,
    }
    console.print(f"\n[bold {sospechoso.color}]{sospechoso.nombre}[/] —", end=" ")
    try:
        for chunk, metadata in grafo.stream(jugada, config, stream_mode="messages"):
            if metadata.get("langgraph_node") == "interrogar":
                # print() plano, no rich: el texto del LLM podría tener
                # corchetes que rich interpretaría como markup.
                print(texto_de(chunk), end="", flush=True)
    except Exception as error:
        console.print(f"\n[red]El interrogatorio se cortó: {error}[/red]")
        return
    print("\n")

    # El streaming ya terminó: el checkpointer tiene el estado final del turno.
    estado = grafo.get_state(config).values
    for pista_id in estado.get("pistas_nuevas", []):
        secreto = caso.secreto(pista_id)
        if secreto is not None:
            console.print(Panel(secreto.pista, title="🔎 Nueva pista", border_style="green"))


def _turno_acusacion(grafo, config: dict, caso: Caso, sospechoso: Sospechoso) -> None:
    """La jugada final: acusación, veredicto, epílogo y puntaje."""
    estado = grafo.invoke({"accion": "acusar", "sospechoso_actual": sospechoso.id}, config)

    if estado["resultado"] == "victoria":
        console.print(Panel(estado["respuesta"], title="⚖️  CASO RESUELTO", border_style="green"))
    else:
        console.print(Panel(estado["respuesta"], title="⚖️  CASO FALLIDO", border_style="red"))

    console.print(Panel(caso.epilogo, title="📜 La verdad", border_style="cyan"))

    encontradas = len(estado.get("pistas_descubiertas", []))
    usadas = estado.get("preguntas_usadas", 0)
    console.print(
        f"Pistas: [bold]{encontradas}/{caso.total_secretos()}[/bold] · "
        f"Preguntas usadas: [bold]{usadas}/{caso.max_preguntas}[/bold]"
    )
    console.print(_calificacion(estado["resultado"], encontradas, caso.total_secretos()))


def _calificacion(resultado: str, encontradas: int, total: int) -> str:
    """Un remate según cómo jugaste. Puro chiche de presentación."""
    if resultado != "victoria":
        return (
            "🪦 [red]El culpable sigue suelto. El CALAFATE-2 "
            "va a necesitar otro detective.[/red]"
        )
    if encontradas >= total * 0.8:
        return (
            "🏆 [green]Detective de leyenda: resolviste el caso "
            "con la evidencia en la mano.[/green]"
        )
    if encontradas >= total * 0.4:
        return "🕵️ [green]Buen ojo, detective. Un par de pistas más y era de manual.[/green]"
    return (
        "🍀 [yellow]Acertaste... con más instinto que evidencia. "
        "La suerte también cuenta.[/yellow]"
    )


# ── Pantallas informativas (no invocan el grafo) ─────────────────────────────


def _mostrar_briefing(caso: Caso) -> None:
    console.print(Panel(caso.briefing, title=f"🛰️  {caso.titulo}", border_style="cyan"))


def _mostrar_sospechosos(caso: Caso) -> None:
    tabla = Table(title="Sospechosos", show_lines=True)
    tabla.add_column("Nombre", style="bold")
    tabla.add_column("Cargo")
    tabla.add_column("Qué dice que hizo esa noche")
    for s in caso.sospechosos:
        tabla.add_row(f"[{s.color}]{s.nombre}[/]", s.cargo, s.coartada)
    console.print(tabla)


def _mostrar_pistas(caso: Caso, estado: dict) -> None:
    descubiertas: list[str] = estado.get("pistas_descubiertas", [])
    if not descubiertas:
        console.print(
            Panel(
                "Tu libreta está vacía. Interrogá a los sospechosos: las pistas "
                "aparecen cuando alguien suelta algo que no debía.",
                title="🗒️  Libreta",
                border_style="yellow",
            )
        )
        return
    lineas = []
    for numero, pista_id in enumerate(descubiertas, start=1):
        secreto = caso.secreto(pista_id)
        if secreto is not None:
            lineas.append(f"{numero}. {secreto.pista}")
    titulo = f"🗒️  Libreta — {len(descubiertas)}/{caso.total_secretos()} pistas"
    console.print(Panel("\n\n".join(lineas), title=titulo, border_style="yellow"))


def _etiqueta(restantes: int, seleccionado: Sospechoso | None) -> str:
    """El prompt de entrada: cuántas preguntas quedan y con quién hablás."""
    quien = (
        f"[{seleccionado.color}]{seleccionado.nombre.split()[0]}[/]"
        if seleccionado
        else "[dim]nadie[/dim]"
    )
    return f"[bold]({restantes}❓)[/bold] {quien} ›"


def _mostrar_error_de_motor(error: Exception) -> None:
    console.print(
        Panel(
            f"No pude inicializar el modelo de lenguaje:\n[red]{error}[/red]\n\n"
            "Opciones para jugar:\n"
            "  1. [bold]Anthropic[/bold]: copiá .env.example a .env y completá tu "
            "ANTHROPIC_API_KEY.\n"
            "  2. [bold]Ollama local[/bold] (gratis): corré [cyan]ollama serve[/cyan], mirá tus "
            "modelos con [cyan]ollama list[/cyan]\n"
            "     y poné [cyan]DETECTIVE_MODEL=ollama:<modelo>[/cyan] en el .env "
            "(ej. [cyan]ollama:llama3.1:8b[/cyan]).\n"
            "  3. [bold]Sin nada[/bold]: [cyan]DETECTIVE_MODEL=fake[/cyan] para probar la "
            "mecánica sin ningún LLM.",
            title="⚠️  Motor no disponible",
            border_style="red",
        )
    )
