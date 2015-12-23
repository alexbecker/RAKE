"""
Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm as described in:

Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
Automatic keyword extraction from indi-vidual documents.
In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.
"""

import re
from collections import Counter, namedtuple, defaultdict
from string import punctuation, whitespace


#phrase_delimiters = [i for i in punctuation]
#word_delimiters = [i for i in whitespace]

WordScore = namedtuple('WordScore', ['word', 'deg', 'freq', 'score'])
KeywordScore = namedtuple('KeywordScore', ['keyword', 'sum_deg', 'sum_freq', 'score'])


class Rake(object):
	#WordScore = namedtuple('WordScore', ['word', 'deg', 'freq', 'score'])
	#KeywordScore = namedtuple('KeywordScore', ['keyword', 'sum_deg', 'sum_freq', 'score'])
	#phrase_delimiters = [i for i in punctuation]
	#word_delimiters = [i for i in whitespace]

	"""Extract keywords from a document using the Rapid Automtic Keyword Exraction (RAKE) algorithm.

	Parameters
	----------
	stop_words_source : string {'smart', 'fox'}, default='fox'
		If 'fox' uses , Fox’s stop word list (Fox 1989). len=425
		If 'smart' uses stop word list from SMART (Salton 1971). len=571
	"""
	def __init__(self, stop_words_source='fox'):
		#self.stop_words_source = stop_words_source
		self.phrase_delimiters = [i for i in punctuation]
		self.word_delimiters = [i for i in whitespace]
		self.word_scores = "Call `run` to calculate word scores"
		self.keyword_scores = "Call `run` to calculate keyword scores"


	def _load_stopword_list(self, source='fox'):
		source = source.lower().strip()
		if source == 'smart':
			from .SmartStoplist import stopwords
		elif source == 'fox':
			from .FoxStoplist import stopwords
		else:
			raise ValueError('Stopword source {} not found'.format(source))
		return stopwords


	def _generate_candidate_keywords(self, text, stopwords):
		keywords = []
		phrase_builder = []

		word_array = re.split(r'|'.join(self.word_delimiters), text)

		# newlines are split into tokens, remove them
		word_array = [word for word in word_array if word]

		for token in word_array:
			word = token.lower()

			punct_flag = word[-1] in self.phrase_delimiters
			nonempty_flag = phrase_builder != []

			if punct_flag:
				word = word[:-1]

			stopword_flag = word in stopwords

			if not stopword_flag and not punct_flag:
				phrase_builder.append(word)
			elif stopword_flag and nonempty_flag:
				phrase = ' '.join(phrase_builder)
				keywords.append(phrase)
				phrase_builder = []
			elif punct_flag and nonempty_flag:
				phrase_builder.append(word)
				phrase = ' '.join(phrase_builder)
				keywords.append(phrase)
				phrase_builder = []

		return keywords

	def _calculate_word_scores(self, candidate_keywords):
		freq_counter = Counter()
		degree_counter = defaultdict(int)

		for keyword in candidate_keywords:
			word_list = keyword.split()
			degree = len(word_list)
			freq_counter += Counter(word_list)
			for word in word_list:
				degree_counter[word] += degree

		score = {word: round(degree_counter[word] / freq_counter[word], 2) for word in degree_counter.keys()}

		word_scores = []
		for word in score.keys():
			word_tuple = WordScore(word=word,
								   deg=degree_counter[word],
								   freq=freq_counter[word],
								   score=score[word])
			word_scores.append(word_tuple)

		sorted_word_scores = sorted(word_scores, key=lambda x: x.score, reverse=True)


		self.word_scores = sorted_word_scores

		return word_scores


	def _calculate_phrase_scores(self, candidate_keywords, word_scores):
		keyword_scores = []

		candidate_keywords = list(set(candidate_keywords))

		for keyword in candidate_keywords:
			word_list = keyword.split()
			words = [WordScore for WordScore in word_scores if WordScore.word in word_list]
			keyword_tuple = KeywordScore(keyword=keyword,
										 sum_deg=sum(i.deg for i in words),
										 sum_freq=sum(i.freq for i in words),
										 score=sum(i.score for i in words))
			keyword_scores.append(keyword_tuple)

		sorted_keywords = sorted(keyword_scores, key=lambda x: x.score, reverse=True)

		return sorted_keywords

	def run(self, text):
		"""Runs the RAKE algorithm on `text`

		Parameters
		----------
		text : string
			A string object containing the text for keyword extraction

		Returns
		-------
		sorted_keywords : list of tuples, len=n_keywords
		"""
		stopwords = self._load_stopword_list(source='fox')
		candidate_keywords = self._generate_candidate_keywords(text, stopwords)

		word_scores = self._calculate_word_scores(candidate_keywords)
		self.word_scores = word_scores

		keywords = self._calculate_phrase_scores(candidate_keywords, word_scores)
		self.keyword_scores = keywords

		return keywords
