# ecdsa-nonce-reuse-attack
A script to derive the private key if a nonce is ever reused across two different signatures.

$$n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141$$
$$ n = 115792089237316195423570985008687907852837564279074904382605163141518161494337$$

**Public-Private-Key-Relationship**
$$ Q_{A} = d_{A} \cdot G $$


**The secp256k1 32-byte signature parameter `r`**

$$ r = G \cdot k \mod n $$

**The secp256k1 32-byte signature parameter `s`**

$$ s = \frac{h + d_{A} \cdot r}{k} \mod n $$

**Recover Private Key**

Let's assume $d_{A}$ reused the same random value $k$. This implies from the above definition of $r$ that, $r$ is the same for both signatures since $G$ and $n$ are constants.

$$ s_{1} = \frac{h_{1} + d_{A} \cdot r}{k} \mod n $$

$$ s_{2} = \frac{h_{2} + d_{A} \cdot r}{k} \mod n $$

$$ k = \frac{h_{1} + d_{A} \cdot r}{s_{1}} \mod n $$

$$ k = \frac{h_{2} + d_{A} \cdot r}{s_{2}} \mod n $$

Set equal

$$\left(\frac{h_{1} + d_{A} \cdot r}{s_{1}}\right) \mod n = \left(\frac{h_{2} + d_{A} \cdot r}{s_{2}}\right) \mod n$$

Solve for $d_{A}$:

$$\left(\frac{h_{1}}{s_{1}}-\frac{h_{2}}{s_{2}}\right) \mod n = d_{A} \cdot r \cdot \left(\frac{1}{s_{2}} - \frac{1}{s_{1}}\right) \mod n$$

$$ d_{A} \mod n = \frac{(s_{2} \cdot h_{1} - s_{1} \cdot h_{2})}{r \cdot (s_{1} - s_{2})} $$

## References
- https://bertcmiller.com/2021/12/28/glimpse_nonce_reuse.html
- https://datatracker.ietf.org/doc/html/rfc6979
- https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
- https://www.halborn.com/blog/post/how-hackers-can-exploit-weak-ecdsa-signatures
- https://github.com/Marsh61/ECDSA-Nonce-Reuse-Exploit-Example
- https://link.springer.com/content/pdf/10.1007/978-3-030-00470-5_29.pdf
