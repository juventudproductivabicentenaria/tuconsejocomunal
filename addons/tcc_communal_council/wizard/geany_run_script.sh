#!/bin/sh

rm $0

python "wizard_communal_council_admin.py"

echo "

------------------
(program exited with code: $?)" 		


echo "Press return to continue"
#to be more compatible with shells like dash
dummy_var=""
read dummy_var
