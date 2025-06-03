# New York Times Crosswords

Every New York Times crossword since Jan 1st, 1977, available in JSON format.

This repository was established as an open-source archive and a crude API, with data for a given date's crossword being available from its corresponding RAW JSON file at:
```
https://raw.githubusercontent.com/doshea/nyt_crosswords/master/#{year}/#{month}/#{day}.json
```

====

### Mind the Gap!
There are known gaps in coverage:
- **1978: Aug 10 - Nov 5**
- **2015-16: Aug 30 - May 1**

---
This README written in [Github Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)


## Fork： 
- gen.py
    - According to the json file, two files are generated in the directory:
        - XX_crossword.pdf
            include 2 pages
	    - XX_crossword_answers.pdf
		    include 1 page
- move.py
    - git clone `https://github.com/sxtiger/nyt_crosswords.git`
    - in the previous directory, create a directory `downloads/`
    - this code can move all files .json in the `nyt_crosswords/` to `downloads/`, then rename `year+month+day.json`
- batch_gen.py
    - all .json files in `downloads/` generate two .pdf files