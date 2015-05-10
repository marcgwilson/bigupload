#! /usr/bin/env python
import requests, json

CHUNK_SIZE = 1024 * 1024
URL = 'http://0.0.0.0:8000/api/upload/'
TOKEN_URL = 'http://0.0.0.0:8000/api/upload/token.json'
ITEM_URL = 'http://0.0.0.0:8000/api/item/create.json'

# define the function to split the file into smaller chunks
def sendFile(input_fn, url, token_url, chunk_size):
	#read the contents of the file
	f = open(input_fn, 'rb')
	data = f.read() # read file contents
	f.close()

	# get the length of data, ie size of the input file in bytes
	num_bytes = len(data)

	#calculate the number of chunks to be created
	num_chunks = num_bytes // chunk_size
	if(num_bytes % chunk_size):
		num_chunks+=1

	# Get upload token from server:
	t = requests.post(token_url)
	token = json.loads(t.text)['token']
	token_data = { 'token': token }

	for i in range(0, num_bytes + 1, chunk_size):
		chunk = data[i : i + chunk_size]
		files = {'chunk': (input_fn, chunk)}
		r = requests.post(url, files=files, data=token_data)
		# print '%s' % r.status_code
		print "%s %s" % (r.status_code, r.text)

	return token


def createItem(url, token):
	data = { 'token': token }
	headers = {'Content-type': 'application/json'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	print 'createItem: %s %s' % (r.status_code, r.text)


def main():
	token = sendFile('001.mov', URL, TOKEN_URL, CHUNK_SIZE)
	createItem(ITEM_URL, token)


if __name__ == '__main__':
	main()

