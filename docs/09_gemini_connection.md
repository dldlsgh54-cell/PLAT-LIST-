# Gemini Connection

Creator OS always displays the Gemini API connection status.

## Status Values

- `Connected`
- `Rate Limited`
- `Disconnected`
- `Offline`

## Startup Connection Test

When the program starts, Creator OS runs a Gemini API health check.

### Test Prompt

```text
Reply only: OK
```

### Expected Response

```text
OK
```

## Display Fields

- Model
- API Status
- Response Time
- Requests Today
- Last Error

## Usage Notes

- The Gemini connection state should be visible from the main application shell or Dashboard.
- Failed health checks should not crash the application.
- `Rate Limited` should be treated differently from `Disconnected`.
- `Offline` can be used when the local network is unavailable or the user has disabled online AI features.
- Last error details should be concise and useful for troubleshooting.

