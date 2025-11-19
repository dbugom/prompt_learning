-- Database initialization script
-- This script runs on first database startup

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for performance (will be created by SQLAlchemy, but good to have as backup)
-- These will be created after tables exist

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE coding_platform TO platform_user;

-- Set timezone
SET timezone = 'UTC';
