import requests
import re
from os.path import join, splitext
from os import listdir


def download(url, filename):
	"Download File Using Requests"

	r = requests.get(url, stream=True)
	if not r.status_code == 200:
		return
	with open(filename, 'wb') as f:
		for chunk in r.iter_content():
			f.write(chunk)

def slackDownloadIcons(token, dirname="."):
	""" Download Icon of Team Members Using Slack API"""

	import json

	r = requests.post("https://slack.com/api/users.list", data={"token": TOKEN}) # get user list by json
	jobj = json.loads(r.text)
	def user_infos(jobj):
		return ({"name": u["name"], "image": u["profile"]["image_72"]} for u in jobj["members"])
	for u in user_infos(jobj):
		download(u["image"], os.path.join(dirname, u["name"] + ".jpg"))
	

def getInputTagValue(body, name):
	""" Search value of first input tag which has specified name field """"
	return re.search(r'name="{}" value="(.*)"'.format(name), body).group(1)


def slackLogin(team, email, password):
	""" Login to Slack and Return login information """

	s = requests.Session()
	url = "https://{}.slack.com/".format(team)
	t = s.get(url).text
	payload = {
		"crumb": getInputTagValue(t, "crumb"),
		"signin": getInputTagValue(t, "signin"),
		"redir": getInputTagValue(t, "redir"),
		"remember": "on",
		"email": email,
		"password": password,
	}
	s.post(url, data = payload) # login request
	return (team, s)

def pathOnSlack(team, path):
	return join("https://{}.slack.com/".format(team), path)

def slackGetPage(info, path):
	url = pathOnSlack(info[0], path)
	r = info[1].get(url)
	return r

def slackRegisterEmoji(info, name, filename):
	""" Register Emoji to Slack """
	team = info[0]
	s = info[1]

	path = "customize/emoji"
	t = slackGetPage(info, path).text
	payload = {
		"crumb": getInputTagValue(t, "crumb"),
		"add": "1",
		"mode": "data",
		"name": name
	}
	files = {
		"img": open(filename, "rb")
	}
	return s.post(pathOnSlack(info[0], path), data = payload, files=files)
	

