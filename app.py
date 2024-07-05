from flask import Flask, render_template,request
import pickle
import numpy as np

pickle_df = pickle.load(open('p.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(pickle_df['Book-Title'].values),
                           author=list(pickle_df['Book-Author'].values),
                           image=list(pickle_df['Image-URL-S'].values),
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_inp = request.form.get('title')
    indx = np.where(pt.index == user_inp)[0][0]
    res = similarity_score[indx]
    sugg = sorted(list(enumerate(res)), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in sugg:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(items)
    print(data)
    return render_template('recommend.html',data = data)


if __name__ == '__main__':
    app.run(debug=True)
