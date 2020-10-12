
def print_stuff(splitt):
    for s in "200, 204, 208, 20C, 2F4, 2F0, 200, 204, 218, 21C, 24C, 2F4".split(', '):
        x = int(s, 16)
        binray = "{0:12b}".format(x)
        tag, cache_index, byte_select = splitt(binray)
        print(s, '\\_'.join(splitt(binray)), tag + " ({0:2x})".format(int(tag, 2)), 
                cache_index + " ({0:1x})".format(int(cache_index, 2)),
                byte_select + " ({0:1x})".format(int(byte_select, 2)),
                end='\\\\\n', sep=' & ')

print_stuff(lambda s: (s[0:7], s[7:10],  s[10:12]))
print('two way')
print_stuff(lambda s: (s[0:8], s[8:10],  s[10:12]))
print('three way')
print_stuff(lambda s: (s[0:9], s[9:10],  s[10:12]))
print(set("200, 204, 208, 20C, 2F4, 2F0, 200, 204, 218, 21C, 24C, 2F4".split(', ')))
