# Movie Ticket Service

A backend service and supporting components for browsing movies, creating showtimes, selecting seats, and purchasing tickets. This repository implements the core APIs and business logic for a Movie Ticket Service used by web and mobile clients.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Install & Run Locally](#install--run-locally)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Movies](#movies)
  - [Theaters & Auditoriums](#theaters--auditoriums)
  - [Showtimes](#showtimes)
  - [Seats & Availability](#seats--availability)
  - [Bookings & Payments](#bookings--payments)
- [Database & Migrations](#database--migrations)
- [Running Tests](#running-tests)
- [Docker](#docker)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License & Contact](#license--contact)

## Project Overview
Movie Ticket Service is a backend system that supports:
- Browsing movies and showtimes
- Managing theaters and auditoriums
- Seat availability and selection
- Creating and managing bookings
- Integrating with payment gateways

It is intended to be used by a frontend (web or mobile) and can be extended to support features like promotional codes, dynamic pricing, and user loyalty.

## Features
- RESTful API for all core operations
- JWT-based authentication for users and admins
- Seat locking and reservation flow to avoid double bookings
- Payment integration hooks (e.g., Stripe)
- Role-based access control for admin operations
- Database migrations and seed scripts

## Architecture
Typical architecture:
- Client (web/mobile) -> API Gateway / Backend REST API
- Backend -> Relational DB (Postgres recommended)
- Optional: Redis for ephemeral seat locks and rate limiting
- Optional: Message queue (RabbitMQ / Kafka) for async tasks (email, receipts)

Sequence for booking:
1. Client retrieves showtime and seat map.
2. Client requests to lock selected seats for a limited window.
3. Client completes payment using a payment gateway.
4. On success, backend confirms booking, persists ticket(s), releases locks, sends receipt.

## Tech Stack
- Language: Node.js / TypeScript OR Java / Kotlin OR Python (update to match repository)
- Web Framework: Express / Fastify / Spring Boot / Django Rest Framework (update as appropriate)
- Database: PostgreSQL (recommended)
- Cache: Redis (for seat locks & sessions)
- Payments: Stripe (sample), provider of choice
- Tests: Jest / Mocha / Pytest / JUnit
- Containerization: Docker

(Adjust the stack above to match the actual project.)

## Getting Started

### Prerequisites
- Git >= 2.x
- Node.js >= 16.x (or the project's specified runtime)
- PostgreSQL >= 12
- Redis (optional but recommended)
- Docker & Docker Compose (optional, for local full-stack dev)

### Environment Variables
Create a `.env` in the project root or set these in your environment. Example values (replace with real ones):

```
# Server
NODE_ENV=development
PORT=4000

# Database
DATABASE_URL=postgresql://dbuser:dbpass@localhost:5432/movie_tickets

# Auth
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=3600s

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Payments (optional)
STRIPE_API_KEY=sk_test_xxx

# Other
SENDER_EMAIL=no-reply@example.com
```

### Install & Run Locally

1. Clone the repo:
   git clone https://github.com/Ranger-DRAX/Movie-Ticket-Service.git
   cd Movie-Ticket-Service

2. Install dependencies:
   - Node.js (example)
     npm install
     OR
     yarn install

3. Prepare database:
   - Create the database using your DB admin tools, or via psql:
     createdb movie_tickets
   - Run migrations (see [Database & Migrations](#database--migrations))

4. Start the application:
   npm run dev
   OR
   yarn dev

The API should be available at http://localhost:4000 (or the PORT you configured).

## API Reference
Below are example endpoints. Adjust to match your actual routes.

Base URL: http://localhost:4000/api/v1

Authentication
- POST /auth/register
  - Body: { "email", "password", "name" }
  - Response: 201 Created + user payload

- POST /auth/login
  - Body: { "email", "password" }
  - Response: 200 OK + { token }

- POST /auth/refresh
  - Body: { "refreshToken" }

Movies
- GET /movies
  - Query params: page, limit, q
  - Response: list of movies

- GET /movies/:movieId
  - Response: movie detail

Theaters & Auditoriums
- GET /theaters
- GET /theaters/:theaterId/auditoriums

Showtimes
- GET /showtimes?movieId=&theaterId=&date=
- GET /showtimes/:showtimeId

Seats & Availability
- GET /showtimes/:showtimeId/seats
  - Returns seat map with availability and seat types (regular, VIP)

Seat Locking (critical for concurrency)
- POST /showtimes/:showtimeId/lock
  - Body: { "seatIds": [...], "holdDurationSeconds": 300 }
  - Response: lock token + expiration

- POST /showtimes/:showtimeId/release
  - Body: { "lockToken" }

Bookings & Payments
- POST /bookings
  - Body: {
      "showtimeId",
      "seatIds": [...],
      "paymentMethod": "stripe",
      "paymentToken": "tok_..."
    }
  - Flow: Validate lock -> charge payment -> persist booking -> return tickets or failure

- GET /bookings/:bookingId
- GET /users/:userId/bookings

Webhooks (Payments)
- POST /webhooks/payments/stripe
  - For handling asynchronous payment events (success, disputes)

Authentication header:
Authorization: Bearer <jwt-token>

Examples
- Get movies:
  curl -X GET "http://localhost:4000/api/v1/movies"

- Book seats (example):
  curl -X POST "http://localhost:4000/api/v1/bookings" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"showtimeId":"abc","seatIds":["s1","s2"],"paymentMethod":"stripe","paymentToken":"tok_..."}'

## Database & Migrations
- Database: PostgreSQL recommended.
- Use your chosen migration tool:
  - Node: Knex / TypeORM / Sequelize CLI
  - Python: Alembic / Django migrations
  - Java: Flyway / Liquibase

Example migration commands (Node + Knex example):
- npx knex migrate:latest
- npx knex seed:run

Schema overview (high-level)
- users (id, name, email, password_hash, role, created_at)
- movies (id, title, description, runtime, rating, poster_url)
- theaters (id, name, address)
- auditoriums (id, theater_id, name, seat_map_json)
- showtimes (id, movie_id, auditorium_id, starts_at, price)
- seats (id, auditorium_id, row, number, type)
- seat_locks (id, showtime_id, seat_id, lock_token, locked_until)
- bookings (id, user_id, showtime_id, total_amount, status)
- tickets (id, booking_id, seat_id, qr_code, status)
- payments (id, booking_id, provider, provider_id, amount, status)



## License & Contact
- License: MIT (or update to your chosen license)
- Maintainer: Ranger-DRAX
- For support or questions, open an issue on the repository.


