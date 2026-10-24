"""A · o baú de sempre: tampa abaulada em três quartos (a frente à esquerda, a ponta à direita), tábuas castanhas,
cintas de ferro nas quinas e o espelho de latão com a fechadura. Grades desenhadas à mão, um caractere por pixel."""

PALETA = {
    "k": "#140e0b",                                   # contorno
    "1": "#341d10", "2": "#552f19", "3": "#764423", "4": "#975a2e", "5": "#b8793f", "6": "#d39a5a",  # madeira
    "a": "#23262e", "b": "#3d4350", "c": "#646d7c", "d": "#9aa3b1", "e": "#d2d8e0",  # ferro
    "g": "#7a4e10", "h": "#b9831f", "G": "#e8b83c", "y": "#fff0a8",  # latão
}
CAMADAS = {  # de baixo para cima: o material de cada caractere
    "madeira": "123456", "ferro": "abcde", "latao": "ghGy", "contorno": "k",
}

G32 = [
    "................................",
    "................................",
    "................................",
    "..........kkkkkkkkkkkkkkkkk.....",
    ".......kkkedc6666665555ddeekk...",
    ".....kk6ddcb65555555554dcb3ddk..",
    "....kddcb55555555555443dcb333dk.",
    "...kddcb544444444444433dcb3311ck",
    "...kdcbb222222222222222dcb1122ck",
    "...kdcb4433333333333332dcb2222ck",
    "...kdeb333333hhh3332222deb22kkck",
    "...kdbb33222hGGGh222222dabkk11ck",
    "...kdcbkkkkkhGyGhkkkkkkdcb2221ck",
    "...kdcb55555hGkGh555555dcb2221ck",
    "...kdcb44444hGkGh444444dcb2211ck",
    "...kdeb44444ghGhg444444deb1121ck",
    "...kdbb333333ggg3333333dab2211bk",
    "...kdcb2222222222222222dcb1111bk",
    "...kdcb4444444444444444dcb2211bk",
    "...kdcb3333333333333333dcb2111bk",
    "...kdcb2222222222222222dcb1111bk",
    "...kdeb4444444444444444deb2211bk",
    "...kcbb3333333333333333cab2111bk",
    "...kcba2222222222222222cba1111bk",
    "...kbaa1111111111111111baa11bk..",
    "...kkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
]
