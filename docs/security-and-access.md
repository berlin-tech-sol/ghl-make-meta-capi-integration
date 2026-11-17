# Security and access

How this integration is set up on a client's accounts without taking over them.

## Rules

1. **No passwords or login codes.** The client signs in to Meta, GoHighLevel and Make themselves. Work happens on a screen share, with the client clicking.
2. **Explain before approving.** Every permission screen is read out and explained before the client clicks Continue.
3. **Inactive until reviewed.** The scenario stays switched off. Tests use "Run once" and a Meta test event code, and the client sees exactly which fields are sent before anything goes live.
4. **Least access.** If access is ever needed, it's a limited role the client can remove afterwards, never their own login.

## What the Make connection gets in Meta

From Business Settings → Integrations → Connected apps → Make, after authorizing:

| Item | Needed for this integration? |
|---|---|
| The dataset (pixel) | Yes: this is where events are sent |
| An ad account | No: can be removed with the trash icon in Connected apps |
| "Manage business extension" | Yes: Make connects through the Facebook Business Extension |
| "Manage ads", "Access ads and stats", "Manage your business" | Requested by the extension. Removing the ad account limits what these apply to |

## Limited access options, if hands-on help is needed

| Platform | Limited option | Removed by |
|---|---|---|
| Meta | Add the freelancer to the business portfolio with access to the dataset only, not the ad account or billing | Business Settings → Users → People |
| GoHighLevel | A sub-account user with permissions limited to Automation and Sites | Settings → My Staff |
| Make | Invite the freelancer to the organization or team with a limited role | Organization → Team |

## Data sent to Meta

Only the fields in [field-mapping.md](field-mapping.md): email, phone, first and last name (hashed by Make with SHA-256), plus the contact ID, event time and form URL. Nothing else from the GHL contact is sent.

## Things to keep private

- The Make webhook URL. Anyone with it can post data into the scenario.
- Conversions API access tokens. Never commit them; use a `.env` file (see `.env.example`).
- Real lead data in screenshots. Use test contacts.
