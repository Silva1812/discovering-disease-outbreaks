# Library for geometry list
import geonamescache
# Library for convert unicode data
from unidecode import unidecode
# Regex for find sub string in string
import re
# Library for visualize data
import pandas as pd

# Put all countries, cities to 2 lists
gc = geonamescache.GeonamesCache()
countries = map(lambda country: unidecode(country["name"]), gc.get_countries().values())
cities = map(lambda city : unidecode(city["name"]), gc.get_cities().values())

''' Read file and return file text '''
def read_file(file_name="headlines.txt"):
	_file = open(file_name)
	result = map(lambda x: x, _file)
	_file.close()
	return result

''' Write extracted data to a text file '''
def write_file(datas):
	_file = open("extract_data.txt", "w")
	_file.write("headline\tcountries\tcities\n")
	for data in datas:
		_file.write(data["headline"] + "\t"+ str(data["country"]) + "\t" + str(data["city"]) + "\n")
	_file.close()

''' Find matched item in list that string holds '''
def get_match_word(string, _list):
	matched_items = []
	if type(string) != str:
		return float("NaN")
	for item in _list:
		match = re.search(item + "\\b", string)
		if match is not None:
			matched_items.append(string[match.start():match.end()])
	return float("NaN") if len(matched_items) == 0 else max(matched_items, key=len) 

''' Main function, return DataFrame '''
def extract_data():
	lines = read_file()
	datas = []
	# Loop each line and find matched country, city
	for i,line in enumerate(lines):
		matched_country = get_match_word(line, countries)
		matched_city = get_match_word(line, cities)
		datas.append({ "headline": line.rstrip("\n"), "country": matched_country, "city": matched_city })
		#print("Process " + str(i+1) + "/" + str(len(lines)))
	# Map result data to DataFrame	
	df = pd.DataFrame({
		'headline': map(lambda data: data["headline"], datas),
		'country': map(lambda data: data["country"], datas),
		'city': map(lambda data: data["city"], datas)
	})
	print(df)
	write_file(datas)
	return df

# Run the main function
extract_data()
