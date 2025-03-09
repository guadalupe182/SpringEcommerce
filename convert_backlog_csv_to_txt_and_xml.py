import csv
import os
import logging
from jira import JIRA, JIRAError
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de logging
logging.basicConfig(filename='jira_updates.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mapeo de palabras clave a tipos de issues
ISSUE_TYPE_MAPPING = {
    'epic': 'Epic',
    'story': 'Story',
    'task': 'Task',
    'bug': 'Bug'
}

def get_issue_type(summary):
    """
    Determina el tipo de issue basado en palabras clave en el resumen.
    """
    summary_lower = summary.lower()
    for keyword, issue_type in ISSUE_TYPE_MAPPING.items():
        if keyword in summary_lower:
            return issue_type
    return 'Task'  # Valor por defecto

def txt_to_csv(txt_file_path, csv_file_path):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as txtfile:
            lines = txtfile.readlines()

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Definir los encabezados del CSV
            fieldnames = ['Issue Key', 'Summary', 'Description', 'Issue Type', 'Project Key']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for line in lines:
                if ':' in line:
                    key, summary = line.split(':', 1)
                    key = key.strip()
                    summary = summary.strip()

                    # Determinar el tipo de issue
                    issue_type = get_issue_type(summary)

                    # Escribir la fila en el CSV
                    writer.writerow({
                        'Issue Key': key,
                        'Summary': summary,
                        'Description': '',  # Descripción vacía por defecto
                        'Issue Type': issue_type,  # Tipo de issue determinado
                        'Project Key': 'GV'  # Clave del proyecto
                    })
        logging.info(f"Archivo CSV creado en {csv_file_path}")
    except Exception as e:
        logging.error(f"Error al convertir TXT a CSV: {e}")

def update_jira_from_csv(csv_file_path, jira_options, jira_auth):
    try:
        # Conectar a Jira
        jira = JIRA(options=jira_options, basic_auth=jira_auth)
        logging.info("Conexión a Jira establecida correctamente.")
    except JIRAError as e:
        logging.error(f"Error al conectar a Jira: {e}")
        return

    try:
        # Leer el archivo CSV
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                issue_key = row['Issue Key']
                new_summary = row['Summary']
                new_description = row.get('Description', '')  # Campo opcional

                # Validar la clave de incidencia
                if not issue_key.startswith('GV-'):
                    logging.warning(f"Clave de incidencia inválida: {issue_key}")
                    continue

                try:
                    # Buscar la tarea en Jira
                    issue = jira.issue(issue_key)

                    # Actualizar el resumen y la descripción
                    issue.update(summary=new_summary, description=new_description)
                    logging.info(f"Tarea {issue_key} actualizada: {new_summary}")
                except JIRAError as e:
                    logging.error(f"Error al actualizar la tarea {issue_key}: {e}")
    except Exception as e:
        logging.error(f"Error al leer el archivo CSV: {e}")

if __name__ == "__main__":
    # Rutas de los archivos
    txt_file_path = "/home/adrian/Proyectos/spring-ecommerce/backlog_actualizado.txt"
    csv_file_path = "/home/adrian/Proyectos/spring-ecommerce/backlog_actualizado.csv"

    # Configuración de Jira desde .env
    jira_options = {'server': os.getenv('JIRA_SERVER')}  # URL base de la API de Jira
    jira_auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))  # Credenciales desde .env

    # Convertir TXT a CSV
    txt_to_csv(txt_file_path, csv_file_path)

    # Actualizar tareas existentes en Jira
    update_jira_from_csv(csv_file_path, jira_options, jira_auth)