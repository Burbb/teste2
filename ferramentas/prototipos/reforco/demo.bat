@echo off
rem Demonstracao do reforco, dos materiais e da desmontagem (prototipo, nada no jogo).
rem Abre o jogo num save temporario novo; os saves pessoais nao sao tocados. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\reforco\demo.py
