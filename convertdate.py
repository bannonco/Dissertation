import datetime
import sys

def main(argv):
	file = open("newdate.txt",'w')
	print argv
	convert = argv[0]
	print convert
	date = datetime.datetime.strptime(convert, '%Y-%m-%d')
	date += datetime.timedelta(days=1)
	output = date.strftime('%Y-%m-%d')
	file.write(output)
	file.close()

if __name__ == '__main__':
	main(sys.argv[1:])