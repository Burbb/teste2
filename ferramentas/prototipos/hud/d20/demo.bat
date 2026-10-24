@echo off
rem Demonstracao do d20 (prototipo, nada no jogo): o painel em http://127.0.0.1:8766/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8766/
python ferramentas\prototipos\hud\d20\auxiliares\demo.py
