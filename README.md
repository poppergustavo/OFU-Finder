# 🔎 Busca Documental V1.3

<p align="center">
  <img src="https://img.shields.io/badge/status-funcional-success" />
  <img src="https://img.shields.io/badge/version-V1.2-blue" />
  <img src="https://img.shields.io/badge/python-3.11+-yellow" />
  <img src="https://img.shields.io/badge/OCR-em%20evolução-orange" />
</p>

<p align="center">
  <b>Aplicação interna para busca documental em rede corporativa</b><br>
  com autenticação manual, localização de pastas de clientes e busca em arquivos.
</p>

---

## ✨ Sobre

A aplicação permite localizar informações dentro de diretórios de rede internos de forma rápida e simples.

⚠️ Para funcionamento correto, é necessário ter o **Python instalado na máquina**.

O usuário informa:

* usuário de rede
* senha
* nome do cliente
* termo a ser pesquisado

E o sistema:

✅ autentica na rede
✅ localiza a pasta do cliente
✅ percorre arquivos e subpastas
✅ realiza busca em arquivos `.txt`
✅ identifica `.pdf` e `.docx` para leitura futura
✅ exibe os resultados em tela

---

## 🚀 Como Funciona

```text
Login de Rede
   ↓
Busca do Cliente
   ↓
Pesquisa do Termo
   ↓
Varredura de Arquivos
   ↓
Resultado em Tela
```

---

## 🖥️ Interface

Interface simples e objetiva:

```text
Usuário de Rede
Senha
Nome do Cliente
Nome a Buscar
[Pesquisar]

Resultados da Busca

Versão atual: V1.2
```

Inclui também um aviso de **disclaimer**, reforçando que os resultados devem sempre ser conferidos manualmente.

---

## ⚙️ Requisito Obrigatório

Antes de executar a aplicação, é necessário instalar:

```text
Python 3.11+
```

Durante a instalação, marcar:

```text
✓ Add Python to PATH
```

Sem o Python instalado, a aplicação não será executada.

---

## ▶️ Execução

Execute:

```bash
python busca_documental_v1.py
```

---

## 🔐 Segurança

A senha informada:

* não é salva
* não vai para logs
* não é armazenada
* é usada apenas na sessão atual

---

## 🛣️ Roadmap

### V1.2 (Atual)

* [x] autenticação manual
* [x] busca por cliente
* [x] leitura de arquivos `.txt`
* [x] identificação de `.pdf` e `.docx`
* [x] interface com versão no rodapé
* [x] disclaimer de validação manual

### Próximas versões

* [ ] OCR para PDFs escaneados
* [ ] leitura completa de PDF
* [ ] busca mais inteligente
* [ ] exportação de resultados
* [ ] versão `.exe`

---

<p align="center">
  <b>Versão atual: V1.2</b><br>
  Projeto interno • Busca Documental Corporativa
</p>
