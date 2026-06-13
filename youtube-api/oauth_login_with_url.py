from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import os
import webbrowser

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
BASE = Path(__file__).resolve().parent
TOKEN_FILE = BASE / "token.json"
CLIENT_SECRET = BASE / "client_secret.json"
AUTH_URL_FILE = BASE / "oauth-auth-url.txt"
RESULT_FILE = BASE / "oauth-result.json"

PORT = int(os.environ.get("YOUTUBE_OAUTH_PORT", "8093"))
REDIRECT_URI = f"http://localhost:{PORT}/"

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
flow.redirect_uri = REDIRECT_URI

auth_url, _ = flow.authorization_url(
    access_type="offline",
    include_granted_scopes="true",
    prompt="select_account consent",
)
AUTH_URL_FILE.write_text(auth_url, encoding="utf-8")
webbrowser.open(auth_url)


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if "code=" not in parsed.query:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing OAuth code.")
            return

        authorization_response = REDIRECT_URI.rstrip("/") + self.path
        flow.fetch_token(authorization_response=authorization_response)
        creds = flow.credentials
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

        youtube = build("youtube", "v3", credentials=creds)
        channel = youtube.channels().list(part="snippet", mine=True).execute()["items"][0]
        result = {
            "channelId": channel["id"],
            "title": channel["snippet"]["title"],
            "customUrl": channel["snippet"].get("customUrl"),
        }
        RESULT_FILE.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube OAuth complete. You can close this tab.")

    def log_message(self, format, *args):
        return


server = HTTPServer(("localhost", PORT), OAuthCallbackHandler)
server.handle_request()
