import json
import subprocess
import os
Name_len=0
Value0_len=0
Value1_len=0

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
    global Name_len
    global Value1_len
    global Value0_len

    for i in converted_parameter_json_dev1["Parameters"]:
        json_dev1_dict[i['Name']] = [i['Value'], "***NULL***"]
        if len(json_dev1_dict[i['Name']])> Name_len:
            Name_len=len(json_dev1_dict[i['Name']])
        if len(json_dev1_dict.get(i['Name'])[0])> Value0_len:
            Value0_len=len(json_dev1_dict.get(i['Name'])[0])

    for j in converted_parameter_json_dev2["Parameters"]:
        if j['Name'] not in json_dev1_dict.keys():
            result_dict[j['Name']] = ["***NULL***", j['Value']]
        if len(j['Name'])>Name_len:
            Name_len=len(j['Name'])
        if len(j['Value'])>Value1_len:
            Value1_len=len(j['Value'])
        if j['Name'] in json_dev1_dict.keys():
            if len(j['Name'])>Name_len:
                Name_len=len(j['Name'])
            if j['Value'] != json_dev1_dict.get(j['Name'])[0]:
                result_dict[j['Name']] = [json_dev1_dict.get(j['Name'])[0], j['Value']]
                if len(j['Value'])>Value1_len:
                    Value1_len=len(j['Value'])
                if len(json_dev1_dict.get(j['Name'])[0])>Value0_len:
                    Value0_len=len(json_dev1_dict.get(j['Name'])[0])
            del json_dev1_dict[j['Name']]
    result_dict.update(json_dev1_dict)
    return result_dict


def data_display(resultant_dict,env1,env2,serv):
    global Name_len
    global Value0_len
    global Value1_len

    f=open("output.txt","a+")
    print(serv)
    formatter = "|{:<" + str(Name_len) + "}| {:<" + str(Value0_len) + "} |{:<" + str(Value1_len) + "} "
    f.write(serv)
    f.write("\n")
    f.write(formatter.format('Name', env1, env2))
    f.write("\n")
    for Name, Value in resultant_dict.items():
        f.write(formatter.format(Name, Value[0], Value[1]))
        f.write("\n")
    f.write("\n\n")
    f.close()
    print("\n")


if __name__ == "__main__":
    f = open('output.txt', 'r+')
    f.truncate(0)
    print("Select two environment for comparison \n1.ula-dev \n2.ula-stg \n3.ula-prod")
    ch1 = input("Enter the first env ")
    env1 = get_environment(ch1)
    ch2 = input("Enter the second env ")
    env2 = get_environment(ch2)
    service = get_services()
    for serv in service:
        Name_len=0
        Value0_len=0
        Value1_len=0
        conv_json_dev1 = get_parameters(serv,env1)
        conv_json_dev2 = get_parameters(serv,env2)
        result_dict = comparsion(conv_json_dev1,conv_json_dev2)
        data_display(result_dict,env1,env2,serv)
    subprocess.run(['gedit','output.txt&'])

