from configobj import ConfigObj
config = ConfigObj()
config.filename = "configTrial.txt"
#
config['keyword1'] = 'value1'
config['keyword2'] = 'value2'
#
config['section1'] = {}
config['section1']['keyword3'] = 'value3'
config['section1']['keyword4'] = 'value4'
#
section2 = {
    'keyword5': 'value5',
    'keyword6': 'value6',
    'sub-section': {
        'keyword7': 'value7'
        }
}
config['section2'] = section2
#
config['section3'] = {}
config['section3']['keyword 8'] = ['value8', 'value9', 'value10']
config['section3']['keyword 9'] = ['value11', 'value12', 'value13']
#
config.write()  