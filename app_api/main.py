from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

origins = [
    "http://0.0.0.0",
    "http://0.0.0.0:3000",
]

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    try:
        # Query all users from the table
        users = db.query(UserDB).all()
        return {"message": users}
    except Exception as e:
        return {"Failed": str(e)}
    finally:
        db.close()


@app.post("/users/")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        db_user = UserDB(**user.dict())
        db.add(db_user)
        db.commit()
        return user
    except Exception as e:
        return {"Failed": str(e)}
    finally:
        db.close()
    
@app.delete("/users/{item_id}")
async def delete_user(item_id: int,db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserDB).filter(UserDB.id == item_id).first()
        if db_user is None:
            return {"message": "User not found"}
        db.delete(db_user)
        db.commit()
        return {"message": f"User {item_id} deleted"}
    except Exception as e:
        return {"Failed": str(e)}
    finally:
        db.close()

    
@app.put("/users/")
async def update_user(updated_user:User ,db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserDB).filter(UserDB.id == updated_user.id).first()
        if db_user is None:
            return {"message": "User not found"}
        db_user.id = updated_user.id
        db_user.name = updated_user.name
        db.commit()
        return {"message": f"User {id} updated"}
    except Exception as e:
        return {"Failed": str(e)}
    finally:
        db.close()

