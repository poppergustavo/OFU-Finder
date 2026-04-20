# README - Busca de Documentos em Rede

<p align="center">
  <img src="https://img.shields.io/badge/status-funcional-success" />
  <img src="https://img.shields.io/badge/version-V1.4-blue" />
  <img src="https://img.shields.io/badge/python-3.11+-yellow" />
  <img src="https://img.shields.io/badge/OCR-em%20evolução-orange" />
</p>

## Sobre a aplicação

Esta aplicação em Python foi desenvolvida para facilitar a busca de documentos PDF dentro do diretório de rede:

```text
\\Srv-fs-01.whebdc.com.br\fs2\EMR\Oficializacoes_Uso
```

A ferramenta permite:

- autenticação com usuário e senha de rede
- busca aproximada da pasta do cliente
- varredura completa dentro da pasta localizada
- leitura interna de arquivos PDF
- busca por palavra-chave específica (palavra inteira)
- exibição do arquivo encontrado e da página onde a palavra foi localizada
- interface simples com retorno estilo terminal (CMD)

> Importante: a aplicação é um apoio operacional e não substitui a validação manual do usuário.

---

## Requisitos

Antes de executar a aplicação, é necessário instalar:

- Python 3.10 ou superior
- biblioteca `pdfplumber`

---

## 1. Instalando o Python

### Baixe o Python

Acesse o site oficial:

```text
https://www.python.org/downloads/
```

Baixe a versão mais recente recomendada.

### Durante a instalação

Marque obrigatoriamente a opção:

```text
☑ Add Python to PATH
```

Depois clique em:

```text
Install Now
```

Isso evita diversos problemas futuros.

---

## 2. Verificando se o Python foi instalado

Abra o Prompt de Comando (CMD):

```text
Win + R
→ digite: cmd
→ pressione Enter
```

Digite:

```bash
python --version
```

Se aparecer algo como:

```text
Python 3.12.1
```

está tudo certo.

---

## 3. Instalando a biblioteca necessária

No CMD, execute:

```bash
pip install pdfplumber
```

Se ocorrer erro com `pip`, tente:

```bash
python -m pip install pdfplumber
```

ou

```bash
py -m pip install pdfplumber
```

---

## 4. Validando a instalação

Para confirmar:

```bash
pip show pdfplumber
```

Se aparecer informações como Name, Version e Location, a instalação foi concluída com sucesso.

---

## 5. Como executar a aplicação

Salve o arquivo principal como:

```text
busca_documentos.py
```

Depois execute no CMD:

```bash
python busca_documentos.py
```

A tela da aplicação será aberta.

---

## Como utilizar

Preencha os campos:

- Usuário de Rede
- Senha
- Cliente
- Palavra-chave

Depois clique em:

```text
Buscar
```

A aplicação irá:

1. autenticar na rede
2. localizar a pasta do cliente
3. abrir os PDFs encontrados
4. buscar a palavra-chave dentro dos documentos
5. mostrar os resultados encontrados

---

## Observações importantes

### A busca é feita por palavra inteira

Exemplo:

Buscar por:

```text
contrato
```

Encontra exatamente a palavra desejada, evitando resultados muito aproximados.

---

### PDFs digitalizados podem falhar

Alguns PDFs são imagens escaneadas e podem não permitir leitura correta.

Nestes casos:

- podem ocorrer falhas
- pode ser necessária análise manual

---

## Disclaimer

Esta ferramenta ainda necessita de testes e não garante 100% de precisão em todos os cenários.

Ela não substitui a análise humana.

Caso nenhum resultado seja encontrado, a validação e ação manual continuam sendo obrigatórias.

A ferramenta não pensa pelo usuário — ela apenas auxilia e facilita o processo.

---

## Autor

Aplicação interna para apoio operacional de busca documental.

