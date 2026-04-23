# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly by contacting the maintainer directly.

## Exposed Credentials — Action Required

A Google Gemini API key was previously committed to this repository and has since been removed from the latest code. However, because the key existed in repository history, it must be treated as compromised.

### Affected credentials

| Credential | Exposure location |
|---|---|
| `GOOGLE_API_KEY` | Repository history |
| `TELEGRAM_BOT_TOKEN` | Public discussion/comments |

### Required actions

1. **Rotate the Google Gemini API key** — generate a new key at [Google AI Studio](https://ai.google.dev/) and revoke the old one.
2. **Rotate the Telegram Bot token** — generate a new token via [@BotFather](https://t.me/botfather) and revoke the old one.
3. **Update your `.env` file** with the new credentials.
4. **Review recent activity/logs** for unauthorized use of exposed credentials.

> **Important:** Removing a secret from current files is not enough. If a secret was ever committed or posted publicly, rotate it immediately.

## Best Practices

- **Never commit real credentials** to the repository, even temporarily.
- Store all secrets in a `.env` file, which is excluded via `.gitignore`.
- Use the `.env.example` file as a reference — it should contain placeholder values only.
- Enable automated secret scanning in CI (for example, [gitleaks](https://github.com/gitleaks/gitleaks)).
- Restrict API key permissions and set usage quotas/alerts where possible.