from os import name
import yaml 
import os 
with open(os.path.dirname(__file__)+"/people.yaml", 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    people = yaml.load(file, Loader=yaml.FullLoader)
    names = people['images']
    
    for people in names:
        print(str(people))        
        