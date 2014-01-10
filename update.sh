#!/bin/bash
function fail {
	echo "Updating failed."
	exit
}
function finish {
	echo "Updating finished!"
	exit
}

#[移動到update.sh所在資料夾]
function findNowExeBashDir {
	first=`echo $0 | head -c 1`
	if [ $first == "/" ]; then 
		nowdir=$0
	else
		nowdir=`pwd`/$0
	fi
	nowdir=`echo $nowdir | sed s/update.sh//`
	
}
function moveToNowExeBashDir {
	cd $nowdir
	echo "cd to $nowdir"
}

#在此執行cfg中的內容
source /etc/xdg/ezgo/ezgomenu_filelist.cfg
source ${file_pos_rt[update_cfg]}$update_cfg
server_list_len=${#server_list[@]}

mkdir -p $tmpdir
cd $tmpdir

#[測試用echo]
:<<COMMENT
#echo $filename
#echo ${server_list[0]}
#echo -n "server_list_len="
#echo $server_list_len
for (( i=0; i<$server_list_len; i++ ))
do
	#echo $i
	echo ${server_list[$i]}
done
COMMENT


#檢測能否連接到網路
ping -c 1 8.8.8.8 > /dev/null
if [ $? != 0 ]; then
	echo "Can't connect to internet."
	fail
fi

#依伺服器優先順序抓下version
#若version_server版本比version_local版本更高再抓.tar.gz
#若任一version_server版本 <= version_local版本，就停止更新
echo "Connect to Network."
for (( i=0; i<$server_list_len; i++ ))
do
	wget ${server_list[$i]}$version_file -O ./ezgomenu_version_server
	if [ $? != 0 ]; then
		echo "Can't wget "${server_list[$i]}$version_file
		if [ $i == $(($server_list_len-1)) ]; then
			echo "All version_files of servers can't be touched."
			fail
		fi
	else
		echo "Downloaded "${server_list[$i]}$version_file
		python3 ${file_pos_rt[update_compare]}$update_compare ${file_pos_rt[version_file]}$version_file ./ezgomenu_version_server
		if [ $? == 0 ]; then
			echo "Local version already is the new one."
			finish
		fi
		
		echo "Found new version on server."
		zenity --title=ezgomenu --question --text="發現新版本的ezgomenu，\n要更新並執行嗎？\n（建議進行更新）" --ok-label="更新並執行" --cancel-label="下次再提醒"
		
		if [ $? == 1 ]; then
			echo "Updating is canceled."
			fail
		fi
		
		echo "Start to download the new version."
		#將下載好的壓縮檔，直接解壓縮覆蓋目前的資料夾檔案
		#mkdir $tmpdir
		#壓縮檔md5下載
		wget ${server_list[$i]}$md5file_targz -O $tmpdir$md5file_targz
		if [ $? != 0 ]; then
			echo "Can't wget "${server_list[$i]}$md5file_targz
			fail
		fi		
		echo "Downloaded "${server_list[$i]}$md5file_targz
				
		#主壓縮檔下載
		wget ${server_list[$i]}$filename -O $tmpdir$filename
		if [ $? != 0 ]; then
			echo "Can't wget "${server_list[$i]}$filename
			fail
		fi		
		echo "Downloaded "${server_list[$i]}$filename
		
		#壓縮檔 md5 檢查
		#cd $tmpdir
		pwd
		ls -l > log
		md5sum -c $md5file_targz
		if [ $? != 0 ]; then
			echo $filename "md5 checksum error"
			fail
		fi
		
		#在tmpdir解壓縮，做md5檢查再搬檔案到正確位置
		#解壓縮
		echo "Unzip new version file"
		tar -zxvf $filename
		md5sum -c $md5file_files
		if [ $? != 0 ]; then
			echo $md5file_files "md5 checksum error"
			fail
		fi
		copyFilesFromDevToRt
		
		finish
	fi
done