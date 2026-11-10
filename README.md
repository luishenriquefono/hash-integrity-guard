# hash-integrity-guard
Ferramenta CLI desenvolvida para auditar integridade de diretórios usando streams de leitura de baixo consumo de memória e hashing SHA-256, gerando manifestos JSON versionáveis.
# 🔒 Hash Integrity Guard

Um utilitário CLI em Python puro para monitoramento e auditoria de integridade de arquivos em diretórios locais, utilizando assinaturas criptográficas **SHA-256**.

---

### 📌 Sobre o Projeto

Garantir a integridade de dados e arquivos de configuração é essencial tanto em rotinas de segurança quanto em auditorias forenses e de conformidade. 

O **Hash Integrity Guard** automatiza a criação de uma linha de base (*baseline*) criptográfica de uma pasta inteira. Em auditorias posteriores, o script compara o estado atual contra o manifesto original, identificando instantaneamente qualquer arquivo modificado, excluído ou introduzido sem autorização.

---

### ⚙️ Funcionalidades

- **Varredura Recursiva:** Percorre diretórios e subpastas de forma automática via `pathlib.Path`.
- **Cálculo de Hash Eficiente:** Processa arquivos em blocos de memória (*chunks* de 4 KB), permitindo calcular o hash de arquivos grandes sem estourar o consumo de RAM.
- **Manifesto em JSON:** Exporta o catálogo com os caminhos relativos e os respectivos hashes SHA-256 em formato legível e versionável.
- **Detecção de 3 Estados de Violação:**
  - 🚨 **Modificados:** Arquivos cujo conteúdo foi alterado (divergência de hash).
  - ❌ **Ausentes:** Arquivos que constavam no manifesto e foram deletados/movidos.
  - ✨ **Não catalogados:** Novos arquivos adicionados após a geração do manifesto.
- **Zero Dependências:** Construído exclusivamente com bibliotecas padrão do Python (`hashlib`, `json`, `pathlib`, `os`).

---

### 🚀 Como Executar

#### Pré-requisitos
- Python 3.10 ou superior instalado.

#### Passo a passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/hash-integrity-guard.git](https://github.com/seu-usuario/hash-integrity-guard.git)
   cd hash-integrity-guard
