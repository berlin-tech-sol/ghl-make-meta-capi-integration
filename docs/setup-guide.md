# Setup guide

The full build, in the order it was done. Time needed: about 2 to 3 hours, most of it account setup.

## What you need

- A Meta business portfolio where you have admin rights. Creating a dataset needs admin, and partial access fails with "Admin permissions needed".
- A GoHighLevel account. A sub-account inside an agency account is enough. For testing, HighLevel's Marketplace developer sandbox gives a free test agency.
- A Make account. The free plan works.

## Phase 1: Meta dataset

1. Events Manager → **Connect data** → **Web** → **Connect**.
2. Name the dataset and click **Create**. Untick "Connect all new and existing datasets... to the Conversions API with Meta". That option changes a portfolio-wide setting and isn't needed when Make sends the events.
3. Close the "Connect your web data" and "Set up Conversions API" wizards. The dataset already exists at this point.
4. Datasets → open the dataset → copy the **Dataset ID**.
5. **Test events** tab → set the channel dropdown to **Website** → copy the test event code from the "server's events" box. The code is tied to an active Test Events session, so check it again right before testing.

## Phase 2: GoHighLevel form

1. In the sub-account: **Sites → Forms → Builder → Add Form** → blank.
2. Fields: First Name, Last Name, Phone (required), Email (required).
3. Remove the default SMS consent checkboxes, or fill in their placeholders.
4. Save, then **Integrate** → copy the form link.

## Phase 3: Make webhook

1. **Create a new scenario** → **Webhooks → Custom webhook** → **Create a webhook** → Save.
2. Copy the webhook URL. Keep it private: anyone with it can post data into the scenario.
3. Click **Run once** so Make waits for the first payload.

## Phase 4: GoHighLevel workflow

1. **Automation → Workflows → Create Workflow → Start from scratch**.
2. Trigger: **Form Submitted**, filtered to your form.
3. Action: **Webhook**, method POST, URL = the Make webhook. No custom data needed, because GHL sends the full contact.
4. Publish and save.
5. Submit the form once. Make shows the contact fields: `contact_id`, `first_name`, `last_name`, `email`, `phone`, `date_created` and more.

## Phase 5: Facebook Conversions API module

1. Add **Facebook Conversions API → Send Event(s)** after the webhook.
2. Create the connection. Make uses Meta's Facebook Business Extension, so it asks for a business name, currency, timezone and an **External Business ID**. The ID can be any text, but it must be unique per connection, for example `client-name-01`.
3. In the Facebook pop-up, select the business portfolio and the dataset.
4. Fill in the fields as listed in [field-mapping.md](field-mapping.md).
5. Turn on **Show advanced settings** and paste the test event code.

## Phase 6: Test with the scenario inactive

1. Keep the Events Manager **Test events** tab open.
2. In Make: **Run once**, then submit the form.
3. Make output should show `Events Received: 1` and a Facebook trace ID.
4. Meta shows a **Lead** row: Processed, received from Server.

If Make returns a message that the test code "does not match an active Test Events session", the event was received but the Test Events page wasn't live. Reload that page, confirm the code and run again.

## Phase 7: Reproduce the OAuth error and fix it

1. Meta Business Settings → **Integrations → Connected apps** → Make → **Remove**.
2. Run once and submit the form. The Facebook module fails with `190, OAuthException`. The webhook module still succeeds, which shows the GHL side is fine.
3. Make → **Credentials** → the Facebook connection → **Reauthorize**, and select the business and dataset again.
4. Run once and submit. The run succeeds again.

## Phase 8: Before going live

- Clear the **Test Event Code** field. Test codes are for testing only.
- Have the client review a sample of what will be sent, then switch the scenario to active.
- Export the scenario blueprint (scenario menu → **Export Blueprint**) and keep it in [`make/`](../make/).
