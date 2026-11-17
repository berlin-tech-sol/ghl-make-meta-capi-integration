# Troubleshooting: OAuth 401 / error 190

## Start here: which module fails?

Open the failed run in Make's execution history.

- **Webhook module fails, or never receives data:** the problem is on the GoHighLevel side. Check that the workflow is published, the trigger filter names the right form, and Make is listening (Run once) or the scenario is active.
- **Webhook succeeds, Facebook module fails:** the problem is the Meta connection or the event data. Continue below.

## Error 190, OAuthException (often shown as 401)

Example from the reproduced failure:

```
Error validating access token: Sessions for the user are not allowed because
the user is not a confirmed user. (190, OAuthException)
```

Meta code 190 means the access token Make holds is invalid, expired or revoked. The wording varies, but the cause is one of these:

| Cause | How it happens |
|---|---|
| Make's access was removed | Someone removed Make under Business Settings → Integrations → Connected apps |
| Password change | The person who authorized the connection changed their Facebook password |
| Lost admin rights | That person was removed from the business portfolio or lost access to the dataset |
| Meta security update | Meta changed its requirements for the Facebook Conversions API app, and Make asked users to reauthorize existing connections before May 9, 2026. Connections that weren't reauthorized can fail after that date |

**Fix:** Make → **Credentials** → the Facebook Conversions API connection → **Reauthorize**. Sign in, then select the business portfolio and the dataset in the pop-up. Don't create a second connection with **Add**, because the External Business ID must be unique.

If reauthorizing works but the error comes back, check that the person authorizing has full control of the dataset in Business Settings.

## Other errors

| Symptom | Cause | Fix |
|---|---|---|
| "test_event_code does not match an active Test Events session" | Events Manager's Test Events page wasn't live when the event arrived | Reload Test Events, confirm the code, keep the page open while you run |
| "Admin permissions needed" when creating a dataset | Partial access to the business portfolio | Ask an admin for full control, or use a portfolio where you're admin |
| Event in Make but nothing in Meta | Missing test code, or event time in milliseconds | Add the code; use `formatDate(now; X)` for seconds |
| Second lead from same person not showing | Repeated event ID | Use the contact ID plus a timestamp as the event ID |
| Poor match quality | Phone with spaces or missing country code, or values hashed twice | Digits with country code only; let Make do the hashing |
| Facebook pop-up doesn't open | Browser blocked the pop-up | Allow pop-ups for make.com and try again |

## Checking Meta without Make

[`scripts/send_test_event.py`](../scripts/send_test_event.py) sends one test Lead straight to the Conversions API with an access token generated in Events Manager. If the script works but Make fails, the problem is in Make's connection. If both fail, the problem is in the dataset or the token permissions.
