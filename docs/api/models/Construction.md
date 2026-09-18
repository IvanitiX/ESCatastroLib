# Construction

**Módulo:** `models`

Clase base para construcciones catastrales (INSPIRE BU).
**Atributos:**

- `id` — Identificador único de la construcción.
- `geometria` — Geometría de la construcción, o None si no está disponible.
- `condition` — Estado de la construcción (ej. "Functional", "Ruins").


## Atributos

| Atributo | Tipo | Default |
|----------|------|---------|
| `id` | `str` | - |
| `geometria` | `Geometria | None` | `None` |
| `condition` | `str | None` | `None` |
