from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, conlist
from typing import List, Dict
import math

app = FastAPI()

@app.get("/trivia")
async def get_trivia_answers():
    answers = [4, 3, 2, 2, 3, 3, 3, 5, 4]
    return JSONResponse(content={"answers": answers})

from fit_spline import *
class MissingDataInput(BaseModel):
    series: List[List[float|None]]

@app.post("/blankety", status_code=status.HTTP_200_OK)
def blankety(request: Request, payload: MissingDataInput):
    ans = []
    for array in payload.series:
        filled_data = fill_missing_values(array, smoothing_param=1, plot_result=False)
        ans.append(filled_data)
    result = {
        "answer" : ans
    }

    return JSONResponse(content=result, media_type="application/json")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)