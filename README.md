# OpenLMS

Sistema de gestión de aprendizaje (LMS) construido con FastAPI y SQLite.

**URL de producción:** https://opnlms.onrender.com

---

## Cómo registrarse o iniciar sesión

### Documentación interactiva (Swagger)

La forma más sencilla de probar la plataforma es desde el navegador:

👉 **https://opnlms.onrender.com/docs**

Desde ahí puedes ejecutar cualquier endpoint directamente, sin necesidad de herramientas externas.

---

### Registrar un usuario nuevo

**`POST /api/v1/auth/register`**

```bash
curl -X POST https://opnlms.onrender.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu@email.com",
    "first_name": "Nombre",
    "middle_name": "Segundo nombre",
    "last_name": "Apellido",
    "second_last_name": "Segundo apellido",
    "password": "TuPassword123",
    "role": "student"
  }'
```

Roles disponibles: `student`, `teacher`, `admin`

Los campos `middle_name` y `second_last_name` son opcionales.

La respuesta incluye un `access_token` (válido 30 min) y un `refresh_token` (válido 7 días).

---

### Iniciar sesión

**`POST /api/v1/auth/login`**

```bash
curl -X POST https://opnlms.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu@email.com",
    "password": "TuPassword123"
  }'
```

---

### Ver tu perfil (requiere token)

**`GET /api/v1/auth/me`**

```bash
curl https://opnlms.onrender.com/api/v1/auth/me \
  -H "Authorization: Bearer <tu_access_token>"
```

---

## Usar el token en Swagger

1. Abre **https://opnlms.onrender.com/docs**
2. Ejecuta `/auth/register` o `/auth/login`
3. Copia el `access_token` de la respuesta
4. Haz clic en el botón **Authorize** (candado 🔒) arriba a la derecha
5. Pega el token en el campo `Value` con el formato: `Bearer <token>`
6. Haz clic en **Authorize** — ya puedes usar todos los endpoints protegidos

---

## Endpoints disponibles

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| GET | `/api/v1/auth/me` | Ver perfil propio | Sí |
| GET | `/api/v1/courses` | Listar cursos | Sí |
| POST | `/api/v1/courses` | Crear curso | Sí (admin/teacher) |
| GET | `/api/v1/courses/{id}` | Ver curso | Sí |
| PUT | `/api/v1/courses/{id}` | Editar curso | Sí (admin/teacher) |
| DELETE | `/api/v1/courses/{id}` | Eliminar curso | Sí (admin) |
| POST | `/api/v1/courses/{id}/modules` | Agregar módulo | Sí (admin/teacher) |
| GET | `/api/v1/courses/{id}/modules` | Ver módulos | Sí |
| POST | `/api/v1/enrollments/{course_id}` | Inscribirse | Sí (student) |
| DELETE | `/api/v1/enrollments/{course_id}` | Cancelar inscripción | Sí (student) |
| GET | `/api/v1/enrollments/my-courses` | Mis cursos | Sí (student) |
| GET | `/api/v1/enrollments/{course_id}/students` | Ver alumnos | Sí (admin/teacher) |
| GET | `/health` | Estado del servidor | No |
| GET | `/health/db` | Estado de la base de datos | No |

---

## Stack tecnológico

- **Framework:** FastAPI
- **Base de datos:** SQLite (producción en Render) / PostgreSQL (local con Docker)
- **Auth:** JWT — access token 30 min, refresh token 7 días
- **Python:** 3.12.13
- **Deploy:** Render.com — rama `develop`
