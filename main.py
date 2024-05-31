from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pickle
import numpy as np
from database import SessionLocal, engine, get_db
from models import UserModel

# Memuat model KNN
with open('knn_model.pkl', 'rb') as model_file:
    knn_model = pickle.load(model_file)

# Memuat label encoder
with open('label_encoder_status.pkl', 'rb') as le_file:
    label_encoder_status = pickle.load(le_file)

# Inisialisasi FastAPI
app = FastAPI()

# Definisi kelas untuk validasi input
class Balita(BaseModel):
    umur: int
    jenis_kelamin: int
    tinggi_badan: float

# Endpoint untuk prediksi
@app.post("/predict")
def predict(balita: Balita):
    try:
        # Mengambil data dari input dan memastikan tipe data benar
        data = np.array([[balita.umur, balita.jenis_kelamin, balita.tinggi_badan]], dtype=float)
        
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
        return {"status_gizi": status_gizi}
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Menambahkan root endpoint untuk memastikan API berjalan
@app.get("/")
def read_root():
    return {"message": "API is working"}


@app.get("/users")
def get_users(skip: int = 0, limit: int =10, db: Session = Depends(get_db)):
    users = db.query(UserModel.UserModel).offset(skip).limit(limit).all()
    return users
