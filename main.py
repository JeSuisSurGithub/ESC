import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/html", StaticFiles(directory="html"), name="html")

@app.get("/")
def racine() -> str:
    return FileResponse('html/index.html')

if __name__ == "__main__":
    uvicorn.run(app)