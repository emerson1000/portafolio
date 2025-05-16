import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict

def calculate_portfolio_metrics(weights: np.ndarray, returns: np.ndarray) -> tuple:
    """Calcula el retorno esperado y la volatilidad del portafolio."""
    portfolio_return = np.sum(returns.mean() * weights) * 252  # Anualizado
    portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    sharpe_ratio = portfolio_return / portfolio_vol  # Asumiendo tasa libre de riesgo = 0
    return portfolio_return, portfolio_vol, sharpe_ratio

def negative_sharpe_ratio(weights: np.ndarray, returns: np.ndarray) -> float:
    """Función objetivo para maximizar el ratio de Sharpe (minimizando su negativo)."""
    return -calculate_portfolio_metrics(weights, returns)[2]

def optimize_portfolio(
    returns_df: pd.DataFrame,
    risk_level: float,
    max_weight: float
) -> Dict[str, float]:
    """Optimiza el portafolio usando el modelo de Markowitz.
    
    Args:
        returns_df: DataFrame con retornos diarios (columnas son tickers)
        risk_level: Nivel máximo de riesgo permitido (volatilidad anualizada)
        max_weight: Peso máximo permitido por activo
    
    Returns:
        Dict con los pesos óptimos por ticker
    """
    returns = returns_df.values
    n_assets = returns.shape[1]
    tickers = returns_df.columns.tolist()
    
    # Restricciones
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Suma de pesos = 1
        {'type': 'ineq', 'fun': lambda x: risk_level - 
         np.sqrt(np.dot(x.T, np.dot(returns.cov() * 252, x)))}  # Restricción de riesgo
    ]
    
    # Límites por activo
    bounds = tuple((0, max_weight) for _ in range(n_assets))
    
    # Pesos iniciales equitativos
    initial_weights = np.array([1/n_assets] * n_assets)
    
    # Optimización
    result = minimize(
        negative_sharpe_ratio,
        initial_weights,
        args=(returns,),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    if not result.success:
        raise ValueError("La optimización no convergió: " + result.message)
    
    # Redondear pesos pequeños a 0 y renormalizar
    optimal_weights = result.x.copy()
    optimal_weights[optimal_weights < 0.0001] = 0
    optimal_weights = optimal_weights / optimal_weights.sum()
    
    # Crear diccionario de resultados
    return {ticker: float(weight) for ticker, weight in zip(tickers, optimal_weights)}