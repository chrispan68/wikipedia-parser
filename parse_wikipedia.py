from wiki_xml_handler import *
import xml.sax
import sys
import subprocess

data_path = sys.argv[1]
output = sys.argv[2]
error = sys.argv[3]
year_file = sys.argv[4]

# Object for handling xml
handler = WikiXmlHandler()
# Parsing object
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
# Iteratively process file
with open(output, 'w') as f_out:
    with open(error , 'w') as f_error:
        with open(year_file, 'w') as f_year:
            failures = 0
            for line in subprocess.Popen(['bzcat'], 
                                        stdin = open(data_path), 
                                        stdout = subprocess.PIPE).stdout:
                begin = len(handler._people)
                try:
                    parser.feed(line)
                except StopIteration:
                    break

                if len(handler._people) > begin:
                    name = handler._people[-1][0]
                    year = handler._people[-1][1]
                    summary = handler._people[-1][2]
                    year_raw = handler._people[-1][3]
                    text = handler._people[-1][4]
                    size = len(handler._people)
                    print("Current number of Biographies: " + str(size) + ". Current success rate: " + str(failures / size), end="\r")
                    if year == 'ERROR' or year == 'EMPTY' or int(year) > 2000:
                        failures += 1
                        f_error.write("========================================================\n")
                        f_error.write("== " + name + ", " + year + "==\n")
                        f_error.write(year_raw + "\n")
                        f_error.write(text + "\n")
                    else: 
                        f_year.write(year + "\n")
                        f_out.write("== " + name + ", " + year + " ==\n")
                        f_out.write(summary +"\n")
                    



        