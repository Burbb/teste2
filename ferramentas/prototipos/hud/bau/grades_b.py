"""B · o baú trancado: de frente e um pouco de cima (o tampo à vista), carvalho escuro, cantoneiras de latão e o
cadeado de ferro pendurado na aldraba. Grades desenhadas à mão, um caractere por pixel."""

PALETA = {
    "k": "#140e0b",                                   # contorno
    "1": "#2e1a12", "2": "#4a2a1a", "3": "#653a22", "4": "#83502e", "5": "#a3693d", "6": "#c48a55",  # carvalho
    "g": "#6e4610", "h": "#a87520", "G": "#dcae3c", "y": "#fbe7a0",  # latão
    "a": "#1d2027", "b": "#3a404c", "c": "#68717f", "d": "#a5adb9",  # ferro (o cadeado)
}
CAMADAS = {"madeira": "123456", "latao": "ghGy", "ferro": "abcd", "contorno": "k"}

G32 = [
    "................................",
    "................................",
    "................................",
    "................................",
    ".......kkkkkkkkkkkkkkkkkk.......",
    ".....kkyG66666666666666Ghkk.....",
    "....kyG666555555555555555Ghk....",
    "...kGh55555555555555555555hgk...",
    "...kGh44444444444444444444hgk...",
    "...kyh66666666666666666666hgk...",
    "...kGhg4444444hGGh4444444ghgk...",
    "...kGh33333333hyGh33333333hgk...",
    "...khg22222222hGGh22222222ghk...",
    "...k1111111111gGGg1111111111k...",
    "...kkkkkkkkkkkhGGhkkkkkkkkkkk...",
    "...k5555555555ghhg5555555555k...",
    "...k444444444kdhhck444444444k...",
    "...k444444444kdkkbk444444444k...",
    "...k11111111kddcccbk11111111k...",
    "...k44444444kdcckcbk44444444k...",
    "...k33333333kccbkbak33333333k...",
    "...kGh333333kbbbbaak333333hgk...",
    "...kGh1111111kkkkkk1111111hgk...",
    "...kGh33333333333333333333hgk...",
    "...kGhh222222222222222222hhgk...",
    "...khggg1111111111111111ggghk...",
    "...kkkkkkkkkkkkkkkkkkkkkkkkkk...",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
]
