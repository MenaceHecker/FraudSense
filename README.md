# FraudSense

FraudSense is a small fraud detection system built as a set of microservices. A transaction comes in, a rules engine scores how risky it looks, and if the score is high enough an alert gets raised for an analyst to look at. A single GraphQL gateway sits in front of everything so clients only ever talk to one endpoint.

It is meant as a realistic but approachable example of how you might wire up a few Python services behind a Node gateway, so nothing here is trying to be clever for the sake of it.

## How it fits together

There are three backend services and one gateway, all talking to the same Postgres database.

```
                        ┌─────────────────┐
      client  ────────▶ │  GraphQL Gateway │  (Node + Apollo, port 4000)
                        └────────┬─────────┘
                                 │
             ┌───────────────────┼────────────────────┐
             ▼                   ▼                     ▼
   ┌──────────────────┐ ┌─────────────────┐  ┌──────────────────┐
   │ transaction-svc  │ │   risk-service  │  │   alert-service  │
   │   (FastAPI 8001) │ │  (FastAPI 8002) │  │  (FastAPI 8003)  │
   └────────┬─────────┘ └────────┬────────┘  └────────┬─────────┘
            │                    │                     │
            └────────────────────┴─────────────────────┘
                                 ▼
                          ┌─────────────┐
                          │  Postgres   │
                          └─────────────┘
```

- **transaction-service** stores transactions and hands them back out. It seeds a couple of example rows on startup so you are not staring at an empty database.
- **risk-service** takes a transaction id, pulls the transaction from the transaction-service, runs it through a rules engine, and saves a risk assessment. It reuses a single HTTP client so it is not opening a fresh connection on every call.
- **alert-service** stores alerts and answers dashboard queries. It only ever knows about flagged transactions, so it does not try to guess the total transaction count.
- **gateway** is the only thing clients touch. It exposes a GraphQL schema, fans requests out to the services, and orchestrates the "analyze a transaction and open an alert if needed" flow.

## Running it

The quickest way to get everything up is Docker Compose. It builds all four services and starts Postgres for you.

```bash
cp .env.example .env   # optional, only if you want to change ports
docker compose up --build
```

Once it is running:

- GraphQL playground: http://localhost:4000/
- Gateway health check: http://localhost:4000/health

The ports are configurable through the `.env` file. The defaults are 4000 for the gateway and 8001 to 8003 for the services.

## Running a service on its own

If you just want to work on one Python service, each one is a normal FastAPI app. They target Python 3.13.

```bash
cd services/risk-service
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

The gateway is a TypeScript app:

```bash
cd gateway
npm install
npm run dev
```

Every service exposes a `/health` endpoint that returns its name and an `ok` status, which is handy for checking things are actually up.

## The GraphQL API

Everything goes through the gateway. Here are the main things you can do.

Queries:

- `transactions(flaggedOnly: Boolean)` and `transaction(id)` for reading transactions
- `transactionsByUser(userId)` for one user's history
- `riskAssessment(transactionId)` for a saved risk score
- `alerts(status, severity)` and `alert(id)` for reading alerts
- `dashboardStats` for the summary numbers behind an analyst dashboard

Mutations:

- `ingestTransaction(input)` to record a new transaction
- `analyzeTransaction(transactionId)` to score a transaction and open an alert if it looks risky
- `createAlert(input)` and `updateAlertStatus(input)` to manage alerts by hand

A typical flow looks like this: ingest a transaction, call `analyzeTransaction` with the id it gives you back, and then check `alerts` to see if anything was raised.

## How the scoring works

The risk logic lives in the risk-service and is deliberately a simple rules engine rather than a model, so you can read it top to bottom and understand every decision.

Each transaction starts with a small base score and picks up points for things that tend to look suspicious:

- large amounts (a bigger jump once it crosses a high threshold)
- risky categories like crypto, gift cards, and wire transfers
- rapid repeat activity
- transactions at odd hours

The points are capped at 100, and the total decides the outcome:

- **75 and up** is high severity, marked suspicious, recommended action is block
- **45 to 74** is medium severity, still suspicious, recommended action is review
- **below 45** is low severity and allowed

Only medium and high assessments turn into alerts. The thresholds and point values are all defined in one config object, so tuning the model is a matter of editing that rather than hunting through the code.

## Project layout

```
gateway/                 GraphQL gateway (TypeScript, Apollo Server)
services/
  transaction-service/   stores and serves transactions
  risk-service/          scores transactions with a rules engine
  alert-service/         stores alerts and dashboard stats
infra/postgres/          database init script
docker-compose.yml       brings the whole thing up
```

Each service follows the same shape: an `api` layer for routes, a `services` layer for the actual work, `models` for the database tables, `schemas` for request and response validation, and a thin `db` layer for the session and connection.
