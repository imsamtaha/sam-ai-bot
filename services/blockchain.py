import os
import logging
from typing import Optional
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError

load_dotenv()

logger = logging.getLogger(__name__)

# Polygon network configuration
POLYGON_RPC_URL = os.getenv('POLYGON_RPC_URL', 'https://polygon-rpc.com')
POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY', '')

# Common token addresses on Polygon.
# MATIC is listed here for completeness (used as a display label and in swap guidance),
# but its balance is fetched via get_matic_balance() rather than the ERC-20 ABI, because
# 0x1010 is the native-token precompile — not a standard ERC-20 contract.
POLYGON_TOKENS = {
    'MATIC': '0x0000000000000000000000000000000000001010',
    'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
    'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
    'WETH': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
    'WBTC': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
    'DAI':  '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063',
    'LINK': '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39',
    'AAVE': '0xD6DF932A45C0f255f85145f286eA0b292B21C90B',
}

# Minimal ERC-20 ABI for balance and token info
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
]


def get_web3() -> Optional[Web3]:
    """Return a connected Web3 instance or None on failure."""
    try:
        w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
        if w3.is_connected():
            return w3
        logger.warning("Web3 provider is not connected.")
        return None
    except Exception as e:
        logger.error(f"Failed to initialise Web3: {e}")
        return None


def is_valid_address(address: str) -> bool:
    """Return True if *address* is a valid Ethereum/Polygon address."""
    return Web3.is_address(address)


def get_matic_balance(address: str) -> Optional[float]:
    """Return the native MATIC balance (in MATIC) for *address*."""
    w3 = get_web3()
    if not w3:
        return None
    try:
        checksum = Web3.to_checksum_address(address)
        balance_wei = w3.eth.get_balance(checksum)
        return float(Web3.from_wei(balance_wei, 'ether'))
    except Exception as e:
        logger.error(f"Error fetching MATIC balance for {address}: {e}")
        return None


def get_token_balance(address: str, token_symbol: str) -> Optional[float]:
    """Return the ERC-20 token balance for a known *token_symbol*."""
    token_address = POLYGON_TOKENS.get(token_symbol.upper())
    if not token_address:
        logger.warning(f"Unknown token symbol: {token_symbol}")
        return None

    w3 = get_web3()
    if not w3:
        return None

    try:
        checksum_wallet = Web3.to_checksum_address(address)
        checksum_token = Web3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=checksum_token, abi=ERC20_ABI)
        raw_balance = contract.functions.balanceOf(checksum_wallet).call()
        decimals = contract.functions.decimals().call()
        return raw_balance / (10 ** decimals)
    except (ContractLogicError, Exception) as e:
        logger.error(f"Error fetching {token_symbol} balance for {address}: {e}")
        return None


def get_wallet_portfolio(address: str) -> dict:
    """
    Return a summary of token balances for a wallet address.

    Returns a dict with:
      - address: the checksummed address
      - matic: native MATIC balance
      - tokens: {symbol: balance} for every known ERC-20
      - network: always 'Polygon'
    """
    if not is_valid_address(address):
        return {'error': f'Invalid address: {address}'}

    matic = get_matic_balance(address)
    tokens: dict[str, float] = {}
    for symbol in POLYGON_TOKENS:
        if symbol == 'MATIC':
            continue
        balance = get_token_balance(address, symbol)
        if balance is not None and balance > 0:
            tokens[symbol] = round(balance, 6)

    return {
        'address': Web3.to_checksum_address(address),
        'network': 'Polygon',
        'matic': round(matic, 6) if matic is not None else 'unavailable',
        'tokens': tokens,
    }


def get_transaction_count(address: str) -> Optional[int]:
    """Return the total number of transactions (nonce) for *address*."""
    w3 = get_web3()
    if not w3:
        return None
    try:
        checksum = Web3.to_checksum_address(address)
        return w3.eth.get_transaction_count(checksum)
    except Exception as e:
        logger.error(f"Error fetching transaction count for {address}: {e}")
        return None


def get_network_info() -> dict:
    """Return basic Polygon network information."""
    w3 = get_web3()
    if not w3:
        return {'error': 'Unable to connect to Polygon network', 'connected': False}
    try:
        block = w3.eth.block_number
        gas_price_gwei = round(float(Web3.from_wei(w3.eth.gas_price, 'gwei')), 2)
        return {
            'network': 'Polygon',
            'chain_id': w3.eth.chain_id,
            'latest_block': block,
            'gas_price_gwei': gas_price_gwei,
            'connected': True,
        }
    except Exception as e:
        logger.error(f"Error fetching network info: {e}")
        return {'error': 'Failed to retrieve network info', 'connected': False}
