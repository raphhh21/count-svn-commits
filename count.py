import os;
import sys;
import csv;
import requests;
import xml.etree.ElementTree as ET;
from operator import itemgetter;

def parse(xml_string):
    # list of dictionaries to return
    entries = [];
    root = ET.fromstring(xml_string);
    for child in root.iter('author'):
        tmp_dict = {};
        tmp_dict[child.tag] = child.text;
        entries.append(tmp_dict);
    return entries;
        
# main func
if __name__ == "__main__":
    # invalid usage
    if (len(sys.argv) != 2):
        print("Usage: python3 count.py SVN_DIR");
        exit;
    
    # valid usage
    pipe = os.popen("svn log -v --xml " + sys.argv[1]);
    svn_log = pipe.read();

    # parse xml
    try:
        entries = parse(svn_log);
        # count
        author_count = {};
        total_count = 0;
        for dict_inside in entries:
            total_count += 1;
            author_name = dict_inside["author"];
            if author_name in author_count:
                author_count[author_name] += 1;
            else:
                author_count[author_name] = 1;
        # sort by count
        author_count = dict(sorted(author_count.items(), key=itemgetter(1)));
        # add total count
        author_count["TOTAL"] = total_count;
        # print
        for author, count in author_count.items():
            print(f'{author:<22} {count}');

    except ET.ParseError:
        print("Usage: python3 count.py SVN_DIR");
        