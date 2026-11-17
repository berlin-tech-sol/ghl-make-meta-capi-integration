# Make blueprint

Put the exported scenario here as `ghl-lead-to-meta-capi.blueprint.json`.

Export it from the scenario: **⋮** menu → **Export Blueprint**.

Before committing, open the file and check that it doesn't contain your webhook URL or any access token. Connections are not included in blueprints, so whoever imports it creates their own Facebook connection.

To import: Make → **Create a new scenario** → **⋮** → **Import Blueprint**, then create a new webhook and a new Facebook Conversions API connection.
