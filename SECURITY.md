# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly by contacting the maintainer directly.

## Exposed Credentials — Action Required

A Google Gemini API key and a Telegram Bot token were previously exposed in this repository. Both have since been removed from the current codebase, but because they appeared in git history and public discussions, both must be treated as compromised and rotated immediately.

### Affected credentials

| Credential | Exposure location |
|---|---|
| `GOOGLE_API_KEY` | Hardcoded in `services/ai_chat.py` at commit [`7a2623a`](https://github.com/imsamtaha/sam-ai-bot/commit/7a2623a18654a3ec86ce48bc9836d1330b06b782); also visible in [PR #3](https://github.com/imsamtaha/sam-ai-bot/pull/3) comments |
| `TELEGRAM_BOT_TOKEN` | Posted in [PR #3](https://github.com/imsamtaha/sam-ai-bot/pull/3) review discussion and publicly visible in [issue #8](https://github.com/imsamtaha/sam-ai-bot/issues/8) |

### Required actions

1. **Rotate the Google Gemini API key** — generate a new key at [Google AI Studio](https://ai.google.dev/) and revoke the old one.
2. **Rotate the Telegram Bot token** — generate a new token via [@BotFather](https://t.me/botfather) and revoke the old one.
3. **Update your `.env` file** with the new credentials.
4. **Review recent activity/logs** for unauthorized use of exposed credentials.
5. **Close or redact** [issue #8](https://github.com/imsamtaha/sam-ai-bot/issues/8) which still contains the raw Telegram Bot token in its title and body.

> **Important:** Removing a secret from current files is not enough. If a secret was ever committed to git history or posted publicly, it must be rotated immediately — git history is permanent and publicly readable.

## Best Practices

- **Never commit real credentials** to the repository, even temporarily.
- Store all secrets in a `.env` file, which is excluded via `.gitignore`.
- Use the `.env.example` file as a reference — it should contain placeholder values only.
- Enable automated secret scanning in CI (for example, [gitleaks](https://github.com/gitleaks/gitleaks)).
- Restrict API key permissions and set usage quotas/alerts where possible.
- **Close or redact any public issues or comments** that contain raw credentials.