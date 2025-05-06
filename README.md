# Jawnt Technical Screening Submission

This project solves a real-world fintech use case using a FastAPI backend and a Next.js frontend (with Mantine component library). It fulfills all core requirements described in the screening instructions:

- Organization administrators can manage employees (create, update, delete)
- Employees can initiate ACH debit payments and swipe their debit cards
- Employees can view a table of their payments and card transactions
- Transactions are processed with a simulated external payment system
- A queue system tracks outbound tasks (e.g., swipe/payments) for processing
- SQL query aggregates merchant totals

---

## 🧠 Tech Stack & Design Decisions

### Backend (FastAPI + SQLAlchemy)

- FastAPI was chosen for its speed, clear typing, and easy testing
- SQLAlchemy handles database models and session management
- Simulated external calls (ACH/Swipe) are implemented via the `lib/jawnt/client.py` file
- In-memory `MessageQueue` simulates a task queue and is used to enqueue outbound ACH/swipe events
- Testing is handled with `pytest`, using a temp SQLite file to preserve DB state across requests

### Frontend (Next.js + Mantine + Mantine React Table)

- Built with Next.js App Router using React Server Components + Client Components
- Mantine was used for fast styling and flexibility without custom CSS boilerplate
- Mantine React Table renders the payments and transactions with sorting and styling
- Tables are populated via calls to the FastAPI backend at `localhost:8000/api`

---

## 🧪 Running Unit Tests (Backend)

From the `app/` directory or project root:

# Run all backend unit tests
pytest

# Running SQL Query
- The SQL file is located at:
  
  step3_merchant_aggregation.sql
- To test it manually (e.g., using SQLite CLI):

  sqlite3 your_database.db < sql/aggregate_transactions.sql
- To test it with code:

  pytest app/test/test_sql_query.py

# Running Message Queue
- Queue Consumer (in a second terminal):

python app/scripts/consume_queue.py

- Simulates a message queue worker that processes ACH/swipe events.

# Running the Full Stack Locally
1. Start the FastAPI Backend:

- Run: cd app, and then, uvicorn main:app --reload

- The API will be available at: http://localhost:8000/api

2. Start the Queue Consumer (in a second terminal)

- Run: python app/scripts/consume_queue.py

- This will simulate a message queue worker processing ACH/swipe events.

3. Seed the Database (optional)

- Run: python app/scripts/seeding.py

- This script will add a sample organization and employee data.

4. Start the React Frontend (in a 3rd terminal)

- Run: cd frontend, npm install, npm run dev

- Visit http://localhost:3000 to view the Employee Dashboard with live data.

Screenshots of the frontend locally:
![Dashboard Screenshot](https://private-user-images.githubusercontent.com/42252676/440962031-c605ab60-0f12-433c-9e7e-ec16f8781f2f.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDY1NjU1NTYsIm5iZiI6MTc0NjU2NTI1NiwicGF0aCI6Ii80MjI1MjY3Ni80NDA5NjIwMzEtYzYwNWFiNjAtMGYxMi00MzNjLTllN2UtZWMxNmY4NzgxZjJmLmpwZWc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNTA2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDUwNlQyMTAwNTZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mNGNmN2RlNmNjYWM2M2U1MjczZThhMTkzODc1NjZiMTA5ZGU5OGQ1MzFlN2M1Y2Q1ZmNmYzg2ZGM4NGQxNDRlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.7_nOyqYCqMQQZRbf2eDILqv5JY9h8J2WzQXfLKpVTVM)
![Dashboard Screenshot](https://private-user-images.githubusercontent.com/42252676/440962030-acda73e6-b8de-45db-b891-12d5fdb0f587.jpeg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDY1NjU2OTMsIm5iZiI6MTc0NjU2NTM5MywicGF0aCI6Ii80MjI1MjY3Ni80NDA5NjIwMzAtYWNkYTczZTYtYjhkZS00NWRiLWI4OTEtMTJkNWZkYjBmNTg3LmpwZWc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNTA2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDUwNlQyMTAzMTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01MzA3OWExNzkwMGI5ODMzOTA0NWJiOTEwYjJkYzQ4OWYyZmNjMzU2NTI0MzNmZWZiMzIxOTQ3MWViYTI5YmU0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.81HN7unlKFLO-n6G4MKRAQ05dfpv_GIP6DtF6Ca5WyQ)
