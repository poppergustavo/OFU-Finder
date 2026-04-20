# OFU Finder

<p align="center">
  <img src="https://img.shields.io/badge/status-funcional-success" />
  <img src="https://img.shields.io/badge/version-V1.5-blue" />
  <img src="https://img.shields.io/badge/formato-.exe-lightgrey" />
</p>

---

## Como executar

A aplicação não precisa de instalação de Python na máquina do usuário.

Basta executar o arquivo:

```text
busca_documental_v1.5.exe
```

Este executável já contém todas as dependências necessárias para funcionamento.

---

## Onde encontrar o executável

Após a geração com PyInstaller, o arquivo ficará dentro da pasta:

```text
dist
```

Exemplo:

```text
Projeto/
├── dist/
│   └── busca_documental_v1.5.exe
├── build/
├── busca_documental_v1.5.py
└── README_EXECUTAVEL.md
```

O arquivo que deve ser utilizado e distribuído é:

```text
dist\busca_documental_v1.5.exe
```

---

## Como utilizar

1. Abra o executável `busca_documental_v1.5.exe`
2. Preencha os campos obrigatórios:

   * Usuário de Rede
   * Senha
   * Cliente
   * Palavra-chave
3. Clique em **Buscar**
4. Aguarde a autenticação e a varredura dos PDFs
5. Verifique os resultados exibidos no painel inferior estilo terminal

---

## Importante

Mesmo utilizando o `.exe`, ainda é necessário:

* possuir acesso à rede corporativa
* ter permissão no compartilhamento de rede
* informar corretamente usuário e senha de rede

A aplicação depende dessas permissões para localizar os documentos.

---

## Disclaimer

A ferramenta é um apoio operacional e não substitui a análise manual do usuário.

Ela pode apresentar limitações dependendo da qualidade dos arquivos PDF, estrutura de pastas ou critérios de pesquisa utilizados.

Caso nenhum resultado seja encontrado, a validação manual continua sendo necessária.

A responsabilidade da conferência final permanece sempre com o usuário.
