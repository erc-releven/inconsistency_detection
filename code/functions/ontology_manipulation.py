import xml.etree.ElementTree as ET

def create_rule_xml(head_relation,head_actors,list_of_relations,list_of_actors):
    
    # Create root element
    root = ET.Element("swrl:Imp")

    #BULID right sight of the implication 
    head = ET.SubElement(root, "swrl:head")
    AtomList = ET.SubElement(head,"swrl:AtomList")
    ET.SubElement(AtomList,"rdf:rest",xmlns_rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil")
    first = ET.SubElement(AtomList,"rdf:first")
    IndividualPropertyAtom = ET.SubElement(first,"swrl:IndividualPropertyAtom")
    ET.SubElement(IndividualPropertyAtom,"swrl:propertyPredicate",{"rdf:resource": head_relation})
    ET.SubElement(IndividualPropertyAtom,"swrl:argument1",{"rdf:resource": f"urn:swrl#{head_actors[0]}"})
    ET.SubElement(IndividualPropertyAtom,"swrl:argument2",{"rdf:resource": f"urn:swrl#{head_actors[1]}"})


    # Left side
    body = ET.SubElement(root, "swrl:body")
    AtomList = ET.SubElement(body,"swrl:AtomList")
    # First Argumnet on the left side 
    first = ET.SubElement(AtomList,"rdf:first")
    IndividualPropertyAtom = ET.SubElement(first,"swrl:IndividualPropertyAtom")
    ET.SubElement(IndividualPropertyAtom,"swrl:propertyPredicate",{"rdf:resource": list_of_relations[0]})
    ET.SubElement(IndividualPropertyAtom,"swrl:argument1",{"rdf:resource": f"urn:swrl#{list_of_actors[0][0]}"})
    ET.SubElement(IndividualPropertyAtom,"swrl:argument2",{"rdf:resource": f"urn:swrl#{list_of_actors[0][1]}"})

    # Next arguments on the left side 
    for i in range(1,len(list_of_actors)):
        rest = ET.SubElement(AtomList,"rdf:rest")
        InsideAtomList = ET.SubElement(rest,"swrl:AtomList")
        ET.SubElement(InsideAtomList,"rdf:rest",xmlns_rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#nil")
        insdiefirst = ET.SubElement(InsideAtomList,"rdf:first")
        IndividualPropertyAtom = ET.SubElement(insdiefirst,"swrl:IndividualPropertyAtom")
        ET.SubElement(IndividualPropertyAtom,"swrl:propertyPredicate",{"rdf:resource": list_of_relations[i]})
        ET.SubElement(IndividualPropertyAtom,"swrl:argument1",{"rdf:resource": f"urn:swrl#{list_of_actors[i][0]}"})
        ET.SubElement(IndividualPropertyAtom,"swrl:argument2",{"rdf:resource": f"urn:swrl#{list_of_actors[i][1]}"})

    # Convert to a string and print
    xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
    return xml_string

def modify_ontology_file(ontology_path,new_rule):
    remove_last_n_lines(ontology_path,1)
    append_to_file(ontology_path,new_rule)
    append_to_file(ontology_path,"</rdf:RDF>")



def remove_last_n_lines(file_path, n):
    try:
        # Open file with utf-8 encoding to handle non-ASCII characters
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Remove the last 'n' lines
        new_lines = lines[:-n]  # Slicing removes the last n lines
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
    
    except UnicodeDecodeError as e:
        print(f"Error reading the file: {e}")
        # You can try using 'ISO-8859-1' if utf-8 doesn't work
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()
        
        # Remove the last 'n' lines
        new_lines = lines[:-n]  # Slicing removes the last n lines
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='ISO-8859-1') as file:
            file.writelines(new_lines)

def append_to_file(file_path, text_to_append):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(text_to_append + '\n') 