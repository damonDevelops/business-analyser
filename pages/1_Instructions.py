# pages/1_Instructions.py

import streamlit as st

def main():
    st.title("📖 Instructions")

    st.markdown("""
    ## How to Use the Business Analyzer

    Welcome to the **Business Analyzer**! This guide will help you obtain your Google Places API Key and use the service effectively.

    ### Step 1: Obtain Your Google Places API Key

    To use this application, you'll need a **Google Places API Key**. Follow these steps to get one:

    1. **Create a Google Cloud Account:**
       - If you don't have a Google Cloud account, [sign up here](https://cloud.google.com/free).

    2. **Create a New Project:**
       - Go to the [Google Cloud Console](https://console.cloud.google.com/).
       - Click on the project dropdown at the top and select **New Project**.
       - Enter a project name and click **Create**.

    3. **Enable Billing:**
       - Before you can use Google APIs, billing must be enabled.
       - Navigate to **Billing** in the console and follow the prompts to set up billing for your project. *Note: Google offers a free tier with $300 credit for new users.*

    4. **Enable the Necessary APIs:**
       - Go to **APIs & Services > Library** in the Google Cloud Console.
       - Search for and enable the following APIs:
         - **Places API**

    5. **Generate API Credentials:**
       - Navigate to **APIs & Services > Credentials**.
       - Click **+ CREATE CREDENTIALS** and select **API key**.
       - Your new API key will appear. **Copy and keep it secure**.

    ### Step 2: Using the Business Analyzer

    1. **Enter Your API Key:**
       - On the **Main** page, locate the **🔑 Google Places API Key** input field.
       - Paste your API key into this field.

    2. **Specify Location and Industry:**
       - **📍 Location:** Enter the location you want to search in (e.g., "San Diego, California").
       - **🏢 Industry Type:** Enter the industry you're interested in (e.g., "painter").

    3. **Set Number of Results:**
       - **📊 Number of Results:** Specify how many businesses you want to fetch (up to 50).

    4. **Set Grade Threshold:**
       - **📈 Grade Threshold:** Define the minimum grade score required for a business to be included in the final results.

    5. **Customize Grading Weights (Optional):**
       - Click on the **🛠️ Customize Grading Weights** expander.
       - Adjust the sliders to prioritize different grading criteria as per your preferences.
       - **Note:** If you do not customize the grading weights, default values will be applied.

    6. **Customize CSV Columns (Optional):**
       - Click on the **📋 Customize CSV Columns** expander.
       - Select or deselect the columns you wish to include in your CSV download by checking or unchecking the corresponding boxes.
       - **Note:** By default, all columns are selected. If you do not customize the CSV columns, the default set will be used.

    7. **Analyze Businesses:**
       - Click on the **Analyze Businesses** button.
       - The app will fetch, analyze, and display qualified businesses based on your inputs.

    8. **Download Results:**
       - If businesses meet the grading criteria, you can download the results as a CSV file by clicking the **📥 Download as CSV** button.
       - The downloaded CSV will include only the columns you selected in the **📋 Customize CSV Columns** section.

    ### Tips for Effective Use

    - **API Usage:** Be mindful of your API usage to avoid unexpected charges. Monitor your usage in the [Google Cloud Console](https://console.cloud.google.com/).
    - **API Key Security:** Never share your API key publicly. Restrict its usage as described above.
    - **Data Accuracy:** Ensure that the location and industry inputs are accurate for the best results.
    - **Custom Grading Weights:** Adjusting the grading weights can help prioritize certain business attributes over others based on your specific needs.
    - **Custom CSV Columns:** Tailor the CSV output by selecting only the data columns relevant to your analysis, making the dataset more manageable and focused.

    ### Troubleshooting

    - **Geocoding Errors:**
      - If the app cannot geocode your location, double-check the location input for accuracy.
      - Ensure that your API key has the necessary permissions and that billing is enabled.

    - **API Errors:**
      - Ensure that the correct APIs are enabled in your Google Cloud project.
      - Verify that your API key is correctly entered and not restricted incorrectly.

    - **No Businesses Found:**
      - Try expanding the search radius or adjusting the industry keyword for broader results.
      - Ensure that your grade threshold is set appropriately.

    - **CSV Download Issues:**
      - Ensure that at least one CSV column is selected. If all columns are deselected, the app will prompt you to select at least one column.

    ### Additional Resources

    - [Google Cloud Documentation](https://cloud.google.com/docs)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Google Places API Overview](https://developers.google.com/places/web-service/overview)

    We hope this guide helps you get started with the **Business Analyzer**! If you encounter any issues or have suggestions, feel free to reach out.
    """)

if __name__ == "__main__":
    main()
