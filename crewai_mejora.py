# Requiere: pip install crewai python-dotenv
import os

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Falta GROQ_API_KEY en .env")

llm = LLM(
    model="openai/openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0,
)


# 3. Crear agente investigador
investigador = Agent(
    role="Investigador de inteligencia artificial",
    goal="Analizar qué son los agentes de IA y sus aplicaciones",
    backstory=("Eres especialista en inteligencia artificial y sistemas multiagente."),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# 4. Crear agente redactor
redactor = Agent(
    role="Redactor técnico",
    goal="Explicar conceptos técnicos de manera clara",
    backstory=("Eres un experto en documentación técnica y divulgación de tecnología."),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# 5. Tarea del investigador
tarea_investigacion = Task(
    description=(
        "Explica qué es un agente de inteligencia "
        "artificial, cómo funciona y menciona "
        "tres aplicaciones prácticas."
    ),
    expected_output="Un análisis con tres ejemplos.",
    agent=investigador,
)

# 6. Tarea del redactor
tarea_redaccion = Task(
    description=(
        "Redacta un informe breve y claro en español "
        "usando la información del investigador."
    ),
    expected_output="Un informe de máximo 200 palabras.",
    agent=redactor,
    context=[tarea_investigacion],
)

# 7. Crear equipo
equipo = Crew(
    agents=[investigador, redactor],
    tasks=[tarea_investigacion, tarea_redaccion],
    process=Process.sequential,
    verbose=True,
)

# 8. Ejecutar agentes
if __name__ == "__main__":
    resultado = equipo.kickoff()

    print("\n===== RESULTADO FINAL =====\n")
    print(resultado.raw)
