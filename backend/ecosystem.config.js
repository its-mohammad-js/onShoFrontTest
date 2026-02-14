module.exports = {
  apps : [{
    name: "mahoverse",
    script: ".venv/bin/gunicorn",
    args: "mahoverse.wsgi:application -b 127.0.0.1:8000 --workers 3",
    cwd: "/home/mahoverse/backend",
    env: {
      DJANGO_SETTINGS_MODULE: "mahoverse.settings",
      # put other env vars here (use secure methods in prod)
    }
  }]
}