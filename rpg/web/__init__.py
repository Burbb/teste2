"""Interface web: o jogo em Python, a tela em HTML/CSS/JS.

Abre numa janela própria se o pywebview estiver instalado; senão, no navegador.
Tudo é local e offline: o servidor escuta só em 127.0.0.1.
"""

import os
import threading
import time
import traceback
import webbrowser

from .ponte import WebUI
from .servidor import Servidor


def jogar(args, menu_principal):
    ui = WebUI()
    ui.jogo = None
    # as preferências da tela numa pasta ao lado dos saves (fora da lista deles, que lê os .json da pasta dos saves)
    srv = Servidor(ui, porta=args.porta, config={"velocidade": args.velocidade},
                   preferencias=os.path.join(args.saves, "preferencias", "tela.json")).iniciar()

    def rodar_jogo():
        try:
            menu_principal(ui, args)
        except SystemExit:
            pass
        except Exception as e:  # mostra o erro na tela em vez de travar a janela
            traceback.print_exc()
            ui._enviar("erro", texto=f"{type(e).__name__}: {e}")
        finally:
            ui.fim("Até a próxima jornada!")

    jogo = threading.Thread(target=rodar_jogo, daemon=True, name="jogo")
    jogo.start()
    print(f"The Unquiet está rodando em:\n  {srv.url}\nPara encerrar, feche esta janela ou tecle Ctrl+C.")

    webview = None
    if not args.navegador:
        try:
            import webview
        except ImportError:
            webview = None
    try:
        if webview:
            janela = webview.create_window("The Unquiet", srv.url, width=1440, height=900, min_size=(960, 640),
                                           background_color="#0c0a09")

            def fechar_quando_acabar():
                jogo.join()
                time.sleep(1.5)
                janela.destroy()

            threading.Thread(target=fechar_quando_acabar, daemon=True).start()
            webview.start()
        else:
            if args.abrir:
                webbrowser.open(srv.url)
            while jogo.is_alive():
                jogo.join(0.5)
            time.sleep(1.5)  # dá tempo de o navegador receber a mensagem final
    except KeyboardInterrupt:
        pass
    finally:
        ui.respostas.put((None, None))
        srv.parar()
