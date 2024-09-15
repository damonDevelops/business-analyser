
# 📈 Business Analyzer

**Business Analyzer** is a Streamlit application designed to help you find and grade businesses based on your industry and location. Customize grading preferences, select desired CSV columns, and download the results for your analysis.

## Features

- **Google Places Integration:** Fetch businesses based on industry and location using the Google Places API.
- **Custom Grading Weights:** Adjust the importance of various criteria such as rating, number of reviews, website presence, etc.
- **CSV Column Customization:** Choose which data columns to include in your CSV download.
- **Downloadable Results:** Export the analyzed businesses as a CSV file for further use.
- **User-Friendly Interface:** Intuitive design with progress indicators and informative messages.

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/your-username/business-analyzer/main)

*Replace the above link with your deployed app link if available.*

## Getting Started

### Prerequisites

- **Python 3.7 or higher**
- **Google Places API Key:** You'll need a valid Google Places API Key to fetch business data.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/business-analyzer.git
   cd business-analyzer
   ```

2. **Create a Virtual Environment:**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download TextBlob Corpora:**

   TextBlob requires additional data for sentiment analysis.

   ```bash
   python -m textblob.download_corpora
   ```

5. **Obtaining a Google Places API Key**

   To use the Business Analyzer, you'll need a Google Places API Key. Follow these steps:

   - **Create a Google Cloud Account:** Sign up if you don't have one.
   - **Create a New Project:** Go to the Google Cloud Console, create a project.
   - **Enable Billing:** Set up billing for your project.
   - **Enable the Places API:** Navigate to APIs & Services > Library and enable Places API.
   - **Generate API Credentials:** Obtain your API key.

### Running the Application

1. **Activate the Virtual Environment:**

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Streamlit App:**

   ```bash
   streamlit run Business_Analyzer.py
   ```

### Usage

1. **Enter Your API Key:** Provide your Google Places API Key.
2. **Specify Location and Industry:** Enter the location and industry type.
3. **Set Number of Results:** Specify how many businesses to fetch (up to 50).
4. **Set Grade Threshold:** Define the minimum grade score required.
5. **Customize Grading Weights (Optional):** Adjust criteria priorities.
6. **Customize CSV Columns (Optional):** Select or deselect the columns.
7. **Analyze Businesses:** Fetch, analyze, and display businesses.
8. **Download Results:** Download the results as a CSV file.

## Contributing

1. **Fork the Repository**
2. **Create a New Branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes:**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch:**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [DamonDevelops](https://www.damon-develops.tech/)


## Contact
For any inquiries, reach out at damon.oneil2.newsletter@gmail.com.

