RAKE
====

A Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm as described in: Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons.

The source code is released under the MIT License.

### Updates from [aneesha/RAKE](https://github.com/aneesha/RAKE)
  - Complete rewrite of the `Rake` class.
    - Cleaned up code by using tools from python's `collections` lib (`Counter` and `defaultdict`)
    - Methods now exist inside the `Rake` class, no need for them to be exposed outside (though they can still be called if need be
    - Rewrote the existing string tokenizer based on the process listed in the original paper (ie. *"First, the document text is split into an array of words by the specified word delimiters. This array is then split into sequences of contiguous words at phrase delimiters and stop word positions."*)
    - Uses the `fox` stopword list by default, since it returns results more similar to the *abstract* used as an example in the original paper, and the `smart` stopword list is overkill
    - `Rake.run()` can now take a tokenized list of words as input for alternative tokenizer use
    - `Rake.run()` now returns a sorted list of `namedtuple KeywordScores`, sorted by overall score and also containing `sum_deg` and `sum_freq` metrics. These can also be accessed via the `Rake.keyword_scores` attribute after a call to `Rake.run()`
    - `Rake.word_scores` is a class attribute that returns a sorted list of `namedtuple WordScores`, sorted by overall score and containing `deg` and `freq` metrics, available after calling `Rake.run()`
  - Package should be almost ready to install from pypi or github (thanks to [@tomaspinho](https://github.com/tomaspinho/python-rake) and [@fabinvf](https://github.com/fabianvf/RAKE/tree/develop]))

### To-Do:
 - Develop some tests and make sure we're legit
 - Add adjoining features functionality (two potential keywords split by a stopword) https://github.com/aneesha/RAKE/issues/8

Development
===========
Dependencies for development are specified in the dev-requirements.txt file. You can install them with
`pip install -r dev-requirements.txt`. You can run the tests with `py.test tests` after the requirements
are installed.
