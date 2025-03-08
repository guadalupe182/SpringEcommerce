import csv
import xml.etree.ElementTree as ET

def csv_to_txt(csv_file_path, txt_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(txt_file_path, 'w') as txtfile:
            for row in reader:
                txtfile.write(f"{row['key']}: {row['summary']}\n")

def csv_to_xml(csv_file_path, xml_file_path):
    csv_data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_data.append(row)

    root = ET.Element("Tasks")
    for row in csv_data:
        task = ET.SubElement(root, "Task")
        for key, value in row.items():
            element = ET.SubElement(task, key)
            element.text = value

    tree = ET.ElementTree(root)
    tree.write(xml_file_path)

if __name__ == "__main__":
    csv_file_path = "tasks.csv"  # Cambia esto al nombre de tu archivo CSV
    txt_file_path = "tasks.txt"
    xml_file_path = "tasks.xml"

    # Exportar a TXT
    csv_to_txt(csv_file_path, txt_file_path)
    print(f"Archivo TXT guardado en {txt_file_path}")

    # Exportar a XML
    csv_to_xml(csv_file_path, xml_file_path)
    print(f"Archivo XML guardado en {xml_file_path}")
