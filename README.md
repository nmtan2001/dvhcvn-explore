# Administrative units of Vietnam explore
## Video Demo:  <https://youtu.be/Gk0MTQQ7syU>
## Description:

This interactive text-based program enables users to explore and delve into the administrative structure of Vietnam. As well as see the how many units that have the same levels. Data is taken from [dvhcvn](https://github.com/daohoangson/dvhcvn). Data is updated from the Administrative Directory page of the General Statistics Office and the Administrative Map System of the Government Electronic Information Portal.

## Key Features:

- __Administrative Unit Navigation__: Seamlessly navigate through the three levels of administrative divisions: provinces, districts, and communes.

- __Unit Statistics__: Gain insights into the administrative hierarchy by accessing statistics on the number of child units within each current unit.

- __Unit Level Count__: Discover the distribution of administrative units across different levels, providing a comprehensive overview of Vietnam's administrative structure.

- __Data Visualization__: Enhance understanding with interactive data visualizations that represent the hierarchical relationships between administrative units.

## Commands:
There will be some commands that you can perform at each stages:
- **e (Explore)**: Input the next level unit you want to explore (***City -> District -> Commune***)
- **l (List)**: Lists all the child units of the parent unit (***Cities -> Districts -> Communes***)
- **s (Statistics)**: Statistics about the current selected unit (***Country -> City -> District***)
- **q (Quit)**: Quit the program

## Brief explanation:
Functions: 
- __get_country__: Create a dictionary out of the JSON file taken from dvhcvn

- __remove_diacritics__: Remove all the diacritics of a word/phrase using RegEx

- __get_city/get_district/get_commune__: Take the required unit based on the parents

- __list_city/list_district/list_commune__: List all the child units based on the parents

- __total/data_explore/stat_city__ :Perform calcualtion to get statistics

- __bold__ : Make the required phase bold

- __intro/run__: Control the flow of program

Libraries:
- __pytest__:Perform unit tests on functions
- __colorama__: give colors to prints
