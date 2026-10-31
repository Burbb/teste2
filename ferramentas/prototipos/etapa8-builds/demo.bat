@echo off
rem Prototipo X1 da etapa 8 (nada no jogo): montagem de builds e estrutura dos talentos, em http://127.0.0.1:8797/
rem O registro das lutas vai para uma pasta temporaria nova a cada vez. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
start "" http://127.0.0.1:8797/
python ferramentas\prototipos\etapa8-builds\servidor.py
