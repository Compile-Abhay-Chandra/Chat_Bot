# import requests

# url = "https://lecture-rebecca-multiple-bobby.trycloudflare.com  "  # exact URL, no spaces
# prompt = "capital of india."

# try:
#     response = requests.post(url, json={"prompt": prompt})
#     # print("Status code:", response.status_code)
#     # print("Response text:", response.text)

#     if response.status_code == 200:
#         data = response.json()
#         print("Model response:", data["response"])
#     else:
#         print("Server returned an error")
# except requests.exceptions.RequestException as e:
#     print("Request failed:", e)


import requests
import json

# ================================
# 1. Configuration
# ================================
# ⚠️ IMPORTANT: Replace this with the live URL from your Colab output
# Add /query to the end of the URL
api_url = "https://mating-mc-associate-these.trycloudflare.com/query"

# Your question for the model
prompt = "What are the three most famous landmarks in Agra?"

# ================================
# 2. API Request Logic
# ================================
def query_model(text_prompt ,url = "https://dated-selections-counters-tyler.trycloudflare.com/query"):
    """Sends a prompt to the Flask API and returns the model's response."""

    print(f"▶️  Sending prompt: '{text_prompt}'")

    # The data payload to be sent as JSON
    payload = {"prompt": text_prompt + " keep the answer short and precise"}
    
    # Set headers to indicate we are sending JSON data
    headers = {"Content-Type": "application/json"}

    try:
        # Send the POST request with a 30-second timeout
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response from the server
        data = response.json()
        
        # Extract and print the model's response
        print("✅ Model Response:")
        print(data.get("response", "No 'response' key found in the JSON data."))
        return data.get("response", "No 'response' key found in the JSON data.")

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError:
        # Handle cases where the response is not valid JSON
        print(f"❌ Failed to decode JSON. Server response:\n{response.text}")

# ================================
# 3. Run the script
# ================================
if __name__ == "__main__":
    # Check if the URL is still a placeholder
    if "your-unique-url" in api_url:
        print("❗️ Please update the 'api_url' variable with your actual Cloudflare URL.")
    else:
        query_model( prompt,api_url)
