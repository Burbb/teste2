# auxiliar: as linhas retocadas à mão (só a transição focinho/arcada) para a camada cranio; o "A" (contorno) fica como está
import sys
LEG = {"B": "8A704C", "C": "140C08", "D": "2E2014", "E": "DCC79A", "F": "5A4430", "G": "F4E8C8", "H": "B89C70"}
# (x do primeiro caractere, linhas): a mesma ideia nas duas grades
R = {36: (12, {28: "ABEEEHDHHBBFA", 29: "AEEDEHCHBDBFA", 30: "AGECEHCHBCHBA", 31: "AEHAHBAHBAHBA"}),
     32: (10, {23: "ABEEEHDHHBBFA", 24: "AEEDEHCHBDBFA", 25: "AGECEHCHBCHBA", 26: "AEHAHBAHBAHBA"})}
n = int(sys.argv[1]); x0, linhas = R[n]
px = [f"{x0 + i},{y},{LEG[c]}" for y, l in linhas.items() for i, c in enumerate(l) if c != "A"]
open(f"retoque{n}.lua", "w").write('return "' + ";".join(px) + '"\n'); print(n, len(px))
