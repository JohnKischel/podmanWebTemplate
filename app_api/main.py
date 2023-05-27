from fastapi import FastAPI
from models import User
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy engine
engine = create_engine('postgresql://postgres:postgres@dbend:5432/postgres')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define a model representing a table
class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

# Create the table in the database (if it doesn't exist)
Base.metadata.create_all(engine)


app = FastAPI()

@app.post("/users/")
async def create_user(user: User):
    try:
        session = Session()
        db_user = UserDB(**user.dict())
        session.add(db_user)
        session.commit()
        session.close()
        return {"Success": user}
    except Exception as e:
        return {"Failed": str(e)}

@app.get("/users")
async def users():
    try:
        session = Session()
        # Query all users from the table
        users = session.query(UserDB).all()
        return {"message": users}
    except Exception as e:
        return {"Failed": str(e)}
