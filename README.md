# BYOF Halo2 Circuit (ง'̀-'́)ง
## We're freakin' kicking off our first rendezvous on Halo2 together 🏃🏻🏃🏼🏃🏽🏃🏾🏃

### Environment
* Python 3.10 (maturin) & rustup 1.26.0 (5af9b9484 2023-04-05)
* https://pyo3.rs/v0.18.3/getting_started
```shell
pip install -r requirements.txt
cd voice_recovery_python
maturin develop
```
* Export the Halo2 circuit to Solidity Verifier
  * You need to run the command below from the root directory of this repository.
  * Please make sure that you have
```
cargo run gen-params --k 20
cargo run gen-keys
cargo run gen-evm-verifier
```