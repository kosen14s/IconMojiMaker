from slack import *
from os import mkdir

mkdir("dir")
slackDownloadIcons(TOKEN, "dir")
loginfo = slackLogin(TEAM, EMAIL, PASSWORD)
for img in listdir("dir"):
	name = splitext(img)[0]
	slackRegisterEmoji(loginfo, name, os.path.join("dir", img))
