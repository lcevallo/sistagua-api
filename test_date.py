# from pygrok import Grok

# input_string = '2021-04-07T05:00:00.000Z'
# date_pattern = '%{YEAR:year}-%{MONTHNUM:month}-%{MONTHDAY:day}'
# date_pattern = '%{YEAR:year}-%{MONTHNUM:month}-%{MONTHDAY:day}'

# grok = Grok(date_pattern)
# print(grok.match(input_string))

import re, datetime
s = "I have a meeting on 2021-04-07T05:00:00.000Z in New York"
match = re.search('\d{4}-\d{2}-\d{2}', s)
date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
print(date)