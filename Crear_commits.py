import csv
import os
from git import Repo

# Ruta al repositorio Git
repo_path = os.getcwd()  # Cambia esto si tu repositorio está en otra ruta
repo = Repo(repo_path)

# Ruta al archivo CSV
csv_file = "backlog_actualizado.csv"  # Cambia esto al nombre de tu archivo CSV

# Leer el archivo CSV
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        issue_key = row["Issue Key"]
        summary = row["Summary"]

        # Verificar si ya existe un commit con el mismo Issue Key
        commit_exists = False
        for commit in repo.iter_commits():
            if issue_key in commit.message:
                commit_exists = True
                print(f"El commit para {issue_key} ya existe: {commit.message.strip()}")
                break

        # Si no existe, crear el commit
        if not commit_exists:
            # Crear un archivo temporal para el commit
            file_name = f"{issue_key}.txt"
            with open(file_name, "w") as f:
                f.write(summary)

            # Agregar el archivo al stage
            repo.index.add([file_name])

            # Crear el commit
            commit_message = f"{issue_key} {summary}"
            repo.index.commit(commit_message)
            print(f"Commit creado: {commit_message}")

            # Eliminar el archivo temporal (opcional)
            os.remove(file_name)
        else:
            print(f"Saltando {issue_key}: ya existe un commit.")

print("¡Proceso completado!")