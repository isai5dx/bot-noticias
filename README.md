# 📰 Bot de noticias de computación en México

Bot que busca automáticamente las noticias más recientes de computación y tecnología en México, y las envía por correo electrónico cada mañana. Corre completamente automatizado con GitHub Actions — no necesita ningún servidor prendido 24/7.

## Cómo funciona

1. Un workflow de **GitHub Actions** se activa todos los días a las 7:00 AM (hora Ciudad de México) mediante un `cron`.
2. Construye una imagen de **Docker** con el bot empaquetado.
3. El contenedor busca noticias recientes en un feed **RSS de Google News**, filtrado por tema y país.
4. Arma un correo en formato **HTML** con las noticias encontradas.
5. Envía el correo por **Gmail SMTP**, usando un *App Password* en vez de la contraseña real.

## Stack

- Python 3.11
- [`feedparser`](https://pypi.org/project/feedparser/) — lectura del feed RSS
- `smtplib` (librería estándar) — envío de correo
- Docker — empaquetado
- GitHub Actions — automatización (CI/CD)

## Estructura del proyecto

```
bot-noticias/
├── bot.py                        # Lógica principal: buscar noticias, armar y enviar el correo
├── requirements.txt               # Dependencias de Python
├── Dockerfile                     # Empaqueta el bot en una imagen
├── .github/
│   └── workflows/
│       └── noticias.yml           # Workflow de GitHub Actions (cron + build + run)
└── README.md
```

## Configuración necesaria

Este proyecto necesita tres *secrets* configurados en **Settings → Secrets and variables → Actions** del repositorio:

| Secret | Descripción |
|---|---|
| `EMAIL_FROM` | Correo de Gmail que envía las noticias |
| `EMAIL_APP_PASSWORD` | [App Password](https://myaccount.google.com/apppasswords) de 16 caracteres (no la contraseña normal de Gmail) |
| `EMAIL_TO` | Correo que recibe las noticias (puede ser el mismo que `EMAIL_FROM`) |

## Correr localmente

```bash
pip install -r requirements.txt
export EMAIL_FROM="tu@gmail.com"
export EMAIL_APP_PASSWORD="xxxxxxxxxxxxxxxx"
export EMAIL_TO="tu@gmail.com"
python bot.py
```

## Correr con Docker localmente

```bash
docker build -t bot-noticias .
docker run \
  -e EMAIL_FROM="tu@gmail.com" \
  -e EMAIL_APP_PASSWORD="xxxxxxxxxxxxxxxx" \
  -e EMAIL_TO="tu@gmail.com" \
  bot-noticias
```

## Probar el workflow manualmente

En la pestaña **Actions** del repositorio, selecciona el workflow **"Enviar noticias diarias"** y usa el botón **"Run workflow"** — no hace falta esperar hasta el horario programado.

## Personalización

- **Cambiar el tema de búsqueda:** edita la variable `QUERY` en `bot.py`.
- **Cambiar el horario de envío:** edita la línea `cron` en `.github/workflows/noticias.yml`. El formato es `minuto hora * * *` en UTC (México está en UTC-6, sin horario de verano).
- **Cambiar cuántas noticias se envían:** edita el `[:10]` en la función `obtener_noticias()` de `bot.py`.

## Notas

- El workflow usa `workflow_dispatch`, lo que permite dispararlo manualmente para pruebas sin esperar al cron.
- Los secrets nunca quedan expuestos en el código ni en los logs — se inyectan como variables de entorno solo durante cada ejecución.
