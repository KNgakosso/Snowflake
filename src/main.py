from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from src.models import CellModel, MeshModel, MeshParamsModel
import os
import uvicorn
from src.mesh_maker import Snowflake

snowflake_path = "/mesh/"
sf = Snowflake(snowflake_path)
app = FastAPI()


@app.patch("/params")
def update_params_endpoint(mesh_params_model : MeshParamsModel):
    return sf.update_params(mesh_params_model)

@app.put("/mesh")
def run_simulation_endpoint():
    return sf.run_simulation()

@app.get("/mesh")
def get_mesh_endpoint():
    mesh_model = sf.load_simulation()
    return mesh_model