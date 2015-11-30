import operator

from rake import (
    Rake,
    split_sentences,
    calculate_word_scores,
    build_stop_word_regex,
    generate_candidate_keywords,
    generate_candidate_keyword_scores,
)


def test_rake():
    text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

    # Split text into sentences
    sentenceList = split_sentences(text)
    # Fox stoplist contains "numbers", so it will not find "natural numbers" like in Table 1.1
    # stoppath = "FoxStoplist.txt"

    # SMART stoplist misses some of the lower-scoring keywords in Figure 1.5, which means that the top 1/3 cuts off one of the 4.0 score words in Table 1.1
    stop_source = 'smart'
    stopwordpattern = build_stop_word_regex(stop_source)

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

    rake = Rake(stop_source)
    keywords = rake.run(text)
    print(keywords)
