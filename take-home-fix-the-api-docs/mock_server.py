#!/usr/bin/env python3
"""
StyleZone API — mock server for the take-home assignment.

Dependency-free (Python 3 standard library only). Run it, then point your code at
http://localhost:8080 with the bearer token from the README.

    python3 mock_server.py

This is a throwaway toy that serves canned responses for a handful of real
StyleZone endpoints. It holds no real data and is not connected to anything.
"""
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = "sz-demo-token-abc123"
PORT = 8080

# A couple of known ids so calls can succeed against real-looking data.
KNOWN_STYLE = "5f8d0a1b2c3d4e5f60718293"
KNOWN_GARMENT = "60718293a4b5c6d7e8f90a1b"
KNOWN_OUTLINE = "0a1b2c3d4e5f60718293a4b5"
KNOWN_EMAIL = "designer@lumen-studio.example"

ALLOWED_RESOURCE_TYPES = {"image", "file", "turntable", "3d", "bw"}


class Handler(BaseHTTPRequestHandler):
    # ---- helpers -------------------------------------------------------
    def _send(self, code, payload=None, headers=None):
        body = b"" if payload is None else json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _error(self, code, message, data=None):
        payload = {"error": message}
        if data is not None:
            payload["data"] = data
        self._send(code, payload)

    def _authed(self):
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self._error(401, "Unauthorized")
            return False
        return True

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return None

    def log_message(self, fmt, *args):  # quieter console
        print(f"  {self.command} {self.path} -> {args[1] if len(args) > 1 else ''}")

    # ---- routing -------------------------------------------------------
    def do_GET(self):
        if not self._authed():
            return
        path = self.path.split("?")[0]

        m = re.fullmatch(r"/styles/([0-9a-f]{24})/", path)
        if m:
            if m.group(1) == KNOWN_STYLE:
                return self._send(200, {
                    "id": KNOWN_STYLE, "name": "Sheath Dress", "status": "in_review",
                    "liked": False, "group_id": "aa11bb22cc33dd44ee55ff66",
                })
            return self._error(404, "Style not found")

        m = re.fullmatch(r"/garments/([0-9a-f]{24})/resources/", path)
        if m:
            return self._send(200, [
                {"outline_id": KNOWN_OUTLINE, "type": "bw", "filename": "sheath_dress.bw"},
                {"outline_id": "1111222233334444aaaabbbb", "type": "image", "filename": "front.png"},
                {"outline_id": "5555666677778888ccccdddd", "type": "turntable", "filename": "spin.mp4"},
            ])

        m = re.fullmatch(r"/garments/([0-9a-f]{24})/outlines/([0-9a-f]{24})/af_download", path)
        if m:
            # Real behaviour: 302 redirect to a time-limited signed URL.
            signed = f"https://cdn.mock.stylezone.example/af/{m.group(2)}?sig=demo&expires=900"
            return self._send(302, None, headers={"Location": signed})

        m = re.fullmatch(r"/users/email/(.+)/", path)
        if m:
            if m.group(1) == KNOWN_EMAIL:
                return self._send(200, {
                    "id": "9988776655443322110aabbc", "email": KNOWN_EMAIL,
                    "name": "Dana Lumen", "role": "editor",
                })
            return self._error(404, "User not found")

        return self._error(404, "Unknown endpoint", {"hint": "Check the API reference — this path may not exist."})

    def do_POST(self):
        if not self._authed():
            return
        path = self.path.split("?")[0]
        body = self._read_json()
        if body is None:
            return self._error(400, "Malformed JSON body")

        if path == "/styles/":
            if not body.get("name"):
                return self._error(400, "Field 'name' is required")
            return self._send(201, {"id": "abcabcabcabcabcabcabcabc", "name": body["name"],
                                     "status": "draft", "group_id": body.get("group_id")})

        m = re.fullmatch(r"/garments/([0-9a-f]{24})/resources/", path)
        if m:
            rtype = body.get("type")
            if rtype not in ALLOWED_RESOURCE_TYPES:
                return self._error(400, "Unsupported resource type",
                                   {"allowed": sorted(ALLOWED_RESOURCE_TYPES)})
            return self._send(200, {"outline_id": "dddd0000eeee1111ffff2222",
                                    "type": rtype, "filename": body.get("filename"),
                                    "status": "processing"})

        if path == "/style/tags_relations/bulk/":
            tag_ids = body.get("tag_ids") or []
            object_ids = body.get("object_ids") or []
            if not tag_ids or not object_ids:
                return self._error(400, "Both 'tag_ids' and 'object_ids' are required")
            return self._send(200, {"created": len(tag_ids) * len(object_ids),
                                    "tags": len(tag_ids), "objects": len(object_ids)})

        if path == "/global_search/":
            q = body.get("query", "")
            return self._send(200, {"query": q, "results": {
                "styles": [{"id": KNOWN_STYLE, "name": "Sheath Dress"}],
                "garments": [{"id": KNOWN_GARMENT, "name": "Sheath Dress / base"}],
                "boards": [], "groups": [],
            }})

        return self._error(404, "Unknown endpoint", {"hint": "Check the API reference — this path may not exist."})

    def do_DELETE(self):
        if not self._authed():
            return
        # Note: no garment-deletion endpoint is documented. This is intentional.
        return self._error(404, "Unknown endpoint",
                           {"hint": "Check the API reference — this path may not exist."})


if __name__ == "__main__":
    print(f"StyleZone mock API on http://localhost:{PORT}")
    print(f"  Authorization: Bearer {TOKEN}")
    print(f"  Known style id:   {KNOWN_STYLE}")
    print(f"  Known garment id: {KNOWN_GARMENT}  (outline {KNOWN_OUTLINE})")
    print(f"  Known user email: {KNOWN_EMAIL}")
    print("  Ctrl+C to stop.\n")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
