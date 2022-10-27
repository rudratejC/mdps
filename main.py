import pickle
import streamlit as st
import pyrebase
from datetime import datetime

selected = 'None'
diab_res = ''
# Configuration Key
firebaseConfig = {
  'apiKey': "AIzaSyA3w4vMYA9yoCrVUOxpQEP-ZdRcCFRACtA",
  'authDomain': "maps-5444e.firebaseapp.com",
  'projectId': "maps-5444e",
  'databaseURL':
  "https://maps-5444e-default-rtdb.asia-southeast1.firebasedatabase.app/",
  'storageBucket': "maps-5444e.appspot.com",
  'messagingSenderId': "1066848782898",
  'appId': "1:1066848782898:web:cdc8a82aecca5cf69c8a2b",
}
#from streamlit_option_menu import option_menu

# loading the saved models

diabetes_model = pickle.load(open('saved/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('saved/heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open('saved/parkinsons_model.sav', 'rb'))

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("Multiple Disease Prediction")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

# Sign up Block
if choice == 'Sign up':
  handle = st.sidebar.text_input('Please input your app handle name',
                                 value='Default')
  submit = st.sidebar.button('Create my account')

  if submit:
    user = auth.create_user_with_email_and_password(email, password)
    st.success('Your account is created suceesfully!')
    st.balloons()
    # Sign in
    user = auth.sign_in_with_email_and_password(email, password)
    db.child(user['localId']).child("Handle").set(handle)
    db.child(user['localId']).child("ID").set(user['localId'])
    st.title('Welcome' + handle)
    st.info('Login via login drop down selection')

# Login Block
if choice == 'Login':
  login = st.sidebar.checkbox('Login')
  if login:
    user = auth.sign_in_with_email_and_password(email, password)
    st.write(
      '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
      unsafe_allow_html=True)
    selected = st.radio(
      'Jump to',
      ['Diabetes Prediction', 'Parkinsons Prediction', 'Previous Results'],
    )

# sidebar for navigation
# with st.sidebar:

# selected = option_menu(
#   'Disease Prediction Application',
#   ['Parkinsons Prediction', 'Diabetes Prediction', 'Heart Disease Prediction'],
#   icons=['person', 'activity', 'heart'],
#   default_index=0,
#   orientation="horizontal",
#   styles={
#     "nav-link": {
#       "font-size": "30px",
#       "text-align": "center"
#     },
#     "icon": {
#       "color": "orange",
#       "font-size": "25px"
#     },
#     "nav-link-selected": {
#       "background-color": "blue"
#     },
#   })
# selected = 'Parkinsons Prediction'


# selected = st.selectbox("Hello Select Disease",
#                         ('Diabetes Prediction', 'Parkinsons Prediction'))
# Diabetes Prediction Page
def addPostPark(fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA,
                spread1, spread2, D2, PPE, parkinsons_diagnosis):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  post = {
    'result': parkinsons_diagnosis,
    'fo': fo,
    'fhi': fhi,
    'flo': flo,
    'Jitter_percent': Jitter_percent,
    'Jitter_Abs': Jitter_Abs,
    'RAP': RAP,
    'PPQ': PPQ,
    'DDP': DDP,
    'Shimmer': Shimmer,
    'Shimmer_dB': Shimmer_dB,
    'APQ3': APQ3,
    'APQ5': APQ5,
    'APQ': APQ,
    'DDA': DDA,
    'NHR': NHR,
    'HNR': HNR,
    'RPDE': RPDE,
    'DFA': DFA,
    'spread1': spread1,
    'spread2': spread2,
    'D2': D2,
    'PPE': PPE
  }
  results = db.child(user['localId']).child("Posts").push(post)
  st.success('Your Data has been stored suceesfully!')


def addPost(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
            DiabetesPedigreeFunction, Age, diab_diagnosis):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  post = {
    'result': diab_diagnosis,
    'Pregnancies': Pregnancies,
    'Glucose': Glucose,
    'BloodPressure': BloodPressure,
    'SkinThickness': SkinThickness,
    'Insulin': Insulin,
    'BMI': BMI,
    'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
    'Age': Age
  }
  results = db.child(user['localId']).child("Posts").push(post)
  st.success('Your Data has been stored suceesfully!')


if (selected == 'Previous Results'):
  all_posts = db.child(user['localId']).child("Posts").get()
  if all_posts.val() is not None:
    for Posts in reversed(all_posts.each()):
      st.code(Posts.val(), language='')

if (selected == 'Diabetes Prediction'):

  # page title
  st.title('Diabetes Prediction  ')

  # getting the input data from the user
  col1, col2, col3 = st.columns(3)

  with col1:
    gen = st.select_slider("Gender:", ["Male", "Female"])
    if (gen == 'Female'):
      Pregnancies = st.text_input('Number of Pregnancies')
    else:
      Pregnancies = 0

  with col2:
    Glucose = st.text_input('Glucose Level')

  with col3:
    BloodPressure = st.text_input('Blood Pressure value')

  with col1:
    SkinThickness = st.text_input('Skin Thickness value')

  with col2:
    Insulin = st.text_input('Insulin Level')

  with col3:
    BMI = st.text_input('BMI value')

  with col1:
    DiabetesPedigreeFunction = st.text_input(
      'Diabetes Pedigree Function value')

  with col2:
    Age = st.text_input('Age of the Person')

  # code for Prediction
  diab_diagnosis = ''

  # creating a button for Prediction

  if st.button('Diabetes Test Result'):
    diab_prediction = diabetes_model.predict([[
      Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
      DiabetesPedigreeFunction, Age
    ]])
    if (diab_prediction[0] == 1):
      diab_diagnosis = 'The person is diabetic'
      addPost(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
              DiabetesPedigreeFunction, Age, diab_diagnosis)
    else:
      diab_diagnosis = 'The person is not diabetic'
      addPost(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
              DiabetesPedigreeFunction, Age, diab_diagnosis)
  st.success(diab_diagnosis)

  #add_post = st.button('Save to Database')
  # if add_post:
  #   now = datetime.now()
  #   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  #   post = {
  #     'result': diab_res,
  #     'Timestamp': dt_string,
  #     'Pregnancies': Pregnancies,
  #     'Glucose': Glucose,
  #     'BloodPressure': BloodPressure,
  #     'SkinThickness': SkinThickness,
  #     'Insulin': Insulin,
  #     'BMI': BMI,
  #     'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
  #     'Age': Age
  #   }
  #   results = db.child(user['localId']).child("Posts").push(post)
  #   st.success('Your Data has been stored suceesfully!')

if (selected == 'None'):
  st.title('Please SignUp or Login')
# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):

  # page title
  st.title('Heart Disease Prediction  ')

  col1, col2, col3 = st.columns(3)

  with col1:
    age = st.text_input('Age')

  with col2:
    sex = st.text_input('Sex')

  with col3:
    cp = st.text_input('Chest Pain types')

  with col1:
    trestbps = st.text_input('Resting Blood Pressure')

  with col2:
    chol = st.text_input('Serum Cholestoral in mg/dl')

  with col3:
    fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

  with col1:
    restecg = st.text_input('Resting Electrocardiographic results')

  with col2:
    thalach = st.text_input('Maximum Heart Rate achieved')

  with col3:
    exang = st.text_input('Exercise Induced Angina')

  with col1:
    oldpeak = st.text_input('ST depression induced by exercise')

  with col2:
    slope = st.text_input('Slope of the peak exercise ST segment')

  with col3:
    ca = st.text_input('Major vessels colored by flourosopy')

  with col1:
    thal = st.text_input(
      'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

  # code for Prediction
  heart_diagnosis = ''

  # creating a button for Prediction

  if st.button('Heart Disease Test Result'):
    heart_prediction = heart_disease_model.predict([[
      age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,
      slope, ca, thal
    ]])

    if (heart_prediction[0] == 1):
      heart_diagnosis = 'The person is having heart disease'
    else:
      heart_diagnosis = 'The person does not have any heart disease'

  st.success(heart_diagnosis)

# Parkinson's Prediction Page
if (selected == "Parkinsons Prediction"):

  # page title
  st.title("Parkinson's Disease Prediction  ")

  col1, col2, col3, col4, col5 = st.columns(5)

  with col1:
    fo = st.text_input('MDVP:Fo(Hz)')

  with col2:
    fhi = st.text_input('MDVP:Fhi(Hz)')

  with col3:
    flo = st.text_input('MDVP:Flo(Hz)')

  with col4:
    Jitter_percent = st.text_input('MDVP:Jitter(%)')

  with col5:
    Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

  with col1:
    RAP = st.text_input('MDVP:RAP')

  with col2:
    PPQ = st.text_input('MDVP:PPQ')

  with col3:
    DDP = st.text_input('Jitter:DDP')

  with col4:
    Shimmer = st.text_input('MDVP:Shimmer')

  with col5:
    Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

  with col1:
    APQ3 = st.text_input('Shimmer:APQ3')

  with col2:
    APQ5 = st.text_input('Shimmer:APQ5')

  with col3:
    APQ = st.text_input('MDVP:APQ')

  with col4:
    DDA = st.text_input('Shimmer:DDA')

  with col5:
    NHR = st.text_input('NHR')

  with col1:
    HNR = st.text_input('HNR')

  with col2:
    RPDE = st.text_input('RPDE')

  with col3:
    DFA = st.text_input('DFA')

  with col4:
    spread1 = st.text_input('spread1')

  with col5:
    spread2 = st.text_input('spread2')

  with col1:
    D2 = st.text_input('D2')

  with col2:
    PPE = st.text_input('PPE')

  # code for Prediction
  parkinsons_diagnosis = ''

  # creating a button for Prediction
  if st.button("Parkinson's Test Result"):
    parkinsons_prediction = parkinsons_model.predict([[
      fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer,
      Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2,
      D2, PPE
    ]])

    if (parkinsons_prediction[0] == 1):
      parkinsons_diagnosis = "The person has Parkinson's disease"
      addPostPark(fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                  Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE,
                  DFA, spread1, spread2, D2, PPE, parkinsons_diagnosis)
    else:
      parkinsons_diagnosis = "The person does not have Parkinson's disease"
      addPostPark(fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                  Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE,
                  DFA, spread1, spread2, D2, PPE, parkinsons_diagnosis)
  st.success(parkinsons_diagnosis)
