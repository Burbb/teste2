"""A paleta da forja F, por materiais (rampas do escuro ao claro). A base do ambiente é mapeada nela e os retoques e o
ferreiro usam só estas cores."""


def hx(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


RAMPAS = {
    # o escuro e a pedra fria (a parede longe do fogo, as sombras)
    "pedra": ["#08070a", "#111014", "#1a1a20", "#24242c", "#2f2f38", "#3c3c47", "#4d4d58", "#62626c"],
    # a pedra e o tijolo na luz do fogo
    "quente": ["#1f1714", "#2e211b", "#423024", "#5c3e2a", "#7a4e30", "#9c6638", "#c0804a"],
    # a madeira
    "madeira": ["#1d130d", "#2d1e13", "#43301e", "#5d4329", "#7a5935", "#99744a"],
    # o fogo e o metal em brasa
    "fogo": ["#3f1006", "#7a240a", "#b8400f", "#e86a18", "#ff9a30", "#ffcc66", "#fff2c4"],
    # o dia lá fora, frio
    "dia": ["#2c3a48", "#4a5e70", "#7690a2", "#a8bccb", "#d6e2ea"],
    # a pele
    "pele": ["#3a1c12", "#5a2e1e", "#8a4c30", "#b87250", "#dc9a70", "#f0bc8c"],
    # a barba ruiva
    "barba": ["#3a1208", "#6a2410", "#9c3a18", "#c85e28", "#e88a44"],
    # o couro do avental, das luvas e das botas
    "couro": ["#24160e", "#40281a", "#5a3a24", "#78502e", "#966a40"],
    # o pano escuro da calça (azulado)
    "pano": ["#14151d", "#22242e", "#323646", "#4a5062"],
    # o ferro frio
    "ferro": ["#1c1e24", "#2e3139", "#474b55", "#6a6e7a", "#80848e", "#a8acb4", "#cfd2d8", "#eef0f2"],
}
TODAS = [c for r in RAMPAS.values() for c in r]
K = "#08070a"  # o contorno
