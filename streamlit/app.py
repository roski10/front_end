import streamlit as st
import numpy as np
import pandas as pd
from streamlit_player import st_player
import joblib as jl

from PIL import Image
image = Image.open('media_files/GTA.png')
st.image(image, use_column_width=True)

st.markdown("""# GTA Mortgage approval form
## Using ML to get your dream home faster
Welcome to our Loan Approval Model landing page! At GTA, we understand that securing a loan can be a stressful and overwhelming process. That's why we've developed a loan approval model that makes it easier than ever to get the financing you need.

Our loan approval model is designed to help you navigate the loan application process with confidence. By using advanced data analysis and machine learning algorithms, our model is able to accurately predict your likelihood of getting approved for a loan based on a variety of factors, including your credit score, income, and employment history.

Here are some of the key benefits of using our loan approval model:

Faster and more accurate loan approvals: With our model, you can receive a loan approval decision in a matter of minutes, rather than waiting days or weeks for a traditional lender to review your application.

Increased transparency: Our loan approval model provides you with a clear understanding of the factors that are influencing your loan approval decision. This can help you make more informed decisions about your finances.

Personalized recommendations: Our loan approval model takes your unique financial situation into account, providing you with personalized recommendations for loan products that are best suited to your needs.

Easy to use: Our loan approval model is user-friendly and intuitive, making it easy for you to input your information and receive a loan approval decision.

Whether you're looking to finance a home, a car, or any other major purchase, our loan approval model can help make the process easier and more streamlined.

Try it out today and see how we can help you get the financing you need.
""")

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
if st.button("credit"):
    nav_page("credit")
if st.button("form"):
    nav_page("form")
