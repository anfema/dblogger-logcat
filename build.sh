#!/bin/bash
echo "#!$(which python)" >logcat
cat src/cmdline.py src/model.py src/db.py logcat.py|sed -e '/from \./d' -e '/from src\./d' >>logcat
chmod a+x logcat
