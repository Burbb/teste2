@echo off
rem Abre o prototipo da ficha num servidor local (serve para qualquer navegador).
rem Para parar, feche a janela "servidor do prototipo".
cd /d "%~dp0..\..\.."
start "servidor do prototipo" python -m http.server 8765
timeout /t 2 /nobreak >nul
start "" "http://localhost:8765/ferramentas/prototipos/hud/index.html"
