import pandas as pd
import os
import asyncio
from datetime import timedelta
from apify_client import ApifyClientAsync
from dotenv import load_dotenv
load_dotenv()

# You can find your API token at https://console.apify.com/settings/integrations.
TOKEN = os.environ.get("APIFY_API_KEY")
CSV_PATH = "../dataset/data.csv"
RESULTS_PER_CALL = 100

async def main() -> None:
    # Client initialization with the API token
    apify_client = ApifyClientAsync(token=TOKEN)

    # Get the Actor client
    actor_client = apify_client.actor('infoweaver/my-actor')

    input_data = [
        {
            "deliveryLocation": "IIIT Lucknow",
            "maxResults": RESULTS_PER_CALL,
            "search": "Veg foods"
        },
        {
            "deliveryLocation": "IIIT Lucknow",
            "maxResults": RESULTS_PER_CALL,
            "search": "Non Veg"
        },
        {
            "deliveryLocation": "IIIT Lucknow",
            "maxResults": RESULTS_PER_CALL,
            "search": "Cafes"
        }
    ]

    # Run the Actor and wait for it to finish up to 60 seconds.
    # Input is not persisted for next runs.
    total_items = []
    
    for inputs in input_data:
        run_result = await actor_client.call(
            run_input=inputs, timeout_secs=300
        )
        dataset_id = run_result.get("defaultDatasetId")

        if dataset_id:
            dataset_client = apify_client.dataset(dataset_id)
            list_items = await dataset_client.list_items()
            items = list_items.items

            if items:
                total_items.extend(items)
                print(f"got around, {len(items)} results")
    
    run_result = pd.DataFrame(total_items)
    run_result = run_result.drop_duplicates(subset=['restaurantUrl'])
    run_result.to_csv(CSV_PATH)
    print("Successfully scraped data and created dataset/data.csv")


if __name__ == '__main__':
    asyncio.run(main())
