#### SETUP #### 
relation_data = "code\data\\relation_data.csv" ## CSV 1 
gender_data = 'code\\data\\gender_data.csv' ## CSV 2 

#ontology_url = 
out_data = "code\\out\\final_data.xlsx" ## output data

##############
import os 
print(os.getcwd())

import pandas as pd

gender_data_frame = pd.read_csv(gender_data)
relation_data_frame = pd.read_csv(relation_data)

# extract pnode, persnon, knode,kinsman, kt, kinship 
cuted_data = relation_data_frame[['pnode', 'person', 'knode', 'kinsman', 'kt', 'kinship']]
cuted_data = cuted_data.drop_duplicates()

mapping = pd.read_csv("code\\data\\relation_map.csv",sep=';')

# convert mapping into a dictionary 
mapping_dict = dict(zip(mapping['Set 1'], mapping['Set 2']))

# generate csv with new relations 
cuted_data['ontology_kinship']= cuted_data['kinship'].map(mapping_dict)

## get gender data 
gender_data = pd.read_csv(gender_data)

cut_gender_data = gender_data[['pnode', 'person','gender']]
cut_gender_data = cut_gender_data.drop_duplicates()


# right join with cuted data 
merged_data = pd.merge(cuted_data, cut_gender_data , on="pnode", how="left")
cut_merged_data = merged_data[['pnode', 'person_x', 'knode', 'kinsman', 'kinship', 'ontology_kinship','gender']]

# raname column 
cut_merged_data = cut_merged_data.rename(columns={'gender': 'person_gender'})

# add gender fot a kinsman 
full_merged_data = pd.merge(cut_merged_data,cut_gender_data,left_on="knode",right_on='pnode', how="left")
full_merged_data = full_merged_data.rename(columns={'gender': 'kinsman_gender'})

# remove unacepted characters
full_merged_data['person_x'] = full_merged_data['person_x'].str.replace('"', '')
full_merged_data['kinsman'] = full_merged_data['kinsman'].str.replace('"', '')

# export data 
final_data=full_merged_data[['person_x','kinsman','person_gender','kinsman_gender',"ontology_kinship"]]
final_data.drop_duplicates(inplace=True)
final_data.dropna(inplace=True)
final_data.to_excel(out_data,index=False)
