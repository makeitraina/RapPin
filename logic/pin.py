import requests

pinterest_api_url = 'https://api.pinterest.com/v1/'

def create_pin(access_token,board,note,link,image_url):
	print("Pinning: " + note)
	url = pinterest_api_url + 'pins/'
	params = {
		'access_token': access_token,
		'board': board,
		'note': note,
		'link': link,
		'image_url': image_url
	}
	print(params)
	requests.post(url, data=params)


def pin_new_items(access_token, new_data, board="neilraina/hip-hop"):
	for key in new_data:
		pin_data = new_data[key]
		create_pin(access_token, board, pin_data['description'], pin_data['url'], pin_data['image_url'])
