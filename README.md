# Orquestación multi-agente con CrewAI

Ejemplo de dos agentes CrewAI (Investigador y Redactor) que colaboran sobre una tarea, usando un modelo alojado en Groq. Esta guía cubre la configuración del entorno con **UV** en Windows y Visual Studio Code.

## Requisitos

- Windows con PowerShell
- [UV](https://docs.astral.sh/uv/) (se instala en el paso 1)
- Una clave de API de [Groq](https://console.groq.com/keys)

## Estructura

| Archivo | Descripción |
|---|---|
| `crewai_orchestration.py` | Script principal: define el LLM, los agentes, las tareas y el crew |
| `requirements.txt` | Dependencias (`python-dotenv`, `crewai[litellm]`) |
| `.env` | Variables de entorno (no se versiona) |

## 1. Instalar UV

Verificar si ya está instalado:

```powershell
uv --version
```

Si no lo está:

```powershell
winget install --id=astral-sh.uv -e
```

Reiniciar la terminal y volver a comprobar con `uv --version`.

## 2. Instalar Python 3.13

```powershell
uv python install 3.13
uv python list --only-installed
```

## 3. Crear y activar el entorno virtual

Desde la raíz del repositorio:

```powershell
uv venv --python 3.13
.\.venv\Scripts\Activate.ps1
python --version
```

Resultado esperado: `Python 3.13.x`.

> Si `.venv` ya existe, no es necesario crearlo de nuevo. Reemplazarlo elimina las dependencias instaladas.

Si PowerShell bloquea la ejecución de scripts, habilitarla solo para la sesión actual y repetir la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## 4. Instalar las dependencias

```powershell
uv pip install -r requirements.txt
```

## 5. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```dotenv
GROQ_API_KEY=tu_clave_api
```

`.env` ya está en `.gitignore`. Comprobar que `.venv/` tampoco se versione.

## 6. Configurar VS Code

1. Presionar `Ctrl + Shift + P`.
2. Seleccionar `Python: Select Interpreter`.
3. Elegir `.venv\Scripts\python.exe`.

## 7. Ejecutar

```powershell
python .\crewai_orchestration.py
```

Al terminar, CrewAI pregunta `Share this execution trace with CrewAI? [y/N]`. Responder `N` o esperar 20 segundos.

## Cómo se conecta con Groq

El script usa el proveedor OpenAI nativo de CrewAI apuntando a la API compatible de Groq:

```python
llm = LLM(
    model="openai/openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0,
)
```

El prefijo `openai/` doble es intencional: CrewAI consume el primero para elegir el proveedor, y el segundo forma parte del id del modelo en Groq (`openai/gpt-oss-120b`).

## Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| `property 'cache_breakpoint' is unsupported` | Se usó `model="groq/..."`. Esa ruta pasa por LiteLLM, que no elimina el campo interno de caché de CrewAI. Usar la configuración de la sección anterior. |
| `The model 'gpt-oss-120b' does not exist` | Falta el prefijo doble. Usar `openai/openai/gpt-oss-120b`. |
| `'charmap' codec can't ...` | Codificación de la consola en Windows. Ejecutar con `$env:PYTHONIOENCODING = "utf-8"`. |
| `Falta GROQ_API_KEY en .env` | Crear el `.env` en la raíz y reiniciar la terminal. |

## Desactivar el entorno

```powershell
deactivate
```
