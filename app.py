
from random import choice

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests


# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()


# Security

import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False






def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():
    """Menu Of Page"""

    st.title("Main Menu")

    menu = ["Home","Login","Registration","About","Feedback"]
    choice = st.sidebar.selectbox("Main Menu",menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.button("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task",["Profiles"])

                if task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")





    elif choice == "Registration":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        email_id = st.text_input("email_id")
        new_password = st.text_input("Password",type='password')
        confirm_password = st.text_input("confirm password",type="password")

        if new_password == confirm_password:
            st.warning("Password not the same")


        if new_password == confirm_password:
                st.success("Valid Password Confirmed")
        else:
                st.warning("Password not the same")
        if st.button("Register"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully Registered")
            st.info("Go to Login Menu to login")









if __name__ == '__main__':
    main()














footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by Riddhi Gupta
<a style='display: block; text-align: center; target="_blank"></a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)







def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.title("Movie Recommendatation system")
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
import base64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image[1].jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://github.com/kishan0725/AJAX-Movie-Recommendation-System-with-Sentiment-Analysis/raw/master/static/image.jpg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)




if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
movie_df=pickle.load(open("movie_recm.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))
list_movie=np.array(movie_df["title"])
option = st.selectbox(

"Select Movie ",

(list_movie))

def show_url(movie):

     x=[]
     index = movie_df[movie_df['title'] == movie].index[0]

     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

     for i in distances[1:6]:

          x.append(movie_df.iloc[i[0]].urls)
     return(x)


def movie_recommend(movie):

     index = movie_df[movie_df['title'] == movie].index[0]

     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
     l=[]

     for i in distances[1:6]:
          l.append("{}".format(movie_df.iloc[i[0]].title))


          # return("{} {}".format(movie_df.iloc[i[0]].title, movie_df.iloc[i[0]].urls))
     return(l)

if st.button('Recommend Me'):

     st.write('Movies Recomended for you are:')

     # st.write(movie_recommend(option),show_url(option))

     df = pd.DataFrame({

          'Movie Recommended': movie_recommend(option),

          'Movie Url': show_url(option)

     })


     st.table(df)

if choice == "About":
    st.success("About")

st.info("About App")
if st.button("About"):
    st.text("Built with pycharm and jupyter notebook")
    st.text("you can easily search your movies")






def create_database():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='user'
    """)
    if not c.fetchone():
        c.execute('''CREATE TABLE user
                     (name text, email_id text, gender text, YourFeedback text)''')
        conn.commit()
    conn.close()


def add_user(name, email_id, gender, YourFeedback):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (name, email_id, gender, YourFeedback))
    conn.commit()
    conn.close()


def delete_user(name):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("DELETE FROM user WHERE name=?", (name,))

    conn.commit()

    conn.close()





def view_user():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user")
    user = c.fetchall()
    conn.close()
    return user





class YourFeedback:
    pass


def main():
    st.title("FeedBack")

    create_database()

    name = st.text_input("Name")
    email_id = st.text_input("Email_Id")
    gender = st.text_input("Gender")
    YourFeedback = st.text_input("YourFeedback")
    st.header("Click for operations")
    if st.button("Add"):
        add_user(name, email_id, gender, YourFeedback)







    if st.button("View"):
        user = view_user()
        st.header("User File")
        st.table(user)
    if st.button("Delete"):
        delete_user(name)

if __name__ == '__main__':
    main()