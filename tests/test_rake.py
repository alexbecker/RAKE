import operator

import pytest

from .rake import (
    Rake,
    is_number,
    split_sentences,
    load_stopword_list,
    calculate_word_scores,
    build_stop_word_regex,
    generate_candidate_keywords,
    generate_candidate_keyword_scores,
)


def test_rake():
    text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

    # Split text into sentences
    sentenceList = split_sentences(text)

    stopwords = load_stopword_list()
    stopwordpattern = build_stop_word_regex(stopwords)

    # generate candidate keywords
    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

    # calculate individual word scores
    wordscores = calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    print(keywordcandidates)

    sortedKeywords = sorted(keywordcandidates.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedKeywords)

    totalKeywords = len(sortedKeywords)
    print(totalKeywords)
    print(sortedKeywords[0:(totalKeywords // 3)])

    rake = Rake()
    keywords = rake.run(text)
    print(keywords)


# SMART stoplist misses some of the lower-scoring keywords in Figure 1.5, which means that the top 1/3 cuts off one of the 4.0 score words in Table 1.1
# Fox stoplist contains "numbers", so it will not find "natural numbers" like in Table 1.1
@pytest.mark.parametrize('source', ['fox', 'smart'])
def test_stopwords_loader(source):
    stopwords = load_stopword_list(source)
    assert stopwords
    assert type(stopwords) in (list, tuple)


def test_stopwords_loader_fails():
    stopwords = None
    with pytest.raises(ValueError):
        stopwords = load_stopword_list('nonsense')
    assert stopwords is None


def test_is_number():
    assert is_number(200)
    assert is_number(200.00)
    assert is_number(-200)
    assert is_number(-200.00)
    assert is_number('200')
    assert is_number('200.00')
    assert is_number('-200')
    assert is_number('-200.00')

    assert not is_number('My Cousin Vinny')
    assert not is_number('200 + 0.00')
    assert not is_number('My Cousin 2 Removed, Vinny')
