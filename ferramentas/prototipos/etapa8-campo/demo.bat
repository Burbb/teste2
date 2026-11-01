@echo off
rem Prototipo de campo livre da etapa 8 (nada no jogo): o heroi em tempo real no meio de tropas pequenas.
rem O servidor mostra a versao, procura uma porta livre a partir da 8801 e abre o navegador na porta certa.
rem Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\etapa8-campo\servidor.py
