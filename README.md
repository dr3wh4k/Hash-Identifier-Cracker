# 🔓 Hash Toolkit — Identificador y Cracker de Hashes (educativo)

Herramienta de línea de comandos escrita en Python que:

1. **Identifica** el algoritmo probable de un hash (MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3) según su longitud y formato.
2. **Intenta crackearlo** mediante un ataque de diccionario contra una wordlist, con soporte opcional para salting.

Proyecto creado con fines educativos para practicar conceptos de hashing y seguridad de contraseñas en laboratorios propios y CTFs.

> ⚠️ **Uso responsable:** esta herramienta está pensada para practicar en tus propios hashes o en entornos autorizados (CTFs, labs). No la uses contra cuentas o sistemas de terceros sin permiso explícito.

## ⚙️ Instalación

No requiere librerías externas, solo Python 3.9 o superior.

```bash
# 1. Clona el repositorio
git clone https://github.com/dr3wh4k/Hash-Identifier-Cracker
cd hash-toolkit

# 2. Comprueba que tienes Python 3.9+
python3 --version

# 3. (Opcional) Dale permisos de ejecución al script
chmod +x hash_toolkit.py

# 4. Listo, ya puedes ejecutarlo
python3 hash_toolkit.py --help
```

No hace falta `pip install` ni entorno virtual, ya que solo usa la librería estándar (`hashlib`, `argparse`, `time`).

## 🚀 Uso

```bash
# Solo identificar el tipo de hash
python3 hash_toolkit.py 5f4dcc3b5aa765d61d8327deb882cf99

# Identificar y crackear contra una wordlist
python3 hash_toolkit.py 5f4dcc3b5aa765d61d8327deb882cf99 -w sample_wordlist.txt

# Con sal (por ejemplo, si sospechas que se aplicó "sal123" al final)
python3 hash_toolkit.py <hash> -w sample_wordlist.txt -s sal123 --salt-position suffix
```

### Ejemplo

```
$ python3 hash_toolkit.py d6a6bc0db10694a2d90e3a69648f3a03 -w sample_wordlist.txt
[*] Analizando hash: d6a6bc0db10694a2d90e3a69648f3a03
[*] Algoritmo(s) probable(s) según longitud (32 caracteres): md5, ntlm
[*] Probando 10 palabras contra 1 algoritmo(s): md5
[+] ¡Encontrado! 'hacker' -> algoritmo: md5 (en 0.00s)
```

## 🧠 Cómo funciona

- La **identificación** se basa en la longitud del hash en hexadecimal (32 chars → MD5, 40 → SHA1, 64 → SHA256, etc.). No es 100% infalible ya que varios algoritmos comparten longitud, pero da candidatos razonables.
- El **cracking** genera el hash de cada palabra de la wordlist con cada algoritmo candidato y compara contra el hash objetivo — el mismo principio que usan herramientas como `hashcat` o `john`, simplificado.
- Incluye una `sample_wordlist.txt` pequeña para probar rápido; puedes sustituirla por wordlists más grandes (ej. `rockyou.txt`).

## 🛠️ Posibles mejoras (ideas para seguir el proyecto)

- Soporte para hashes salados con formato `hash:salt`
- Multithreading para acelerar el diccionario en wordlists grandes
- Soporte para bcrypt/scrypt (requieren comparación distinta, no por igualdad directa)
- Modo interactivo / barra de progreso

## 📦 Requisitos

Solo Python 3.9+ (usa la librería estándar `hashlib`, sin dependencias externas).

---

Parte de mi práctica en ciberseguridad — más proyectos y writeups en [dr3wh4k.github.io](https://dr3wh4k.github.io) y [CTF-writeups](https://github.com/dr3wh4k/CTF-writeups).
