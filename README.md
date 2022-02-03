# wordle

Run wordle offline using a python script!
Simply start the game with `python wordle.py` or `python3 wordle.py`.

You can run a version with all English words by running `python wordle.py --all`, otherwise it'll be the 1000 most common English words.

If you'd rather include the number of letters directly in the command line rather than type it in when prompted, simply run `python wordle.py --num <num-letters>` instead.

- Supports words from 3-10 letters
- Completely offline
- Words are randomly selected (could be an extremely rarely used word if you pass the --all flag)

Words taken from: https://github.com/dwyl/english-words/blob/master/words_alpha.txt and https://gist.github.com/deekayen/4148741
Wordle clone from: https://www.powerlanguage.co.uk/wordle/