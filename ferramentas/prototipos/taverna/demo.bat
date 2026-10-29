@echo off
rem Demonstracao do interior da taverna (prototipo, nada no jogo).
rem Abre o jogo num save temporario novo; os saves pessoais nao sao tocados. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\taverna\demo.py
