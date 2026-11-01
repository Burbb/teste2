@echo off
rem Prototipo tatico da etapa 8 (nada no jogo): o combate numa grade vista de cima.
rem O servidor mostra a versao, procura uma porta livre a partir da 8799 e abre o navegador na porta certa.
rem Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\etapa8-tatico\servidor.py
