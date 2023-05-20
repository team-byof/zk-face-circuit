# BYOF (Bring Your Own Face) - Halo2 Circuit 🔐🔎🌐
<p align="center">
  <img src="https://th.bing.com/th/id/OIG.9pxIagvlAC.Hn0uHKVhU?pid=ImgGn" width="300px" alt="image"/>
</p>

Welcome to **BYOF**, where you bring your own face to unlock the secure and privacy-conscious world that enhances the user experience in web3 world like in web2 world. Leverage the power of facial recognition and zero-knowledge proofs to ensure ultimate security for your Ethereum wallets. Say goodbye to traditional passwords or keys and let your face be the key!

## About 📖

Inspired by the subtle and intricate patterns of human facial features, BYOF presents a robust Face Wallet Verification system for Ethereum wallets. By transforming biometric data into unique digital representations, our system guarantees that each access is secure, private, and intuitive.

This metaphorical human face you see here illustrates the blend of advanced technology with user convenience – a facial recognition technology that keeps your data safe secure and well-crafted user-experience within the web3 and zero-knowledge proof realm.

## Setup 💻

### Prerequisites

* Python 3.10 (maturin)
* Rustup 1.26.0 (5af9b9484 2023-04-05)
* Visit [Pyo3](https://pyo3.rs/v0.18.3/getting_started) for getting started with Pyo3

### Installation

```bash
# Install the required packages
pip install -r requirements.txt

# Navigate to bridge
cd bridge

# Run maturin
maturin develop
```

### Generate Halo2 Circuit for Ethereum Solidity Verifier

* Export the Halo2 circuit to Solidity Verifier
  * Run the command below from the root directory of this repository.

```bash
# Generate parameters with power of 2
cargo run gen-params --k 20

# Generate keys
cargo run gen-keys

# If you want to download the binaries directly, use the script
./halo2-binary.sh

# Generate EVM verifier
cargo run gen-evm-verifier
```

## Disclaimer
* See the monorepo of halo2-lib [forked repository](https://github.com/sigridjineth/halo2-lib)

## Journey Ahead 🚀
* The on-chain verification is not yet to be implemented since the gas optimization is a hard task above the hackathon.
---
