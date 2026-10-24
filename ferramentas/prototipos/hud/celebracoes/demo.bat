@echo off
rem Demonstracao da etapa 2 (prototipo, nada no jogo): o painel em http://127.0.0.1:8765/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8765/
python ferramentas\prototipos\hud\celebracoes\auxiliares\demo.py
