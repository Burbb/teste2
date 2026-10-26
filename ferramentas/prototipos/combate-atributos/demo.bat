@echo off
rem Demonstracao do combate e dos atributos (prototipo, nada no jogo): a v2 em http://127.0.0.1:8781/
rem e a v1 (a primeira, preservada) em http://127.0.0.1:8781/v1/
rem Os resultados das lutas vao para uma pasta temporaria nova a cada vez. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
start "" http://127.0.0.1:8781/
python ferramentas\prototipos\combate-atributos\servidor.py
