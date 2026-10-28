# AGENTS.md

`AGENTS.md` es un formato abierto: un Markdown en la raíz del repositorio que los agentes de código leen antes de actuar. Se formalizó como especificación abierta en agosto de 2025 (impulsada por OpenAI con Google, Cursor y Factory) y hoy la mantiene la Agentic AI Foundation, bajo la Linux Foundation. Lo leen de forma nativa Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, Zed y otras herramientas — por eso conviene mantener **un** archivo y symlinkear los formatos propietarios hacia él (§16), en vez de sostener copias que divergen.

La especificación no impone secciones: define el lugar y la regla de precedencia (§14). Todo lo que sigue es la convención de este equipo, no el estándar.

## 0. Jerarquía de reglas

Cuando dos reglas de este archivo entran en conflicto, se resuelven en este orden:

1. Seguridad y corrección — nunca se sacrifican por ninguna otra regla.
2. Convenciones del proyecto (stack, estilo, arquitectura) — se siguen salvo instrucción explícita en contrario.
3. Minimalismo (sección 6, disciplina Ponytail) — se aplica solo después de satisfacer 1 y 2.

## 1. Resumen del proyecto

Ejemplo de orquestación multi-agente con CrewAI: dos agentes (Investigador de IA y Redactor técnico) trabajan en secuencia sobre una tarea y producen un informe breve en español. Usa un modelo alojado en Groq (`openai/gpt-oss-120b`) mediante su API compatible con OpenAI. Proyecto personal de aprendizaje; lo ejecuta su autor desde Windows con UV y VS Code.

## 2. Stack técnico

- Lenguaje: Python 3.13 (venv local en `.venv/`, verificado 3.13.17)
- Framework: CrewAI 1.15.32 (`crewai[litellm]`), con `python-dotenv` 1.2.4 para cargar `.env`
- LLM: Groq vía proveedor OpenAI nativo de CrewAI (`base_url="https://api.groq.com/openai/v1"`, modelo `openai/openai/gpt-oss-120b`). Requiere `GROQ_API_KEY` en `.env`
- Gestor de paquetes: uv
- Plataforma de desarrollo: Windows 11, PowerShell, VS Code

(Versiones tomadas del venv instalado. `requirements.txt` no las fija: lista `python-dotenv` y `crewai[litellm]` sin versión. Pendiente decidir si se pinean.)

## 3. Estructura del proyecto

```text
crewai_mejora.py   # script principal: LLM, agentes, tareas y crew
requirements.txt   # dependencias (python-dotenv, crewai[litellm])
README.md          # guía de entorno con UV, ejecución y solución de problemas
AGENTS.md          # este archivo
.env               # GROQ_API_KEY (no se versiona)
.venv/             # entorno virtual (no se versiona)
.vscode/           # configuración del editor
.projectmem/       # memoria de proyecto (events.jsonl y derivados no se versionan)
```

Nota: `README.md` documenta el script como `crewai_orchestration.py`, pero el archivo actual se llama `crewai_mejora.py`. Corregir el README o renombrar el script para que coincidan.

## 11. Commits y PR

Conventional Commits v1.0.0 (spec estricta, sin desviaciones). Formato:

```
<tipo>(<alcance>)?(!)?: <sujeto>
<línea en blanco>
<cuerpo>
<línea en blanco>
<footer>
```

PR debe indicar qué cambia y por qué, no solo qué archivos.

### 11.0 Reglas de la spec (MUST, no negociables)

Directo de conventionalcommits.org v1.0.0 — violar cualquiera de estas invalida el commit como Conventional Commit, no es cuestión de estilo:

- Header: `tipo` + alcance opcional entre paréntesis + `!` opcional + `:` + espacio único + sujeto. Sin espacio antes de los dos puntos, sujeto arranca justo tras `:`.
- `feat` únicamente para funcionalidad nueva (MINOR en semver). `fix` únicamente para corrección de bug (PATCH en semver).
- Cuerpo, si existe, separado del header por exactamente una línea en blanco.
- Footer, si existe, separado del cuerpo por una línea en blanco. Formato git trailer: `Token: valor` o `Token #valor`. El token usa guiones en vez de espacios (`Reviewed-by`, `Refs`, no "Reviewed by"). El valor de un footer puede extenderse en varias líneas hasta que aparece el siguiente token válido.
- Breaking change — dos formas, no excluyentes, con una alcanza:
  1. Footer `BREAKING CHANGE: <descripción>` (el token va siempre en mayúsculas — única unidad de la spec que es case-sensitive; `BREAKING-CHANGE` es sinónimo válido de `BREAKING CHANGE`).
  2. `!` inmediatamente antes de los dos puntos del header: `feat(scope)!: ...`.
  Un breaking change en cualquier tipo (no solo `feat`/`fix`) fuerza MAJOR en semver.
