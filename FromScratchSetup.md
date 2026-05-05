Prerequisites to install on the new machine

  # Python 3.11   
  sudo apt install python3.11 python3.11-venv python3-pip

  # PostgreSQL 16
  sudo apt install postgresql postgresql-client

  # Redis
  sudo apt install redis-server

  # Node.js 18+                                                                                                                           
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt install nodejs

  ---                                                                                                                                     
  Step 0 — Export your current DB (do this NOW on your current machine)

  Your DB is currently inside Docker, so pull it out first:

  cd /root/ppf

  # Dump from the running Docker container                                                                                                
  docker-compose exec db pg_dump \
    -U portfolio \
    -d portfolio_db \
    --no-owner --no-acl \
    > portfolio_dump.sql

  Keep portfolio_dump.sql safe — copy it to a USB, cloud drive, or just push it temporarily somewhere private.

  ---                                                                                                                                     
  Step 1 — Get the code on the new machine

  # After you push to GitHub (from DEPLOY.md Step 1)
  git clone https://github.com/YOUR_USERNAME/portfolio.git
  cd portfolio

  ---                                                                                                                                     
  Step 2 — Setup PostgreSQL

  # Start postgres
  sudo systemctl start postgresql
  sudo systemctl enable postgresql

  # Create user and database                                                                                                              
  sudo -u postgres psql <<EOF
  CREATE USER portfolio WITH PASSWORD 'strongpassword';
  CREATE DATABASE portfolio_db OWNER portfolio;
  EOF

  # Import your data                                                                                                                      
  psql -U portfolio -d portfolio_db -f /path/to/portfolio_dump.sql

  ---             
  Step 3 — Setup Redis

  sudo systemctl start redis-server
  sudo systemctl enable redis-server

  # Verify it works                                                                                                                       
  redis-cli ping   # should return PONG

  ---                                                                                                                                     
  Step 4 — Setup Backend

  cd portfolio/backend

  # Create virtual environment                                                                                                            
  python3.11 -m venv .venv
  source .venv/bin/activate

  # Install dependencies                                                                                                                  
  pip install -r requirements.txt

  # Create .env file
  cp ../.env.example .env

  Now edit .env — the key changes from the example:

  APP_ENV=development
  DATABASE_URL=postgresql+asyncpg://portfolio:strongpassword@localhost:5432/portfolio_db
  REDIS_URL=redis://localhost:6379/0
  CELERY_BROKER_URL=redis://localhost:6379/1
  CELERY_RESULT_BACKEND=redis://localhost:6379/2
  ALLOWED_ORIGINS=http://localhost:3000

  Fill in your real values for SECRET_KEY, GITHUB_TOKEN, MAIL_*, ADMIN_EMAIL, ADMIN_PASSWORD.

  # Run migrations (schema is already there from dump, but safe to run)                                                                   
  alembic upgrade head

  # Start backend                                                                                                                         
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  Test: http://localhost:8000/health → {"status":"ok"}

  ---                                                                                                                                     
  Step 5 — Setup Frontend

  # Open a new terminal
  cd portfolio/frontend

  # Install dependencies                                                                                                                  
  npm install

  # Create env file                                                                                                                       
  echo "VITE_API_URL=http://localhost:8000" > .env.local

  # Start frontend                                                                                                                        
  npm run dev

  Test: http://localhost:3000 → your portfolio loads with your data.

  ---
  Step 6 — Run Celery (optional, for GitHub sync)

  # Open another terminal
  cd portfolio/backend
  source .venv/bin/activate

  celery -A app.tasks.worker worker --loglevel=info --concurrency=2

  ---
  Running the app daily (3 terminals)

  # Terminal 1 — Backend
  cd portfolio/backend && source .venv/bin/activate && uvicorn app.main:app --reload

  # Terminal 2 — Frontend
  cd portfolio/frontend && npm run dev

  # Terminal 3 — Celery (only if you need GitHub sync)
  cd portfolio/backend && source .venv/bin/activate && celery -A app.tasks.worker worker --loglevel=info