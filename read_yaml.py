import yaml 

with open("test_yaml.yaml", "r") as file: 
    data = yaml.safe_load(file)

print(data)
print(data["base"])