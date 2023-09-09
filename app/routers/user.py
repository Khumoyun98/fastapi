from fastapi import status, HTTPException, Depends, APIRouter

from ..database import SessionLocal, get_db
from .. import utils, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    
    hashed_password = utils.hash(user.password) # hashed password
    user.password = hashed_password # change the password into hashed password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with {id} does not exist')

    return user