from mcv_socket import McvClient, McvServer

from utils import *

client_creds = get_creds('mcv-seif-client')
server_creds = get_creds('mcv-seif-server')
local_ip_addr = '10.42.35.17'

def client_test():
	client = McvClient(local_ip_addr, client_creds)
	client.connect(local_ip_addr, server_creds._pub)

def server_test():
	server = McvServer(local_ip_addr, server_creds)
	server.listen(1)
	print('Server listening . . .')
	print(server.accept().__dict__)