# API Documentation Findings

The running `mock_server.py` was treated as the source of truth. I verified the
requests below against `http://localhost:8080` using the required bearer token.

## 1. Token authentication recognized

First thing that i recognized that the api-reference said that no authentication header was required, but the server actually requires a bearer token for every request. 
I noticed it as first beacause at the top of the mock_server.py there is a TOKEN final variable :)

## 2. Completed endpoint list

I asked Github Copilot for creating complete endpoint application endpoints. 
Then, I verified each route with `curl` and recorded the results in the table below. 
I also went through the mock_server.py to take a look in the code of endpoints.

| `POST` | `/styles/` | `201 Created`, creates a style |
| `GET` | `/styles/{style_id}/` | `200 OK`, returns a style |
| `GET` | `/garments/{garment_id}/resources/` | `200 OK`, returns a resource array |
| `POST` | `/garments/{garment_id}/resources/` | `200 OK`, creates a processing resource |
| `GET` | `/garments/{garment_id}/outlines/{outline_id}/af_download` | `302 Found`, redirects to a signed URL |
| `GET` | `/users/email/{email}/` | `200 OK`, returns a user |
| `POST` | `/style/tags_relations/bulk/` | `200 OK`, creates bulk tag relations |
| `POST` | `/global_search/` | `200 OK`, returns grouped search results |

## 3. Application versus draft documentation

* Documentation said that no authentication header was required, but the server requires a bearer token for every request.

* Wrong method and path for creating a style. The draft said `GET /styles/` with a body, but the application actually does `POST /styles/` with a required `name` field.

* Corrected allowed resource upload types. The draft said `image|file|turntable|3d|bw|pdf`, but the application actually does not allow `pdf`.

* af_download endpoint returns `302` with a time-limited signed url in `Location`

* Delete garment does not exist

* tags_relations, global_search endpoints was not documented

* error can also include `data.hint` 

## 4. Proposed plan to prevent documentation drift

1. Generate the reference from an API schema maintained with the server, such as
   OpenAPI, including request and response schemas.
2. Add contract tests that start the mock or test server, call every documented
   route, and assert the method, status code, headers, and response shape. Run
   them in CI whenever the server or documentation changes.
3. Run the contract tests and OpenAPI validation automatically in CI for every
   pull request. If an endpoint, request field, response model, or status code
   changes without a matching documentation update, the CI check should fail.
4. In prod application I would consider using FastAPI framework which generates docs from code.
