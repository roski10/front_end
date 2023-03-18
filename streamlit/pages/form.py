# this page is the form the client to file in

import streamlit as st
import numpy as np
import pandas as pd
from streamlit_player import st_player
import joblib as jl


#Embed the music
audio_file = open('media_files/GTA-song.mp3', 'rb')
audio_bytes = audio_file.read()
#st.audio(audio_bytes, format='audio/ogg')
import base64
import time
mymidia_placeholder = st.empty()
mymidia_str = "data:audio/ogg;base64,%s"%(base64.b64encode(audio_bytes).decode())
mymidia_html = """
                <audio autoplay class="stAudio">
                <source src="%s" type="audio/ogg">
                Your browser does not support the audio element.
                </audio>
            """%mymidia_str
mymidia_placeholder.empty()
time.sleep(1)
mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)


def main():
    st.title("GTA Mortgage approval form")
    menu = ["app","form","credit"]
    choice = st.sidebar.selectbox("Menu",menu)
    with st.form(key='form1'):
        loan_amount = st.number_input('Insert the amount of money to borrow in 000s')
        loan_purpose_name = st.selectbox('What is the purpose of the loan?',(' ','Refinancing', 'Home purchase', 'Home improvement'))
        lien_status_name = st.selectbox('What is the lien status of the loan?',(' ','Secured by a first lien', 'Secured by a subordinate lien', 'Not secured by a lien'))
        loan_type_name = st.selectbox('What is the type of loan you are applying for?',(' ','Conventional','FHA-insured', 'VA-guaranteed', 'FSA/RHS-guaranteed'))
        principal_dwelling = st.selectbox('Does the Owner intend to occupy the property as their principal dwelling?',(' ','Yes', 'No'))
        property_region = st.selectbox('What is the region of the property?',(' ','Northern Cascades','Western  Region','Eastern Washington', 'Southwest Washington','Olympic peninsula'))
        main_applicant_full_name = st.text_input("Full name of main applicant")
        co_applicant_full_name = st.text_input("Full name of co applicant")
        main_dob = st.date_input("Date of Birth")
        co_dob = st.date_input("Date of Birth")
        main_app_gender = st.selectbox('What is the gender of the main applicant?',(' ','male', 'female'))
        co_app_gender = st.selectbox('What is the gender of the co applicant?',(' ','male', 'female'))
        main_app_ethnicity = st.selectbox('What is the ethnicity of the main applicant?',(' ','White', 'Asian','Black or African American', 'Native Hawaiian or Other Pacific Islander','American Indian or Alaska Native'))
        co_app_ethnicity = st.selectbox('What is the ethnicity of the co applicant?',(' ','White', 'Asian','Black or African American', 'Native Hawaiian or Other Pacific Islander','American Indian or Alaska Native'))

        submit_button = st.form_submit_button(label="Submit Form")
    if submit_button:
        st.success("Thank you {}! We are now checking your loan eligibility...".format(first_name))

# Model and transformer for results
    model = jl.load("model/xgbmodel.pkl")
    transformer = jl.load("model/preprocessor.pkl")

    x = pd.DataFrame({"first name": first_name,"last name":last_name , "date of birth":dob , "loan amount":loan_amount })
    x_transformed = transformer.transform(x)

    result = model.predict(x_transformed)

    print(result)

if __name__== '__main__':
    main()


# Code below is needed for the next and previous buttons
from streamlit.components.v1 import html
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)
if st.button("app"):
    nav_page("app")
if st.button("credit"):
    nav_page("credit")
