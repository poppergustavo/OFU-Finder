import os
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

# Versão da aplicação
VERSAO = "V1.3"


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
root.title("OFU Finder V1.3")
root.geometry("800x750")  # aumentei um pouco para comportar o disclaimer

# =============================
# DISCLAIMER
# =============================

disclaimer_texto = (
    "DISCLAIMER:\n"
    "Esta aplicação realiza buscas automatizadas e pode apresentar erros de interpretação "
    "devido à qualidade dos arquivos, digitalização, OCR, estrutura do documento ou método "
    "de pesquisa utilizado.\n\n"
    "Os resultados apresentados servem apenas como apoio à análise e NÃO substituem a "
    "validação manual do usuário.\n\n"
    "A aplicação não deve limitar a análise crítica, sendo indispensável que o usuário "
    "revise, confira e valide cuidadosamente todas as informações retornadas antes de "
    "qualquer decisão ou conclusão."
)

disclaimer_label = tk.Label(
    root,
    text=disclaimer_texto,
    font=("Arial", 9),
    fg="darkred",
    justify="left",
    wraplength=760,
    padx=10,
    pady=10,
    relief="solid",
    bd=1
)
disclaimer_label.pack(padx=10, pady=(10, 5), fill="x")

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

# Rodapé com versão
rodape = tk.Label(
    root,
    text=f"Versão {VERSAO}",
    font=("Arial", 9),
    fg="gray"
)
rodape.pack(side="bottom", pady=5)


root.mainloop()