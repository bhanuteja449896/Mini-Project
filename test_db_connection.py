#!/usr/bin/env python3
"""
Database Connection Test Script
Test if PostgreSQL connection is working properly
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_db_connection():
    """Test PostgreSQL connection"""
    try:
        print("🔌 Testing PostgreSQL Connection...")
        print("=" * 60)
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("❌ ERROR: DATABASE_URL not found in .env file")
            return False
        
        print(f"📍 Connecting to database...")
        
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            connection.commit()
            print("✅ PostgreSQL Connection: SUCCESS")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"❌ PostgreSQL Connection: FAILED")
        print(f"Error: {str(e)}")
        print("=" * 60)
        print("\nTroubleshooting Tips:")
        print("1. Check if DATABASE_URL is correct in .env file")
        print("2. Verify your internet connection")
        print("3. Check if Neon database is active")
        print("4. Ensure psycopg2 is installed: pip install psycopg2-binary")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)
