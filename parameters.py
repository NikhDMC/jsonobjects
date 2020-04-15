import json
import subprocess
import os


def get_services():
    services=[]
    file_path = 'services.txt'
    exists = os.path.isfile(file_path)
    if exists:
        with open(file_path) as f:
            services = f.read().splitlines()
        return services
    else:
        print("The file doesnt exist or path mentioned is incorrect")


def get_environment(ch):
    if ch=='1':
        env='ula-dev'
        return env
    elif ch=='2':
        env='ula-stg'
        return env
    elif ch=='3':
        env='ula-prod'
        return env
    else:
        print("No such Choice!!")


def get_parameters(service,environment):
        cmd=['aws', 'ssm', 'get-parameters-by-path', '--path', '/ula/stage/general/{}/'.format(service), '--profile',environment]
        result=subprocess.run(cmd, stdout=subprocess.PIPE)
        parameter_json_dev=result.stdout
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


def data_display(resultant_dict,env1,env2):
    f=open("output.txt","w")
    f.write("|{:<70}| {:<180} |{:<150} ".format('Name', env1, env2))
    f.write("\n")
    for Name, Value in resultant_dict.items():
        f.write("|{:<70}| {:<180} |{:<150} ".format(Name, Value[0], Value[1]))
        f.write("\n")
    f.close()
    subprocess.run(['gedit', 'output.txt'])


if __name__ == "__main__":
    print("Select two environment for comparison \n1.ula-dev \n2.ula-stg \n3.ula-prod")
    ch1 = input("Enter the first env ")
    env1 = get_environment(ch1)
    ch2 = input("Enter the second env ")
    env2 = get_environment(ch2)
    service = get_services()
    for serv in service:
        conv_json_dev1 = get_parameters(serv,env1)
        conv_json_dev2 = get_parameters(serv,env2)
        result_dict = comparsion(conv_json_dev1,conv_json_dev2)
        data_display(result_dict,env1,env2)

