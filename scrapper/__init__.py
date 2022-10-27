import sys
from scrapper.html_scapper import HTMLScrapper

HELP_CONTENT = '''
The software is intented to scrap content from 
HTML file ( both css classes and html content )
To Scrap Content use
    scrapper 

OUTPUT
>> Input html filepath 
>> [INPUT_FILE_PATH_THAT_IS_REQUIRED_TO_SCRAPPED]

>> Input tag 
>> [INPUT_TAG_NAME]  # div, section

>> Input tag ID
>> [INPUT_ID_THAT_IS_ATTACHED_TO_TAG] 
'''
def run():
    args = sys.argv[1:]
    filepath = None
    tag = None
    tag_id = None
    for arg in args:
        if arg.split("=")[0] == "--html-file":
            filepath = arg.split("=")[1]
        elif arg.split("=")[0] == "--tag":
            tag = arg.split("=")[1]
        elif arg.split("=")[1] == "--id":
            tag_id = arg.split("=")[1]
        else:
            if arg == "help" or arg == "--html":
                print (HELP_CONTENT)
                return True

    return HTMLScrapper(filepath, tag, tag_id).scrap
