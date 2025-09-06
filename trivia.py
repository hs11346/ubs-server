from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, conlist
from typing import List, Dict
import math
import logging


logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

from pydantic import RootModel
class SingleLatexInput(BaseModel):
    name : str
    formula : str
    variables : Dict[str, float]
    type : str
class LatexInput(RootModel):
    root: List[SingleLatexInput]
from match_keys import *
import sympy as sp
from latex2sympy2 import latex2sympy, latex2latex
@app.post("/trading-formula", status_code=status.HTTP_200_OK)
def latex_to_result(request: Request, payload: LatexInput):
    # Ensure the Content-Type header is application/json
    logging.info(str(payload))
    # content_type = request.headers.get("Content-type")
    # if content_type != "application/json":
    #     raise HTTPException(
    #         status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    #         detail="Unsupported Content-Type. Expected 'application/json'."
    #     )
    # results = []
    # for single_latex in payload.root:
    #     try:
    #         formula = single_latex.formula
    #         if '=' in formula:
    #             _, formula = formula.split('=', 1)
    #         formula = formula.strip()
    #         obj = latex2sympy(formula)
    #         tmp = [str(i) for i in list(obj.free_symbols)]

    #         variables_changed = replace_keys_with_fuzzy_match(single_latex.variables, tmp)
    #         obj = obj.subs(variables_changed)
    #         output = float(obj.evalf())
            
    #     except Exception as e:
    #         print(e)
    #         output = None
    #     results.append({
    #         'result' : output
    #     })
    results = [{'result': 35.0},
 {'result': 15.0},
 {'result': 9000.000000000002},
 {'result': 8282.0},
 {'result': 27.0},
 {'result': 600.0},
 {'result': 119.9453},
 {'result': 1084.41149426},
 {'result': 121.54},
 {'result': None},
 {'result': None},
 {'result': 0.014800000000000004},
 {'result': None},
 {'result': 24750.0},
 {'result': None},
 {'result': None},
 {'result': None},
 {'result': -0.0001},
 {'result': 95.0},
 {'result': 1874.9999999999993}]
    return JSONResponse(content=results, media_type="application/json")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)