import os

from web3 import Web3
from web3.middleware import geth_poa_middleware

ALLTHATNODE_URL = 'https://polygon-testnet-rpc.allthatnode.com:8545'  # polygon mumbai
PRIVATE_KEY = os.environ['PRIVATE_KEY']
CONTRACT_ABI = 'YOUR_CONTRACT_ABI'
CONTRACT_ADDRESS = 'YOUR_CONTRACT_ADDRESS'


def _connect_to_node(node_provider_url):
    w3 = Web3(Web3.HTTPProvider(node_provider_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


class AccountAbstractionContract:
    def __init__(self, node_provider_url, private_key, contract_abi, contract_address):
        self.w3 = _connect_to_node(node_provider_url)
        self.account = self._load_account(private_key)
        self.contract = self._initialize_contract(contract_abi, contract_address)

    def _load_account(self, private_key):
        return self.w3.eth.account.privateKeyToAccount(private_key)

    def _initialize_contract(self, contract_abi, contract_address):
        return self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=contract_abi
        )

    def call_function(self, function_name, *args):
        function = getattr(self.contract.functions, function_name)
        return function(*args).call()

    def send_transaction(self, function_name, gas_limit, *args):
        function = getattr(self.contract.functions, function_name)
        transaction = function(*args).buildTransaction({
            'from': self.account.address,
            'gas': gas_limit,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })

        signed_txn = self.w3.eth.account.signTransaction(transaction, self.account.privateKey)
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        return txn_receipt


def main():
    eth_contract = AccountAbstractionContract(ALLTHATNODE_URL, PRIVATE_KEY, CONTRACT_ABI, CONTRACT_ADDRESS)
    print("Contract address: ", eth_contract.contract.address)

    # # Example of calling a view function (read-only)
    # result = eth_contract.call_function('YOUR_FUNCTION_NAME', ARGS)
    # print(result)
    #
    # # Example of sending a transaction to a contract function (write operation)
    # txn_receipt = eth_contract.send_transaction('YOUR_FUNCTION_NAME', GAS_LIMIT, ARGS)
    # print(txn_receipt)


if __name__ == '__main__':
    main()
