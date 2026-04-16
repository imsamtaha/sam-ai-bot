# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly by opening a private issue or contacting the maintainer directly.

## Exposed Credentials — Action Required

A Google Gemini API key was previously hardcoded in `services/ai_chat.py` (commit `7a2623a`) and has since been removed. However, the key remains in the Git history and was also disclosed in pull-request comments.

### Affected credentials

| Credential | Location |
|---|---|
| `GOOGLE_API_KEY` | Git history (`services/ai_chat.py`) and PR #3 comments |
| `TELEGRAM_BOT_TOKEN` | PR #3 comments |

### Required actions

1. **Rotate the Google Gemini API key** — generate a new key at [Google AI Studio](https://ai.google.dev/) and revoke the old one.
2. **Rotate the Telegram Bot token** — generate a new token via [@BotFather](https://t.me/botfather) and revoke the old one.
3. **Update your `.env` file** with the new credentials.

> **Note:** Removing a secret from the latest code is not enough — anyone with access to the repository history can still retrieve it. Always rotate credentials that have been committed to version control.

## Best Practices

- **Never commit real credentials** to the repository, even temporarily.
- Store all secrets in a `.env` file, which is excluded via `.gitignore`.
- Use the `.env.example` file as a reference — it contains only placeholder values.
- Consider using a secret-scanning tool such as [gitleaks](https://github.com/gitleaks/gitleaks) in your CI pipeline to catch accidental leaks.
