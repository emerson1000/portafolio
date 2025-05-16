from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from io import StringIO
from typing import Dict
from .optimizer import optimize_portfolio

app = FastAPI(
    title="Servicio de Optimización de Portafolios",
    description="API para optimización de portafolios usando el modelo de Markowitz",
    version="1.0.0"
)

@app.post("/optimize-portfolio")
async def create_optimal_portfolio(
    file: UploadFile,
    risk_level: float = Form(...),
    max_weight: float = Form(...)
) -> Dict:
    try:
        # Validar parámetros
        if not 0 < risk_level <= 2.0:
            raise HTTPException(
                status_code=400,
                detail="El nivel de riesgo debe estar entre 0 y 2.0"
            )
        
        if not 0 < max_weight <= 1.0:
            raise HTTPException(
                status_code=400,
                detail="El peso máximo debe estar entre 0 y 1.0"
            )

        # Leer y procesar el archivo CSV
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode('utf-8')))
        
        # Validar el formato del archivo
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="El archivo CSV está vacío"
            )

        # Calcular el portafolio óptimo
        optimal_weights = optimize_portfolio(
            returns_df=df,
            risk_level=risk_level,
            max_weight=max_weight
        )

        return {"optimal_portfolio": optimal_weights}

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="Error al leer el archivo CSV"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el servidor: {str(e)}"
        )

@app.get("/")
def read_root():
    return {"message": "Servicio de Optimización de Portafolios"}