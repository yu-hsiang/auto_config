# auto_config

A auto configuration tool for cisco IOS.

(1)How to use

./auto_config.py "your input file" "the device's ip" Example: ./auto_config.py my_file.txt 192.168.1.1

(2)The .txt file format

"#" is for comment "%" is for task title "end" is for end of each block

(3)the problem I am working on

the version can't display a long "show" command respectively. Some output is missing.

#cmd_prompt

using cmd module to implement the User interface, instead of the telnetlib module. This one is still testing and the feature will added into auto_config version 2.
