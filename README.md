You can place this anywhere since it uses relative paths to work. As long as it has permission to the folder it will work.

For this code to work on WINDOWS, you have to install google chrome and following libraries: 
requests, selenium. 


you can do so by typing following commands to CMD:

- pip install requests
- pip install selenium
- pip install patoolib


for linux to work, in main code, Line 33, 
change variable to linux64 instead of windows64





This code uses Request library to download the items, and selenium to preload the website from javascript to get html items properly. since it uses the fact the website has the codes listed in one unsorted list.