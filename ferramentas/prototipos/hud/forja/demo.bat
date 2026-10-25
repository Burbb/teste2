@echo off
rem Demonstracao da forja (prototipo, nada no jogo): o painel em http://127.0.0.1:8775/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8775/
python ferramentas\prototipos\hud\forja\auxiliares\demo.py
