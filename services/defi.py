import logging
from typing import Optional

from services.blockchain import (
    POLYGON_TOKENS,
    get_network_info,
    get_wallet_portfolio,
    is_valid_address,
)
from services.ai_chat import chat_with_gemini

logger = logging.getLogger(__name__)

# QuickSwap (Uniswap-v2 fork) router on Polygon – read-only reference
QUICKSWAP_ROUTER = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'

# Well-known Polygon DeFi protocols
DEFI_PROTOCOLS = {
    'QuickSwap': {
        'type': 'DEX',
        'url': 'https://quickswap.exchange',
        'description': 'Leading DEX on Polygon with fast, low-cost swaps',
    },
    'Aave': {
        'type': 'Lending',
        'url': 'https://app.aave.com',
        'description': 'Decentralised liquidity protocol for lending and borrowing',
    },
    'Uniswap v3': {
        'type': 'DEX',
        'url': 'https://app.uniswap.org',
        'description': 'Concentrated-liquidity DEX deployed on Polygon',
    },
    'Curve': {
        'type': 'Stablecoin DEX',
        'url': 'https://polygon.curve.fi',
        'description': 'Efficient stablecoin and pegged-asset swaps',
    },
    'Balancer': {
        'type': 'AMM',
        'url': 'https://app.balancer.fi',
        'description': 'Programmable liquidity with weighted pools',
    },
}


def get_supported_tokens() -> list[str]:
    """Return the list of supported token symbols."""
    return list(POLYGON_TOKENS.keys())


def get_protocol_info(protocol_name: str) -> Optional[dict]:
    """Return information about a named DeFi protocol."""
    return DEFI_PROTOCOLS.get(protocol_name)


def list_protocols() -> dict:
    """Return all known DeFi protocols."""
    return DEFI_PROTOCOLS


async def get_swap_info(from_token: str, to_token: str, amount: float) -> str:
    """
    Use AI to explain a proposed token swap on Polygon.

    This is an informational assistant — it does *not* execute transactions.
    """
    if amount <= 0:
        return "❌ Swap amount must be greater than zero."

    supported = get_supported_tokens()
    from_upper = from_token.upper()
    to_upper = to_token.upper()

    if from_upper not in supported:
        return (
            f"❌ Token '{from_token}' is not in the supported list.\n"
            f"Supported tokens: {', '.join(supported)}"
        )
    if to_upper not in supported:
        return (
            f"❌ Token '{to_token}' is not in the supported list.\n"
            f"Supported tokens: {', '.join(supported)}"
        )

    prompt = (
        f"A user wants to swap {amount} {from_upper} for {to_upper} on the Polygon blockchain. "
        f"Explain in a concise, friendly way: "
        f"1) What this swap does, "
        f"2) Which Polygon DEX protocols they could use (e.g. QuickSwap, Uniswap v3), "
        f"3) Key considerations such as slippage, gas fees, and price impact, "
        f"4) Any risks to be aware of. "
        f"Keep the response under 250 words and do not provide financial advice."
    )
    return await chat_with_gemini(prompt)


async def analyze_portfolio_with_ai(address: str) -> str:
    """
    Fetch the on-chain portfolio for *address* and ask Gemini for an AI analysis.
    """
    if not is_valid_address(address):
        return f"❌ Invalid wallet address: {address}"

    portfolio = get_wallet_portfolio(address)
    if 'error' in portfolio:
        return f"❌ Could not fetch portfolio: {portfolio['error']}"

    token_lines = '\n'.join(
        f"  - {sym}: {bal}" for sym, bal in portfolio.get('tokens', {}).items()
    ) or '  (no ERC-20 balances found)'

    portfolio_text = (
        f"Wallet: {portfolio['address']}\n"
        f"Network: {portfolio['network']}\n"
        f"MATIC balance: {portfolio['matic']}\n"
        f"ERC-20 tokens:\n{token_lines}"
    )

    prompt = (
        f"Here is a snapshot of a Polygon wallet portfolio:\n\n"
        f"{portfolio_text}\n\n"
        f"Provide a brief, educational analysis covering: "
        f"1) Portfolio diversification, "
        f"2) Notable holdings or risks, "
        f"3) General DeFi strategy suggestions that could apply to this kind of portfolio. "
        f"Keep under 300 words. Do not provide specific financial advice."
    )
    return await chat_with_gemini(prompt)


async def get_defi_strategy(risk_profile: str = "moderate") -> str:
    """
    Use AI to suggest a general DeFi strategy on Polygon for a given risk profile.
    """
    valid_profiles = {"conservative", "moderate", "aggressive"}
    profile = risk_profile.lower().strip()
    if profile not in valid_profiles:
        profile = "moderate"

    prompt = (
        f"Suggest a general educational DeFi strategy on Polygon for a user with a "
        f"'{profile}' risk profile. "
        f"Include: available yield opportunities (lending, LP, staking), "
        f"relevant protocols (Aave, QuickSwap, Curve, Balancer), "
        f"and typical risks. "
        f"Keep under 350 words. This is for educational purposes only."
    )
    return await chat_with_gemini(prompt)


async def automate_blockchain_task(user_intent: str) -> str:
    """
    Use AI to interpret a natural-language blockchain intent and explain
    the steps needed to accomplish it on Polygon.

    This function does *not* execute any transactions; it generates an
    action plan that the user can follow manually.
    """
    prompt = (
        f"A user wants to automate the following blockchain task on Polygon: "
        f'"{user_intent}"\n\n'
        f"Respond with: "
        f"1) Whether this is feasible on Polygon, "
        f"2) A clear step-by-step action plan using available tools/protocols, "
        f"3) Any smart-contract interactions required, "
        f"4) Estimated gas costs and risks. "
        f"Keep the response practical and under 400 words. "
        f"Do not execute any transactions; provide guidance only."
    )
    return await chat_with_gemini(prompt)


def format_portfolio_message(portfolio: dict) -> str:
    """Format a portfolio dict into a user-friendly Telegram message."""
    if 'error' in portfolio:
        return f"❌ {portfolio['error']}"

    lines = [
        f"💼 *Wallet Portfolio*",
        f"📍 Address: `{portfolio['address']}`",
        f"🌐 Network: {portfolio['network']}",
        f"",
        f"💎 *Balances:*",
        f"  • MATIC: {portfolio['matic']}",
    ]

    tokens = portfolio.get('tokens', {})
    if tokens:
        for symbol, balance in tokens.items():
            lines.append(f"  • {symbol}: {balance}")
    else:
        lines.append("  • No ERC-20 token balances found")

    return '\n'.join(lines)


def format_network_info(info: dict) -> str:
    """Format network info dict into a user-friendly Telegram message."""
    if 'error' in info:
        return f"❌ Network error: {info['error']}"

    return (
        f"🌐 *Polygon Network Status*\n"
        f"  • Chain ID: {info.get('chain_id')}\n"
        f"  • Latest block: {info.get('latest_block')}\n"
        f"  • Gas price: {info.get('gas_price_gwei')} Gwei\n"
        f"  • Status: {'✅ Connected' if info.get('connected') else '❌ Disconnected'}"
    )
