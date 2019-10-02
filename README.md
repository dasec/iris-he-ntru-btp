# NTRU Homomorphic Encryption for Iris-code Template Protection

The repository provides a reference implementation for Biometric Template Protection based on NTRU Homomorphic Encryption and Iris-codes. Biometric templates are stored and compared in the encrypted domain. To solve the problem of the computational overload linked to the encryption scheme, an early decision making strategy is implemented. However, in order to improve the recognition accuracy, the most consistent bits of the iris-code are moved to the beginning of the template. This allows an accurate block-wise comparison, thereby reducing the execution time. Hence, the resulting system grants template protection in a computationally efficient way.


## Warranty

This software is provided "as is", without warranty of any kind. Especially the cryptographic functions are not secured against side-channel attacks etc. The whole program serves as a reference implementation on how to apply homomorphic encryption for iris-biometric template protection but qualifies not for being a secure solution.


## Attribution

Any publications using the code must cite and reference the conference paper [1].


## References

* [1] Jascha Kolberg, Pia Bauspieß, Marta Gomez-Barrero, Christian Rathgeb, Markus Dürmuth and Christoph Busch. "Template Protection based on Homomorphic Encryption: Computationally Efficient Application to Iris-Biometric Verification and Identification", in IEEE Workshop on Information Forensics and Security, Delft ,Netherlands, December 2019.