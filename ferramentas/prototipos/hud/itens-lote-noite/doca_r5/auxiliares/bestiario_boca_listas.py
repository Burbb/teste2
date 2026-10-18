# auxiliar: das linhas desenhadas à mão, as listas do pintar.lua (cranio e contorno), apagando o resto dessas linhas
import importlib, sys
mod = importlib.import_module(sys.argv[1]); n = int(sys.argv[2])
crania, cont = [], []
for y, l in mod.LINHAS.items():
    assert len(l) == n, (y, len(l))
    for x, ch in enumerate(l):
        if ch == ".": crania.append(f"{x},{y},00000000"); cont.append(f"{x},{y},00000000")
        elif ch == "A": cont.append(f"{x},{y},{mod.LEG[ch]}"); crania.append(f"{x},{y},00000000")
        else: crania.append(f"{x},{y},{mod.LEG[ch]}"); cont.append(f"{x},{y},00000000")
open(f"cranio{n}.lua", "w").write('return "' + ";".join(crania) + '"\n')
open(f"contorno{n}.lua", "w").write('return "' + ";".join(cont) + '"\n')
print("ok", len(crania), len(cont))
