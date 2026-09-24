# StyleZone API — Reference (DRAFT — may be out of date)

> ⚠️ This draft has not been reviewed against the current API. Correct it against the
> running service (`mock_server.py`), which is the source of truth.

## Base URL

```
http://localhost:8080
```

## Authentication

The API is open for read and write operations — no authentication header is required.

## Conventions

- IDs are 24-character hex strings.
- Requests and responses are JSON.
- Errors return `{ "error": "message" }`.

---

## Endpoints

### Styles

**`GET /styles/`** — Create a new style.
Body: `{ "name": "<optional>", "group_id": "<optional>" }`.
Returns the created style.

**`GET /styles/{style_id}/`** — Retrieve a style's details.

### Garments

**`GET /garments/{garment_id}/resources/`** — List a garment's resources.

**`POST /garments/{garment_id}/resources/`** — Upload a resource.
Body: `{ "type": "image|file|turntable|3d|bw|pdf", "filename": "<name>", "url": "<source-url>" }`.
Returns the created resource.

**`GET /garments/{garment_id}/outlines/{outline_id}/af_download`** — Download an
artwork file. Returns `200` with the file contents in the response body.

**`DELETE /garments/{garment_id}/`** — Delete a garment.
Returns `204` on success.

### Users

**`GET /users/email/{email}/`** — Look up a user by their email address.

---

*If anything here doesn't match the running API, the running API wins.*
