# Backend (FastAPI) — Airline Reservation System

This folder (`src/`) contains the backend modules (routers/controllers/models) for the Airline Reservation System API. The app entrypoint is `main.py` at the repo root.

## Tech stack

- FastAPI
- SQLAlchemy
- JWT auth (Bearer tokens)
- Settings via `.env` (Pydantic Settings)

## Project layout

- `main.py` (repo root): creates the FastAPI app, registers routers, configures CORS
- `src/utils/settings.py`: loads environment variables from `.env`
- `src/utils/db.py`: SQLAlchemy engine/session + `get_db` dependency
- Feature modules: `src/user`, `src/flights`, `src/booking`, `src/payment`, `src/airline`, `src/airport`, `src/seats`, `src/passenger`

## Requirements

- Python 3.10+ recommended
- A database supported by SQLAlchemy (project is currently configured via `connection_string`)

Install dependencies:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the repo root (same folder as `main.py`) with:

```env
connection_string="postgresql://USER:PASSWORD@HOST:5432/DB_NAME"
EXP_TIME=30
ALGORITHM="HS256"
SECRET_KEY="replace-me"
```

Notes:

- `SECRET_KEY` is sensitive. Don’t commit real secrets.
- `connection_string` must be a valid SQLAlchemy DB URL.

## Run the API (local)

From the repo root:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- API docs (Swagger): `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## CORS / Frontend

`main.py` allows these origins by default:

- `http://localhost:5173`
- `http://localhost:3000`
- `http://localhost:8080`

If your frontend runs on a different port, add it to `allow_origins` in `main.py`.

## Auth overview

Login returns a JWT token. For protected routes, send the token as:

`Authorization: Bearer <token>`

Admin-only routes use `is_admin` (see `src/user/controller.py`).

## API routes (high-level)

User:

- `POST /Users/register`
- `POST /Users/login`
- `GET /Users/is_auth`

Flights:

- `GET /flights/all`
- `GET /flights/id/{id}`
- `POST /flights/create` (admin)
- `PUT /flights/update/{id}` (admin)
- `DELETE /flights/dletete/{id}` (admin)

Bookings (requires auth):

- `POST /bookings/create`
- `GET /bookings/`
- `GET /bookings/{id}`
- `PUT /bookings/{id}`
- `DELETE /bookings/{id}`

Payments (requires auth):

- `POST /payments/`
- `GET /payments/`
- `GET /payments/{payment_id}`
- `PUT /payments/{payment_id}`
- `POST /payments/{payment_id}/process`
- `POST /payments/{payment_id}/cancel`
- `GET /payments/booking/{booking_id}`

Airlines (admin):

- `POST /airline/create`
- `GET /airline/all`
- `GET /airline/{id}`
- `GET /airline/search/{name}`
- `PUT /airline/update/{id}`
- `DELETE /airline/delete/{id}`

Airports (admin):

- `POST /airport/create`
- `GET /airport/all`
- `GET /airport/id/{id}`
- `GET /airport/name/{name}`
- `PUT /airport/update/{id}`
- `DELETE /airport/delete/{id}`

Seats:

- `POST /seats/create`
- `GET /seats/`
- `GET /seats/{id}`
- `PUT /seats/{id}`
- `DELETE /seats/{id}`

