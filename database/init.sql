DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'user_name') THEN
        CREATE USER :'user_name' WITH PASSWORD :'user_password';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE :'db_name' TO :'user_name';