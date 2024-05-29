from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Classification API"}

@app.get("/hallo")
def get_hallo():
    return {
        "message":"Success",
        "status": 200,
        "data": [
            {"name":"ananta",
            "age":20,
            "sign":"virgo"}
        ]
    }
