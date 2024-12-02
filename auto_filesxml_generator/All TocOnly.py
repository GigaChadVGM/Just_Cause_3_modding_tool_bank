# this script is free to use and edit
import os
import xml.etree.ElementTree as ET

def AutoFilesXMLAll_TocXML(folder_path: str):
    """
    This function generates one xml file @tocFiles.xml used to create an epe.
    In this file, there are all the relative paths of each files from a certain folder and also
    the relative paths of external files stored in the dropzone folder.

    :param folder_path: path of the folder for the @tocFiles.xml generation
    :return:
    """
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"The provided path '{folder_path}' is not a valid directory.")

    files_to_check = ['@tocFiles.xml', '@files.xml']
    existing_files = [file_name for file_name in files_to_check if file_name in os.listdir(folder_path)]

    if not existing_files:
        raise FileNotFoundError(
            f'Missing existing @tocFiles.xml or @files.xml, cannot proceed.'
        )

    source_file = existing_files[0]
    source_file_path = os.path.join(folder_path, source_file)

    combined_entries = []
    try:
        tree = ET.parse(source_file_path)
        root = tree.getroot()
        for elem in root.iter():
            if 'size' in elem.attrib:
                combined_entries.append((elem.attrib.get("name", ""), elem))
    except ET.ParseError:
        raise ValueError(f"Error parsing {source_file}, ensure it is a valid XML file.")

    for root_dir, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.xml'):
                relative_path = os.path.relpath(os.path.join(root_dir, file), start=folder_path)
                combined_entries.append((relative_path.replace('\\', '/'), None))

    epe_files = [file for file, offset in combined_entries if str(file).endswith('.epe')]
    if len(epe_files) > 1:
        raise FileExistsError(
            f"more than one .epe file found associated to the directory external or internal: {epe_files}.\nOnly one can exist in the directory")

    priorities = {
        ".trim": 0,
        ".ddsc": 1,
        ".hmddsc": 2,
        ".rbm": 3,
        ".lod": 4,
        ".epe": 5
    }

    def sort_key(entry):
        path, elem = entry
        for ext, prio in priorities.items():
            if path.endswith(ext):
                return 1, prio, path
        return 0, 0, path

    combined_entries = sorted(combined_entries, key=sort_key)

    root = ET.Element("files", extension='.ee')

    for path, elem in combined_entries:
        if elem is not None:
            new_elem = ET.Element(elem.tag, attrib=elem.attrib)
            new_elem.text = elem.text
            root.append(new_elem)
        else:
            file_element = ET.Element("file", name=path)
            file_element.text = path.replace('/', '\\')
            root.append(file_element)

    ET.indent(root, space="  ", level=0)
    tree = ET.ElementTree(root)
    output_path = os.path.join(folder_path, '@tocFiles.xml')
    try:
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
    except IOError as e:
        raise IOError(f"Failed to write XML file '@tocFiles.xml': {e}")


#AutoFilesXMLAll_TocXML('../Example/files_xml_test')  # Example of use
