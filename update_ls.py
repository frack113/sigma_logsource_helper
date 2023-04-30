# Very bad script
# Test done with Python 3.11.3 on windows 11
import pathlib

from ruamel.yaml import YAML
from collections import OrderedDict

import uuid

class Quizz():
    def __init__(self):
        self.yaml_data = {}
        self.sigma = {}
        self.fhash = []
        
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.explicit_start = False
        self.yaml.preserve_quotes =True
        self.yaml.width = 2000
        self.yaml.indent(mapping=4, sequence=4, offset=4)

    
    def load(self,filename):
        with open(filename,encoding='UTF-8') as file_in:
            self.yaml_data = self.yaml.load(file_in)
        self.__init_fhash()

    def save(self,filename):
        with open(filename,'w',encoding='UTF-8',newline='') as file_out:
            self.yaml.dump(self.yaml_data,file_out)

    def __get_fhash(self,data) -> str:
        product = data["product"] if "product" in data else "none"
        category = data["category"] if "category" in data else "none"
        service = data["service"] if "service" in data else "none"
        fhash = f"{product}_{category}_{service}" 
        return fhash

    def __init_fhash(self):
        for uuid_key in self.yaml_data['logsources']:
            fhash = self.__get_fhash(self.yaml_data['logsources'][uuid_key])
            self.fhash.append(fhash)


    def read_sigma_file(self,path):
        rules_list = [yml for yml in pathlib.Path(path).glob('**/*.yml')]
        for rule in rules_list:
            with rule.open('r',encoding='UTF-8') as file:
                sigma = self.yaml.load(file)
                product = sigma['logsource']["product"] if "product" in sigma['logsource'] else "none"
                category = sigma['logsource']["category"] if "category" in sigma['logsource'] else "none"
                service = sigma['logsource']["service"] if "service" in sigma['logsource'] else "none"
                the_fhash = f"{product}_{category}_{service}" 
                if the_fhash in self.fhash:
                    pass
                else:
                    new_uuid4 = str(uuid.uuid4())
                    self.fhash.append(the_fhash)
                    print(f"New {the_fhash} with uuid {new_uuid4}")
                    self.yaml_data['logsources'][new_uuid4] = {}
                    self.yaml_data['logsources'][new_uuid4]['product'] = None if product == "nome" else product
                    self.yaml_data['logsources'][new_uuid4]['category'] = None if category == "nome" else category
                    self.yaml_data['logsources'][new_uuid4]['service'] = None if service == "nome" else service

    def get_number_default_question(self,section:str,default_ask:str)->int:
        int_q = 0
        for uuid_key in self.yaml_data[section]:
            if self.yaml_data[section][uuid_key]['ask'] == default_ask :
                int_q += 1
        return int_q

    def create_missing_question(self,section_name:str,section_ref:str,default_ask:str,sigma:bool):
        if sigma:
            uuid_from = 'logsource'
        else:
            uuid_from = 'question'
       
        uuid_done = []
        for uuid_key in self.yaml_data[section_name]:
            for uuid_logsource in self.yaml_data[section_name][uuid_key][uuid_from]:
                uuid_done.append(uuid_logsource)

        for uuid_key in self.yaml_data[section_ref]:
            if uuid_key in uuid_done:
                pass
            else:
                new_uuid4 = str(uuid.uuid4())
                information = self.__get_fhash(self.yaml_data[section_ref][uuid_key]) if sigma else self.yaml_data[section_ref][uuid_key]['information']
                self.yaml_data[section_name][new_uuid4] = {}
                self.yaml_data[section_name][new_uuid4]['information'] = information
                self.yaml_data[section_name][new_uuid4]['ask'] = default_ask
                self.yaml_data[section_name][new_uuid4][uuid_from] = [uuid_key]
                uuid_done.append(uuid_key)
                print(f"Missing question for {information} add with uuid {new_uuid4}")


print("Do not use unless you realy want it")
logsource = Quizz()
print("Open logsource.yml")
logsource.load('logsource.yml')

print("Load sigma rules")
logsource.read_sigma_file('../../sigma/rules')
logsource.read_sigma_file('../../sigma/rules-emerging-threats')
logsource.read_sigma_file('../../sigma/rules-threat-hunting')

print("Check missing boolean logsource question")
logsource.create_missing_question(section_name='questions_logsources',
                                  section_ref='logsources',
                                  default_ask="Missing",
                                  sigma=True
                                  )

print("Check missing question to select list of logsource question")
logsource.create_missing_question(section_name='questions_type',
                                  section_ref='questions_logsources',
                                  default_ask="Missing",
                                  sigma=False
                                  )

print("Check missing question to select list of type question")
logsource.create_missing_question(section_name='question_general',
                                  section_ref='questions_type',
                                  default_ask="Missing",
                                  sigma=False
                                  )

print("Save logsource.yml with no backup :)")
logsource.save('logsource.yml')

print("-----------------------")
print("| Data Information")
print(f"You have {len(logsource.yaml_data['logsources'])} Logsources")
print(f"You have {len(logsource.yaml_data['questions_logsources'])} logsource questions")
print(f"You have {len(logsource.yaml_data['questions_type'])} type questions")
print(f"You have {len(logsource.yaml_data['question_general'])} general questions")

print("\n-----------------------")
print("| Working to do")
to_work = logsource.get_number_default_question('questions_logsources',"Missing")
if to_work == 0 :
    print(f"It is a great day , there is no logsource question with the default text")
else:
    print(f"You have {to_work} logsource question(s) with the default text")

to_work = logsource.get_number_default_question('questions_type',"Missing")
if to_work == 0 :
    print(f"It is a great day , there is no type question with the default text")
else:
    print(f"You have {to_work} type question(s) with the default text")

to_work = logsource.get_number_default_question('question_general',"Missing")
if to_work == 0 :
    print(f"It is a great day , there is no genral question with the default text")
else:
    print(f"You have {to_work} general question(s) with the default text")

