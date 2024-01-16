# ECDSA Nonce Reuse Attack

This repository implements a [function](./recover_private_key.py) that recovers the private key from two different signatures that use the same random nonce `k` during signature generation. Note that if `k` is reused in two signatures, this implies that the secp256k1 32-byte signature parameter `r` is be identical. This property is asserted in this function.

## Mathematical Derivation

First, note that the integer order $n$ of $G$ (a base point of prime order on the curve) for the [secp256k1 elliptic curve](https://en.bitcoin.it/wiki/Secp256k1) is:

```console
# as hex value
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036414
# as integer value
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
```

**Public-Private-Key-Relationship**
$$ Q_{A} = d_{A} \cdot G $$

$Q_{A}$ is the public key, $d_{A}$ is the private key, and $G$ is the elliptic curve base point.

**The secp256k1 32-byte signature parameter `r`**
$$ r = G \cdot k \quad \left(\textnormal{mod} \enspace n\right) $$

$r$ is the first secp256k1 32-byte signature parameter, $n$ is the integer order of $G$, and $k$ is the random nonce value.

**The secp256k1 32-byte signature parameter `s`**
$$ s = \frac{h + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right) $$

$s$ is the second secp256k1 32-byte signature parameter, $h$ is the 32-byte message digest of a message.

**Recover the Private Key**

Let's assume that $d_{A}$ has used the same random value $k$ for two different signatures. This implies from the above definition of $r$ that $r$ is the same for both signatures, since $G$ and $n$ are constants. Thus, we have:

$$ s_{1} = \frac{h_{1} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right) $$

and

$$ s_{2} = \frac{h_{2} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right). $$

Given the above system of equations we can solve for $k$:

$$ s_{1} - s_{2} =  \frac{h_{1} + d_{A} \cdot r}{k} - \frac{h_{2} + d_{A} \cdot r}{k} \quad \left(\textnormal{mod} \enspace n\right),$$

$$ s_{1} - s_{2} =  \frac{h_{1} + d_{A} \cdot r - h_{2} - d_{A} \cdot r}{k}\quad \left(\textnormal{mod} \enspace n\right),$$

$$ s_{1} - s_{2} =  \frac{h_{1} - h_{2}}{k}\quad \left(\textnormal{mod} \enspace n\right),$$

$$ k =  \frac{h_{1} - h_{2}}{s_{1} - s_{2}}\quad \left(\textnormal{mod} \enspace n\right).$$

Eventually, we can now plugin $k$ into the $s_{1}$ equation and solve for the privat key $d_{A}$:

$$ s_{1} = \frac{h_{1} + d_{A} \cdot r}{\frac{h_{1} - h_{2}}{s_{1} - s_{2}}} \quad \left(\textnormal{mod} \enspace n\right),$$

$$ s_{1} = \frac{\left(s_{1} - s_{2}\right)\cdot\left(h_{1} + d_{A} \cdot r\right)}{h_{1} - h_{2}} \quad \left(\textnormal{mod} \enspace n\right),$$

$$ d_{A} = \frac{(s_{2} \cdot h_{1} - s_{1} \cdot h_{2})}{r \cdot (s_{1} - s_{2})} \quad \left(\textnormal{mod} \enspace n\right).$$

## Further References

- https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
- https://datatracker.ietf.org/doc/html/rfc6979
- https://bertcmiller.com/2021/12/28/glimpse_nonce_reuse.html
- https://www.halborn.com/blog/post/how-hackers-can-exploit-weak-ecdsa-signatures
- https://github.com/Marsh61/ECDSA-Nonce-Reuse-Exploit-Example
- https://link.springer.com/content/pdf/10.1007/978-3-030-00470-5_29.pdf
- https://bitcoin.stackexchange.com/a/73624
