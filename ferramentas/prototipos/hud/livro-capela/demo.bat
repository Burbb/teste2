@echo off
rem Demonstracao do livro da capela (prototipo, nada no jogo): o painel em http://127.0.0.1:8767/
rem Feche esta janela para parar.
cd /d "%~dp0..\..\..\.."
start "" http://127.0.0.1:8767/
python ferramentas\prototipos\hud\livro-capela\auxiliares\demo.py
