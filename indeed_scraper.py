from apify_client import ApifyClient
import requests
import json
import time

# Replace with your actual API token
api_token = 'apify_api_o7A5ePAQp9vBQW6cjXmdChXjJrgtTh2VfyTy'

def start_indeed_scraper():
    # The URL for the task trigger (replace with the task you are triggering)
    post_url = 'https://api.apify.com/v2/actor-tasks/raishills~indeed-scraper-task-smm-job/runs'

    # Define the parameters (API token is in the URL query string)
    params = {
        'token': api_token
    }

    # Define the request body (payload)
    body = {
        "followApplyRedirects": False,
        "location": "New York",
        "maxItems": 10,
        "parseCompanyDetails": True,
        "position": "Software Engineer",
        "saveOnlyUniqueItems": True
    }

    # Step 1: Trigger the task via POST request
    response = requests.post(post_url, params=params, json=body)

    # Print the response body
    print("Request body sent:")
    print(json.dumps(body, indent=2))

    # Optionally, print the response to see what Apify returns
    print("\nResponse from API:")
    print(response.json())  # Assuming the response is in JSON format

    # Check if the request was successful
    if response.status_code in [200, 201]:
        print("Task triggered successfully.")
        
        # Extract the task data from the response
        task_data = response.json()
        
        # Get the default KeyValueStoreId from the response
        data_set_id = task_data.get('data', {}).get('defaultDatasetId')

        fetch_indeed_scraper(data_set_id)
    else:
        print(f"Error triggering task: {response.status_code}")
        


def fetch_indeed_scraper(data_set_id):
    if data_set_id:
        print(f"Using Dataset ID: {data_set_id}")
        
        # Step 2: Check the output using GET request and dynamically use Datset ID
        get_url = f'https://api.apify.com/v2/datasets/{data_set_id}/items?token={api_token}'

        def check_output():
            while True:
                # Send the GET request to check the output
                output_response = requests.get(get_url)

                # If the response is successful
                if output_response.status_code == 200:
                # Check if there is data in the response (i.e., the output is ready)
                    output = output_response.json()

                    if output:
                        print("Output received:")
                        print(output)  # Print the output data
                        break  # Exit the loop and end the process
                    else:
                        print("Output not yet available, checking again in 5 seconds...")
                else:
                    print(f"Error checking output: {output_response.status_code}")

                # Wait for 5 seconds before checking again
                time.sleep(5)

        # Start checking for output
        check_output()

    else:
        print("Error: defaultDatasetId not found in the task response.")

start_indeed_scraper()