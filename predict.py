import sys
import json


input_data = json.loads(sys.argv[1])


prediction = {'result': 'Your prediction goes here'}

print(json.dumps(prediction))
