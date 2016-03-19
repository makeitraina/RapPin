import requests

from analyzer import process
from lxml import html
from pin import pin_new_items
from storage import update_data

BASE_URL = "http://www.hotnewhiphop.com/"
TOP_100_URL = BASE_URL + "top100/"

def get_first_child_element(parent, element_selector):
	element = None
	element_array = parent.cssselect(element_selector)
	if len(element_array) > 0:
		element = element_array[0]

	return element

def get_first_child_element_attribute(parent, element_selector, attribute_selector):
	attribute_val = ""
	element = get_first_child_element(parent, element_selector)
	if element is not None:
		attribute_values = element.xpath(attribute_selector)
		if len(attribute_values) > 0:
			attribute_val = attribute_values[0]
			
	return attribute_val

def extract_information(song_figure, song_body, song_stats, song):
	song_details = []
	song_details.append(get_first_child_element_attribute(song_figure, 'img', '@src'))
	song_details.append(BASE_URL + get_first_child_element_attribute(song_body, 'a', '@href'))
	song_details.append(get_first_child_element_attribute(song_body, 'em.chartItem-artist-trackTitle', 'text()'))
	song_details.append(get_first_child_element_attribute(song_body, 'strong.chartItem-artist-artistName', 'text()'))
	song_details.append(get_first_child_element_attribute(song_stats, 'b.chartItem-stats-views', 'text()'))
	song_details.append(get_first_child_element_attribute(song_stats, 'span.pull-left', 'text()'))
	return song_details

def parse(access_token):
	scrape_result = {}
	page = requests.get(TOP_100_URL)
	page_html = html.fromstring(page.text)
	songs = page_html.cssselect('li.chartItem')
	for song in songs:
		# Get the main figure, body and stats of the song
		song_figure = get_first_child_element(song, 'a.chartItem-cover-anchor')
		song_body = get_first_child_element(song, 'div.chartItem-body-artist')
		song_stats = get_first_child_element(song, 'div.chartItem-stats')
		
		# If the figure or body is not present skip to next article
		if song_figure is None or song_body is None:
			continue

		# details represented by index
		# [image, url, name, artist, views, likes]
		song_details = extract_information(song_figure, song_body,
			song_stats, song)
		
		# If full details not present continue to next song
		if "" in song_details:
			continue
		scrape_result[song_details[1]] = {
			'image_url': song_details[0].replace('38x38', '300x300'),
			'url': song_details[1],
			'description': song_details[2].strip() + " by: " + song_details[3].strip(),
			'views': int(song_details[4].split()[0].replace(",", "")),
			'likes': int(song_details[5].split()[0].replace(",", ""))
		}
	
	data_to_process = update_data(scrape_result)
	data_to_promote = process(data_to_process)
	pin_new_items(access_token, data_to_promote)
