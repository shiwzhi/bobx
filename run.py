import sys
import bobx

home_url = sys.argv[1]
filename = sys.argv[2]


jpg = bobx.from_home_get_large_jpg(home_url)

f = open(filename, 'a')
for i in jpg:
	f.write(i+'\n')
f.close()