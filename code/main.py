from functions.generate_xlsx import read_data, modify_data, merge_relation_map, merge_data_and_generate_xlsx
from functions.network import generate_graph , save_subgraphs
from functions.ontology_manipulation import modify_ontology_file,create_rule_xml
# PATHS TO SETUP 
GENDER_PATH = '.\\code\\data\\gender_query.csv'
RELATION_PATH = '.\\code\\data\\query-result.csv'
RELATION_MAP = '.\\code\\data\\relation_map.csv'
OUT_PATH = '.\\code\\out\\final_data.xlsx'
OUT = ".\\code\\out"

# STEP 1 format data and save to xmls 
relation_data , gender_data ,map_data = read_data(RELATION_PATH,GENDER_PATH,RELATION_MAP)
relation_data, gender_data ,map_data = modify_data(relation_data,gender_data,map_data)
relation_data = merge_relation_map(relation_data,map_data)
merge_data_and_generate_xlsx(relation_data,gender_data,OUT_PATH)
# STEP 2 split data in to subsets 
G,data = generate_graph(OUT_PATH)
save_subgraphs(G,[0,[1,100],[100,-999]],data,OUT)

# STEP 3 needs to be done in Protege, check README (STEP 4)

# ADDITIONAL STEP 4 extend ontology with required data
# This is already performed on an existing ontology
# this can be used to  extend ontology by rules you want to include 

if False: # change to run STEP 4 
    ONTOLOGY_PATH = "TODO"
    xml_string = create_rule_xml(
        head_relation="#102",
        head_actors=["x","y"],
        list_of_relations=["#1.3.2","#5.2"],
        list_of_actors=[["x","y"],["x","y"]]
    )
   # <!-- if Father(x,y) and Brother(x,y) -> Inconsistency  -->
    modify_ontology_file(ONTOLOGY_PATH,xml_string)
