import nltk
import string
from lxml import etree
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    xml_file = r"D:\OneDrive - Universidad Peruana de Ciencias\Documentos\Estudios\Jetbrains_Academy\Python\Key" \
               r" Terms Extraction\Key Terms Extraction\task\news.xml"
    root = etree.parse(xml_file).getroot()
    news = root[0]
    lemma = nltk.stem.WordNetLemmatizer()
    vectorize = TfidfVectorizer()
    sp_pun = nltk.corpus.stopwords.words("english") + list(string.punctuation)
    document = []
    for new in news:
        word_token = nltk.tokenize.word_tokenize(new[1].text.lower())
        list_lemma = map(lambda x: lemma.lemmatize(x), word_token)
        list_lemma = map(lambda x: nltk.pos_tag([x])[0], filter(lambda x: x not in sp_pun, list_lemma))
        list_lemma = map(lambda x: x[0], filter(lambda x: x[1] == "NN", list_lemma))
        document.append(' '.join(list_lemma))
    matrix = vectorize.fit_transform(document).toarray()
    terms = list(vectorize.get_feature_names_out())

    for new, vector, doc in zip(news, matrix, document):
        print(new[0].text + ':')
        tokens = sorted(doc.split(), reverse=True)
        aux = tokens.copy()
        values = []
        for i in tokens:
            try:
                y = terms.index(i)
            except ValueError:
                aux.remove(i)
            else:
                values.append(vector[y])
        words = dict(zip(aux, values))
        print(*sorted(words, key=words.get, reverse=True)[:5], end='\n\n')


if __name__ == '__main__':
    main()
