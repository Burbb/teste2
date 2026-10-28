@echo off
rem Demonstracao do interior do templo (prototipo, nada no jogo): as candidatas A e B.
rem Abre o jogo num save temporario novo; os saves pessoais nao sao tocados. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\templo\demo.py
