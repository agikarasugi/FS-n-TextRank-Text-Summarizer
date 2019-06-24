from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from lemmatizer import Lemmatizer as indoLemmatizer
from collections import defaultdict


def fs(text, lang='indonesian', topsent=2):
    # Ubah dari paragraf menjadi kumpulan kalimat
    sentences = [sent for sent in sent_tokenize(text)]

    # pprint(sentences)

    # Postprocess setiap kalimat
    # dengan mengeleminasi angka, karakter spesial/simbol, dan stop word
    # serta lemmatize setiap kalimat
    _stopwords_ = stopwords.words(lang)
    if lang == 'indonesian':
        lemmatizer = indoLemmatizer()
    else:
        lemmatizer = WordNetLemmatizer()

    preprocessed_sentences = []

    for sentence in sentences:
        preprocessed_sent = []
        for word in word_tokenize(sentence):
            if word.isalpha() and (word.lower() not in _stopwords_):
                preprocessed_sent.append(lemmatizer.lemmatize(word.lower()))
        sentence = ' '.join(preprocessed_sent)
        preprocessed_sentences.append(sentence)

    # pprint(preprocessed_sentences)

    # Tokenisasi setiap kalimat pada preprocessed_sentences
    tokens = []
    for sent in preprocessed_sentences:
        for word in word_tokenize(sent):
            tokens.append(word)

    # pprint(tokens)

    # Hitung frekuensi dari setiap token
    token_frequency = defaultdict(float)

    for tok in tokens:
        token_frequency[tok] += 1

    # pprint(token_frequency)

    # Mengubah frekuensi menjadi weighted frequency:
    # ambil token dengan frekuensi terbesar dan simpan sebagai hf_value,
    # kemudian bagi nilai frekuensi setiap token dengan hf_value
    hf_token = (max(token_frequency, key=token_frequency.get))
    hf_value = token_frequency[hf_token]

    for x in token_frequency:
        token_frequency[x] /= hf_value

    # pprint(token_frequency)

    # Beri nilai ke setiap kalimat
    # dengan menjumlahkan weighted frequency setiap kata pada kalimat tsb.
    sentences_score = defaultdict(float)

    ori_sent_idx = 0
    for sent in preprocessed_sentences:
        sent_score = 0

        for tok in word_tokenize(sent):
            sent_score += token_frequency[tok]

        sentences_score[sentences[ori_sent_idx]] = sent_score
        ori_sent_idx += 1

    # pprint(sentences_score)

    # Urutkan kalimat berdasarkan nilai nya
    sorted_sentences = sorted(
        sentences_score.items(), key=lambda kv: kv[1], reverse=True
    )

    # Print kalimat yang sudah diringkas
    top = topsent
    if top > len(sorted_sentences):
        top = len(sorted_sentences)

    sent_res = []
    for i in range(top):
        sent_res.append(sorted_sentences[i][0] + ' ')
    return sent_res
