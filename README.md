# Attendance & Payroll Automation  
### Python-based Attendance Processing System (Biometric / ZKTime)

Sistema de automatización para procesamiento de asistencia y generación de reportes de nómina a partir de registros biométricos.

---

## 📌 Contexto Empresarial

En el entorno productivo, el proceso de consolidación de asistencia se realizaba manualmente, requiriendo aproximadamente **5 horas por corte de nómina**.

La automatización:

- Reduce el tiempo de procesamiento a **menos de 1 minuto**
- Elimina errores humanos por digitación
- Genera reportes estructurados y legibles
- Se ejecuta automáticamente los días **15 y 30 de cada mes**

---

## 🚀 Funcionalidades

- Lectura y normalización de eventos (Entrada / Salida / Descanso)
- Emparejamiento automático de jornadas
- Cálculo de:
  - Horas totales
  - Horas diurnas
  - Horas nocturnas
  - Horas dominicales
  - Horas extra
- Generación automática de Excel:
  - Resumen por empleado
  - Detalle diario

---

## 🏗 Arquitectura

El proyecto está estructurado de forma modular:

src/app/

├── main.py → Orquestador DEMO / PROD

├── payroll.py → Lógica de cálculo de horas

├── events.py → Normalización de eventos

├── zkteco_prod.py → Integración biométrico (PROD)

├── zktime_db.py → Lectura base de datos ZKTime (PROD)

├── timeparse.py → Parsing de fechas y horas

├── config.py → Carga de configuración por entorno



🏢 Modo PROD (Entorno Empresarial)

En producción el sistema:
Detecta el dispositivo biométrico en red
Extrae registros de asistencia
Cruza información con base de datos ZKTime
Genera reporte consolidado para el área de nómina
Copia automáticamente el archivo a carpeta compartida
La configuración productiva se gestiona mediante variables de entorno (.env) 
que no se incluyen en este repositorio por razones de seguridad.


🛠 Tecnologías Utilizadas

Python

OpenPyXL

PyZK

SQLite

Arquitectura modular

Control de versiones con Git

🎯 Impacto Técnico

Este proyecto demuestra:

Automatización de procesos empresariales

Reducción medible de tiempo operativo

Eliminación de procesos manuales críticos

Separación de entornos DEMO / PROD

Buenas prácticas de configuración segura

📎 Autor

Cristian Córdoba
Desarrollador enfocado en automatización empresarial y optimización de procesos.

GitHub: https://github.com/cordoba1991

