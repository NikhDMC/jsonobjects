import json
import subprocess
import os

def get_service():
    service=[]
    exists=os.path.isfile('myfile')
    if exists:
        with open('myfile') as f:
            for line in f:
                service.append(line)
        return service
    else:
        print("The file doesnt exist or path mentioned is incorrect")


def get_parameters(service,environment):
        cmd='aws ssm get-parameters-by-path --path "/ula/stage/general/{}/" --profile {}'.format(service,environment)
        p=subprocess.Popen([cmd], stdout=subprocess.PIPE)
        parameter_json_dev=p.communicate()
        converted_parameter_json_dev = json.loads(parameter_json_dev)
        return converted_parameter_json_dev

def comparsion(converted_parameter_json_dev1,converted_parameter_json_dev2):
    json_dev1_dict = dict()
    result_dict = dict()

    for i in converted_parameter_json_dev1["Parameters"]:
        json_dev1_dict[i['Name']] = [i['Value'], "Null"]
    for j in converted_parameter_json_dev2["Parameters"]:
        if j['Name'] not in json_dev1_dict.keys():
            result_dict[j['Name']] = ["Null", j['Value']]
        elif j['Name'] in json_dev1_dict.keys():
            if j['Value'] != json_dev1_dict.get(j['Name'])[0]:
                result_dict[j['Name']] = [json_dev1_dict.get(j['Name'])[0], j['Value']]
            del json_dev1_dict[j['Name']]
    result_dict.update(json_dev1_dict)
    return result_dict
def data_display(result_dict,indent=-1):
    print("|{:<70}| {:<180} |{:<150} ".format('Name', 'Value0', 'Value1'))
    for Name, Value in result_dict.items():
        print("|{:<70}| {:<180} |{:<150} ".format(Name, Value[0], Value[1]))

if __name__ == "__main__":
    print("Select two environment for comparison \n1.ula-dev \n2.ula-stg \n3.ula-prod")
    env1=input("Enter the first env")
    env2=input("Enter the second env")
    service=get_service()
    for serv in service:
        conv_json_dev1=get_parameters(serv,env1)
        conv_json_dev2=get_parameters(serv,env2)
    result_dict = comparsion(conv_json_dev1,conv_json_dev2)
    data_display(result_dict)

