import sys

#參數:version_local_filename version_server_filename
#回傳有沒有必要更新
#有:1
#沒有:0
if __name__ == "__main__":
	version_local = float(open(sys.argv[1], 'r').read())
	version_server = float(open(sys.argv[2], 'r').read())
	if version_local < version_server :
		exit(1)
	else :
		exit(0)
