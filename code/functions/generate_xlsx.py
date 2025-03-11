import pandas as pd

def read_data(path_relation: str, path_gender: str, path_map: str):
    """
    Reads data from CSV files and returns them as pandas DataFrames.
    
    Parameters:
        path_relation (str): Path to the relation data CSV file.
        path_gender (str): Path to the gender data CSV file.
        path_map (str): Path to the mapping data CSV file.
    
    Returns:
        tuple: relation_data, gender_data, map_data as pandas DataFrames.
    """
    relation_data = pd.read_csv(path_relation)
    gender_data = pd.read_csv(path_gender)
    map_data = pd.read_csv(path_map,sep=';')
    return relation_data, gender_data, map_data

def modify_data(relation_data, gender_data, map_data):
    """
    Cleans and modifies the relation and gender data by selecting relevant columns and removing duplicates.
    
    Parameters:
        relation_data (DataFrame): DataFrame containing relation data.
        gender_data (DataFrame): DataFrame containing gender data.
        map_data (DataFrame): DataFrame containing mapping data.
    
    Returns:
        tuple: Modified relation_data, gender_data, and map_data DataFrames.
    """
    relation_data = relation_data[['pnode', 'person', 'knode', 'kinsman', 'kt', 'kinship']]
    relation_data.drop_duplicates()
    gender_data = gender_data[['pnode', 'person', 'gender']]
    gender_data.drop_duplicates()
    
    return relation_data, gender_data, map_data

def merge_relation_map(relation_data, map_data):
    """
    Merges relation data with mapping data to create an ontology kinship mapping.
    
    Parameters:
        relation_data (DataFrame): DataFrame containing relation data.
        map_data (DataFrame): DataFrame containing mapping data.
    
    Returns:
        DataFrame: Updated relation_data with ontology_kinship mapping.
    """
    mapping_dict = dict(zip(map_data['Set 1'], map_data['Set 2']))
    relation_data['ontology_kinship'] = relation_data['kinship'].map(mapping_dict)
    return relation_data

def merge_data_and_generate_xlsx(relation_data, gender_data, out_path):
    """
    Merges relation data with gender data, processes it, and saves the final result as an Excel file.
    
    Parameters:
        relation_data (DataFrame): DataFrame containing relation data.
        gender_data (DataFrame): DataFrame containing gender data.
        out_path (str): Output file path for the Excel file.
    """
    merged_data = pd.merge(relation_data, gender_data, on="pnode", how="left")
    print(merged_data.columns)
    cut_merged_data = merged_data[['pnode', 'person_x', 'knode', 'kinsman', 'kinship', 'ontology_kinship','gender']]
    cut_merged_data = cut_merged_data.rename(columns={'gender': 'person_gender'})
    
    full_merged_data = pd.merge(cut_merged_data, gender_data, left_on="knode", right_on='pnode', how="left")
    full_merged_data = full_merged_data.rename(columns={'gender': 'kinsman_gender'})
    
    # Remove unwanted characters
    full_merged_data['person_x'] = full_merged_data['person_x'].str.replace('"', '', regex=True)
    full_merged_data['kinsman'] = full_merged_data['kinsman'].str.replace('"', '', regex=True)
    
    final_data = full_merged_data[['person_x', 'kinsman', 'person_gender', 'kinsman_gender', "ontology_kinship"]]
    final_data.drop_duplicates(inplace=True)
    final_data.dropna(inplace=True)
    
    final_data.to_excel(out_path, index=False)
