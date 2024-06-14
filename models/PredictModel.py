from sqlalchemy import Column, Integer, Float, String
from database import Base

class PredictModel(Base):
    __tablename__ = 'histori_prediksi'

    id_histori = Column(Integer, primary_key=True, index=True)
    nama_balita = Column(String)
    umur = Column(Integer)
    jenis_kelamin = Column(String)
    tinggi_badan = Column(Float)
    hasil_prediksi = Column(String)