# Field mapping

Make module: **Facebook Conversions API → Send Event(s)**. Module `1` is the GHL custom webhook.

## Event fields

| Meta field | Make value | Why |
|---|---|---|
| Pixel ID | your dataset ID | Makes the target dataset explicit |
| Event Name | `Lead` | Standard event for form leads |
| Event Time | `{{formatDate(now; X)}}` | Submission time as a Unix timestamp in seconds |
| Action Source | `website` | The GHL form is a web form |
| Event Source URL | the GHL form link | Required when the action source is website |
| Event ID | `{{1.contact_id}}-{{formatDate(now; X)}}` | Unique for every submission |

## User data

| Meta field | Make value |
|---|---|
| Email | `{{1.email}}` |
| Phone | `{{replace(1.phone; +; )}}` |
| First name | `{{1.first_name}}` |
| Last name | `{{1.last_name}}` |
| External ID | `{{1.contact_id}}` (optional, helps matching) |

Make hashes user data with SHA-256 itself. The module says so in a reminder above the User Data fields. Don't wrap the values in `sha256()`, or they get hashed twice and stop matching.

## Things that went wrong during the build

**Quotes inside Make functions.** Make sends text inside a function literally, so `replace(1.phone; "+"; "")` looks for a quote mark followed by a plus. Write `replace(1.phone; +; )` with no quotes.

**Typing a formula as plain text.** `replace( + phone + ; ...)` typed into the field is sent as text. Paste the whole `{{...}}` expression, or insert the function from the mapping panel, so it turns into a function pill.

**Using contact fields for event ID and time.** The first version used `contact_id` as the event ID and `date_created` as the event time. When the same email submitted the form again, GHL reused the existing contact, so Meta got the same event ID and the original sign-up time:

- Meta dedupes events with the same event ID, so the second lead could be dropped.
- Meta rejects events older than 7 days, so a returning contact's lead could fail.

The fix takes both values from the submission: `formatDate(now; X)` for the time, and the contact ID plus that timestamp for the event ID.

**Country.** GHL filled `country` from the sub-account address, not from the lead. It's left unmapped so Meta doesn't get wrong data.
