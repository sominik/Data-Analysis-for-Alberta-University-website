from keybert import KeyBERT
import matplotlib.pyplot as plt
import pandas as pd
import nltk

is_noun = lambda pos: pos[:2] == 'NN'


class KeywordExtraction:

    def __init__(self, df):
        self.df = df

    def keywords_inventory(self, column):
        stemmer = nltk.stem.SnowballStemmer("english")
        keywords_roots = dict()  # collect the words / root
        keywords_select = dict()  # association: root <-> keyword
        category_keys = []
        count_keywords = dict()
        for keyword in self.df[column]:
            if pd.isnull(keyword): continue
            lines = keyword.lower()
            tokenized = nltk.word_tokenize(lines)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

            for noun in nouns:
                noun = noun.lower()
                racine = stemmer.stem(noun)
                if racine in keywords_roots:
                    keywords_roots[racine].add(noun)
                    count_keywords[racine] += 1
                else:
                    keywords_roots[racine] = {noun}
                    count_keywords[racine] = 1

        for keyword in keywords_roots.keys():
            if len(keywords_roots[keyword]) > 1:
                min_length = 1000
                for k in keywords_roots[keyword]:
                    if len(k) < min_length:
                        clef = k
                        min_length = len(k)
                category_keys.append(clef)
                keywords_select[keyword] = clef
            else:
                category_keys.append(list(keywords_roots[keyword])[0])
                keywords_select[keyword] = list(keywords_roots[keyword])[0]
        print("Nb of keywords in variable '{}': {}".format(column, len(category_keys)))
        list_courses = []
        for k, v in count_keywords.items():
            list_courses.append([keywords_select[k], v])
        list_courses.sort(key=lambda x: x[1], reverse=True)
        self.plot_word_occurence(list_courses)
        return category_keys, keywords_roots, keywords_select, count_keywords

    def plot_word_occurence(self, courses):
        course_list = sorted(courses, key=lambda x: x[1], reverse=True)
        plt.rc('font', weight='normal')
        fig, ax = plt.subplots(figsize=(7, 25))
        y_axis = [i[1] for i in course_list[:125]]
        x_axis = [k for k, i in enumerate(course_list[:125])]
        x_label = [i[0] for i in course_list[:125]]
        plt.yticks(x_axis, x_label)
        plt.tick_params(axis='y', which='major', labelsize=3)
        plt.xlabel("Nb. of occurences", fontsize=10, labelpad=10)
        ax.barh(x_axis, y_axis, align='center')
        ax = plt.gca()
        ax.invert_yaxis()
        plt.title("Words occurrence", bbox={'facecolor': 'k', 'pad': 5}, color='w', fontsize=15)
        plt.show()
