#!/usr/bin/env python3
"""
Hash Identifier & Cracker (educativo)
--------------------------------------
Herramienta CLI que:
  1. Identifica el tipo probable de un hash según su longitud y formato.
  2. Intenta "crackearlo" contra una wordlist (ataque de diccionario),
     probando también variantes con sal si el usuario la indica.

Uso educativo: pensado para practicar conceptos de hashing y
seguridad de contraseñas en entornos controlados (CTFs, laboratorios
propios). No debe usarse contra sistemas o cuentas de terceros sin
autorización explícita.
"""

import argparse
import hashlib
import sys
import time

# Longitud en caracteres hex -> algoritmos candidatos
HASH_LENGTHS = {
    32: ["md5", "ntlm"],
    40: ["sha1"],
    56: ["sha224"],
    64: ["sha256", "sha3_256"],
    96: ["sha384"],
    128: ["sha512", "sha3_512"],
}

SUPPORTED_ALGOS = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_256", "sha3_512"]


def identify_hash(hash_str: str) -> list[str]:
    """Devuelve la lista de algoritmos candidatos según la longitud del hash."""
    hash_str = hash_str.strip()
    length = len(hash_str)

    if not all(c in "0123456789abcdefABCDEF" for c in hash_str):
        return []

    return HASH_LENGTHS.get(length, [])


def hash_with_algo(text: str, algo: str) -> str:
    """Calcula el hash de un texto con el algoritmo indicado."""
    if algo == "ntlm":
        # NTLM = MD4 sobre UTF-16LE. hashlib no trae md4 en todos los builds,
        # así que lo dejamos fuera del cracking activo y solo lo mostramos
        # como candidato informativo en la identificación.
        return ""
    h = hashlib.new(algo)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def crack_hash(target_hash: str, algos: list[str], wordlist_path: str, salt: str = "", salt_position: str = "suffix"):
    """
    Intenta encontrar la palabra original probando cada línea de la wordlist
    contra cada algoritmo candidato. Devuelve (palabra, algoritmo) o (None, None).
    """
    target_hash = target_hash.strip().lower()
    algos = [a for a in algos if a in SUPPORTED_ALGOS]

    if not algos:
        print("[!] No hay algoritmos soportados para crackear este hash (ej: NTLM requiere librerías extra).")
        return None, None

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] No se encontró la wordlist: {wordlist_path}")
        return None, None

    print(f"[*] Probando {len(words)} palabras contra {len(algos)} algoritmo(s): {', '.join(algos)}")
    start = time.time()

    for word in words:
        candidates = [word]
        if salt:
            candidates.append(f"{word}{salt}" if salt_position == "suffix" else f"{salt}{word}")

        for candidate in candidates:
            for algo in algos:
                computed = hash_with_algo(candidate, algo)
                if computed and computed == target_hash:
                    elapsed = time.time() - start
                    print(f"[+] ¡Encontrado! '{word}' -> algoritmo: {algo} (en {elapsed:.2f}s)")
                    return word, algo

    elapsed = time.time() - start
    print(f"[-] No se encontró ninguna coincidencia en la wordlist ({elapsed:.2f}s)")
    return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Identifica el tipo de un hash y opcionalmente intenta crackearlo con una wordlist."
    )
    parser.add_argument("hash", help="Hash a analizar (en hexadecimal)")
    parser.add_argument("-w", "--wordlist", help="Ruta a la wordlist para intentar crackear el hash")
    parser.add_argument("-s", "--salt", default="", help="Sal a aplicar a cada palabra probada (opcional)")
    parser.add_argument(
        "--salt-position",
        choices=["prefix", "suffix"],
        default="suffix",
        help="Dónde colocar la sal respecto a la palabra (por defecto: suffix)",
    )
    args = parser.parse_args()

    print(f"[*] Analizando hash: {args.hash}")
    candidates = identify_hash(args.hash)

    if not candidates:
        print("[!] No se reconoce el formato. ¿Es realmente un hash en hexadecimal?")
        sys.exit(1)

    print(f"[*] Algoritmo(s) probable(s) según longitud ({len(args.hash.strip())} caracteres): {', '.join(candidates)}")

    if args.wordlist:
        crack_hash(args.hash, candidates, args.wordlist, args.salt, args.salt_position)
    else:
        print("[*] Ejecuta con -w wordlist.txt para intentar crackearlo por diccionario.")


if __name__ == "__main__":
    main()
