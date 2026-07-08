"""Tests del reducer de pistas.

Es una función pura de cuatro líneas, pero es la que garantiza que las pistas
nunca se pierdan ni se dupliquen entre turnos — vale la pena clavarla con tests.
"""

from caso_calafate.estado import acumular_pistas


def test_acumula_pistas_nuevas_al_final():
    assert acumular_pistas(["a"], ["b", "c"]) == ["a", "b", "c"]


def test_no_duplica_pistas_ya_conocidas():
    assert acumular_pistas(["a", "b"], ["b", "c", "a"]) == ["a", "b", "c"]


def test_lista_nueva_vacia_no_cambia_nada():
    assert acumular_pistas(["a"], []) == ["a"]


def test_arranca_de_cero_sin_problemas():
    assert acumular_pistas([], ["a"]) == ["a"]
