import os
import pandas as pd
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path

# =============================
# CONFIGURAÇÃO
# =============================
# Ajuste aqui o caminho raiz da rede
REDE_PATH = r"\\Srv-fs-01.whebdc.com.br\fs2\EMR\Oficializacoes_Uso"

# Extensões permitidas (V1 simples)
EXTENSOES = [".pdf", ".txt", ".docx"]

# Arquivo de base de busca
BASE_BUSCA_FILE = "base_busca.xlsx"


# =============================
# FUNÇÕES
# =============================

def autenticar_rede(usuario, senha):
    """
    Faz autenticação simples na rede usando net use.
    """
    try:
        comando = f'net use {REDE_PATH} /user:{usuario} {senha}'
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return True, "Autenticação realizada com sucesso."
        else:
            return False, resultado.stderr or resultado.stdout

    except Exception as e:
        return False, str(e)



def carregar_base_busca():
    """
    Lê a base de busca em Excel.
    Estrutura esperada:
    coluna 1: termo_digitado
    coluna 2: variacoes_busca
    """
    try:
        if not os.path.exists(BASE_BUSCA_FILE):
            return {}

        df = pd.read_excel(BASE_BUSCA_FILE)
        base = {}

        for _, row in df.iterrows():
            termo = str(row["termo_digitado"]).strip().lower()
            variacoes = str(row["variacoes_busca"]).strip().lower().split(";")
            base[termo] = [v.strip() for v in variacoes if v.strip()]

        return base

    except Exception as e:
        print(f"Erro ao carregar base de busca: {e}")
        return {}


def localizar_pasta_cliente(nome_cliente):
    """
    Procura uma pasta que contenha o nome informado.
    Busca simples por substring.
    """
    try:
        raiz = Path(REDE_PATH)

        if not raiz.exists():
            return None

        for pasta in raiz.iterdir():
            if pasta.is_dir() and nome_cliente.lower() in pasta.name.lower():
                return pasta

        return None

    except Exception:
        return None



def buscar_nome_em_arquivos(pasta_cliente, termo_busca):
    """
    V1 SIMPLES:
    Busca apenas em arquivos TXT.

    PDFs escaneados + OCR entram na V2.
    """
    resultados = []

    base = carregar_base_busca()

    if termo_busca.lower() in base:
        termos_para_busca = [termo_busca.lower()] + base[termo_busca.lower()]
    else:
        termos_para_busca = [termo_busca.lower()]

    for root, _, files in os.walk(pasta_cliente):
        for arquivo in files:
            caminho = os.path.join(root, arquivo)
            ext = Path(caminho).suffix.lower()

            if ext not in EXTENSOES:
                continue

            # V1 funcional: leitura direta apenas TXT
            if ext == ".txt":
                try:
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read()

                        if any(t in conteudo.lower() for t in termos_para_busca):
                            trecho = conteudo[:500]
                            resultados.append(
                                f"\nArquivo: {caminho}\n"
                                f"Trecho inicial:\n{trecho}\n"
                                f"{'-'*60}\n"
                            )
                except Exception:
                    pass

            else:
                # PDF/DOCX ficam preparados para V2
                resultados.append(
                    f"\nArquivo encontrado (leitura futura V2): {caminho}\n"
                    f"Tipo: {ext}\n"
                    f"Observação: OCR/leitura avançada será implementado na próxima versão.\n"
                    f"{'-'*60}\n"
                )

    return resultados



def executar_busca():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    cliente = entry_cliente.get().strip()
    nome_busca = entry_nome.get().strip()

    if not all([usuario, senha, cliente, nome_busca]):
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, "Autenticando na rede...\n")
    root.update()

    ok, msg = autenticar_rede(usuario, senha)

    if not ok:
        messagebox.showerror("Erro de autenticação", msg)
        return

    resultado_texto.insert(tk.END, "Autenticação realizada com sucesso.\n\n")
    resultado_texto.insert(tk.END, f"Procurando pasta do cliente: {cliente}\n")
    root.update()

    pasta = localizar_pasta_cliente(cliente)

    if not pasta:
        messagebox.showinfo("Não encontrado", "Pasta do cliente não localizada.")
        return

    resultado_texto.insert(tk.END, f"Pasta encontrada:\n{pasta}\n\n")
    resultado_texto.insert(tk.END, f"Buscando por: {nome_busca}\n")
    resultado_texto.insert(tk.END, "Aguarde...\n\n")
    root.update()

    resultados = buscar_nome_em_arquivos(str(pasta), nome_busca)

    if resultados:
        resultado_texto.insert(tk.END, "RESULTADOS ENCONTRADOS:\n")
        for item in resultados:
            resultado_texto.insert(tk.END, item)
    else:
        resultado_texto.insert(tk.END, "Nenhum resultado encontrado.\n")


# =============================
# INTERFACE
# =============================

root = tk.Tk()
root.title("Busca Documental V1")
root.geometry("800x650")

VERSAO_ATUAL = "Versão atual: V1.1"

# Login

tk.Label(root, text="Usuário de Rede").pack(pady=(10, 0))
entry_usuario = tk.Entry(root, width=50)
entry_usuario.pack()


tk.Label(root, text="Senha").pack(pady=(10, 0))
entry_senha = tk.Entry(root, width=50, show="*")
entry_senha.pack()

# Busca

tk.Label(root, text="Nome do Cliente").pack(pady=(20, 0))
entry_cliente = tk.Entry(root, width=60)
entry_cliente.pack()


tk.Label(root, text="Nome a Buscar").pack(pady=(10, 0))
entry_nome = tk.Entry(root, width=60)
entry_nome.pack()


btn_buscar = tk.Button(
    root,
    text="Pesquisar",
    command=executar_busca,
    width=20,
    height=2
)
btn_buscar.pack(pady=20)


resultado_texto = scrolledtext.ScrolledText(root, width=90, height=20)
resultado_texto.pack(padx=10, pady=10)

label_versao = tk.Label(root, text=VERSAO_ATUAL)
label_versao.pack(pady=(0, 10))


root.mainloop()
