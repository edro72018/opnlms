# CLAUDE.md — OpenLMS

Contexto permanente del proyecto para sesiones de desarrollo con Claude Code.

---

## Qué es el proyecto

**OpnLMS** es un sistema de gestión de aprendizaje (LMS) en Python. Permite administrar cursos en línea con inscripciones de estudiantes y seguimiento de progreso. Versión actual: `v0.1.0` (etapa temprana). Lenguaje predominante en código y mensajes: **español**.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy 2.0 async |
| Driver DB | asyncpg (PostgreSQL) |
| Migraciones | Alembic |
| Validación | Pydantic v2 |
| Auth | JWT via python-jose + bcrypt via passlib |
| Testing | pytest + pytest-asyncio |
| Runtime | Python 3.12.13 |
| Deploy | Docker Compose (local) + Render (producción) |

---

## Arquitectura

Arquitectura en capas estricta. Respetar siempre este flujo:

```
app/api/          → Solo maneja HTTP: validación de entrada, respuesta
app/services/     → Lógica de negocio. Aquí van las reglas
app/repositories/ → Solo queries a la base de datos
app/models/       → Entidades SQLAlchemy ORM
app/schemas/      → DTOs de Pydantic (request/response)
app/core/         → Config, seguridad, DB session, excepciones
```

**Patrones en uso:**
- Repository Pattern — los services nunca hacen queries directas
- Service Layer — los routers nunca contienen lógica de negocio
- Dependency Injection — `Depends()` para DB session y usuario actual
- `APIResponse[T]` — wrapper genérico para todas las respuestas (ver `app/schemas/base.py`)

---

## Entidades del dominio

```
User        → id (UUID), email, first_name, middle_name?, last_name, second_last_name?
              role: admin | teacher | student (default: student)
              is_active, hashed_password, timestamps

Course      → id (UUID), title, description?, status: draft|published|archived
              thumbnail_url?, created_by (FK → User), timestamps
              - Relación: tiene muchos Module (cascade delete)

Module      → id (UUID), title, description?, order (int), is_visible
              course_id (FK → Course, cascade delete), timestamps

Enrollment  → id (UUID), student_id (FK → User), course_id (FK → Course)
              progress (float 0.0–100.0), is_active, completed, timestamps
              - Unique: (student_id, course_id)
```

---

## Endpoints actuales

Prefijo base: `/api/v1`

```
Auth:
  POST /auth/register
  POST /auth/login
  GET  /auth/me

Cursos:
  GET    /courses
  POST   /courses
  GET    /courses/{id}
  PUT    /courses/{id}
  DELETE /courses/{id}
  POST   /courses/{id}/modules
  GET    /courses/{id}/modules

Inscripciones:
  POST   /enrollments/{course_id}
  DELETE /enrollments/{course_id}
  GET    /enrollments/my-courses
  GET    /enrollments/{course_id}/students

Sistema:
  GET /health
  GET /health/db
```

---

## RBAC (Roles)

| Acción | admin | teacher | student |
|--------|-------|---------|---------|
| Crear curso | ✓ | ✓ | ✗ |
| Editar curso | ✓ | ✓ (solo el suyo — pendiente implementar) | ✗ |
| Eliminar curso | ✓ | ✗ | ✗ |
| Ver cursos | ✓ | ✓ | ✓ |
| Inscribirse | ✗ | ✗ | ✓ |
| Ver alumnos del curso | ✓ | ✓ | ✗ |

---

## Autenticación

- JWT con `python-jose`, algoritmo HS256
- `access_token`: expira en 30 minutos
- `refresh_token`: expira en 7 días (generado, **endpoint de refresh no implementado aún**)
- Header: `Authorization: Bearer <token>`
- Dependencia reutilizable: `get_current_user` en `app/core/database.py`

---

## Convenciones de código

- Todas las funciones de DB son `async`
- IDs son UUID v4 generados por la DB (no por la app)
- Timestamps: `created_at` y `updated_at` via `TimestampMixin` en `app/models/base.py`
- Errores se manejan con excepciones custom en `app/core/exceptions.py`
- Las respuestas siempre usan `APIResponse[T]` de `app/schemas/base.py`
- Nombres de variables, mensajes y comentarios: **español**
- Nombres de funciones, clases y archivos: **inglés** (convención Python)

---

## Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última
alembic downgrade -1
```

Migraciones existentes (en orden):
1. `e8e438695d6f` — tabla users
2. `235b91aebee2` — tablas courses y modules
3. `8c328da1017a` — tabla enrollments
4. `50a5b153ae46` — campos de nombre en users
5. `b85a2ebd5164` — split full_name en campos separados

---

## Deuda técnica conocida

Ordenada por prioridad:

1. **Tests** — directorio `tests/` vacío. Falta `conftest.py`, fixtures async, y tests de integración
2. **Endpoint `/auth/refresh`** — el refresh_token se genera pero no hay endpoint para usarlo
3. **CORS** — `allow_origins=["*"]` en producción debe restringirse
4. **Paginación** — `GET /courses` sin paginación
5. **Progress endpoint** — no hay endpoint para actualizar `enrollment.progress`
6. **Autorización de curso por owner** — teachers pueden editar cualquier curso, no solo el suyo
7. **Redis sin uso** — está en docker-compose pero el código no lo usa
8. **Contenido/Lecciones** — los módulos no tienen lecciones (la funcionalidad core del LMS)

---

## Entorno local

```bash
# Levantar DB y Redis
docker-compose up -d

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
alembic upgrade head

# Iniciar servidor en desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Documentación interactiva disponible en:
# http://localhost:8000/docs
```

Variables de entorno necesarias (`.env`):
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/opnlms1
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## Estructura de archivos clave

```
app/
├── main.py               # Punto de entrada FastAPI
├── api/
│   ├── auth.py           # Rutas de autenticación
│   ├── course.py         # Rutas de cursos y módulos
│   └── enrollments.py    # Rutas de inscripciones
├── services/
│   ├── auth.py
│   ├── course.py
│   └── enrollment.py
├── repositories/
│   ├── user.py
│   ├── course.py
│   └── enrollment.py
├── models/
│   ├── base.py           # Base + TimestampMixin
│   ├── user.py
│   ├── course.py
│   └── enrollment.py
├── schemas/
│   ├── base.py           # APIResponse[T] genérico
│   ├── user.py
│   ├── course.py
│   └── enrollment.py
└── core/
    ├── config.py         # Settings con pydantic-settings
    ├── database.py       # Session async + get_current_user
    ├── security.py       # JWT + hashing
    └── exceptions.py     # Excepciones custom
alembic/
├── env.py
└── versions/
docker-compose.yml
requirements.txt
runtime.txt               # Python 3.12.13 para Render
```
