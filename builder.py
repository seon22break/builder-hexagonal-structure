import json
import os
import argparse
from os.path import exists
from colorama import Fore, init,Style
import yaml
from yaml.loader import SafeLoader

init()
def obtain_namespace_from_composer():
    if not exists('./composer.json'):
        return False

    with open('./composer.json') as f:
        composer = json.load(f)
        return list(composer['autoload']['psr-4'].keys())[0]

def obtain_path_to_domain():
    if not exists('./composer.json'):
        return False

    with open('./composer.json') as f:
        composer = json.load(f)
        return list(composer['autoload']['psr-4'].values())[0]


contentClassValueObject = "<?php\n"
contentClassValueObject += "declare(strict_types=1);\n"
contentClassValueObject += "namespace {namespace};\n\n"
contentClassValueObject += "final class {name}{{ \n "
contentClassValueObject += "\t\tpublic function __construct(string $value) {{}}\n"
contentClassValueObject += "\t\tpublic function value(): string {{}}\n\n"
contentClassValueObject += "}}"

def create_value_object(entitie,pathToCreateValueObject,domain):

    try:
        f = open(pathToCreateValueObject, "w")
        f.write(contentClassValueObject.format(namespace=obtain_namespace_from_composer()+domain+"\\Domain\\ValueObjects\\"+entitie, name=entitie))
        f.close()
    except IOError:
        print("An IOError has occurred!")
        os.remove(pathToCreateValueObject)

def read_schema(file):

    if not file.endswith(".yml"):
        raise Exception(Fore.RED + "The file must be a .yml")

    with open(file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        return data

if __name__ == "__main__":

    print(Fore.GREEN + "Welcome to Builder DDD")
    parser = argparse.ArgumentParser(
                    prog = 'Builder DDD',
                    description = 'Its a create build for DDD')

    parser.add_argument('-p', '--path-scheme', action='store', help='Path to schema') 

    args = parser.parse_args()

    if not exists(args.path_scheme):
        print(Fore.RED + "The schema file is not exist")
        exit(1)

    print("Reading schema....")

    try:
        schema = read_schema(args.path_scheme)
    except Exception as e:
        print(Style.NORMAL)
        print(Fore.RED + str(e) )
        exit(1)

    print("Create folder to Domain..")

    path = obtain_path_to_domain()
    namespace = obtain_namespace_from_composer()

    if not path or not namespace:
        print()
        print(Style.NORMAL+Fore.RED + "The composer.json is not exist")
        exit(1)
    try:
        for domain in schema:
            os.makedirs("./"+path+domain+"/Domain/ValueObjects",exist_ok=True)
            f = open("./"+path+domain+"/Domain/"+domain+".php", "w")
            f.write(contentClassValueObject.format(namespace=obtain_namespace_from_composer()+domain+"\\Domain\\"+domain, name=domain))
            f.close()

            os.makedirs("./"+path+domain+"/Infrastructure",exist_ok=True)
            os.makedirs("./"+path+domain+"/Application",exist_ok=True)
            
            for valueObject in schema[domain]: 
                create_value_object(valueObject,"./"+path+domain+"/Domain/ValueObjects/"+valueObject+".php",domain)

        print(Fore.GREEN + "The domain has been created")

    except Exception as e:
        print(str(e))
        print(Fore.RED + "Dont create folder to Domain "+domain)
        exit(0)

    
        

