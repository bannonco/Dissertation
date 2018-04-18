#!/bin/sh

while IFS='' read -r line || [[ -n "$line" ]]; do
	python convertdate.py $line
	value=`cat newdate.txt`
    python pull_tweets.py --since $line --until $value --querysearch "brexit" --toptweets --maxtweets 100 --output "brexit_$line.txt"
done < "$1"
