"""
Verificador de Integridade de Arquivos via SHA-256.
Gera e valida assinaturas criptográficas de diretórios.
"""

import hashlib
import json
import os
from pathlib import Path


def calcular_hash_arquivo(caminho_arquivo: Path) -> str:
    hasher = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def indexar_diretorio(diretorio: str) -> dict[str, str]:
    caminho = Path(diretorio)
    manifesto = {}

    for item in caminho.rglob("*"):
        if item.is_file() and not item.name.endswith(".manifest.json"):
            rel_path = str(item.relative_to(caminho))
            manifesto[rel_path] = calcular_hash_arquivo(item)

    return manifesto


def salvar_manifesto(manifesto: dict[str, str], arquivo_saida: str) -> None:
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=4)
    print(f" Manifest gerado com sucesso em: {arquivo_saida}")


def validar_integridade(diretorio: str, arquivo_manifesto: str) -> None:
    caminho = Path(diretorio)
    with open(arquivo_manifesto, "r", encoding="utf-8") as f:
        manifesto_original = json.load(f)

    manifesto_atual = indexar_diretorio(diretorio)

    alterados = []
    ausentes = []
    novos = []

    for arq, hash_original in manifesto_original.items():
        if arq not in manifesto_atual:
            ausentes.append(arq)
        elif manifesto_atual[arq] != hash_original:
            alterados.append(arq)

    for arq in manifesto_atual:
        if arq not in manifesto_original:
            novos.append(arq)

    print("\n--- Resultado da Auditoria ---")
    if not alterados and not ausentes and not novos:
        print(" Todos os arquivos conferem com o manifesto original.")
    else:
        if alterados:
            print(f"🚨 Arquivos modificados ({len(alterados)}): {alterados}")
        if ausentes:
            print(f"❌ Arquivos ausentes ({len(ausentes)}): {ausentes}")
        if novos:
            print(f"✨ Arquivos não catalogados ({len(novos)}): {novos}")


if __name__ == "__main__":
    pasta_teste = Path("./lab_integridade")
    pasta_teste.mkdir(exist_ok=True)

    arquivo_a = pasta_teste / "config.ini"
    arquivo_a.write_text("debug=true\nport=8080", encoding="utf-8")

    manifesto_path = pasta_teste / "checksums.manifest.json"

    print("Passo 1: Criando manifesto base...")
    dados_hash = indexar_diretorio(str(pasta_teste))
    salvar_manifesto(dados_hash, str(manifesto_path))

    print("\nPasso 2: Simulando verificação em conformidade...")
    validar_integridade(str(pasta_teste), str(manifesto_path))

    print("\nPasso 3: Simulando adulteração...")
    arquivo_a.write_text("debug=false\nport=9090", encoding="utf-8")
    validar_integridade(str(pasta_teste), str(manifesto_path))
