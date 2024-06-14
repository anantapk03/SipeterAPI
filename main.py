from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pickle
import numpy as np
from database import SessionLocal, engine, get_db
from models import UserModel
# import baru
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from typing import Annotated
from models import PredictModel


# Memuat model KNN
with open('knn_model.pkl', 'rb') as model_file:
    knn_model = pickle.load(model_file)

# Memuat label encoder
with open('label_encoder_status.pkl', 'rb') as le_file:
    label_encoder_status = pickle.load(le_file)

# Inisialisasi FastAPI
app = FastAPI()

# Endpoint untuk prediksi
@app.post("/predict")
def predict(nama_balita: str, umur : int, jenis_kelamin : int, tinggi_badan: float):

    try:
        # Mengambil data dari input dan memastikan tipe data benar
        data = np.array([[umur, jenis_kelamin, tinggi_badan]], dtype=float)
        
        # Melakukan prediksi
        prediksi = knn_model.predict(data)
        
        # Mengonversi hasil prediksi ke label asli
        status_gizi = label_encoder_status.inverse_transform(prediksi)[0]
        
        # Pastikan hasil prediksi adalah tipe data dasar Python
        status_gizi = str(status_gizi)

        # STATUS GIZI RESPONSE : 
        """
        "0" : normal
        "1" : severely stunted
        "2" : stunted
        "3" : tinggi
        """
        # Jenis Kelamin
        """
        "0" : laki-laki
        "1" : perempuan
        """

        # simpan data
        db = SessionLocal()
        db_item = PredictModel.PredictModel(nama_balita = nama_balita, umur = umur, jenis_kelamin = jenis_kelamin, tinggi_badan = tinggi_badan, hasil_prediksi = status_gizi)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
        #return {"status_gizi": status_gizi}
        
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))



# Menambahkan root endpoint untuk memastikan API berjalan
@app.get("/")
def read_root():
    return {"message": "API is working"}


@app.get("/users")
def get_users(skip: int = 0, limit: int =10, db: Session = Depends(get_db)):
    users = db.query(UserModel.UserModel).offset(skip).limit(limit).all()
    return users

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

# Function to authenticate the user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(UserModel.UserModel).filter(username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return {'username': username}

# Endpoint to login and get access token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code = 401,
            detail = "login failed"
        )
    return user

@app.post('/input')
async def request(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}