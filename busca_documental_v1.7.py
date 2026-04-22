import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from pathlib import Path
from flask import Flask, jsonify
import threading

app = Flask(__name__)


@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "app": "busca_documental_v1.7.py"
    })


def iniciar_servidor_local():
    app.run(host="127.0.0.1", port=8765, debug=False, use_reloader=False)


threading.Thread(target=iniciar_servidor_local, daemon=True).start()


# =============================
# CONFIGURAÇÃO
# =============================

REDE_PATH = r"\\Srv-fs-01.whebdc.com.br\fs2\EMR\Oficializacoes_Uso"


# =============================
# FUNÇÕES
# =============================


def conectar_rede(usuario, senha):
    try:
        comando = [
            "net",
            "use",
            REDE_PATH,
            senha,
            f"/user:{usuario}"
        ]

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=True
        )

        if resultado.returncode != 0:
            return False, resultado.stderr.strip()

        return True, "Conectado com sucesso."

    except Exception as e:
        return False, str(e)



def buscar_arquivos(cliente, palavra_chave):
    import pdfplumber
    import re

    resultados = []

    cliente_digitado = cliente.strip().lower()
    palavra_digitada = palavra_chave.strip().lower()

    palavras_cliente = cliente_digitado.split()
    palavras_chave = palavra_digitada.split()

    pasta_encontrada = None

    for item in Path(REDE_PATH).iterdir():
        if item.is_dir():
            nome = item.name.lower().replace("_", " ").replace("-", " ").replace(".", " ")

            if all(p in nome for p in palavras_cliente):
                pasta_encontrada = item
                break

    if not pasta_encontrada:
        return [f"Nenhuma pasta encontrada para: {cliente}"]

    resultados.append(f"Pasta encontrada: {pasta_encontrada}")
    resultados.append("Iniciando busca nos PDFs...\n")

    termo_regex = r"\s+".join([re.escape(p) for p in palavras_chave])
    padrao = re.compile(rf"\b{termo_regex}\b", re.IGNORECASE)

    for root, dirs, files in os.walk(pasta_encontrada):
        for arquivo in files:
            if not arquivo.lower().endswith(".pdf"):
                continue

            caminho_pdf = os.path.join(root, arquivo)

            try:
                with pdfplumber.open(caminho_pdf) as pdf:
                    for numero_pagina, pagina in enumerate(pdf.pages, start=1):
                        texto = pagina.extract_text()

                        if not texto:
                            continue

                        texto = texto.lower().replace("_", " ").replace("-", " ").replace(".", " ")

                        if padrao.search(texto):
                            resultados.append(
                                f"[OK] {caminho_pdf} | Página: {numero_pagina}"
                            )
                            break

            except Exception as e:
                resultados.append(
                    f"[ERRO PDF] {caminho_pdf} -> {str(e)}"
                )

    if len(resultados) <= 2:
        resultados.append("Nenhum PDF encontrado contendo essa palavra-chave.")

    resultados.append("\nBusca finalizada.")
    return resultados



def executar_busca(event=None):
    usuario = f"WHEBDC\\{entry_usuario.get().strip()}"
    senha = entry_senha.get().strip()
    cliente = entry_cliente.get().strip()
    palavra = entry_palavra.get().strip()

    if not all([entry_usuario.get().strip(), senha, cliente, palavra]):
        messagebox.showwarning(
            "Campos obrigatórios",
            "Preencha todos os campos."
        )
        return

    resultado_texto.delete(1.0, tk.END)
    resultado_texto.insert(tk.END, "Conectando na rede...\n")

    sucesso, msg = conectar_rede(usuario, senha)

    if not sucesso:
        resultado_texto.insert(
            tk.END,
            f"\nErro:\n{msg}\n"
        )
        return

    resultado_texto.insert(
        tk.END,
        f"{msg}\n\nBuscando arquivos...\n\n"
    )

    resultados = buscar_arquivos(cliente, palavra)

    for item in resultados:
        resultado_texto.insert(
            tk.END,
            item + "\n"
        )


# =============================
# UI
# =============================

janela = tk.Tk()
janela.title("OFU Finder - Busca de Documentos")
janela.geometry("950x700")
janela.configure(bg="#F4F7FA")

try:
    janela.iconbitmap(
        r"C:\Users\320128547\Desktop\OFU Finder\yoshi.ico"
    )
except:
    pass


# =============================
# PALETA DE CORES
# =============================

