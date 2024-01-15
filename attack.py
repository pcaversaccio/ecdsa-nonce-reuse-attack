from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigdecode_string
from ecdsa.numbertheory import inverse_mod
import hashlib

# d = The 32-byte private key.
# s = The secp256k1 32-byte signature parameter `s`.
# r = The secp256k1 32-byte signature parameter `r`.
# k = The 32-byte random nonce value. (it's called nonce since it must only be used once!)
# n = integer order of G (part of the public key)
# h = The 32-byte message digest of a message.


def attack(h1, h2, s1, s2, r1, r2, n):
    assert r1 == r2, "No ECDSA nonce reuse detected"
    return ((s2 * h1 - s1 * h2) * inverse_mod(r1 * (s1 - s2), n)) % n


if __name__ == "__main__":
    m1 = b"wagmi1"
    m2 = b"wagmi2"
    k = 1337
    n = SECP256k1.order

    d_A = SigningKey.generate(curve=SECP256k1)
    original_private_key = d_A.privkey.secret_multiplier
    Q_A = d_A.verifying_key

    h1 = hashlib.sha256(m1).hexdigest()
    h2 = hashlib.sha256(m2).hexdigest()

    signature_1 = d_A.sign(m1, hashfunc=hashlib.sha256, k=k)
    signature_2 = d_A.sign(m2, hashfunc=hashlib.sha256, k=k)

    (r1, s1) = sigdecode_string(signature_1, n)
    (r2, s2) = sigdecode_string(signature_2, n)

    recovered_private_key = attack(
        int(h1, base=16), int(h2, base=16), s1, s2, r1, r2, n
    )

    print(f"Original private key: {original_private_key}")
    print(f"Recovered private key: {recovered_private_key}")
    assert (
        original_private_key == recovered_private_key
    ), "Recovered private key not equal to original private key"
