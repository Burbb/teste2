@echo off
rem Demonstracao do Carregar jogo (prototipo, nada no jogo): o painel em http://127.0.0.1:8772/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8772/
python ferramentas\prototipos\hud\carregar-jogo\auxiliares\demo.py