- `revert`: sujeto describe el commit revertido; footer obligatorio `This reverts commit <hash-completo>.`
- Tipos fuera de `feat`/`fix`/breaking (`docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`) son permitidos por la spec pero no aportan bump de semver por sí solos.

### 11.1 Reglas del proyecto

- Idioma: sujeto/cuerpo/footer en español. Tipo siempre en inglés (estándar commitlint config-conventional).
- Sujeto: imperativo presente, minúsculas, sin punto final, ≤72 chars (ideal ≤50). Detalle en el cuerpo, nunca en el sujeto.
- Alcance opcional, kebab-case, lista cerrada del área tocada: (no aplica por ahora: el proyecto es un solo script sin áreas recurrentes; omitir el alcance). Agregar alcance nuevo a la lista si el área es real y recurrente, no inventar uno de un solo uso; omitir si el cambio es transversal.
- Cuerpo: qué y por qué, nunca cómo (el diff ya dice cómo). Un commit = un cambio lógico.
- Footer: `Closes #N`/`Fixes #N` para issues; breaking change siempre documentado en footer aunque ya lleve `!` en el header.
- Enforcement mecánico (opcional, recomendado): `commitlint` + hook de `husky`/`lefthook` en `commit-msg` — si no está instalado, decirlo explícito, no asumir que un agente valida esto solo. Estado actual: no instalado en este proyecto (sin `package.json` ni hooks de git). Nadie valida el formato automáticamente.

Nunca agregar trailers/firmas de autoría de agente/IA a un commit ni a un PR (líneas tipo `Co-Authored-By: <agente>`, `<Agente>-Session: <url>`, "Generated with…", enlaces de sesión, o equivalentes de cualquier herramienta, no solo una en particular), salvo que el usuario lo pida explícitamente para ese commit o PR puntual. Por defecto, mensaje de commit y descripción de PR limpios, sin firma de agente, sin importar cuál se esté usando.

**Alcance ampliado (no solo commits/PR):** sin comentarios tipo "generado por IA/agente", sin headers de archivo con firma de autoría de agente, sin menciones en README/CHANGELOG/licencias, sin watermarks en código o docs generados — salvo pedido explícito del usuario puntual para ese artefacto.

### 11.2 Gitmoji

Este proyecto adopta Gitmoji: el emoji es obligatorio en todo commit.

Formato con Gitmoji: `:emoji: <tipo>(<alcance>)?(!)?: <sujeto>`.

- Emoji obligatorio al inicio de todo commit, prioridad de menor a mayor:
  1. Gitmoji por defecto según tipo (gitmoji.dev), con el significado oficial de cada uno — el mapeo funciona porque coincide con la semántica del catálogo, no por convención local: `feat`→✨ (*introduce new features*), `fix`→🐛 (*fix a bug*), `docs`→📝 (*add or update documentation*), `style`→🎨 (*improve structure/format of the code*), `refactor`→♻️ (*refactor code*), `perf`→⚡️ (*improve performance*), `test`→✅ (*add, update or pass tests*), `build`→📦️ (*update compiled files or packages*), `ci`→👷 (*add or update CI build system*), `chore`→🔧 (*config/tooling change*), `revert`→⏪️ (*revert changes*).
  2. Gitmoji específico del catálogo si encaja mejor: 💥 breaking, 🎉 inicio proyecto, 🔥 quitar código, 💄 UI, 🔒 seguridad, 🚀 deploy — (sin extras del proyecto por ahora).
  3. Emoji personalizado para dominio del proyecto (ej. 🐋 al tocar Docker) — libre si el significado no es ambiguo.
- Excepción: merge commits y bots (dependabot) no se reescriben a este formato.
- No contradice la regla de firma de agente arriba: el emoji es semántico (tipo de cambio), no atribución de autoría — sigue sin ir `Co-Authored-By` ni equivalentes salvo pedido explícito.