COR_BG = "#F4F7FA"
COR_CARD = "#FFFFFF"
COR_PRIMARIA = "#2563EB"
COR_PRIMARIA_HOVER = "#1D4ED8"
COR_TEXTO = "#1F2937"
COR_SUBTEXTO = "#6B7280"
COR_ALERTA = "#B91C1C"
COR_RESULTADO_BG = "#111827"
COR_RESULTADO_TXT = "#A7F3D0"


# =============================
# STYLE
# =============================

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=COR_BG)
style.configure("TLabel", background=COR_BG, foreground=COR_TEXTO, font=("Segoe UI", 10))
style.configure("Title.TLabel", background=COR_BG, foreground=COR_TEXTO, font=("Segoe UI Semibold", 18, "bold"))
style.configure("Sub.TLabel", background=COR_BG, foreground=COR_SUBTEXTO, font=("Segoe UI", 10))

style.configure(
    "TEntry",
    padding=4,
    font=("Segoe UI", 10)
)

style.configure(
    "Buscar.TButton",
    font=("Segoe UI Semibold", 11, "bold"),
    padding=10
)

style.map(
    "Buscar.TButton",
    background=[
        ("active", COR_PRIMARIA_HOVER),
        ("!active", COR_PRIMARIA)
    ],
    foreground=[("!disabled", "white")]
)


# =============================
# MAIN FRAME
# =============================

main = ttk.Frame(janela)
main.pack(fill="both", expand=True, padx=25, pady=20)


ttk.Label(main, text="OFU Finder", style="Title.TLabel").pack(anchor="w")

ttk.Label(
    main,
    text="Busca inteligente de documentos de oficialização",
    style="Sub.TLabel"
).pack(anchor="w", pady=(0, 15))


disclaimer = tk.Label(
    main,
    text=(
        "AVISO: Esta ferramenta auxilia buscas e pode conter falhas "
        "de interpretação dependendo da qualidade dos PDFs e da "
        "estrutura da rede."
    ),
    bg="#FEF2F2",
    fg=COR_ALERTA,
    font=("Segoe UI", 10, "bold"),
    wraplength=880,
    justify="left",
    padx=12,
    pady=10,
    relief="solid",
    bd=1
)

disclaimer.pack(fill="x", pady=(0, 15))


# =============================
# FORMULÁRIO
# =============================

card = tk.Frame(
    main,
    bg=COR_CARD,
    bd=1,
    relief="solid",
    highlightthickness=0
)

card.pack(fill="x", pady=(0, 8))

form = ttk.Frame(card)
form.pack(fill="x", padx=20, pady=10)


def add_label(text):
    return ttk.Label(form, text=text)


add_label("Usuário de Rede").grid(row=0, column=0, sticky="w")

frame_user = ttk.Frame(form)
frame_user.grid(row=1, column=0, sticky="ew", pady=3)


ttk.Label(frame_user, text="WHEBDC\\").pack(side="left")

entry_usuario = ttk.Entry(frame_user)
entry_usuario.pack(side="left", fill="x", expand=True)


add_label("Senha").grid(row=2, column=0, sticky="w")
entry_senha = ttk.Entry(form, show="*")
entry_senha.grid(row=3, column=0, sticky="ew", pady=3)


add_label("Cliente").grid(row=4, column=0, sticky="w")
entry_cliente = ttk.Entry(form)
entry_cliente.grid(row=5, column=0, sticky="ew", pady=3)


add_label("Palavra-chave").grid(row=6, column=0, sticky="w")
entry_palavra = ttk.Entry(form)
entry_palavra.grid(row=7, column=0, sticky="ew", pady=3)

form.columnconfigure(0, weight=1)


btn = ttk.Button(
    main,
    text="🔎 Buscar Arquivos",
    command=executar_busca,
    style="Buscar.TButton"
)
btn.pack(fill="x", pady=(0, 15))


resultado_label = ttk.Label(
    main,
    text="Resultados da Busca",
    style="Sub.TLabel"
)
resultado_label.pack(anchor="w", pady=(0, 5))


resultado_frame = tk.Frame(
    main,
    bg=COR_RESULTADO_BG,
    bd=1,
    relief="solid"
)
resultado_frame.pack(fill="both", expand=True)


resultado_texto = scrolledtext.ScrolledText(
    resultado_frame,
    bg=COR_RESULTADO_BG,
    fg=COR_RESULTADO_TXT,
    insertbackground="white",
    font=("Consolas", 10),
    wrap="word",
    relief="flat",
    padx=12,
    pady=12
)

resultado_texto.pack(fill="both", expand=True)


janela.bind("<Return>", executar_busca)
entry_usuario.focus()

janela.mainloop()
