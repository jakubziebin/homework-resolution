# StyleZone API Reference

The mock service is the source of truth for this reference.

## Base URL

```text
http://localhost:8080
```

## Authentication

Every request requires this header:

```http
Authorization: Bearer sz-demo-token-abc123
```

Requests without the header receive `401 Unauthorized`:

```json
{
  "error": "Unauthorized"
}
```

## Conventions

- Request and response bodies use JSON unless stated otherwise.
- IDs in path parameters are 24-character lowercase hexadecimal strings.
- Errors use `{ "error": "message" }`. Some errors also include a `data` object.
- The examples below use the known IDs printed by `mock_server.py`.

## Endpoints

### Create a style

**`POST /styles/`**

Creates a style. The `name` field is required; `group_id` is optional.

Request body:

```json
{
  "name": "Demo jacket",
  "group_id": "aa11bb22cc33dd44ee55ff66"
}
```

Example:

```bash
curl -i -X POST \
  -H 'Authorization: Bearer your-token' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Demo jacket","group_id":"aa11bb22cc33dd44ee55ff66"}' \
  http://localhost:8080/styles/
```

Returns `201 Created`.

Response model:

```json
{
  "id": "some-id",
  "name": "some jacket",
  "status": "draft",
  "group_id": "some-group-id"
}
```

### Get a style

**`GET /styles/{style_id}/`**

Returns a style by ID. The known style ID is
`5f8d0a1b2c3d4e5f60718293`.

Example:

```bash
curl -i \
  -H 'Authorization: Bearer your-token' \
  http://localhost:8080/styles/5f8d0a1b2c3d4e5f60718293/
```

Returns `200 OK`.

Response model:

```json
{
  "id": "some-id",
  "name": "some name",
  "status": "some-status",
  "liked": false,
  "group_id": "some-group-id"
}
```

### List garment resources

**`GET /garments/{garment_id}/resources/`**

Returns the resources belonging to a garment. The known garment ID is
`60718293a4b5c6d7e8f90a1b`.

Example:

```bash
curl -i \
  -H 'Authorization: your-token' \
  http://localhost:8080/garments/60718293a4b5c6d7e8f90a1b/resources/
```

Returns `200 OK`.

Response model:

```json
[
  {
    "outline_id": "some-outline-id",
    "type": "some-type",
    "filename": "some-filename.bw"
  }
]
```

The response is an array; the example shows one item from the response model.

### Upload a garment resource

**`POST /garments/{garment_id}/resources/`**

Creates a resource in processing state. Supported `type` values are `image`,
`file`, `turntable`, `3d`, and `bw`.

Request body:

```json
{
  "type": "image",
  "filename": "front.png",
  "url": "https://example.com/front.png"
}
```

Example:

```bash
curl -i -X POST \
  -H 'Authorization: Bearer your-tone' \
  -H 'Content-Type: application/json' \
  -d '{"type":"image","filename":"front.png","url":"https://example.com/front.png"}' \
  http://localhost:8080/garments/60718293a4b5c6d7e8f90a1b/resources/
```

Returns `200 OK`.

Response model:

```json
{
  "outline_id": "some-outline-id",
  "type": "some-type",
  "filename": "some-filename.png",
  "status": "status"
}
```

### Download an artwork file

**`GET /garments/{garment_id}/outlines/{outline_id}/af_download`**

Returns `302 Found`, not the file contents. The response contains a time-limited
signed URL in the `Location` header. 

Example:

```bash
curl -i \
  -H 'Authorization: Bearer your-token' \
  http://localhost:8080/garments/60718293a4b5c6d7e8f90a1b/outlines/0a1b2c3d4e5f60718293a4b5/af_download
```

Response headers include:

```http
HTTP/1.0 302 Found
Location: https://cdn.mock.stylezone.example/af/0a1b2c3d4e5f60718293a4b5?sig=demo&expires=900
```

Response model: empty body; use the `Location` header as the download URL.

### Find a user by email

**`GET /users/email/{email}/`**

Returns a user by email address.

Example:

```bash
curl -i \
  -H 'Authorization: Bearer your-token' \
  http://localhost:8080/users/email/designer@lumen-studio.example/
```

Returns `200 OK`.

Response model:

```json
{
  "id": "some-id",
  "email": "some@lemail.example",
  "name": "Great",
  "role": "examplee"
}
```

### Create tag relations in bulk

**`POST /style/tags_relations/bulk/`**

Creates a relation for every combination of `tag_ids` and `object_ids`. Both
arrays are required and must be non-empty.

Request body:

```json
{
  "tag_ids": ["tag-1", "tag-2"],
  "object_ids": ["obj-1", "obj-2", "obj-3"]
}
```

Example:

```bash
curl -i -X POST \
  -H 'Authorization: Bearer your-token' \
  -H 'Content-Type: application/json' \
  -d '{"tag_ids":["tag-1","tag-2"],"object_ids":["obj-1","obj-2","obj-3"]}' \
  http://localhost:8080/style/tags_relations/bulk/
```

Returns `200 OK`.

Response model:

```json
{
  "created": 1,
  "tags": 2,
  "objects": 3
}
```

### Global search

**`POST /global_search/`**

Searches styles, garments, boards, and groups. The query is optional and
defaults to an empty string.

Request body:

```json
{
  "query": "some-query"
}
```

Example:

```bash
curl -i -X POST \
  -H 'Authorization: Bearer your-token' \
  -H 'Content-Type: application/json' \
  -d '{"query":"dress"}' \
  http://localhost:8080/global_search/
```

Returns `200 OK`.

Response model:

```json
{
  "query": "dress",
  "results": {
    "styles": [{"id": "some-id", "name": "some-name"}],
    "garments": [{"id": "some-id", "name": "some-name"}],
    "boards": [],
    "groups": []
  }
}
```

## Error examples

Unknown paths return `404 Not Found`:

```json
{
  "error": "Unknown endpoint",
  "data": {
    "hint": "Check the API reference, this path may not exist."
  }
}
```

A missing style or user returns `404 Not Found` with a resource-specific error.
Malformed JSON returns `400 Bad Request`. Invalid resource types return `400 Bad
Request` and include the allowed types in `data.allowed`.

## Unsupported operation

There is no garment deletion endpoint. `DELETE /garments/{garment_id}/` returns
`404 Not Found`.
