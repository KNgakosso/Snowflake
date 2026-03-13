from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.models import InitParamsModel, PhysicalParamsModel, SimulParamsModel, UpdateSelectionModel, SelectionModel
import uvicorn
from backend.snowflake import Snowflake
import backend.wrapper as wrapper
from pathlib import Path
import os

snowflake_path = Path(__file__).parent.parent / "mesh"
snowflake = Snowflake()
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")   # ../frontend par rapport à backend/

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
####################################
# GET ROUTES
####################################

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)

@app.get("/mesh")
def get_mesh():
    return wrapper.get_mesh(snowflake)

@app.get("/initialization_params")
def get_initialization_params():
    return wrapper.get_initialization_params(snowflake)

@app.get("/simulation_params")
def get_simulation_params():
    return wrapper.get_simulation_params(snowflake)

@app.get("/physical_params")
def get_physical_params():
    return wrapper.get_physical_params(snowflake)


####################################
# PATCH ROUTES
####################################
@app.patch("/initialization_params")
def update_initialzation_params_endpoint(initialization_params_model : InitParamsModel):
    answer = wrapper.update_initialization_params(snowflake, initialization_params_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/simulation_params")
def update_simulation_params_endpoint(simulation_params_model : SimulParamsModel):
    answer = wrapper.update_simulation_params(snowflake, simulation_params_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/physical_params")
def update_physical_params_endpoint(physical_params_model : PhysicalParamsModel):
    answer = wrapper.update_physical_params(snowflake, physical_params_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/temperature")
def set_temperature_endpoint(update_selection_model : UpdateSelectionModel):
    answer = wrapper.set_temperature(snowflake, update_selection_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/vapor")
def set_vapor_endpoint(update_selection_model : UpdateSelectionModel):
    answer = wrapper.set_vapor(snowflake, update_selection_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/ice_potential")
def set_ice_potential_endpoint(update_selection_model : UpdateSelectionModel):
    answer = wrapper.set_ice_potential(snowflake, update_selection_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/frozen/true")
def set_frozen_true_endpoint(selection_model : SelectionModel):
    answer = wrapper.set_frozen_true(snowflake, selection_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/frozen/false/")
def set_frozen_false_endpoint(selection_model : SelectionModel):
    answer = wrapper.set_frozen_false(snowflake, selection_model)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

@app.patch("/randomize")
def random_initial_state_endpoint():
    answer = wrapper.random_initial_state(snowflake)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer


##############################################
# PUT ROUTES
##############################################

@app.put("/simulation")
def run_simulation_endpoint():
    answer = wrapper.run_simulation(snowflake)
    wrapper.save_snowflake(snowflake, snowflake_path)
    return answer

"""
@app.get("/mesh")
def save_simulation_endpoint():
    mesh_model = wrapper.load_simulation()
    return mesh_model

@app.get("/simulation")
def load_simulation_endpoint():
    pass
"""