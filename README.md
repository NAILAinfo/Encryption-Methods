## Cryptography Tree

```bash
Cryptography methods
Cryptography
│
├── 1. Classical Cryptography
│   │
│   ├── Substitution Ciphers
│   │   ├── Monoalphabetic
│   │   │   ├── Caesar Cipher
│   │   │   ├── Atbash Cipher
│   │   │   ├── ROT13
│   │   │   ├── Affine Cipher
│   │   │   ├── Random Substitution
│   │   │   └── Polybius Square
│   │   │
│   │   └── Polyalphabetic
│   │       ├── Vigenère Cipher
│   │       ├── Beaufort Cipher
│   │       ├── Autokey Cipher
│   │       └── One-Time Pad (OTP)
│   │
│   ├── Polygraphic / Block Substitution
│   │   ├── Playfair Cipher (digraphs)
│   │   └── Hill Cipher (matrix/block-based)
│   │
│   └── Transposition Ciphers
│       ├── Scytale
│       ├── Columnar Transposition
│       └── Rail Fence
│
├── 2. Modern Cryptography
│   │
│   ├── Symmetric Cryptography
│   │   ├── Block Ciphers
│   │   │   ├── DES (deprecated)
│   │   │   ├── 3DES (legacy)
│   │   │   ├── AES (128/192/256)
│   │   │   ├── Blowfish
│   │   │   └── Twofish
│   │   │
│   │   └── Stream Ciphers
│   │       ├── RC4 (obsolete)
│   │       ├── Salsa20
│   │       └── ChaCha20
│   │
│   ├── Asymmetric Cryptography (Public-Key)
│   │   ├── RSA
│   │   ├── Diffie–Hellman (key exchange protocol)
│   │   ├── ElGamal
│   │   └── ECC (Elliptic Curve Cryptography)
│   │       ├── ECDSA (signatures)
│   │       └── Ed25519 / Curve25519 (modern signatures)
│   │
│   ├── Digital Signatures
│   │   ├── RSA Signature
│   │   ├── DSA
│   │   └── ECDSA / Ed25519
│   │
│   ├── Hash Functions & Key Derivation
│   │   ├── MD5 (insecure)
│   │   ├── SHA-1 (deprecated)
│   │   ├── SHA-2 (SHA-256, SHA-512, …)
│   │   ├── SHA-3 (Keccak)
│   │   ├── Bcrypt
│   │   ├── Scrypt
│   │   └── Argon2 / PBKDF2
│   │
│   └── Hybrid Cryptography & Protocols
│       ├── TLS / SSL
│       ├── PGP / OpenPGP
│       ├── S/MIME
│       └── IPSec
│
├── 3. Cryptanalysis Techniques
│   │
│   ├── Classical / Statistical Attacks
│   │   ├── Frequency Analysis
│   │   ├── Kasiski Examination (for Vigenère)
│   │   ├── Probable-word / Crib-dragging
│   │   └── Index of Coincidence (Friedman Test)
│   │
│   ├── Modern Cryptanalysis
│   │   ├── Brute-force / Exhaustive search
│   │   ├── Meet-in-the-middle attack (2DES)
│   │   ├── Differential cryptanalysis (block ciphers)
│   │   ├── Linear cryptanalysis (block ciphers)
│   │   ├── Birthday attack (hash collisions)
│   │   └── Padding oracle attacks (CBC flaws)
│   │
│   └── Side-Channel & Implementation Attacks
│       ├── Timing attacks
│       ├── Power analysis (SPA/DPA)
│       ├── Fault injection
│       └── Replay attacks
│
└── 4. Related / Advanced Topics
    ├── Steganography
    ├── Blockchain & Cryptocurrencies
    ├── Zero-Knowledge Proofs (ZKP)
    └── Homomorphic Encryption
''''