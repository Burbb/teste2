# auxiliar: um dicionário que lembra a camada de cada pixel (a seção do desenho que o pintou por último)
class Grade(dict):
    def __init__(self):
        super().__init__(); self.cam = {}; self.atual = ""
    def __setitem__(self, k, v):
        super().__setitem__(k, v); self.cam[k] = self.atual
