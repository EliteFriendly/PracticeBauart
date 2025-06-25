from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}



@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        file_path = f"test-files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}