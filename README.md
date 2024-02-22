# 🛡️ ECDSA Nonce Reuse Attack

[![👮‍♂️ Sanity checks](https://github.com/pcaversaccio/ecdsa-nonce-reuse-attack/actions/workflows/checks.yml/badge.svg)](https://github.com/pcaversaccio/ecdsa-nonce-reuse-attack/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)

This repository implements a Python function [`recover_private_key`](https://github.com/pcaversaccio/ecdsa-nonce-reuse-attack/blob/main/scripts/recover_private_key.py) that recovers the private key from two different signatures that use the same random nonce $k$ during signature generation. Note that if the same $k$ is used in two signatures, this implies that the secp256k1 32-byte signature parameter $r$ is identical. This property is asserted in this function.

## 🧠 Mathematical Derivation

First, note that the integer order $n$ of $G$ (a base point of prime order on the curve) for the [secp256k1 elliptic curve](https://en.bitcoin.it/wiki/Secp256k1) is:

```console
# Represented as hex value.
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036414
# Represented as integer value.
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
```

#### 1. Public-Private-Key-Relationship

<!-- prettier-ignore-start -->
$$ Q_{A} = d_{A} \cdot G $$
<!-- prettier-ignore-end -->

$Q_{A}$ is the public key, $d_{A}$ is the private key, and $G$ is the elliptic curve base point.

#### 2. The secp256k1 32-Byte Signature Parameter $r$

<!-- prettier-ignore-start -->
$$ r = G \cdot k \quad \left(\textnormal{mod} \enspace n\right) $$
<!-- prettier-ignore-end -->

$r$ is the first secp256k1 32-byte signature parameter, $n$ is the integer order of $G$, and $k$ is the random nonce value.

#### 3. The secp256k1 32-Byte Signature Parameter $s$

<!-- prettier-ignore-start -->
$$ s = \frac{h + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right) $$
<!-- prettier-ignore-end -->

$s$ is the second secp256k1 32-byte signature parameter and $h$ is the 32-byte message digest of a message.

#### 4. Recover the Private Key

Let's assume that $d_{A}$ has used the same random value $k$ for two different signatures. This implies from the above definition of $r$ that $r$ is the same for both signatures, since $G$ and $n$ are constants. Thus, we have:

<!-- prettier-ignore-start -->
$$ s_{1} = \frac{h_{1} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right) $$
<!-- prettier-ignore-end -->

and

<!-- prettier-ignore-start -->
$$ s_{2} = \frac{h_{2} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right). $$
<!-- prettier-ignore-end -->

We can solve for $k$ with the above system of equations:

<!-- prettier-ignore-start -->
$$ s_{1} - s_{2} =  \frac{h_{1} + d_{A} \cdot r}{k} - \frac{h_{2} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right), $$

$$ s_{1} - s_{2} =  \frac{h_{1} + d_{A} \cdot r - h_{2} - d_{A} \cdot r}{k}\quad \left(\textnormal{mod} \enspace n\right), $$

$$ s_{1} - s_{2} =  \frac{h_{1} - h_{2}}{k}\quad \left(\textnormal{mod} \enspace n\right), $$

$$ k =  \frac{h_{1} - h_{2}}{s_{1} - s_{2}}\quad \left(\textnormal{mod} \enspace n\right). $$
<!-- prettier-ignore-end -->

Eventually, we can now plug $k$ into the equation $s_{1}$ and recover the private key $d_{A}$:

<!-- prettier-ignore-start -->
$$ s_{1} = \frac{h_{1} + d_{A} \cdot r}{\frac{h_{1} - h_{2}}{s_{1} - s_{2}}} \quad \left(\textnormal{mod} \enspace n\right), $$

$$ s_{1} = \frac{\left(s_{1} - s_{2}\right)\cdot\left(h_{1} + d_{A} \cdot r\right)}{h_{1} - h_{2}} \quad \left(\textnormal{mod} \enspace n\right), $$

$$ d_{A} = \frac{(s_{2} \cdot h_{1} - s_{1} \cdot h_{2})}{r \cdot (s_{1} - s_{2})} \quad \left(\textnormal{mod} \enspace n\right). $$
<!-- prettier-ignore-end -->

> The function [`recover_private_key`](./scripts/recover_private_key.py) uses the last equation in conjunction with modular arithmetic properties to recover the private key.

## 📚 Further References

- [Elliptic Curve Digital Signature Algorithm](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [RFC 6979](https://datatracker.ietf.org/doc/html/rfc6979)
- [A Glimpse of the Deep: Finding a Creature in Ethereum's Dark Forest](https://bertcmiller.com/2021/12/28/glimpse_nonce_reuse.html)
- [How Hackers Can Exploit Weak ECDSA Signatures](https://www.halborn.com/blog/post/how-hackers-can-exploit-weak-ecdsa-signatures)
- [ECDSA Nonce Reuse Exploit Example](https://github.com/Marsh61/ECDSA-Nonce-Reuse-Exploit-Example)
- [Identifying Key Leakage of Bitcoin Users](https://link.springer.com/content/pdf/10.1007/978-3-030-00470-5_29.pdf)
- [How Do You Derive the Private Key From Two Signatures That Share the Same `k` Value?](https://bitcoin.stackexchange.com/a/73624)
