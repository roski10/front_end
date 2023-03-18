# this page is the form the client to file in

import streamlit as st
import numpy as np
import pandas as pd
from streamlit_player import st_player
import joblib as jl
from PIL import Image
import base64
import time



@st.cache_data
def read_audio_file(file_path):
    with open(file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes

def embed_music(file_path, play_audio):
    if play_audio:
        # Embed the music
        audio_bytes = read_audio_file(file_path)

        mymidia_placeholder = st.empty()
        mymidia_str = "data:audio/ogg;base64,%s" % (base64.b64encode(audio_bytes).decode())
        mymidia_html = """
                        <audio autoplay class="stAudio">
                        <source src="%s" type="audio/ogg">
                        Your browser does not support the audio element.
                        </audio>
                    """ % mymidia_str
        mymidia_placeholder.empty()
        time.sleep(1)
        mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)

    else:
        st.write("Audio stopped")

# Usage
play_audio = True


if st.checkbox("Toggle audio playback"):
    play_audio = not play_audio

embed_music('media_files/GTA-song.mp3', play_audio)


def main():
    st.title("GTA Mortgage approval form")
    menu = ["app","form","credit"]
    choice = st.sidebar.selectbox("Menu",menu)
    with st.form(key='form1'):
        loan_amount = st.number_input('Insert the amount of money to borrow in 000s')
        loan_purpose_name = st.selectbox('What is the purpose of the loan?',(' ','Refinancing', 'Home purchase', 'Home improvement'))
        lien_status_name = st.selectbox('What is the lien status of the loan?',(' ','Secured by a first lien', 'Secured by a subordinate lien', 'Not secured by a lien'))
        loan_type_name = st.selectbox('What is the type of loan you are applying for?',(' ','Conventional','FHA-insured', 'VA-guaranteed', 'FSA/RHS-guaranteed'))
        principal_dwelling = st.selectbox('Does the Owner intend to occupy the property as their principal dwelling?',(' ','Owner-occupied as a principal dwelling', 'Not owner-occupied as a principal dwelling' ))
        property_region = st.selectbox('What is the region of the property?',(' ','Northern Cascades','Western Region','Eastern Washington', 'Southwest Washington','Olympic peninsula'))

        col1, col2 = st.columns(2)
        with col1:
            main_applicant_full_name = st.text_input("Full name of main applicant")
            main_dob = st.date_input("Date of Birth of main applicant")
            main_app_gender = st.selectbox('What is the gender of the main applicant?',(' ','Male', 'Female'))
            main_app_ethnicity = st.selectbox('What is the ethnicity of the main applicant?',(' ','White', 'Asian','Black or African American', 'Native Hawaiian or Other Pacific Islander','American Indian or Alaska Native'))
            applicant_income_000s = st.number_input('Insert the main applicant income in 000s', value=10)

        with col2:
            co_applicant_full_name = st.text_input("Full name of co applicant")
            co_dob = st.date_input("Date of Birth of co applicant")
            co_app_gender = st.selectbox('What is the gender of the co applicant?',('No co-applicant','Male', 'Female'))
            co_app_ethnicity = st.selectbox('What is the ethnicity of the co applicant?',('No co-applicant','White', 'Asian','Black or African American', 'Native Hawaiian or Other Pacific Islander','American Indian or Alaska Native'))
            co_income_000s = st.number_input('Insert the co applicant income in 000s')

        submit_button = st.form_submit_button(label="Submit Form")
    if submit_button:
        st.success("Thank you {}! We are now checking your loan eligibility...".format(main_applicant_full_name))
        play_audio = False

    # Model and transformer for results
        model = jl.load("model/xgbmodel.pkl")
        transformer = jl.load("model/preprocessor.pkl")

        x = pd.DataFrame({"loan_amount_000s": loan_amount,
                        "loan_purpose_name":loan_purpose_name,
                        "lien_status_name":lien_status_name,
                        "loan_type_name":loan_type_name,
                        "owner_occupancy_name": principal_dwelling,
                        "region": property_region,
                        "applicant_sex_name":main_app_gender,
                        "applicant_ethnicity_name": 'Not Hispanic or Latino',
                        "co_applicant_sex_name": co_app_gender,
                        "co_applicant_ethnicity_name":'Not Hispanic or Latino',
                        "tract_to_msamd_income":105,
                        "population": 5294,
                        "minority_population": 25,
                        "number_of_owner_occupied_units": 1391,
                        "number_of_1_to_4_family_units": 1825,
                        "hud_median_family_income": 73300,
                        "applicant_income_000s": applicant_income_000s,
                        "property_type_name": 'One-to-four family dwelling (other than manufactured housing)',
                        "preapproval_name": 'Not applicable',
                        "hoepa_status_name": 'Not a HOEPA loan',
                        "co_applicant_race_name_1": co_app_ethnicity,
                        "applicant_race_name_1": main_app_ethnicity,
                        },index=[0])


        x_transformed = transformer.transform(x)

        result = model.predict(x_transformed)

        #st.write(result)

        if result[0] == 0:
            image2 = Image.open('media_files/wasted.png')
            st.image(image2, use_column_width=True)
            play_audio = False
            embed_music('media_files/wasted.mp3',play_audio=True)

        else:
            image3 = Image.open('media_files/misson-passed.png')
            st.image(image3, use_column_width=True)
            st.balloons()


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
