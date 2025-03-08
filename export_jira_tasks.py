import json
import xml.etree.ElementTree as ET

def export_to_txt(tasks, file_path):
    with open(file_path, 'w') as file:
        for task in tasks:
            file.write(f"{task['key']}: {task['summary']}\n")

def export_to_xml(tasks, file_path):
    root = ET.Element("Tasks")
    for task in tasks:
        task_element = ET.SubElement(root, "Task")
        key_element = ET.SubElement(task_element, "Key")
        key_element.text = task['key']
        summary_element = ET.SubElement(task_element, "Summary")
        summary_element.text = task['summary']

    tree = ET.ElementTree(root)
    tree.write(file_path)

if __name__ == "__main__":
    # Simula la obtención de tareas desde la extensión de Jira en VS Code
    tasks = [
        {"key": "GV-1", "summary": "Implement feature X"},
        {"key": "GV-2", "summary": "Fix bug Y"},
        {"key": "GV-3", "summary": "Update documentation"}
    ]

    # Exportar a TXT
    txt_file_path = "tasks.txt"
    export_to_txt(tasks, txt_file_path)
    print(f"Archivo TXT guardado en {txt_file_path}")

    # Exportar a XML
    xml_file_path = "tasks.xml"
    export_to_xml(tasks, xml_file_path)
    print(f"Archivo XML guardado en {xml_file_path}")
