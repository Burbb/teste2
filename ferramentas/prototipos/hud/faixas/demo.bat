@echo off
rem Demonstracao das faixas de passagem (prototipo, nada no jogo): o painel em http://127.0.0.1:8768/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8768/
python ferramentas\prototipos\hud\faixas\auxiliares\demo.py
