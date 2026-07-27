#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para 'Mis Videos'."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Activaste tu entorno virtual "
            "e instalaste los paquetes de requirements.txt?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
