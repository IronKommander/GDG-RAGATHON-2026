import pandas as pd
import os
import asyncio
from datetime import timedelta
from apify_client import ApifyClientAsync
from dotenv import load_dotenv
load_dotenv()

# You can find your API token at https://console.apify.com/settings/integrations.
TOKEN = os.environ.get("PINECONE_API_KEY")

async def main() -> None:
    apify_client = ApifyClientAsync(TOKEN)

    # Start an Actor and wait for it to finish.
    actor_client = apify_client.actor('infoweaver/my-actor')
    call_result = await actor_client.call()

    if call_result is None:
        print('Actor run failed.')
        return

    # Fetch results from the Actor run's default dataset.
    dataset_client = apify_client.dataset(call_result.default_dataset_id)
    list_items_result = await dataset_client.list_items()
    print(f'Dataset: {list_items_result}')
