# Very bad script
# Test done with Python 3.11.3 on windows 11
import pathlib

from ruamel.yaml import YAML
from collections import OrderedDict

import uuid


yaml = YAML()
yaml.preserve_quotes = True
yaml.explicit_start = False
yaml.preserve_quotes =True
yaml.width = 2000
yaml.indent(mapping=4, sequence=4, offset=4)

def get_fhash(data) -> str:
    product = data["product"] if "product" in data else "none"
    category = data["category"] if "category" in data else "none"
    service = data["service"] if "service" in data else "none"
    fhash = f"{product}_{category}_{service}" 
    return fhash

def update_logsources(data,path):
    logsources = []
    for uuid_key in data:
        fhash = get_fhash(data[uuid_key])
        logsources.append(fhash)

    rules_list = [yml for yml in pathlib.Path(path).glob('**/*.yml')]
    for rule in rules_list:
        with rule.open('r',encoding='UTF-8') as file:
            sigma = yaml.load(file)
            product = sigma["logsource"]["product"] if "product" in sigma["logsource"] else "none"
            category = sigma["logsource"]["category"] if "category" in sigma["logsource"] else "none"
            service = sigma["logsource"]["service"] if "service" in sigma["logsource"] else "none"
            fhash = f"{product}_{category}_{service}"
            if fhash in logsources:
                pass
            else:
                new_uuid4 = str(uuid.uuid4())
                logsources.append(fhash)
                print(f"New {fhash} with uuid {new_uuid4}")
                data[new_uuid4] = {}
                data[new_uuid4]['product'] = None if product == "Nome" else product
                data[new_uuid4]['category'] = None if category == "Nome" else category
                data[new_uuid4]['service'] = None if service == "Nome" else service

def update_boolean_questions(data,default_ask,logsources):
    logsources_done = []
    for uuid_key in data:
        for uuid_logsource in data[uuid_key]['logsource']:
            logsources_done.append(uuid_logsource)

    for uuid_key in logsources:
        if uuid_key in logsources_done:
            pass
        else:
            new_uuid4 = str(uuid.uuid4())
            fhash = get_fhash(logsources[uuid_key])
            data[new_uuid4] = {}
            data[new_uuid4]['information'] = fhash
            data[new_uuid4]['ask'] = default_ask
            data[new_uuid4]['logsource'] = [uuid_key]
            logsources_done.append(uuid_key)
            print(f"Missing question for {fhash} add with uuid {new_uuid4}")

def get_number_default_question(data,default_ask)->int:
    int_q = 0
    for uuid_key in data:
        if data[uuid_key]['ask'] == default_ask :
            int_q += 1
    return int_q
        

print("Do not use unless you realy want it")
print("Open logsource.yml")
with open('logsource.yml',encoding='UTF-8') as file:
    yaml_database = yaml.load(file)

update_logsources(yaml_database["logsources"],'../../sigma/rules')
update_logsources(yaml_database["logsources"],'../../sigma/rules-emerging-threats')
update_logsources(yaml_database["logsources"],'../../sigma/rules-threat-hunting')

update_boolean_questions(yaml_database['questions'],"Missing information to ask",yaml_database["logsources"])

print("Save logsource.yml with no backup :)")
with open('logsource.yml','w',encoding='UTF-8',newline='') as file_out:
    yaml.dump(yaml_database,file_out)

print(f"You have {len(yaml_database['logsources'])} Logsources information")
print(f"You have {len(yaml_database['questions'])} boolean logsource questions")

print("-----------------------")

to_work = get_number_default_question(yaml_database['questions'],"Missing information to ask")
if to_work == 0 :
    print(f"It is a great day , there is no question with the default text")
else:
    print(f"You have {to_work} question(s) with the default text")