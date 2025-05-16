# Servicio de Optimización de Portafolios

## Descripción del Proyecto
Este proyecto implementa un servicio REST para la optimización de portafolios de inversión utilizando el modelo de Markowitz. El servicio acepta datos de retornos diarios y proporciona pesos óptimos para la asignación de activos.

## Método de Optimización
Hemos elegido el modelo de Markowitz (Modern Portfolio Theory - MPT) por las siguientes razones:

1. **Fundamento Teórico Sólido**: El modelo MPT es ampliamente reconocido y probado en la industria financiera.
2. **Balance Riesgo-Retorno**: Optimiza explícitamente el trade-off entre rendimiento esperado y riesgo.
3. **Flexibilidad**: Permite incorporar restricciones como límites de peso por activo y nivel de riesgo máximo.
4. **Interpretabilidad**: Los resultados son fácilmente interpretables para los usuarios finales.

### Métricas Utilizadas
- **Riesgo**: Volatilidad (desviación estándar de los retornos)
- **Optimización**: Maximización del ratio de Sharpe

## Estructura del Proyecto
```
├── app/
│   ├── main.py           # Aplicación FastAPI
│   ├── optimizer.py      # Lógica de optimización
│   └── utils.py          # Funciones auxiliares
├── tests/                # Tests unitarios
├── requirements.txt      # Dependencias
└── Dockerfile           # Configuración de contenedor
```

## Instalación y Ejecución
1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el servidor: `uvicorn app.main:app --reload`

## Uso del API
```bash
curl -X POST http://localhost:8000/optimize-portfolio \
  -H "Content-Type: multipart/form-data" \
  -F "file=@returns.csv" \
  -F "risk_level=1.0" \
  -F "max_weight=0.15"
```

## Tecnologías Utilizadas
- FastAPI: Framework web moderno y de alto rendimiento
- NumPy/Pandas: Procesamiento de datos financieros
- SciPy: Optimización matemática
- Docker: Containerización
- GitHub Actions: CI/CD