from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from schemas.schemas import UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import BookPicture, User
from authentication import auth
from string import ascii_letters
import random
import shutil

router = APIRouter(
    tags=['Admin Files'],
    prefix='/admin/file',
)


@router.post('/upload_book_image/{book_id}')
def admin_upload_book_picture(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db),
                              admin: UserAuth = Depends(auth.get_current_user_admin)):
    admin = db.query(User).filter(User.id == admin.id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    rand_str = ''.join(random.choice(ascii_letters) for _ in range(6))
    new_name = f'_{rand_str}.'.join(file.filename.rsplit('.', 1))

    pic = db.query(BookPicture).filter(BookPicture.book_id == book_id).first()
    if pic:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='This book already has a picture !')

    path_file = f'pictures/{new_name}'

    book_picture = BookPicture(
        book_id=book_id,
        picture=path_file,
    )

    db.add(book_picture)
    db.commit()

    with open(path_file, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return 'Picture Uploaded'


@router.delete('/delete_picture_of_book')
def admin_delete_book_picture(book_id: int, db: Session = Depends(get_db),
                              admin: UserAuth = Depends(auth.get_current_user_admin)):
    admin = db.query(User).filter(User.id == admin.id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    pictures = db.query(BookPicture).filter(BookPicture.book_id == book_id).all()

    if not pictures:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No picture found !')

    for picture in pictures:
        db.delete(picture)
        db.commit()

    return 'All pictures deleted.'
