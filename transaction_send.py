from algosdk import transaction, account, util, mnemonic
from algosdk.v2client import algod
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mnemonic_phrase = os.getenv("MNEMONIC_PHRASE")

# Derive private key from mnemonic
private_key = mnemonic.to_private_key(mnemonic_phrase)
print("Private Key Derived from Mnemonic:", private_key)

# Get private key 
# private_key = os.getenv("PRIVATE_KEY")

# get address from environment variables
address = account.address_from_private_key(private_key)
print("Address:", address)

# Get Algorand client parameters from environment variables
algod_token = os.getenv("TESTNET_ALGOD_TOKEN")
algod_url = os.getenv("TESTNET_ALGOD_URL")
algod_port = os.getenv("TESTNET_ALGOD_PORT")

# Initialize Algorand client
algod_client = algod.AlgodClient(algod_token, algod_url)

# Get suggested transaction parameters
suggested_params = algod_client.suggested_params()

# Create a payment transaction
payment_txn = transaction.PaymentTxn(
    sender=address,
    sp=suggested_params,
    amt=util.algos_to_microalgos(1),
    receiver="2JAZQO6Z5BCXFMPVW2CACK2733VGKWLZKS6DGG565J7H5NH77JNHLIIXLY",
    note=b"bbd7d61f5d00e17bd4c78ae8124ff1fd2837ddf8596a3254e26e3bedcb446d00" # add your encrypted text you got from CTF3 solution
)


# Sign the transaction
signed_txn = payment_txn.sign(private_key)

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print(f"Txn sent: https://testnet.explorer.perawallet.app/tx/{txid}")

# Wait for transaction confirmation
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Txn Confirmed in round {result['confirmed-round']}")