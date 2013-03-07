import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import re
import csv

Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )

NB_ITEM_PAGE = 28
extensions = 'avi,mkv'

filename = '/media/Library/peliculas.csv'
dictReader = csv.DictReader(open(filename, 'rb'), fieldnames = ['NDisc', 'MName', 'NFiles'], delimiter = '|', quotechar = '"')


def GetKeyboard(heading):
	keyboard = xbmc.Keyboard("", heading, False)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		return unicode(keyboard.getText(), "utf-8")
	return default


def PlayVideo(localpath, handle, uri):
	print "Playing: " + uri
	xbmc.Player().play(uri)


def GetParams(args):
	param = []
	paramstring=args[2]
	if len(paramstring) >= 2:
		params = args[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
		return param


def ShowRoot(localpath, handle):
	li = xbmcgui.ListItem("Movies")
	u = localpath + "?mode=1"
	xbmcplugin.addDirectoryItem(handle, u, li, True)

	li=xbmcgui.ListItem("Search")
	u = localpath + "?mode=2"
	xbmcplugin.addDirectoryItem(handle, u, li, True)

	xbmcplugin.endOfDirectory(handle)


def ShowMovies(localpath, handle):
	for row in dictReader:
		# Get the first video file available
		path = "/media/disc/" + row['MName']
		path = localpath + '?mode=3&uri=' + 'file:///' + path + glob.glob(path + '*.[' + extensions + ']')[0]
	
		li = xbmcgui.ListItem('Disc: ' + row['NDisc'] + ' - ' + row['MName'])
		xbmcplugin.addDirectoryItem(handle, path, li, False, NB_ITEM_PAGE)

	xbmcplugin.endOfDirectory(handle)


def ShowSearchList(localpath, handle, strs):
	p = re.compile(('.*' + strs + '.*').replace(' ', '.*'), re.IGNORECASE)
	for row in dictReader:
		if p.search(row['MName']):

			# Get the first video file available
			path = "/media/disc/" + row['MName']
			path = localpath + '?mode=3&uri=' + 'file:///' + path + glob.glob(path + '*.[' + extensions + ']')[0]

			li = xbmcgui.ListItem('Disc: ' + row['NDisc'] + ' - ' + row['MName'])
			xbmcplugin.addDirectoryItem(handle, path, li, False, NB_ITEM_PAGE)

	xbmcplugin.endOfDirectory(handle)


def SearchVideos(localpath, handle):
	vq = GetKeyboard("Enter the query")
	if (not vq):
		return False, 0
	ShowSearchList(localpath, handle, vq)


def main():
	params = GetParams(sys.argv)
	mode = None
	uri = None

	try:
		uri = urllib.unquote_plus(params["uri"])
	except:
		pass

	try:
		mode = int(params["mode"])
	except:
		pass

	if mode==None:
		showRoot(sys.argv[0], int(sys.argv[1]))
	elif mode==1:
		showMovies(sys.argv[0], int(sys.argv[1]))
	elif mode==2:
		SearchVideos(sys.argv[0], int(sys.argv[1]))
	elif mode==3:
		PlayVideo(sys.argv[0], int(sys.argv[1]), uri))

if __name__ == "__main__":
	main()

