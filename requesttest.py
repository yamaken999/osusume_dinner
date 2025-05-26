import requests

tenant_id = "0d82d6f2-dc03-4866-856e-35c29bd311d0"
client_id = "f0efd1b2-b5b9-47c4-9e25-3f1af1824666"
client_secret = "Hfz8Q~XfouQkWA8JB-3HmGc92amakPcFH8BEwc-."
scope = "https://graph.microsoft.com/.default"

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

data = {
    "client_id": client_id,
    "scope": scope,
    "client_secret": client_secret,
    "grant_type": "client_credentials",
}

r = requests.post(token_url, data=data)
print("Status:", r.status_code)
print("Response:", r.text)  # または print(r.json())

