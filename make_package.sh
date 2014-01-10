#!/bin/bash
source ./ezgomenu_filelist.cfg
source ${file_pos_dev[update_cfg]}$update_cfg

rm -f $md5file_files
rm -f $filename
rm -f $md5file_targz

if [[ $1 == '--clear' ]]; then
	echo "Clear mode finished."
	exit
fi

md5sum ./ezgomenu_filelist.cfg $all_file > $md5file_files
echo "=====Start to tar.====="
tar -zcvf $filename ./ezgomenu_filelist.cfg $all_file $md5file_files
echo "=====Tar finished.====="
md5sum $filename > $md5file_targz

echo "Package is made.";
echo "Please upload $filename $version_file $md5file_targz to the server."