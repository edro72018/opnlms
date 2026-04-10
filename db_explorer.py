"""
Explorador de base de datos — uso: python db_explorer.py
Lee DATABASE_URL del archivo .env
"""
import asyncio
import asyncpg
import csv
import os
import re
from pathlib import Path


def cargar_env(path=".env"):
    """Lee el .env y devuelve un dict con las variables."""
    env = {}
    try:
        with open(path) as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    clave, _, valor = linea.partition("=")
                    env[clave.strip()] = valor.strip()
    except FileNotFoundError:
        print(f"No se encontró el archivo {path}")
    return env


def adaptar_url(url: str) -> str:
    """Convierte postgresql+asyncpg:// → postgresql:// para asyncpg directo."""
    return re.sub(r"^postgresql\+asyncpg://", "postgresql://", url)


async def main():
    env = cargar_env()
    database_url = env.get("DATABASE_URL") or os.getenv("DATABASE_URL")

    if not database_url:
        print("ERROR: No se encontró DATABASE_URL en .env")
        return

    url = adaptar_url(database_url)

    print("\nConectando a la base de datos...")
    try:
        conn = await asyncpg.connect(url)
    except Exception as e:
        print(f"ERROR al conectar: {e}")
        return

    # Nombre de la DB
    db_name = await conn.fetchval("SELECT current_database();")
    print(f"Base de datos: {db_name}\n")

    while True:
        # Listar tablas
        tablas = await conn.fetch(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
        )

        if not tablas:
            print("No hay tablas en la base de datos.")
            break

        print("Tablas disponibles:")
        for i, row in enumerate(tablas, start=1):
            print(f"  {i}. {row['tablename']}")
        print("  0. Salir\n")

        opcion = input("Selecciona una tabla (número): ").strip()

        if opcion == "0":
            print("Saliendo...")
            break

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(tablas)):
            print("Opción inválida, intenta de nuevo.\n")
            continue

        tabla = tablas[int(opcion) - 1]["tablename"]
        print(f"\n--- SELECT * FROM {tabla} ---")

        filas = await conn.fetch(f'SELECT * FROM "{tabla}";')

        if not filas:
            print("(tabla vacía)\n")
            continue

        columnas = list(filas[0].keys())

        # --- Exportar CSV completo ---
        carpeta = Path("exports")
        carpeta.mkdir(exist_ok=True)
        archivo_csv = carpeta / f"{tabla}.csv"
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()
            for fila in filas:
                writer.writerow({col: str(fila[col]) for col in columnas})
        print(f"CSV guardado en: {archivo_csv}  ({len(filas)} registros totales)\n")

        # --- Imprimir primeros 10 en terminal ---
        vista = filas[:10]
        anchos = [max(len(col), max(len(str(fila[col])) for fila in vista)) for col in columnas]
        separador = "-+-".join("-" * a for a in anchos)
        encabezado = " | ".join(col.ljust(anchos[i]) for i, col in enumerate(columnas))
        print(encabezado)
        print(separador)
        for fila in vista:
            print(" | ".join(str(fila[col]).ljust(anchos[i]) for i, col in enumerate(columnas)))

        if len(filas) > 10:
            print(f"\n  ... y {len(filas) - 10} registros más (ver CSV para el total)")

        print()

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
