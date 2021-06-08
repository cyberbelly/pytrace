import re
import subprocess
from datetime import datetime

up_arrow   = '\u2191'
down_arrow = '\u2193'
website_dic={'website name':'list of ips'}
traceroute ='traceroute -Tn {}'
today      = datetime.strftime(datetime.today(),'%d%b%y')
log_file   = f'{today}_fulllogs.txt'
results    = f'results_for_{today}.txt'
template = '{}\n{:<13} ---> {:^5} ---> {:>13} {}'

def log_it(name,result_list):
    with open(log_file,'a') as f:
        f.write('{}:\n'.format(name))
        f.write('\n'.join(result_list))

def list_to_dic(traces_list):
    trace_dic={}
    for trace in filter(None,traces_list[1:]):
        print(trace)
        hop,ip=trace.split('  ')[:2]
        if re.match('(\d{,3}\.){3}\d{,3}',ip):
            hop=int(hop)
            trace_dic.update({hop:ip})
    return trace_dic


for name,ip_list in website_dic.items():
    highest_hop=0
    for ip in ip_list:
        current_trace = traceroute.format(ip)
        comeback_list = str(subprocess.check_output(current_trace.split()),'utf-8').split('\n')
        log_it(name,comeback_list)
        trace_dic = list_to_dic(comeback_list)
               
        last_hop = max(trace_dic)
        final_ip = trace_dic[last_hop]

        if final_ip == ip:
            result = template.format(name,ip,last_hop,final_ip,up_arrow)
            break
            
        elif last_hop > highest_hop and last_hop >= 8:
            result = template.format(name,ip,last_hop,final_ip,up_arrow)
            highest_hop = last_hop
        
        
    if highest_hop <8 and final_ip != ip:
        result = template.format(name,ip,last_hop,final_ip,down_arrow)
    with open(results,'a') as f:
        f.write(result)
        f.write('\n\n')
