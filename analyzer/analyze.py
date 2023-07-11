import psycopg2
import re
import matplotlib.pyplot as plt
from statistics import mean
from nltk.corpus import stopwords
import nltk
import pandas as pd


class Analyze:

    @staticmethod
    def count_avg_rating(name_company, id):
        trans_table = {ord('('): None, ord('\''): None, ord(')'): None, ord(','): None}
        conn = psycopg2.connect(
            user="postgres",
            password="qwerty1234",
            host="localhost",
            port="5432",
            database="test"
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT date FROM web_review where company_id = {id} order by id")
        rows = cursor.fetchall()
        date = []
        for row in rows:
            stroka = str(row).split(',')
            date.append([i.translate(trans_table) for i in stroka])

        for d in date:
            for i in d:
                date[date.index(d)][d.index(i)] = i.replace('год', '')
                i = i.replace('год', '')
                date[date.index(d)][d.index(i)] = re.sub(r'^\d{1,2}\s', '', i).strip()
                if '' == i:
                    d.remove(i)

        cursor.execute(f"SELECT rate FROM web_review where company_id = {id} order by id")
        rows = cursor.fetchall()
        for row, d in zip(rows, date):
            row = str(row).translate(trans_table)
            d.append(row)

        dict_rate = {}
        ratings = []
        for index in range(len(date) - 1):
            if date[index][0] + date[index][1] == date[index + 1][0] + date[index + 1][1]:
                ratings.append(date[index][2])
            else:
                ratings.append(date[index][2])
                dict_rate[date[index][0] + date[index][1]] = ratings
                ratings = []
            if index == len(date) - 2:
                if date[index][0] + date[index][1] == date[index - 1][0] + date[index + 1][1]:
                    ratings.append(date[index][2])
                    dict_rate[date[index][0] + date[index][1]] = ratings
                    ratings = []
                else:
                    ratings = [date[index][2]]
                    dict_rate[date[index][0] + date[index][1]] = ratings

        for key, arr in dict_rate.items():
            arr_int = []
            for a in arr:
                arr_int.append(int(a))
            dict_rate[key] = arr_int

        for key, arr in dict_rate.items():
            avg_rate = mean(arr)
            dict_rate[key] = round(avg_rate, 2)

        labels = list(dict_rate.keys())

        insert_query = '''
            insert into web_dataanalyze (name_analyze, title, labels, values, name_company, company_id)
            values (%s, %s, %s, %s, %s, %s)
        '''

        data = ('Средний рейтинг', 'avg_rating', labels, list(dict_rate.values()), name_company, id)

        cursor.execute(insert_query, data)

        conn.commit()

        cursor.close()
        conn.close()

        # plt.figure(figsize=(9, 8.15))
        # plt.plot(labels, dict_rate.values())
        # plt.xlabel('Месяца')
        # plt.xticks(rotation=45)
        # plt.ylabel('Средний рейтинг')
        # plt.title('Среднемесячный рейтинг')
        #
        # plt.savefig(f'media/{name_company}/{name_company}_avg_rating.png')

    @staticmethod
    def rating_distribution(name_company, id):
        trans_table = {ord('('): None, ord('\''): None, ord(')'): None, ord(','): None}
        conn = psycopg2.connect(
            user="postgres",
            password="qwerty1234",
            host="localhost",
            port="5432",
            database="test"
        )
        cursor = conn.cursor()
        cursor.execute(f"select count(*) from web_review where rate = 1 and company_id = {id}"
                       "union all select "
                       f"count(*) from web_review where rate = 2 and company_id = {id} "
                       "union all select "
                       f"count(*) from web_review where rate = 3 and company_id = {id} "
                       "union all select "
                       f"count(*) from web_review where rate = 4 and company_id = {id} "
                       "union all "
                       f"select count(*) from web_review where rate = 5 and company_id = {id}")
        rows = cursor.fetchall()

        ratings = []
        for row in rows:
            row = str(row).translate(trans_table)
            ratings.append(int(row))

        labels = ['1', '2', '3', '4', '5']
        x = range(len(ratings))
        plt.bar(x, ratings)
        plt.xticks(x, labels)
        plt.xlabel('Оценка рейтинга')
        plt.ylabel('Количество оценок')
        plt.title('Распределение рейтинга')

        insert_query = '''
            insert into web_dataanalyze (name_analyze, title, labels, values, name_company, company_id)
            values (%s, %s,  %s, %s, %s, %s)
        '''

        data = ('Распределение рейтинга', 'rating_distribution', labels, ratings, name_company, id)

        cursor.execute(insert_query, data)

        conn.commit()

        cursor.close()
        conn.close()
        # plt.savefig(f'media/{name_company}/{name_company}_rating_distribution.png')

    @staticmethod
    def bigrams(name_company, id, mark):
        conn = psycopg2.connect(
            user="postgres",
            password="qwerty1234",
            host="localhost",
            port="5432",
            database="test"
        )
        cursor = conn.cursor()
        name_analyze = ''
        title = ''
        if mark:
            cursor.execute(
                f"select description from web_review where company_id = {id} and rate between 4 and 5 order by id")
            name_analyze = 'Биграммы для отзывов с оценками 4-5'
            title = 'bigrams_good_grades'
        else:
            cursor.execute(
                f"select description from web_review where company_id = {id} and rate between 1 and 3 order by id")
            name_analyze = 'Биграммы для отзывов с оценками 1-3'
            title = 'bigrams_bad_grades'
        rows = cursor.fetchall()
        reviews = []

        for row in rows:
            reviews.append(str(row))
        tokenizer = nltk.tokenize.RegexpTokenizer('\w+')

        tokens = tokenizer.tokenize(pd.Series(reviews).str.cat(sep=' ').lower())

        nltk.download('stopwords')
        sw = stopwords.words('russian')

        words_ns_b = []

        for word in tokens:
            if word in sw:
                next
            else:
                words_ns_b.append(word)

        from nltk.stem import WordNetLemmatizer
        wordnet_lemmatizer = WordNetLemmatizer()

        lem_words_b = []
        for word in words_ns_b:
            lem_words_b.append(wordnet_lemmatizer.lemmatize(word, 'v'))

        bigrm = nltk.bigrams(lem_words_b)
        bigrm_txt = [bi for bi in bigrm]

        freqdist = nltk.FreqDist(bigrm_txt)
        # plt.figure(figsize=(20, 5))
        # freqdist.plot(30)
        # plt.show()


        insert_query = '''
            insert into web_dataanalyze (name_analyze, title, labels, values, name_company, company_id)
            values (%s, %s, %s, %s, %s, %s)
        '''

        data = (name_analyze, title, list(freqdist.keys()), list(freqdist.values()), name_company, id)

        cursor.execute(insert_query, data)

        conn.commit()

        cursor.close()
        conn.close()


Analyze.count_avg_rating('beeline', 4)
Analyze.rating_distribution('beeline', 4)
Analyze.bigrams('beeline', 4, False)
Analyze.bigrams('beeline', 4, True)
