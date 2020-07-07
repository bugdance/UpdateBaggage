#!/bin/bash
kill -9 `ps -ef | grep update_gun.py | awk '{print $2}' `
echo 3 > /proc/sys/vm/drop_caches
rm -rf log/*.log
rm -rf img/*.png
rm -rf mp3/*.mp3
rm -rf pcm/*.pcm
rm -rf update.log
gunicorn -c update_gun.py update_receiver:app > /dev/null 2>&1 &