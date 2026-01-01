from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.config import settings

# In psycopg3, we can use the same URL for sync and async engine creation
# as long as we use the 'postgresql+psycopg' dialect.
engine = create_engine(settings.DATABASE_URL)

def verify_seeding():
    """Checks if the database has the expected number of records after seeding."""
    try:
        with Session(engine) as session:
            movie_count = session.execute(text("SELECT COUNT(*) FROM movies")).scalar_one()
            director_count = session.execute(text("SELECT COUNT(*) FROM directors")).scalar_one()

            if movie_count == 1000 and director_count > 1000:
                print("✅ Seeding Successful!")
                print(f"   - Movies loaded: {movie_count}")
                print(f"   - Directors loaded: {director_count}")
                return True
            else:
                print(f"❌ Seeding Failed. Expected 1000 movies, found {movie_count}.")
                return False
    except Exception as e:
        print(f"❌ Database connection or query failed: {e}")
        return False

if __name__ == "__main__":
    verify_seeding()