# How to run code 

## Step 1 Download data 
### CSV 1 relation data 
Downland csv using quarry :
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX star: <https://r11.eu/ns/star/>
PREFIX sdhss: <https://r11.eu/ns/prosopography/>

select * where {
    ?pnode a crm:E21_Person ;
         rdfs:label ?person .
    ?a1 a star:E13_sdhss_P17 ;
        crm:P140_assigned_attribute_to ?kr ;
        crm:P141_assigned ?pnode ;
        crm:P14_carried_out_by ?anode ;
        ^crm:P67_refers_to ?snode .
    ?anode rdfs:label ?authority .
    ?a2 a star:E13_sdhss_P18 ;
        crm:P140_assigned_attribute_to ?kr ;
        crm:P141_assigned ?knode .
    ?knode a crm:E21_Person ;
         rdfs:label ?kinsman .
    ?a3 a star:E13_sdhss_P16 ;
        crm:P140_assigned_attribute_to ?kr ;
        crm:P141_assigned ?kt .
    ?kt a sdhss:C4 ;
        rdfs:label ?kinship .
}
```

### CSV 2 gender data 
Download csv using quarry: 
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX star: <https://r11.eu/ns/star/>

select * where {
    ?pnode a crm:E21_Person ;
        rdfs:label ?person .
    ?a1 a star:E13_crm_P41 ;
        crm:P141_assigned ?pnode ;
        crm:P140_assigned_attribute_to ?intermidiet1.
    ?a2 a star:E13_crm_P42;
        crm:P140_assigned_attribute_to ?intermidiet1;
        crm:P141_assigned ?pre_gender.
    ?pre_gender rdfs:label ?gender.
}
```


## Step 2 create virtual environment

Instal uv (https://docs.astral.sh/uv/getting-started/installation/)

Move to code directory and run. 

```
cd code
uv venv 
uv pip install -r pyproject.toml
.venv\Scripts\activate # can be different on OX/Linux
```

## Step 3 run main.py 

On top of the main file setup paths to csvs and path to output data then run. 

``` 
cd ..
<repository_path>/code/.venv/Scripts/python.exe <repository_path>/code/main.py
```


## Step 4 import data to **protege**

1. Open and load ontology form: code/exp_ontology.owl

2. In Tools select *Create axioms from Excel workbook*

3. Load created xlsx file you want to check.

4. Load rule code/data/load_data_transformation.json

5. Generate and add axioms to existing ontology 

6. Run reasoner ELK reasoner.

7. Manual remove any existing inconsistency of gender. (repped 2-5)

8. Run Hermit reasoner to find more complex inconsistency. 
    - By default ontology supports 4 different rules of this type:
        - if Father(x,y) and Brother(x,y) -> Inconsistency
        - if Sister(x,y) and Mather(x,y) -> Inconsistency 
        - if GrandMatherOf(x,y) and Mother(x,y) -> Inconsistency
        - if GrandFatherOf(x,y) and Father(x,y) -> Inconsistency
    - If you want ot add more look main.py STEP 4
