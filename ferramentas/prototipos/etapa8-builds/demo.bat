@echo off
rem Prototipo X1 da etapa 8 (nada no jogo): montagem de builds e estrutura dos talentos.
rem O servidor mostra a versao, procura uma porta livre a partir da 8797 e abre o navegador na porta certa.
rem Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\etapa8-builds\servidor.py
