import requests,argparse,random,string
# comment



def detect_filter(url , method , params , x_parameter , headers):
    special_char = ["<" , ">" , "'" , '"' , "/" , "\\" , "="]
    filtered = []
    for i in  special_char:
        params[x_parameter] = i.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        r = None
        if method and args.method == "GET":
            r = requests.get(url , params=params , headers=headers)
        elif method and args.method == "POST":
            r = requests.post(url , data=params , headers=headers)
        if params[x_parameter] not in r.text:
            print("Filter on {}".format(special_char))
            filtered.append(i)
    return filtered


xss_payload = [

]
rand_payload = []

mode = "man"
parser = argparse.ArgumentParser()
parser.add_argument('-url' , '-u' , dest='url', help='target url')
parser.add_argument('-parameter' , '-p' , dest='parameter', help='parameters to test')
parser.add_argument('-method' , '-m' , dest='method', help='HTTP request method')
parser.add_argument('-header' , '-d' , dest='header', action="append", help='HTTP header request')
args = parser.parse_args()
if args.url and args.parameter:
    url = args.url
    params = {}
    headers = {}
    r = None
    if args.header:
        for i in args.header:
            headers[i.split(':')[0]] = i.split(':')[1]
    for i in args.parameter.split(','):
        rand_payload.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        params[i] = rand_payload[-1]
    if args.method and args.method == "GET":
        r = requests.get(url , params=params , headers=headers)
    elif args.method and args.method == "POST":
        r = requests.post(url , data=params , headers=headers)

    potentional_xss = False
    target_parameters = []
    for i in params.keys():
        if params[i] in r.text:
            potentional_xss = True
            target_parameters.append(i)
    
    if potentional_xss:
        print("Reflected input detected in requests to {} with parameter {} ".format(url , target_parameters))
        for i in target_parameters:
            for j in xss_payload:
                params[potentional_xss] = j
                if args.method and args.method == "GET":
                    r = requests.get(url , params=params , headers=headers)
                elif args.method and args.method == "POST":
                    r = requests.post(url , data=params , headers=headers)
                if j in r.text:
                    print("XSS found in requests to {} with parameter {} ".format(url , target_parameters))
    
    