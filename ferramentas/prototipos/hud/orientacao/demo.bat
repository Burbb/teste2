@echo off
rem Demonstracao dos quadros de orientacao (prototipo, nada no jogo): o painel em http://127.0.0.1:8769/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8769/
python ferramentas\prototipos\hud\orientacao\auxiliares\demo.py
