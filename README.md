# 🔎 Busca Documental V1.1

<p align="center">
  <img src="https://img.shields.io/badge/status-funcional-success" />
  <img src="https://img.shields.io/badge/version-V1.1-blue" />
  <img src="https://img.shields.io/badge/python-3.11+-yellow" />
  <img src="https://img.shields.io/badge/OCR-V2%20em%20breve-orange" />
</p>

<p align="center">
  <b>Aplicação interna para busca documental em rede corporativa</b><br>
  com autenticação manual, localização de pastas de clientes e busca inteligente em arquivos.
</p>

---

## ✨ Sobre o Projeto

A aplicação foi criada para facilitar a localização de informações dentro de diretórios de rede internos.

O usuário informa:

* usuário de rede
* senha de rede
* nome do cliente
* nome/termo que deseja buscar

E o sistema:

✅ autentica na rede interna
✅ localiza a pasta do cliente
✅ percorre arquivos e subpastas
✅ utiliza base de referência inteligente (`base_busca.xlsx`)
✅ retorna os resultados encontrados

---

## 🚀 Fluxo de Uso

```text
Login de Rede
   ↓
Busca do Cliente
   ↓
Busca do Nome/Termo
   ↓
Varredura de Arquivos
   ↓
Resultado em Tela
```

---

## 🖥️ Interface

Tela simples e funcional:

```text
Usuário de Rede
Senha
Nome do Cliente
Nome a Buscar
[Pesquisar]

Resultado da Busca

Versão atual: V1.1
```

Foco total em produtividade e uso rápido.

---

## 📁 Estrutura Esperada

```text
C:\BuscaDocumental\
│
├── busca_documental_v1.py
├── base_busca.xlsx
└── README.md
```

---

## 📊 Base Inteligente de Busca

Arquivo:

```text
base_busca.xlsx
```

Estrutura da planilha:

| termo_digitado | variacoes_busca                           |
| -------------- | ----------------------------------------- |
| CPOE           | cpoe; ordem médica; prescrição eletrônica |
| TASY           | tasy; sistema tasy; erp philips           |
| NIR            | nir; núcleo interno de regulação          |

### Benefício

Ao buscar:

```text
CPOE
```

O sistema também pode procurar por:

* ordem médica
* prescrição eletrônica
* variações cadastradas

Isso reduz falsos positivos e melhora a precisão.

---

## ⚙️ Instalação

## 1. Instalar Python

Recomendado:

```text
Python 3.11+
```

Durante a instalação marcar:

```text
✓ Add Python to PATH
```

---

## 2. Instalar bibliotecas

Execute no terminal:

```bash
pip install pandas openpyxl
```

> V1 utiliza leitura simples e base Excel.
> OCR e leitura avançada de PDF entram na V2.

---

## 3. Ajustar caminho da rede

No código:

```python
REDE_PATH = r"\\servidor\clientes"
```

Alterar para o caminho real da empresa.

Exemplo:

```python
REDE_PATH = r"\\srv-files\clientes"
```

---

## ▶️ Execução

Basta executar:

```bash
python busca_documental_v1.py
```

ou dar duplo clique no arquivo `.py`

---

## 🔐 Segurança

A senha informada:

* não é salva
* não vai para logs
* não vai para banco
* é usada apenas na sessão atual

Foco total em segurança corporativa.

---

## 🧠 Tecnologias Utilizadas

* Python
* Tkinter
* Pandas
* OpenPyXL
* Subprocess
* Pathlib
* OS

---

## 🛣️ Roadmap

## V1.1 (Atual)

* [x] autenticação manual
* [x] busca por cliente
* [x] varredura inicial
* [x] base inteligente com Excel
* [x] interface funcional
* [x] controle de versão no rodapé

## V2 (Próxima)

* [ ] OCR real para PDF escaneado
* [ ] leitura completa de PDF
* [ ] busca fuzzy avançada
* [ ] exportação para Excel
* [ ] cache de OCR
* [ ] versão `.exe`

## V3 (Futuro)

* [ ] dashboard corporativo
* [ ] integração com ServiceNow
* [ ] IA semântica documental
* [ ] indexação automática

---

## 💡 Nome Corporativo Bonito para Reunião

```text
Enterprise Document Search Engine
```

ou

```text
Intelligent OCR Search Platform
```

soa importante e geralmente ajuda bastante 😄

---

## 👨‍💻 Observação Final

Essa V1 foi criada com foco em:

> simplicidade + funcionalidade + evolução futura

A ideia não é começar complexo.

A ideia é começar certo.

E evoluir com segurança.

---

<p align="center">
  <b>Versão atual: V1.1</b><br>
  Projeto interno • Busca Documental Corporativa
</p>
