import os
import requests
from bs4 import BeautifulSoup

def execute_url(url):
	try:
		#first get response from url
		response = requests.get(url)

		#check for status code
		stat_code = response.status_code

		#check the status code 
		if stat_code == 200:

			print("-------------------------Successfull Execution of url----------------------------")

			#on successfull execution call function to retrive the data
			retrive_data(response)

			#check for next pages
			check_for_next_page(response)


		elif stat_code == 503:
			print("!~~~~~~~~~~~~Press enter tocontinue from last url~~~~~~~~~~~!!")
		
			x = input()
		
			execute_url(url)
	
		else:
			print("!~~~~~~~~~~~~~~~~~~~~~Failed to execute url~~~~~~~~~~~~~~~~~~~~~~~~~~!\n !!!!~~~~~~~~~~~~~~~~~~~~Error code : ",stat_code)

	except requests.exceptions.ConnectionError:
		print("!!~~~~~~~No network or Slow Network~~~~~~~~~~!!\n")
		x = input("~~~~~~Check network and press enter to continue from last url~~~~~~")
		execute_url(url)


def retrive_data(response):

	#parse the data from html content to processible format
	soup = BeautifulSoup(response.text,'html.parser')

	rew = soup.find_all('div',{'data-hook','review'})

	for x in rew:
		stri = str(x)
		rew1 = BeautifulSoup(stri,'html.parser')
		
		div = rew1.find("span",{"data-hook":"review-body"}).get_text()

		write_to_file(div)


def write_to_file(data):

	global fname

	data = str(data)
	
	data = check_for_unicodes(data)
	
	data+="\n"
	
	f = open(fname,"a")
	f.write(data)
	f.close()

def check_for_unicodes(data):
	ret = data.isascii()
	if not ret:
		data = data.encode('ascii', 'ignore')
	return(str(data))
		
	
def check_for_next_page(response):
	
	global head

	soup = BeautifulSoup(response.text,'html.parser')

	tag_span = str(soup.find("span",{"data-action":"reviews:page-action"}))

	soup = BeautifulSoup(tag_span,'html.parser')

	tag_ul = str(soup.find("ul",{"class","a-pagination"}))

	soup = BeautifulSoup(tag_ul,'html.parser')

	btn = soup.find("li",{"class","a-selected page-button"})

	btn = btn.find_next_sibling("li")

	if btn['class'] != ['a-disabled','a-last']:

		link = head

		link+=str(btn.a['href'])

		print("\n url :-  ",link)
		
		execute_url(link)

	else:
		print("~~~~~~~~~~~~~~~~~~End of all pages~~~~~~~~~~~~~~~~~~~")


def main():

	global fname, head

	name = input("Enter name of a file : ")
	fname += name+".txt"

	f = open(fname,"w")
	f.write("data\n")
	f.close()

	url = input("Paste the url : ")
	
	spl_data = url.split("/")
	head = spl_data[0] + "//" + spl_data[2]
	execute_url(url)

cwd = os.getcwd()
fname = cwd+"\_"
head = ""
if __name__ == "__main__":
	main()