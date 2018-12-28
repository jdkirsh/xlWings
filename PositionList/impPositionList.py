from configparser import ConfigParser
import oandapyV20
import oandapyV20.endpoints.positions as positions
import json

import sys
import csv

config = ConfigParser()
config.read('oanda.ini')

accountID = config.get('fxpractice','active_account')
client = oandapyV20.API(access_token=config.get('fxpractice','token'))

POSITIONS_FILE = 'positions.json'
POSITIONS_CSV = 'positions.csv'

reduced_item = {}
##
# Convert to string keeping encoding in mind...
##
def to_string(s):
    try:
        return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')


##
# This function converts an item like
# {
#   "item_1":"value_11",
#   "item_2":"value_12",
#   "item_3":"value_13",
#   "item_4":["sub_value_14", "sub_value_15"],
#   "item_5":{
#       "sub_item_1":"sub_item_value_11",
#       "sub_item_2":["sub_item_value_12", "sub_item_value_13"]
#   }
# }
# To
# {
#   "node_item_1":"value_11",
#   "node_item_2":"value_12",
#   "node_item_3":"value_13",
#   "node_item_4_0":"sub_value_14",
#   "node_item_4_1":"sub_value_15",
#   "node_item_5_sub_item_1":"sub_item_value_11",
#   "node_item_5_sub_item_2_0":"sub_item_value_12",
#   "node_item_5_sub_item_2_0":"sub_item_value_13"
# }
##
def reduce_item(key, value):
    # global reduced_item

    # Reduction Condition 1
    if type(value) is list:
        i = 0
        for sub_item in value:
            reduce_item(key + '_' + to_string(i), sub_item)
            i = i + 1

    # Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key + '_' + to_string(sub_key), value[sub_key])

    # Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)

def json_to_csv():
    node = 'positions'
    json_file_path = POSITIONS_FILE
    csv_file_path = POSITIONS_CSV

    fp = open(json_file_path, 'r')
    json_value = fp.read()
    raw_data = json.loads(json_value)

    try:
        data_to_be_processed = raw_data[node]
    except:
        data_to_be_processed = raw_data

    processed_data = []
    header = []
    for item in data_to_be_processed:
        reduced_item = {}
        reduce_item(node, item)

        header += reduced_item.keys()

        processed_data.append(reduced_item)

    header = list(set(header))
    header.sort()

    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

    print ("Just completed writing csv file with %d columns" % len(header))

def read_json_file(filename):
    """Accepts a file name and loads it as a json object.
    Args:
        filename   (str): Filename to be loaded.
     //   path       (str): Directory path to use.
    Returns:
        obj: json object
    """
    result = []
    try:
        with open(filename , "r") as entry:
            result = json.load(entry)
    except IOError as ex:
        print "I/O error({0}): {1}".format(ex.errno, ex.strerror)
    else:
        entry.close()
        return result


if __name__ == "__main__":

    # r = accounts.AccountDetails(accountID=config.get('fxpractice','active_account'))
    r = positions.PositionList(accountID=config.get('fxpractice', 'active_account'))
    client.request(r)
    print r.response

    with open(POSITIONS_FILE, 'w') as outfile:
        json.dump(r.response, outfile)

    jk = read_json_file(POSITIONS_FILE)
    print ('jk=',jk)
    # print ('pause')

    json_to_csv()