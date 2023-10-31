import mlxtend
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from keywordExtraction import KeywordExtraction
# from apyori import apriori as apriori1
# from pyECLAT import ECLAT
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


class Process:
    def __init__(self, path):
        self.data = pd.read_csv(path, encoding="cp1252")
        self.courses = pd.DataFrame(self.data)
        self.symbols = {}
        self.lemmatizer = WordNetLemmatizer()

    def drop_null_values(self):
        self.courses.dropna(axis=1, how='all', inplace=True)

    def convert_objects(self):
        object_cols = ['department_name']
        for col in object_cols:
            self.symbols.update({f'{col}': {}})
            count = 0
            for k in self.courses[f'{col}'].unique():
                self.courses[f'{col}'] = self.courses[f'{col}'].replace([f'{k}'], count)
                self.symbols[f'{col}'][f'{k}'] = count
                count = count + 1

    def clean_text(self,column_name):
        self.courses[f'{column_name}'] = self.courses[f'{column_name}'].apply(self.tokenize_text)
        KeywordExtraction(self.courses).keywords_inventory(f'{column_name}')

    def drop_useless_cols(self):
        object_cols = ['university', 'abbreviation', 'university_homepage', 'course_homepage']
        for col in object_cols:
            self.courses.drop(f'{col}', axis=1, inplace=True)

    def tokenize_text(self, text):
        tokenize_content = nltk.word_tokenize(str(text).lower())
        tokens = self.remove_stop_word_and_lema(tokenize_content)
        return tokens

    def remove_stop_word_and_lema(self, tokenize_content):
        stop_words = stopwords.words('english') + list(punctuation)
        tokens = []
        for token in tokenize_content:
            if token not in stop_words:
                tokens.append(self.lemmatizer.lemmatize(token))
        return ' '.join(tokens)

    def convert_null_desc(self):
        fill_nan_value = "no description"
        self.courses = self.courses.fillna({"description": fill_nan_value})

    def convert_null_prerequisite(self):
        fill_nan_value = "nothing"
        self.courses = self.courses.fillna({"prerequisite": fill_nan_value})

    def reset_index_in_frame(self):
        self.courses.reset_index(inplace=True, drop=True)

    def convert_unit_count(self):
        counter = 0
        for row in self.courses['unit_count']:
            units = row.split("-")
            if len(units) == 1:
                units = float(units[0])
            else:
                min_unit = float(units[0])
                max_unit = float(units[1])
                units = (min_unit+max_unit)/2
            self.courses.loc[counter].at['unit_count'] = units
            counter += 1
        self.courses = self.courses.astype({"unit_count": "float"})

    def remove_extra_lines(self):
        self.courses.dropna(inplace=True, axis=0)

    def sorted_by_department_name(self):
        sorted = self.courses.sort_values(by='department_name')
        print(sorted)

    def get_info(self):
        print(self.courses.info())

    def describe(self):
        print(self.courses.describe())

    def remove_outlier(self):
        int_float_cols = self.courses.select_dtypes(['int64', 'float64'])
        index_array = []
        for col in int_float_cols:
            Q1 = self.courses[f"{col}"].quantile(0.25)
            Q3 = self.courses[f"{col}"].quantile(0.75)
            IQR = Q3 - Q1
            for i in self.courses.index:
                data = self.courses[f"{col}"][i]
                if data < Q1 - 1.5*IQR or data > Q3 + 1.5*IQR:
                    index_array.append(i)
            self.courses.drop(index=index_array, inplace=True)

    def get_stat(self):
        print("departments & number of courses: ")
        courses_count = self.courses.groupby('department_name').size()
        print(courses_count)
        departments = {"department_name": self.courses['department_name'].unique()}
        departments_frame = pd.DataFrame(departments)
        unit_counts = []
        unit_counts_mean = []
        for department in self.courses["department_name"].unique():
            unit_count_sum = self.courses['unit_count'][self.courses["department_name"] == department].sum()
            unit_count_mean = self.courses['unit_count'][self.courses["department_name"] == department].mean()
            unit_counts.append(unit_count_sum)
            unit_counts_mean.append(unit_count_mean)
        departments_frame["unit_count_sum"] = unit_counts
        departments_frame["unit_count_mean"] = unit_counts_mean
        print("-----------------------------------------------------")
        print(departments_frame)
        print("-----------------------------------------------------")

    def print_courses(self):
        print(self.courses.size)
        print(self.courses.columns)
        print(self.courses)

    def circular_plt(self):
        labels = self.courses["department_name"].unique()
        unit_counts = []
        for department in self.courses["department_name"].unique():
            unit_count_sum = self.courses['unit_count'][self.courses["department_name"] == department].sum()
            unit_counts.append(unit_count_sum)
        plt.pie(unit_counts, labels=labels)
        plt.show()

    def bar_plt(self):
        index = self.courses["department_name"].unique()
        unit_counts = []
        for department in self.courses["department_name"].unique():
            unit_count_sum = self.courses['unit_count'][self.courses["department_name"] == department].mean()
            unit_counts.append(unit_count_sum)
        plt.bar(index, unit_counts)
        plt.show()


process = Process('./UAlberta.csv')
process.drop_null_values()
process.drop_useless_cols()
process.convert_null_desc()
process.convert_null_prerequisite()
process.remove_extra_lines()
process.reset_index_in_frame()
process.convert_unit_count()

process.get_stat()
process.describe()
process.sorted_by_department_name()

process.convert_objects()
process.clean_text('description')
process.clean_text('prerequisite')

process.print_courses()
process.get_info()
process.remove_outlier()
process.print_courses()
process.circular_plt()
process.bar_plt()
