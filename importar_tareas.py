from jira import JIRA
import csv
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configura la conexión a Jira
try:
    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )
    print("Conexión a Jira establecida correctamente.")
except Exception as e:
    print(f"Error al conectar con Jira: {e}")
    exit()

# Lee el archivo CSV
csv_file = "backlog_actualizado.csv"  # Asegúrate de que el archivo CSV esté en la misma carpeta que el script
try:
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Crea la tarea
                issue_dict = {
                    "project": {"key": row["Project Key"]},
                    "summary": row["Summary"],
                    "description": row["Description"],
                    "issuetype": {"name": row["Issue Type"]},
                }
                issue = jira.create_issue(fields=issue_dict)
                print(f"Tarea creada: {issue.key} - {issue.fields.summary}")
            except Exception as e:
                print(f"Error al crear la tarea {row.get('Issue Key', 'N/A')}: {e}")
except FileNotFoundError:
    print(f"Error: El archivo {csv_file} no se encontró.")
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")

print("¡Proceso completado!")