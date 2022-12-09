from flask import Flask,render_template,request
import numpy as np
import pickle

popular=pickle.load(open("popular.pkl",'rb'))
pivot=pickle.load(open("pivot.pkl",'rb'))
books=pickle.load(open("books.pkl",'rb'))
score=pickle.load(open("score.pkl",'rb'))
pivot1=pickle.load(open("pivot1.pkl",'rb'))
score1=pickle.load(open("score1.pkl",'rb'))
pivot2=pickle.load(open("pivot2.pkl",'rb'))
score2=pickle.load(open("score2.pkl",'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_ratings'].values),
                           rating=list(popular['Avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pivot.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

@app.route('/recommend by Author')
def recommended_ui():
    return render_template('recommend by Author.html')

# @app.route('/Top 25 Author')
# def Top_Authors():
#     return render_template('Top 25 Author.html',
#                            Country_name=list(topAuthors['Book-Author'].values),
#                            num_ratings=list(topAuthors['Number of ratings'].values),
#                            Avg_rating=list(topAuthors['Avg-ratings'].values)
#                            )

@app.route('/recommend_books_by_Author',methods=['post'])
def recommended():
    user_input = request.form.get('user_input')
    index = np.where(pivot1.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(score1[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Author'] == pivot1.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Author')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Author')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Author')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend by Author.html',data=data)



@app.route('/recommend by Publisher')
def recommendation_ui():
    return render_template('recommend by Publisher.html')

@app.route('/recommend_books_by_Publisher',methods=['post'])
def recommendation():
    user_input = request.form.get('user_input')
    index = np.where(pivot2.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(score2[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Publisher'] == pivot2.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Publisher')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Publisher')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Publisher')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend by Publisher.html',data=data)


if __name__=='__main__':
    app.run(debug=True, port=8080)

