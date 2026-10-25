@echo off
rem Demonstracao do combate e dos atributos (prototipo, nada no jogo): http://127.0.0.1:8781/
rem Os resultados das lutas vao para uma pasta temporaria nova a cada vez. Feche esta janela para parar.
cd /d "%~dp0..\..\.."
start "" http://127.0.0.1:8781/
python ferramentas\prototipos\combate-atributos\servidor.py
