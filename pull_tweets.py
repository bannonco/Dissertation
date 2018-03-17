import got
import re
import sys
import codecs
import getopt
import datetime

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
		
		outputName = "data/"+outputFileName	
		outputFile = codecs.open(outputName, "w+", "utf-8")

		outputFile.write('username;id;date;text;mentions;hashtags;retweets;favorites')

		print('Searching...\n')

		def receiveBuffer(tweets):
			for t in tweets:
				text = t.text
				text = text.replace('\n', ' ')
				#if 'http' in text:
				#	text = re.sub(r"http\S+", "", text)
				#if '#' in text:
				#	text = text.replace("#"," ")
				#if '@' in text:
				#	text = re.sub(r"@\w+","",text)
				#regexp = re.compile(r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:% _\+.~#?&//=]*)')
				#if regexp.search(text):
				#	index = regexp.search(text).start()
  				#	text = re.sub(regexp,"",text)
				outputFile.write(('\n%s;"%s";%s;"%s";%s;%s;%d;%d' % (t.username, t.id, t.date.strftime("%Y-%m-%d %H:%M"), text, t.mentions, t.hashtags, t.retweets, t.favorites)))
			outputFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
