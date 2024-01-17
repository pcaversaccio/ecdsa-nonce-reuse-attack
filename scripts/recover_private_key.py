from hashlib import sha256
from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigdecode_string
from ecdsa.numbertheory import inverse_mod


def recover_private_key(h1, h2, s1, s2, r1, r2, n):
    """Recover the private key via nonce reuse.

    Recover the private key from two different signatures
    that use the same random nonce `k` during signature
    generation. Note that if the same `k` is used in two
    signatures, this implies that the secp256k1 32-byte
    signature parameter `r` is identical. This property is
    asserted in this function.

    Parameters
    ----------
        h1: int
            The 32-byte message digest of the message `m1`.
        h2: int
            The 32-byte message digest of the message `m2`.
        s1: int
            The secp256k1 32-byte signature parameter `s1`.
        s2: int
            The secp256k1 32-byte signature parameter `s2`.
        r1: int
            The secp256k1 32-byte signature parameter `r1`.
        r2: int
            The secp256k1 32-byte signature parameter `r2`.
        n:  int
            The 32-byte integer order of G (part of the public key).

    Returns
    -------
        pk: int
            The recovered 32-byte private key.

    Raises
    ------
        AssertionError
            No ECDSA nonce reuse detected.
    """
    assert r1 == r2, "No ECDSA nonce reuse detected."
    return ((s2 * h1 - s1 * h2) * inverse_mod(r1 * (s1 - s2), n)) % n


if __name__ == "__main__":
    """An illustrative recovery of the private key."""
    m1 = b"wagmi1"
    m2 = b"wagmi2"
    k = 1337
    n = SECP256k1.order

    # Generate the signing key object.
    d_A = SigningKey.generate(curve=SECP256k1)
    # Retrieve the private key.
    original_private_key = d_A.privkey.secret_multiplier
    # Retrieve the public key.
    Q_A = d_A.verifying_key

    # Generate the message digests.
    h1 = sha256(m1).hexdigest()
    h2 = sha256(m2).hexdigest()

    # Generate the signatures using the same `k` value.
    signature_1 = d_A.sign(m1, hashfunc=sha256, k=k)
    signature_2 = d_A.sign(m2, hashfunc=sha256, k=k)

    # Retrieve the secp256k1 32-byte signature parameters `r` and `s`.
    (r1, s1) = sigdecode_string(signature_1, n)
    (r2, s2) = sigdecode_string(signature_2, n)

    # Recover the private key.
    recovered_private_key = recover_private_key(
        int(h1, base=16), int(h2, base=16), s1, s2, r1, r2, n
    )

    print(f"Original private key: {original_private_key}")
    print(f"Recovered private key: {recovered_private_key}")
    assert (
        original_private_key == recovered_private_key
    ), "Recovered private key does not equal the original private key."
