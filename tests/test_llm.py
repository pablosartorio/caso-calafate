"""Tests del catálogo de motores y de cómo se instancian.

Ninguno de estos tests toca una red real: lo que se prueba es la LÓGICA de
selección (el modo fake no cambia, el analista prefiere qwen2.5:7b salvo que
no esté disponible), no el resultado de hablarle a un Ollama de verdad.
"""

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.runnables import RunnableLambda

from caso_calafate.llm import (
    MOTOR_ANALISTA_PREFERIDO,
    MOTOR_FAKE,
    _motor_analista,
    crear_motores,
)

# ── El modo fake no se toca ──────────────────────────────────────────────────


def test_crear_motores_fake_no_cambia():
    """El fake es el que usan TODOS los tests: nada de "forzar otro motor" acá."""
    actor, analista, nombre = crear_motores(MOTOR_FAKE)
    assert nombre == MOTOR_FAKE
    assert isinstance(actor, GenericFakeChatModel)
    assert isinstance(analista, RunnableLambda)


# ── _motor_analista: la preferencia por qwen2.5:7b ───────────────────────────


def test_el_analista_ya_preferido_no_necesita_chequear_nada(monkeypatch):
    def _explota(_modelo):
        raise AssertionError("no debería chequear disponibilidad si ya es el preferido")

    monkeypatch.setattr("caso_calafate.llm._modelo_ollama_disponible", _explota)
    assert _motor_analista(MOTOR_ANALISTA_PREFERIDO) == MOTOR_ANALISTA_PREFERIDO


def test_el_analista_prefiere_qwen_cuando_esta_disponible(monkeypatch):
    monkeypatch.setattr("caso_calafate.llm._modelo_ollama_disponible", lambda _modelo: True)
    assert _motor_analista("ollama:llama3.2:1b") == MOTOR_ANALISTA_PREFERIDO


def test_el_analista_cae_al_motor_del_actor_si_qwen_no_esta(monkeypatch):
    monkeypatch.setattr("caso_calafate.llm._modelo_ollama_disponible", lambda _modelo: False)
    assert _motor_analista("ollama:llama3.2:1b") == "ollama:llama3.2:1b"


# ── _modelo_ollama_disponible: best-effort, nunca explota ────────────────────


def test_modelo_ollama_disponible_es_false_si_ollama_esta_caido(monkeypatch):
    """Servidor apagado, timeout, versión rara del cliente: cualquier falla
    cuenta como "no está", nunca se propaga."""
    import ollama

    from caso_calafate.llm import _modelo_ollama_disponible

    def _cliente_roto(*args, **kwargs):
        raise RuntimeError("ollama serve no está corriendo")

    monkeypatch.setattr(ollama, "Client", _cliente_roto)
    assert _modelo_ollama_disponible("qwen2.5:7b") is False


def test_modelo_ollama_disponible_detecta_el_nombre_exacto(monkeypatch):
    import ollama

    class _ModeloFalso:
        model = "qwen2.5:7b"

    class _RespuestaFalsa:
        models = [_ModeloFalso()]

    class _ClienteFalso:
        def __init__(self, *args, **kwargs):
            pass

        def list(self):
            return _RespuestaFalsa()

    monkeypatch.setattr(ollama, "Client", _ClienteFalso)

    from caso_calafate.llm import _modelo_ollama_disponible

    assert _modelo_ollama_disponible("qwen2.5:7b") is True
    assert _modelo_ollama_disponible("llama3.1:8b") is False


def test_modelo_ollama_disponible_reconoce_el_tag_latest(monkeypatch):
    """Ollama guarda "qwen2.5:latest" pero también acepta "qwen2.5" a secas
    cuando el tag es "latest" — el chequeo tiene que reconocer las dos formas."""
    import ollama

    class _ModeloFalso:
        model = "qwen2.5:latest"

    class _RespuestaFalsa:
        models = [_ModeloFalso()]

    class _ClienteFalso:
        def __init__(self, *args, **kwargs):
            pass

        def list(self):
            return _RespuestaFalsa()

    monkeypatch.setattr(ollama, "Client", _ClienteFalso)

    from caso_calafate.llm import _modelo_ollama_disponible

    assert _modelo_ollama_disponible("qwen2.5") is True
    assert _modelo_ollama_disponible("qwen2.5:latest") is True
