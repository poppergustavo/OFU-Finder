import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from pathlib import Path

# =============================
# CONFIGURAÇÃO
# =============================
# Ajuste aqui o caminho raiz da rede
REDE_PATH = r"\\Srv-fs-01.whebdc.com.br\fs2\EMR\Oficializacoes_Uso"

# Extensões permitidas (V1 simples)
EXTENSOES = [".pdf", ".txt", ".docx"]

# Versão da aplicação
VERSAO = "V1.2"


# =============================
# FUNÇÕES
# =============================

def autenticar_rede(usuario, senha, dominio):
    """
    Faz autenticação simples na rede usando net use.
    """
    try:
        usuario_completo = f"{dominio}\\{usuario}"

        comando = f'net use {REDE_PATH} /user:{usuario_completo} {senha}'
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


def atualizar_campo_dominio(event=None):
    """
    Exibe ou oculta o campo de domínio personalizado.
    """
    opcao = combo_dominio.get()

    if opcao == "outro":
        label_outro_dominio.pack(pady=(5, 0))
        entry_outro_dominio.pack()
    else:
        label_outro_dominio.pack_forget()
        entry_outro_dominio.pack_forget()


def obter_dominio():
    """
    Retorna o domínio selecionado.
    """
    opcao = combo_dominio.get()

    if opcao == "whebdc":
        return "whebdc"

    dominio_personalizado = entry_outro_dominio.get().strip()

    if not dominio_personalizado:
        return None

    return dominio_personalizado


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

    for root_dir, _, files in os.walk(pasta_cliente):
        for arquivo in files:
            caminho = os.path.join(root_dir, arquivo)
            ext = Path(caminho).suffix.lower()

            if ext not in EXTENSOES:
                continue

            if ext == ".txt":
                try:
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read()

                        if termo_busca.lower() in conteudo.lower():
                            trecho = conteudo[:500]
                            resultados.append(
                                f"\nArquivo: {caminho}\n"
                                f"Trecho inicial:\n{trecho}\n"
                                f"{'-'*60}\n"
                            )
                except Exception:
                    pass

            else:
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
    dominio = obter_dominio()

    if not all([usuario, senha, cliente, nome_busca]):
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    if not dominio:
        messagebox.showwarning(
            "Atenção",
            "Informe o domínio de rede."
        )
        return

    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, "Autenticando na rede...\n")
    root.update()

    ok, msg = autenticar_rede(usuario, senha, dominio)

    if not ok:
        messagebox.showerror("Erro de autenticação", msg)
        return

    resultado_texto.insert(
        tk.END,
        f"Autenticação realizada com sucesso ({dominio}\\{usuario}).\n\n"
    )

    resultado_texto.insert(
        tk.END,
        f"Procurando pasta do cliente: {cliente}\n"
    )
    root.update()

    pasta = localizar_pasta_cliente(cliente)

    if not pasta:
        messagebox.showinfo(
            "Não encontrado",
            "Pasta do cliente não localizada."
        )
        return

    resultado_texto.insert(
        tk.END,
        f"Pasta encontrada:\n{pasta}\n\n"
    )

    resultado_texto.insert(
        tk.END,
        f"Buscando por: {nome_busca}\n"
    )
    resultado_texto.insert(tk.END, "Aguarde...\n\n")
    root.update()

    resultados = buscar_nome_em_arquivos(str(pasta), nome_busca)

    if resultados:
        resultado_texto.insert(tk.END, "RESULTADOS ENCONTRADOS:\n")
        for item in resultados:
            resultado_texto.insert(tk.END, item)
    else:
        resultado_texto.insert(
            tk.END,
            "Nenhum resultado encontrado.\n"
        )


# =============================
# INTERFACE
# =============================

root = tk.Tk()
root.title("Busca Documental V1")
root.geometry("800x650")

# -----------------------------
# DOMÍNIO + USUÁRIO
# -----------------------------

tk.Label(root, text="Domínio de Rede").pack(pady=(10, 0))

combo_dominio = ttk.Combobox(
    root,
    values=["whebdc", "outro"],
    state="readonly",
    width=20
)
combo_dominio.pack()
combo_dominio.set("whebdc")
combo_dominio.bind("<<ComboboxSelected>>", atualizar_campo_dominio)

label_outro_dominio = tk.Label(root, text="Informe o domínio")
entry_outro_dominio = tk.Entry(root, width=50)

tk.Label(root, text="Usuário de Rede").pack(pady=(10, 0))
entry_usuario = tk.Entry(root, width=50)
entry_usuario.pack()

tk.Label(root, text="Senha").pack(pady=(10, 0))
entry_senha = tk.Entry(root, width=50, show="*")
entry_senha.pack()

# -----------------------------
# BUSCA
# -----------------------------

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

resultado_texto = scrolledtext.ScrolledText(
    root,
    width=90,
    height=20
)
resultado_texto.pack(padx=10, pady=10)

# Rodapé com versão
rodape = tk.Label(
    root,
    text=f"Versão {VERSAO}",
    font=("Arial", 9),
    fg="gray"
)
rodape.pack(side="bottom", pady=5)

root.mainloop()