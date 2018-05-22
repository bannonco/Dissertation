import got
import re
import sys
import codecs
import getopt
import datetime
from langdetect import detect_langs

count = 0

def main(argv):


	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.txt"

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

		#outputFile.write('username;id;date;text;mentions;hashtags;retweets;favorites;count;language')

		print('Searching...\n')

		def receiveBuffer(tweets):
			global count
			for t in tweets:
				text = t.text
				#langs = detect_langs(text)
				#lan = langs[0]
				count += 1
				if '"' in text:
					text = text.replace('"',"")
				length = len(text.split())
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
  				outputFile.write(('%d of %d DOCUMENTS\n\n' % (count,tweetCriteria.maxTweets)))
  				outputFile.write("Twitter\n\n")
  				outputFile.write(t.date.strftime("%B %d, %Y %A %I:%M %p UTC"))
  				outputFile.write("\n\n")
  				outputFile.write(("%s\n\n" % t.id))
  				outputFile.write(("BYLINE: %s\n\n" % t.username))
  				outputFile.write(("LENGTH: %d words\n\n" % length))
  				outputFile.write(("%s\n\n" % text))
  				outputFile.write(("FAVORITE: %d\n\n" % t.favorites))
  				outputFile.write(("RETWEETS: %d\n\n" % t.retweets))
  				outputFile.write(("MENTIONS: %s\n\n" % t.mentions))
  				outputFile.write(("HASHTAGS: %s\n\n" % t.hashtags))
				#outputFile.write(('\n%s;"%s";%s;"%s";%s;%s;%d;%d;%d;%s' % (t.username, t.id, t.date.strftime("%Y-%m-%d %H:%M"), text, t.mentions, t.hashtags, t.retweets, t.favorites, count, lan)))
				
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
