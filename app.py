from flask import Flask,render_template,request
import pickle
import numpy as np

top_events_info = pickle.load(open('top_events_f.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
events_data = pickle.load(open('events_data_f.pkl','rb'))
similarity_scores_final = pickle.load(open('similarity_scores_final.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Load top events information from the pickle file


    return render_template('index.html',
                           event_name=list(top_events_info['Event Name'].values),
                           category=list(top_events_info['Category'].values),
                           Images=list(top_events_info['Images'].values),
                           Date=list(top_events_info['Date'].values),
                           ratings=list(top_events_info['Ratings'].values)                                 
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(events_data['Event Name'] == user_input)[0][0]
    similar_events = sorted(list(enumerate(similarity_scores_final[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_events:
        item = []
        temp_df = events_data.iloc[i[0]]
        item.append(temp_df['Event Name'])
        item.append(temp_df['Category'])
        item.append(temp_df['Ratings'])
        item.append(temp_df['Attendee Count'])
        item.append(temp_df['Images'])
        item.append(temp_df['Tags/Keywords']) 
        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)