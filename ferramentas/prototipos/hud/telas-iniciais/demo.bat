@echo off
rem Demonstracao das telas iniciais (prototipo, nada no jogo): o painel em http://127.0.0.1:8770/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8770/
python ferramentas\prototipos\hud\telas-iniciais\auxiliares\demo.py
