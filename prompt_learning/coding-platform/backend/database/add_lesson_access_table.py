"""
Migration script to add user_lesson_access table
Run this to enable lesson access control feature
"""

import asyncio
from database.connection import AsyncSessionLocal, init_db
from sqlalchemy import text

async def create_lesson_access_table():
    """Create user_lesson_access table for controlling student access to lessons"""
    await init_db()

    async with AsyncSessionLocal() as session:
        try:
            # Create the table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS user_lesson_access (
                id VARCHAR PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                lesson_id VARCHAR NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
                is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
                disabled_by VARCHAR REFERENCES users(id) ON DELETE SET NULL,
                disabled_reason VARCHAR(500),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE,
                CONSTRAINT uq_user_lesson UNIQUE (user_id, lesson_id)
            );
            """
            await session.execute(text(create_table_sql))

            # Create indexes for better query performance (execute separately)
            await session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_lesson_access_user_id ON user_lesson_access(user_id)"))
            await session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_lesson_access_lesson_id ON user_lesson_access(lesson_id)"))
            await session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_lesson_access_enabled ON user_lesson_access(is_enabled)"))

            await session.commit()

            print("✅ Successfully created user_lesson_access table")
            print("✅ Created indexes for optimal query performance")
            print("\nAccess Control Logic:")
            print("  - By default, all lessons are accessible to all users")
            print("  - Add a record with is_enabled=False to DISABLE a lesson for a user")
            print("  - Add a record with is_enabled=True to explicitly ENABLE a lesson")
            print("  - No record = lesson is accessible (default allow)")

            return True

        except Exception as e:
            print(f"❌ Error creating table: {e}")
            await session.rollback()
            return False

if __name__ == "__main__":
    asyncio.run(create_lesson_access_table())
