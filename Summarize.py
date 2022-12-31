import spacy

from spacy.lang.en.stop_words import STOP_WORDS

from string import punctuation

from heapq import nlargest


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')  # importing pre-processed pipeline
    doc = nlp(text)
    # loading each token into a tokens list
    tokens = [token.text for token in doc]
    word_frequences = {}
    for word in doc:
        temp_word = word.text
        if temp_word.lower() not in list(STOP_WORDS) and temp_word.lower() not in punctuation:
            if temp_word not in word_frequences.keys():
                word_frequences[temp_word] = 1
            else:
                word_frequences[temp_word] += 1
    if len(word_frequences) <= 30:
        return text
    max_frequency = max(word_frequences.values())
    for word in word_frequences.keys():
        word_frequences[word] = word_frequences[word]/max_frequency

    sentence_tokens = [sentence for sentence in doc.sents]
    sentence_scores = {}

    for sentence in sentence_tokens:
        for word in sentence:
            if word.text.lower() in word_frequences.keys():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequences[word.text.lower()]
                else:
                    sentence_scores[sentence] += word_frequences[word.text.lower()]

    select_length = int(len(sentence_tokens)*per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = " "
    for i in final_summary:
        summary += i.strip() + " "
    summary = summary.strip()
    return summary
