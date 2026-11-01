@echo off
rem Prototipo tatico por turnos da etapa 8 (nada no jogo): casas em losango, PA e PM, inspirado em Dofus.
rem O servidor mostra a versao (Tatico 2), procura uma porta livre a partir da 8807 e abre o navegador na porta certa.
rem Feche esta janela para parar.
cd /d "%~dp0..\..\.."
python ferramentas\prototipos\etapa8-tatico2\servidor.py
