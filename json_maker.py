###################################################################################
###     Author:         Tim Hanson                                              ###
###     Date:           06/16/2017                                              ###
###     Title:          JSON Filemaker                                          ###
###     Description:    Interactive python script which allows for easy         ###
###             creation of JSON files to pass in to the music_downloader.py    ###
###             file. Outputs file in the same directory                        ###
###################################################################################

import os
import sys
from types import DictType, ListType
import json

OBJECT_ALIAS = ['object', 'song', 's']
ARRAY_ALIAS = ['array']

class JsonMaker(object):
    def __init__(self, file_name, init_type):
        self.file_name = file_name
        self.init_type = init_type
            
    def return_scope(self, object_type):
        if object_type == 'object':
            return {}
        elif object_type == 'array':
            return []
        else:
            return None
        
    def add_elem(self, scope, label, value):
        if type(scope) == DictType:
            scope[label] = value
        if type(scope) == ListType:
            scope.append(value)
            
    def generate_json(self, scope_name, current_type):
        cur_scope = self.return_scope(current_type)
        cur_input = ''
        while True:
            cur_input = raw_input("{} - {}> ".format(scope_name, current_type))
            input_data = cur_input.split(": ")
            if input_data[0]  == 'end':
                return cur_scope
            if type(cur_scope) == DictType:
                if len(input_data) < 2:
                    print 'Object entries must follow [KEY]: [VALUE]'
                elif input_data[1] in OBJECT_ALIAS:
                    self.add_elem(
                            cur_scope, 
                            input_data[0], 
                            self.generate_json(input_data[0], 'object'))
                elif input_data[1] in ARRAY_ALIAS:
                    self.add_elem(
                            cur_scope, 
                            input_data[0], 
                            self.generate_json(input_data[0], 'array'))
                else:
                    self.add_elem(cur_scope, input_data[0], input_data[1])
            elif type(cur_scope) == ListType:
                if input_data[0] in OBJECT_ALIAS:
                    self.add_elem(
                            cur_scope, 
                            None, 
                            self.generate_json('{}[]'.format(scope_name), 'object'))
                elif input_data[0] == ARRAY_ALIAS:
                    self.add_elem(
                            cur_scope, 
                            None, 
                            self.generate_json('{}[]'.format(scope_name), 'array'))
                else:
                    self.add_elem(cur_scope, None, input_data[0])
        
    def make(self):
        output_file = open(self.file_name, 'w')

        json_data  = self.generate_json('BASE', self.init_type)
        print json_data
        output_file.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',',':')))
        output_file.close()



def print_usage_exit():
    print 'Usage: json_maker.py [FILE_NAME]'
    sys.exit(1)
 

def main():
    if len(sys.argv) < 2:
        print_usage_exit()
    jm = JsonMaker(sys.argv[1], 'object')
    jm.make()


if __name__ == '__main__':
    main()

