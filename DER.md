# Diagrama Entidad-Relación — VetCare

## Tablas y Relaciones

```
┌─────────────────────────────┐
│          USUARIO            │
├─────────────────────────────┤
│ PK id          INTEGER      │
│    nombre      VARCHAR(100) │
│    apellido    VARCHAR(100) │
│    dni         VARCHAR(20)  │── único
│    telefono    VARCHAR(20)  │
│    correo      VARCHAR(150) │── único
│    password_hash VARCHAR(200)
│    rol         VARCHAR(20)  │── dueño | veterinario | admin
│    activo      BOOLEAN      │
└──────────┬──────────────────┘
           │
    ┌──────┼──────────────────────────────┐
    │      │                              │
    ▼      ▼                              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   MASCOTA    │  │    TURNO     │  │ DIAGNOSTICO  │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ PK id        │  │ PK id        │  │ PK id        │
│ FK dueno_id──┼──┼──FK vet_id   │  │FK mascota_id │
│ nombre       │  │ FK dueno_id  │  │FK vet_id     │
│ especie      │  │ FK mascota_id│  │ fecha        │
│ raza         │  │ fecha        │  │ descripcion  │
│ edad         │  │ hora         │  └──────┬───────┘
│ peso         │  │ estado       │         │
└──────────────┘  └──────────────┘         │
                                           │
                                    ┌──────┴──────┐
                                    │ TRATAMIENTO │
                                    ├─────────────┤
                                    │ PK id       │
                                    │FK diag_id   │
                                    │ descripcion │
                                    │ duracion    │
                                    └─────────────┘
                                           │
                                    ┌──────┴──────┐
                                    │ MEDICAMENTO │
                                    ├─────────────┤
                                    │ PK id       │
                                    │FK diag_id   │
                                    │ nombre      │
                                    │ dosis       │
                                    │ frecuencia  │
                                    └─────────────┘

┌─────────────────────────────┐
│         PRODUCTO            │
├─────────────────────────────┤
│ PK id          INTEGER      │
│    nombre      VARCHAR(150) │
│    precio      FLOAT        │
│    stock       INTEGER      │
│    categoria   VARCHAR(80)  │
│    activo      BOOLEAN      │
└──────────┬──────────────────┘
           │
           │
     ┌─────┴──────────────────┐
     │                        │
     ▼                        ▼
┌──────────────────┐  ┌──────────────────┐
│   CARRITO_ITEM   │  │   COMPRA_ITEM    │
├──────────────────┤  ├──────────────────┤
│ PK id            │  │ PK id            │
│ FK usuario_id    │  │ FK compra_id     │
│ FK producto_id   │  │ FK producto_id   │
│ cantidad         │  │ cantidad         │
└──────────────────┘  │ precio_unitario  │
                      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │     COMPRA       │
                      ├──────────────────┤
                      │ PK id            │
                      │ FK usuario_id    │
                      │ fecha            │
                      │ total            │
                      └──────────────────┘
```

## Relaciones (Resumen)

| Tabla A | Relación | Tabla B | Detalle |
|---------|----------|---------|---------|
| USUARIO | 1 → N | MASCOTA | Un dueño tiene muchas mascotas |
| USUARIO | 1 → N | TURNO | Un veterinario atiende muchos turnos |
| USUARIO | 1 → N | TURNO | Un dueño saca muchos turnos |
| USUARIO | 1 → N | DIAGNOSTICO | Un veterinario hace muchos diagnósticos |
| USUARIO | 1 → N | CARRITO_ITEM | Un usuario tiene items en su carrito |
| USUARIO | 1 → N | COMPRA | Un usuario hace muchas compras |
| MASCOTA | 1 → N | TURNO | Una mascota agenda muchos turnos |
| MASCOTA | 1 → N | DIAGNOSTICO | Una mascota tiene muchos diagnósticos |
| DIAGNOSTICO | 1 → N | TRATAMIENTO | Un diagnóstico incluye tratamientos |
| DIAGNOSTICO | 1 → N | MEDICAMENTO | Un diagnóstico prescribe medicamentos |
| PRODUCTO | 1 → N | CARRITO_ITEM | Un producto aparece en muchos carritos |
| PRODUCTO | 1 → N | COMPRA_ITEM | Un producto aparece en muchas compras |
| COMPRA | 1 → N | COMPRA_ITEM | Una compra tiene varios items |
