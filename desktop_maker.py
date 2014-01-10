#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import csv
import os.path
import os
import getpass
import re
import configparser

username = getpass.getuser()

if __name__ == '__main__':
	'''
	要測試前請先備份你的"/usr/share/applications/"資料夾  
	須先把"ezgomenu_database.csv"載到目前資料夾
	請以terminal sudo執行本code
	'''


	#是否要直接更改 參考來源的desktop資料夾(不可逆之行為)
	source_path_is_dest_path = True

	#參考的表格
	list_adr = os.path.abspath( "/etc/xdg/ezgo/ezgomenu_database.csv" )
	#list_adr = os.path.abspath( "./ezgomenu_database.csv" )

	#參考的desktop資料夾
	source_desktop_paths = [
		"/usr/share/applications/",
		"/usr/share/applications/kde4/",
	]

	#新的desktop目標資料夾
	if not source_path_is_dest_path:
		#假設desktop_dir不為任一source_desktop_path
		#source 和 target資料夾必須一對一
		desktop_dirs = [
			"/home/" + username + "/.local/share/applications/",
			"/home/" + username + "/.local/share/applications/kde4/",
		]

	#新的desktop將要移除的屬性
	attribute_to_del = [
		"X-GNOME-Bugzilla-Bugzilla",
		"X-GNOME-Bugzilla-Product",
		"X-GNOME-Bugzilla-Component",
		"X-GNOME-Bugzilla-Version",
		"X-GNOME-Bugzilla-OtherBinaries",
		"X-Ubuntu-Gettext-Domain",
		"X-GNOME-FullName",
		
	]
	
	"""
	#新的desktop將要移除的列
	line_to_del = [
		#"[Drawing Shortcut Group]"
	]
	"""

	'''
	以上變數可以自行更改、測試
	以下建議別動ｳﾜｧｧ━━━｡ﾟ(ﾟ´Д｀ﾟ)ﾟ｡━━━ﾝ!!!!
	'''
	
	if os.path.exists(list_adr) == False:
		print("Can't find menu database %s" % list_adr)
		exit(1)


	print("Using %s as database" % list_adr)

	if source_path_is_dest_path :
		desktop_dirs = source_desktop_paths
	else:
		assert(len(source_desktop_paths)==len(desktop_dirs))

		#替每個desktop_dir創目錄
		for desktop_dir in desktop_dirs:
			try:
				print("Build", desktop_dir)
				os.makedirs(desktop_dir)
			except OSError:
				print(desktop_dir, "exists.")

		
		for i in range(len(source_desktop_paths)):
			desktop_dir = desktop_dirs[i]
			source_desktop_path = source_desktop_paths[i]
			command = "cp -f " + source_desktop_path+"*.desktop " + desktop_dir
			print( command )
			os.system(command)
	session_num = 0
	session_re = re.compile(r'^\[.+\]$')
	
	for desktop_dir in desktop_dirs:
		print("About to update %s.  Please wait..." % desktop_dir)
		list_reader = csv.reader( open(list_adr, 'r'), delimiter=',', quotechar='"' )
		attribute_load = False
		for row in list_reader:
			if 	attribute_load==False : #一開始先把csv的第一行屬性讀進來
				attribute = row
				attribute_load = True
			else :
				#略過空白行和註解
				if row[0] == "" or row[0][0] == '#':
					continue
			
				desktop_adr = desktop_dir+row[0] #將要修改的desktop路徑
				if os.path.exists( desktop_adr ):#確認該路徑是否存在desktop
					print("Updating %s" % desktop_adr)
					
					config = configparser.ConfigParser()
					config.optionxform = str #這樣才能區分大小寫
					config.read(desktop_adr)
					
					#將csv的內容填入desktop
					att_index = 0 #略過'desktop'
					while att_index+1 < len(attribute) :
						att_index += 1
						if attribute[att_index]=='' or attribute[att_index][0]=='#' or row[att_index]=='':
							pass
						else:
							for section in config.sections():
								config[section][ attribute[att_index] ] = row[att_index]
					#要刪除的屬性
					for att in attribute_to_del:
						for section in config.sections():
							if att in config[section].keys():
								del( config[section][ att ] )
					
					with open(desktop_adr, 'w') as configfile:
						config.write(configfile, space_around_delimiters=False)
