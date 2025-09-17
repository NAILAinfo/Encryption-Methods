## Cryptography Tree

```bash
Cryptography methods
│
├── 1. Classical Cryptography
│   │
│   ├── Substitution
│   │   ├── Caesar Cipher
│   │   ├── Atbash Cipher (alphabet reversal)
│   │   ├── ROT13 (Caesar with shift 13)
│   │   ├── Monoalphabetic Substitution
│   │   └── Polybius Square (5x5 grid)
│   │
│   ├── Transposition
│   │   ├── Scytale (Spartan staff)
│   │   ├── Columnar Transposition
│   │   └── Rail Fence Cipher (zigzag writing)
│   │
│   └── Polyalphabetic
│       ├── Vigenère Cipher
│       ├── Beaufort Cipher
│       └── Autokey Cipher
│
├── 2. Modern Cryptography
│   │
│   ├── Symmetric Encryption
│   │   ├── DES (Data Encryption Standard, outdated)
│   │   ├── 3DES (Triple DES)
│   │   ├── AES (128, 192, 256 bits)
│   │   ├── Blowfish
│   │   ├── Twofish
│   │   └── ChaCha20
│   │
│   ├── Asymmetric Encryption
│   │   ├── RSA
│   │   ├── ECC (Elliptic Curve Cryptography: ECDSA, Ed25519, Curve25519)
│   │   ├── Diffie-Hellman (key exchange)
│   │   └── ElGamal
│   │
│   ├── Hash Functions (irreversible)
│   │   ├── MD5 (insecure, deprecated)
│   │   ├── SHA-1 (deprecated)
│   │   ├── SHA-2 (SHA-224, SHA-256, SHA-512)
│   │   ├── SHA-3 (Keccak)
│   │   ├── Bcrypt
│   │   ├── Scrypt
│   │   └── Argon2 / PBKDF2
│   │
│   ├── Digital Signatures
│   │   ├── RSA Signature
│   │   ├── DSA (Digital Signature Algorithm)
│   │   ├── ECDSA
│   │   └── Ed25519
│   │
│   └── Hybrid Cryptography
│       ├── TLS/SSL (HTTPS)
│       ├── PGP (Pretty Good Privacy, secure email)
│       ├── S/MIME (Secure/Multipurpose Internet Mail Extensions)
│       └── IPSec (network security protocol)
│
└── 3. Related Domains
    ├── Steganography (hiding information in media)
    ├── Cryptanalysis (attacks and cipher-breaking)
    ├── Zero-Knowledge Proofs
    ├── Blockchain & Cryptocurrencies (e.g., Bitcoin → ECDSA, SHA-256)
    └── Homomorphic Encryption (computing on encrypted data)
''''