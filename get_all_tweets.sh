#!/bin/sh

while IFS='' read -r line || [[ -n "$line" ]]; do
	python convertdate.py $line
	value=`cat newdate.txt`
    python pull_tweets.py --since $line --until $line --querysearch "brexit" --toptweets --maxtweets 1000 --output "brexit_$line.csv.csv"
done < "$1"