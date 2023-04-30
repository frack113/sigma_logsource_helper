# Very bad script
# Test done with Python 3.11.3 on windows 11
import pathlib
import argparse

from ruamel.yaml import YAML
from collections import OrderedDict

import uuid

SECTION_LOGSOURCE_NAME = "logsources"
SECTION_QLOGSOURCE_NAME = "questions_logsources"
SECTION_QTYPE_NAME = "questions_type"
SECTION_QGENERAL_NAME = "question_general"


class yaml_file:
    def __init__(self, file_name):
        self.yaml_data = {}
        self.sigma = {}
        self.fhash = []
        self.yaml_filename = file_name

        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.explicit_start = False
        self.yaml.preserve_quotes = True
        self.yaml.width = 2000
        self.yaml.indent(mapping=4, sequence=4, offset=4)

    def load(self):
        with open(self.yaml_filename, encoding="UTF-8") as file_in:
            self.yaml_data = self.yaml.load(file_in)
        self.__init_fhash()

    def save(self):
        with open(self.yaml_filename, "w", encoding="UTF-8", newline="") as file_out:
            self.yaml.dump(self.yaml_data, file_out)

    def __get_fhash(self, data) -> str:
        product = data["product"] if "product" in data else "none"
        category = data["category"] if "category" in data else "none"
        service = data["service"] if "service" in data else "none"
        fhash = f"{product}_{category}_{service}"
        return fhash

    def __init_fhash(self):
        for uuid_key in self.yaml_data[SECTION_LOGSOURCE_NAME]:
            fhash = self.__get_fhash(self.yaml_data[SECTION_LOGSOURCE_NAME][uuid_key])
            self.fhash.append(fhash)

    def read_sigma_file(self, path):
        rules_list = [yml for yml in pathlib.Path(path).glob("**/*.yml")]
        for rule in rules_list:
            with rule.open("r", encoding="UTF-8") as file:
                sigma = self.yaml.load(file)
                product = (
                    sigma["logsource"]["product"]
                    if "product" in sigma["logsource"]
                    else "none"
                )
                category = (
                    sigma["logsource"]["category"]
                    if "category" in sigma["logsource"]
                    else "none"
                )
                service = (
                    sigma["logsource"]["service"]
                    if "service" in sigma["logsource"]
                    else "none"
                )
                the_fhash = f"{product}_{category}_{service}"
                if the_fhash in self.fhash:
                    pass
                else:
                    new_uuid4 = str(uuid.uuid4())
                    self.fhash.append(the_fhash)
                    print(f"New {the_fhash} with uuid {new_uuid4}")
                    self.yaml_data[SECTION_LOGSOURCE_NAME][new_uuid4] = {}
                    self.yaml_data[SECTION_LOGSOURCE_NAME][new_uuid4]["product"] = (
                        None if product == "nome" else product
                    )
                    self.yaml_data[SECTION_LOGSOURCE_NAME][new_uuid4]["category"] = (
                        None if category == "nome" else category
                    )
                    self.yaml_data[SECTION_LOGSOURCE_NAME][new_uuid4]["service"] = (
                        None if service == "nome" else service
                    )

    def get_number_default_question(self, section: str, default_ask: str) -> int:
        int_q = 0
        for uuid_key in self.yaml_data[section]:
            if self.yaml_data[section][uuid_key]["ask"] == default_ask:
                int_q += 1
        return int_q

    def __create_missing_question(
        self, section_name: str, section_ref: str, default_ask: str, sigma: bool
    ):
        if sigma:
            uuid_from = "logsource"
        else:
            uuid_from = "question"

        uuid_done = []
        for uuid_key in self.yaml_data[section_name]:
            for uuid_logsource in self.yaml_data[section_name][uuid_key][uuid_from]:
                uuid_done.append(uuid_logsource)

        for uuid_key in self.yaml_data[section_ref]:
            if uuid_key in uuid_done:
                pass
            else:
                new_uuid4 = str(uuid.uuid4())
                information = (
                    self.__get_fhash(self.yaml_data[section_ref][uuid_key])
                    if sigma
                    else self.yaml_data[section_ref][uuid_key]["information"]
                )
                self.yaml_data[section_name][new_uuid4] = {}
                self.yaml_data[section_name][new_uuid4]["information"] = information
                self.yaml_data[section_name][new_uuid4]["ask"] = default_ask
                self.yaml_data[section_name][new_uuid4][uuid_from] = [uuid_key]
                uuid_done.append(uuid_key)
                print(f"Missing question for {information} add with uuid {new_uuid4}")

    def create_all_missing_question(self, missing_ask: str):
        self.__create_missing_question(
            section_name=SECTION_QLOGSOURCE_NAME,
            section_ref=SECTION_LOGSOURCE_NAME,
            default_ask=missing_ask,
            sigma=True,
        )
        self.__create_missing_question(
            section_name=SECTION_QTYPE_NAME,
            section_ref=SECTION_QLOGSOURCE_NAME,
            default_ask=missing_ask,
            sigma=False,
        )
        self.__create_missing_question(
            section_name=SECTION_QGENERAL_NAME,
            section_ref=SECTION_QTYPE_NAME,
            default_ask=missing_ask,
            sigma=False,
        )


def set_argparser():
    argparser = argparse.ArgumentParser(
        description="Select logsource with simple questions",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    argparser.add_argument(
        "--update", "-u", action="store_true", help="Update logsource from sigma rules"
    )
    argparser.add_argument(
        "--info", "-i", action="store_true", help="Get information about logsource.yml"
    )

    return argparser


def main():
    argparser = set_argparser()
    cmdargs = argparser.parse_args()

    logsource = yaml_file("logsource.yml")

    print("Open the yaml database")
    logsource.load()

    if cmdargs.update:
        print("Load sigma rules")
        logsource.read_sigma_file("../../sigma/rules")
        logsource.read_sigma_file("../../sigma/rules-emerging-threats")
        logsource.read_sigma_file("../../sigma/rules-threat-hunting")

        print("Check missing question")
        logsource.create_all_missing_question("Missing")

        print("Save the yaml database with no backup :)")
        logsource.save()

    if cmdargs.info:
        print("-----------------------")
        print("| Data Information")
        print(f"You have {len(logsource.yaml_data[SECTION_LOGSOURCE_NAME])} Logsources")
        print(
            f"You have {len(logsource.yaml_data[SECTION_QLOGSOURCE_NAME])} logsource questions"
        )
        print(f"You have {len(logsource.yaml_data[SECTION_QTYPE_NAME])} type questions")
        print(
            f"You have {len(logsource.yaml_data[SECTION_QGENERAL_NAME])} general questions"
        )

        print("\n-----------------------")
        print("| Working to do")
        to_work = logsource.get_number_default_question(
            SECTION_QLOGSOURCE_NAME, "Missing"
        )
        if to_work == 0:
            print(
                f"It is a great day , there is no logsource question with the default text"
            )
        else:
            print(f"You have {to_work} logsource question(s) with the default text")

        to_work = logsource.get_number_default_question(SECTION_QTYPE_NAME, "Missing")
        if to_work == 0:
            print(
                f"It is a great day , there is no type question with the default text"
            )
        else:
            print(f"You have {to_work} type question(s) with the default text")

        to_work = logsource.get_number_default_question(
            SECTION_QGENERAL_NAME, "Missing"
        )
        if to_work == 0:
            print(
                f"It is a great day , there is no genral question with the default text"
            )
        else:
            print(f"You have {to_work} general question(s) with the default text")


if __name__ == "__main__":
    main()
