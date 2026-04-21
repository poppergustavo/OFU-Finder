import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from pathlib import Path

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
                resultados.append(f"[ERRO PDF] {caminho_pdf} -> {str(e)}")

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
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    resultado_texto.delete(1.0, tk.END)
    resultado_texto.insert(tk.END, "Conectando na rede...\n")

    sucesso, msg = conectar_rede(usuario, senha)

    if not sucesso:
        resultado_texto.insert(tk.END, f"\nErro:\n{msg}\n")
        return

    resultado_texto.insert(tk.END, f"{msg}\n\nBuscando...\n\n")

    resultados = buscar_arquivos(cliente, palavra)

    for item in resultados:
        resultado_texto.insert(tk.END, item + "\n")


# =============================
# UI
# =============================

janela = tk.Tk()
janela.title("OFU Finder - Busca de Documentos")
janela.geometry("900x650")
janela.configure(bg="#1e1e1e")

try:
    janela.iconbitmap(r"C:\Users\320128547\Desktop\OFU Finder\yoshi.ico")
except:
    pass


# ===== STYLE =====
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TFrame", background="#1e1e1e")
style.configure("TButton", padding=6)
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="white")


# ===== MAIN FRAME =====
main = ttk.Frame(janela)
main.pack(fill="both", expand=True, padx=20, pady=20)


# TITLE
ttk.Label(
    main,
    text="Busca de Arquivos - Oficializações",
    style="Header.TLabel"
).pack(pady=(0, 10))


# DISCLAIMER
disclaimer = tk.Label(
    main,
    text="DISCLAIMER: Esta ferramenta auxilia buscas e pode conter falhas de interpretação dependendo da qualidade dos PDFs e estrutura da rede.",
    bg="#1e1e1e",
    fg="#b80e0e",
    wraplength=850,
    justify="left"
)
disclaimer.pack(fill="x", pady=(0, 15))


# ===== FORM =====
form = ttk.Frame(main)
form.pack(fill="x", pady=5)


def add_label(text):
    return ttk.Label(form, text=text)


# usuário
add_label("Usuário de Rede").grid(row=0, column=0, sticky="w")
frame_user = ttk.Frame(form)
frame_user.grid(row=1, column=0, sticky="ew", pady=5)

ttk.Label(frame_user, text="WHEBDC\\").pack(side="left")

entry_usuario = ttk.Entry(frame_user)
entry_usuario.pack(side="left", fill="x", expand=True)


# senha
add_label("Senha").grid(row=2, column=0, sticky="w")
entry_senha = ttk.Entry(form, show="*")
entry_senha.grid(row=3, column=0, sticky="ew", pady=5)


# cliente
add_label("Cliente").grid(row=4, column=0, sticky="w")
entry_cliente = ttk.Entry(form)
entry_cliente.grid(row=5, column=0, sticky="ew", pady=5)


# palavra
add_label("Palavra-chave").grid(row=6, column=0, sticky="w")
entry_palavra = ttk.Entry(form)
entry_palavra.grid(row=7, column=0, sticky="ew", pady=5)


form.columnconfigure(0, weight=1)


# botão
btn = ttk.Button(main, text="🔎 Buscar", command=executar_busca)
btn.pack(fill="x", pady=10)


# resultado
resultado_frame = tk.Frame(main, bg="#0f0f0f", bd=1, relief="solid")
resultado_frame.pack(fill="both", expand=True)

resultado_texto = scrolledtext.ScrolledText(
    resultado_frame,
    bg="#262626",
    fg="#75ffca",
    insertbackground="white",
    font=("Consolas", 10),
    wrap="word"
)
resultado_texto.pack(fill="both", expand=True)


# ENTER pra buscar
janela.bind("<Return>", executar_busca)

entry_usuario.focus()

janela.mainloop()