import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
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
            nome = (
                item.name.lower()
                .replace("_", " ")
                .replace("-", " ")
                .replace(".", " ")
            )

            if all(p in nome for p in palavras_cliente):
                pasta_encontrada = item
                break

    if not pasta_encontrada:
        return [f"Nenhuma pasta encontrada para: {cliente}"]

    resultados.append(f"Pasta encontrada: {pasta_encontrada}")
    resultados.append("Iniciando busca nos PDFs...\n")

    termo_regex = r"\s+".join(
        [re.escape(p) for p in palavras_chave]
    )

    padrao = re.compile(
        rf"\b{termo_regex}\b",
        re.IGNORECASE
    )

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

                        texto = (
                            texto.lower()
                            .replace("_", " ")
                            .replace("-", " ")
                            .replace(".", " ")
                        )

                        if padrao.search(texto):
                            resultados.append(
                                f"[PDF ENCONTRADO] {caminho_pdf} | Página: {numero_pagina}"
                            )
                            break

            except Exception as e:
                resultados.append(
                    f"[ERRO AO LER PDF] {caminho_pdf} -> {str(e)}"
                )

    if len(resultados) <= 2:
        resultados.append(
            "Nenhum PDF encontrado contendo essa palavra-chave."
        )

    resultados.append("\nBusca finalizada.")
    return resultados


def executar_busca():
    # Agora o usuário digita apenas o login
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
            f"\nErro na autenticação:\n{msg}\n"
        )
        return

    resultado_texto.insert(
        tk.END,
        f"{msg}\n\nIniciando busca...\n\n"
    )

    resultados = buscar_arquivos(cliente, palavra)

    for item in resultados:
        resultado_texto.insert(tk.END, item + "\n")


# =============================
# INTERFACE
# =============================

janela = tk.Tk()
janela.title("Busca de Documentos em Rede")
janela.geometry("850x600")
janela.resizable(True, True)

# Ícone da aplicação
try:
    janela.iconbitmap("C:\\Users\\320128547\\Desktop\\OFU Finder\\yoshi.ico")
except:
    pass

# Frame principal
frame = tk.Frame(janela, padx=20, pady=20)
frame.pack(fill="both", expand=True)

# Título
titulo = tk.Label(
    frame,
    text="Busca de Arquivos - Oficializações",
    font=("Arial", 14, "bold")
)
titulo.pack(pady=(0, 15))

# =============================
# DISCLAIMER
# =============================

disclaimer = tk.Label(
    frame,
    text=(
        "DISCLAIMER: Esta ferramenta é um apoio operacional e facilitador de busca, "
        "não substituindo a análise manual do usuário. Podem ocorrer falhas de leitura, "
        "interpretação ou localização de arquivos devido à qualidade dos PDFs, "
        "digitalizações, estrutura de pastas ou critérios de pesquisa utilizados.\n\n"
        "A ferramenta ainda necessita de testes e não garante 100% de precisão em todos os casos. "
        "Caso nenhum resultado seja encontrado, é necessária a validação e ação manual pelo usuário. "
        "A responsabilidade da conferência final sempre deve ser humana."
    ),
    font=("Arial", 9),
    fg="red",
    justify="left",
    wraplength=780,
    anchor="w"
)

disclaimer.pack(fill="x", pady=(0, 15))

# =============================
# USUÁRIO DE REDE (com domínio fixo)
# =============================

tk.Label(frame, text="Usuário de Rede").pack(anchor="w")

frame_usuario = tk.Frame(frame)
frame_usuario.pack(fill="x", pady=(0, 10))

tk.Label(
    frame_usuario,
    text="WHEBDC\\",
    font=("Arial", 10, "bold")
).pack(side="left")

entry_usuario = tk.Entry(frame_usuario, width=50)
entry_usuario.pack(side="left", fill="x", expand=True)

# Senha
tk.Label(frame, text="Senha").pack(anchor="w")
entry_senha = tk.Entry(frame, width=50, show="*")
entry_senha.pack(fill="x", pady=(0, 10))

# Cliente
tk.Label(frame, text="Cliente").pack(anchor="w")
entry_cliente = tk.Entry(frame, width=50)
entry_cliente.pack(fill="x", pady=(0, 10))

# Palavra-chave
tk.Label(frame, text="Palavra-chave").pack(anchor="w")
entry_palavra = tk.Entry(frame, width=50)
entry_palavra.pack(fill="x", pady=(0, 15))

# Botão
btn_buscar = tk.Button(
    frame,
    text="Buscar",
    font=("Arial", 10, "bold"),
    command=executar_busca,
    height=2
)
btn_buscar.pack(fill="x", pady=(0, 15))

# Área de resultado estilo CMD
resultado_texto = scrolledtext.ScrolledText(
    frame,
    height=20,
    bg="black",
    fg="white",
    font=("Consolas", 10)
)
resultado_texto.pack(fill="both", expand=True)

janela.mainloop()