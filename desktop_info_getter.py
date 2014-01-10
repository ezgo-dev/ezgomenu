#!/usr/bin/python
# -*- encoding: utf-8 -*-

import csv
import os.path
import glob
import getpass

username = getpass.getuser()

if __name__ == '__main__':
	#要擷取資訊的desktop資料夾
	desktop_dirs = [ 
		"/usr/share/applications/",
		"/usr/share/applications/kde4/",
		#"/home/" + username + "/.local/share/applications/",
	]

	#最後要輸出到的csv檔
	target_csv = "desktop_app_get.csv"

	#要擷取出來的屬性
	care_atts = [
		"Name",
		"Name[zh_TW]",
		"Name[en_US]",
		"GenericName",
		"GenericName[zh_TW]",
		"GenericName[en_US]",
		"Comment",
		"Comment[zh_TW]",
		"Comment[en_US]",
		"Categories",
	]

	'''
	以上變數可以自行更改、測試
	以下建議別動ｳﾜｧｧ━━━｡ﾟ(ﾟ´Д｀ﾟ)ﾟ｡━━━ﾝ!!!!
	'''
	
	#[get info from desktops]
	all_atts = []
	all_desktop_content = []
	for desktop_dir in desktop_dirs :
		all_desktop_path = glob.glob( desktop_dir + "*.desktop" )
	
		for desktop_path in all_desktop_path :
			print "parsing", desktop_path
			desktop_lines = open(desktop_path).readlines()
			desktop_content = {}
			desktop_content['basename'] = os.path.basename(desktop_path)
			for line in desktop_lines :
				if( line[0] == '#' ):
					pass
				elif '=' in line:
					att = line[ 0 : line.find('=')]
					desktop_content[att] = line[ line.find('=')+1 : -1 ]
					all_atts.append(att)
			all_desktop_content.append(desktop_content)
		
	assert( not ('basename' in all_atts) )
	
	all_atts = list(set(all_atts))
	all_atts.sort()
	#print "all_atts =", all_atts
	#print "all_desktop_content =", all_desktop_content


	#[output to csv]
	output_atts = care_atts
	csvWriter = csv.writer(open(target_csv, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csvWriter.writerow( ['desktop'] + output_atts )
	for desktop_content in all_desktop_content:
		row = []
		row.append(desktop_content['basename'])
		for att in output_atts :
			if att in desktop_content.keys():
				row.append(desktop_content[att])
			else:
				row.append("")
		csvWriter.writerow( row )
	
