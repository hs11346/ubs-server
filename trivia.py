from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/trivia")
async def get_trivia_answers():
    answers = [4, 3, 2, 2, 3, 3, 3, 5, 4]
    return JSONResponse(content={"answers": answers})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)