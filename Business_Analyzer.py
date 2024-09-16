import streamlit as st
import streamlit_extras
from streamlit_extras.buy_me_a_coffee import button
import requests
import pandas as pd
import time
from math import radians, cos, sin, asin, sqrt
from difflib import SequenceMatcher
from textblob import TextBlob
from datetime import datetime, timedelta

# Function Definitions

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r

def geocode_location(location_name, api_key):
    """
    Convert a location name to latitude and longitude using Google Geocoding API.

    Parameters:
        location_name (str): The location name (e.g., "San Diego, California").
        api_key (str): Google Geocoding API key.

    Returns:
        tuple: (latitude, longitude) or (0.0, 0.0) if not found.
    """
    GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location_name,
        'key': api_key
    }
    try:
        response = requests.get(GEOCODE_URL, params=params)
        data = response.json()
        if data.get('status') == 'OK':
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            if data.get('status') == "REQUEST_DENIED":      
                st.error("Request denied, check your API key and ensure you have an active billing account.")
            else:
                st.error(f"Geocoding failed for location: {location_name} with status: {data.get('status')}")
            return (0.0, 0.0)
    except Exception as e:
        st.error(f"Exception during geocoding: {e}")
        return (0.0, 0.0)

def fetch_businesses(keyword, location, radius, api_key, max_results=1):
    """
    Fetch businesses from Google Places Nearby Search API based on a keyword and location.
    
    Parameters:
        keyword (str): The search keyword (e.g., "painter").
        location (tuple): (latitude, longitude) of the base location.
        radius (int): Search radius in meters (max 50000 meters).
        api_key (str): Google Places API key.
        max_results (int): Maximum number of results to fetch.
    
    Returns:
        list: A list of business dictionaries.
    """
    PLACE_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    businesses = []
    params = {
        'keyword': keyword,
        'location': f"{location[0]},{location[1]}",
        'radius': radius,
        'key': api_key,
    }
    
    while True:
        try:
            response = requests.get(PLACE_SEARCH_URL, params=params)
            if response.status_code != 200:
                st.error(f"Error fetching businesses: HTTP {response.status_code}")
                break
            
            data = response.json()
            status = data.get('status')
            if status != 'OK' and status != 'ZERO_RESULTS':
                st.error(f"API returned status: {status}")
                if 'error_message' in data:
                    st.error(f"Error message: {data['error_message']}")
                break
            
            results = data.get('results', [])
            for biz in results:
                if len(businesses) >= max_results:
                    # Removed the info message about reaching maximum limit
                    return businesses
                businesses.append(biz)
            
            # Handle pagination only if needed
            next_page_token = data.get('next_page_token')
            if next_page_token and len(businesses) < max_results:
                time.sleep(2)  # Wait for the token to become active
                params = {
                    'pagetoken': next_page_token,
                    'key': api_key
                }
            else:
                break
        except Exception as e:
            st.error(f"Exception occurred while fetching businesses: {e}")
            break
    
    st.success(f"Total businesses fetched: {len(businesses)}")
    return businesses

def fetch_place_details(place_id, api_key, fields=['website', 'formatted_phone_number', 'rating', 'user_ratings_total', 'price_level', 'types', 'geometry', 'opening_hours', 'reviews']):
    """
    Fetch detailed information about a place using Place Details API.

    Parameters:
        place_id (str): The unique identifier for a place.
        api_key (str): Google Places API key.
        fields (list): List of fields to retrieve.

    Returns:
        dict: A dictionary containing the requested fields.
    """
    PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': ','.join(fields),
        'key': api_key
    }
    
    try:
        response = requests.get(PLACE_DETAILS_URL, params=params)
        if response.status_code != 200:
            st.warning(f"Error fetching place details for {place_id}: HTTP {response.status_code}")
            return {}
        
        data = response.json()
        status = data.get('status')
        if status != 'OK':
            st.warning(f"Place Details API returned status: {status} for Place ID: {place_id}")
            if 'error_message' in data:
                st.warning(f"Error message: {data['error_message']}")
            return {}
        
        result = data.get('result', {})
        return {
            'website': result.get('website', 'N/A'),
            'formatted_phone_number': result.get('formatted_phone_number', 'N/A'),
            'rating': result.get('rating', 0),
            'user_ratings_total': result.get('user_ratings_total', 0),
            'price_level': result.get('price_level', 0),
            'types': result.get('types', []),
            'geometry': result.get('geometry', {}).get('location', {}),
            'opening_hours': result.get('opening_hours', {}).get('open_now', False),
            'reviews': result.get('reviews', [])
        }
        
    except Exception as e:
        st.warning(f"Exception occurred while fetching place details for {place_id}: {e}")
        return {}

def verify_website(url):
    """
    Verify if a website URL is accessible.

    Parameters:
        url (str): The website URL to verify.

    Returns:
        bool: True if accessible, False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            return True
        else:
            return False
    except requests.RequestException:
        return False

def sentiment_score(review_text):
    """
    Calculate sentiment polarity of a review.

    Parameters:
        review_text (str): The text of the review.

    Returns:
        float: Polarity score ranging from -1 (negative) to 1 (positive).
    """
    try:
        blob = TextBlob(review_text)
        return blob.sentiment.polarity
    except Exception:
        return 0.0

def is_recent(review_time_str, within_days=365):
    """
    Determine if a review is recent based on the specified number of days.

    Parameters:
        review_time_str (str): Review time in RFC3339 format.
        within_days (int): Number of days to consider as recent.

    Returns:
        bool: True if the review is recent, False otherwise.
    """
    try:
        review_time = datetime.strptime(review_time_str, "%Y-%m-%dT%H:%M:%S%z")
        return review_time >= datetime.now(tz=review_time.tzinfo) - timedelta(days=within_days)
    except ValueError:
        return False

def analyze_reviews(reviews, min_recent_reviews=1, min_average_rating=3.5, min_average_sentiment=0.0):
    """
    Analyze reviews to determine if a business meets the criteria.

    Parameters:
        reviews (list): List of review dictionaries.
        min_recent_reviews (int): Minimum number of recent reviews (e.g., within the last year).
        min_average_rating (float): Minimum average rating.
        min_average_sentiment (float): Minimum average sentiment score.

    Returns:
        bool: True if the business meets the criteria, False otherwise.
    """
    if not reviews:
        return False
    
    recent_reviews = [review for review in reviews if is_recent(review.get('time_created', ''))]
    if len(recent_reviews) < min_recent_reviews:
        return False
    
    average_rating = sum([review.get('rating', 0) for review in recent_reviews]) / len(recent_reviews)
    if average_rating < min_average_rating:
        return False
    
    # Calculate average sentiment
    sentiments = [sentiment_score(review.get('text', '')) for review in recent_reviews]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
    if average_sentiment < min_average_sentiment:
        return False
    
    return True

def grade_business(
    biz_details, 
    target_types=[], 
    max_distance=50, 
    base_location=(0,0), 
    weights=None
):
    """
    Grade the business based on predefined criteria.

    Parameters:
        biz_details (dict): Dictionary containing business details.
        target_types (list): List of desired business types.
        max_distance (float): Maximum distance in kilometers from base_location.
        base_location (tuple): (latitude, longitude) of the base location.
        weights (dict): Dictionary of grading weights.

    Returns:
        float: Total score out of 100.
        float: Distance from the base location in kilometers.
    """
    # Set default weights if none provided
    if weights is None:
        weights = {
            'rating': 20,
            'user_ratings_total': 10,
            'reviews': 20,
            'website': 15,
            'formatted_phone_number': 15,
            'price_level': 10,
            'types': 10,
            'location_proximity': 5,
        }
    
    total_score = 0
    
    # 1. Business Rating
    rating = biz_details.get('rating', 0)  # 0 to 5
    rating_score = (rating / 5) * 10  # 0 to 10
    total_score += rating_score * (weights.get('rating', 0) / 100)
    
    # 2. Number of User Ratings
    user_ratings_total = biz_details.get('user_ratings_total', 0)
    user_ratings_score = min((user_ratings_total / 100) * 10, 10)  # Cap at 10
    total_score += user_ratings_score * (weights.get('user_ratings_total', 0) / 100)
    
    # 3. Review Analysis
    reviews = biz_details.get('reviews', [])
    reviews_meet_criteria = analyze_reviews(reviews)
    reviews_score = 10 if reviews_meet_criteria else 0
    total_score += reviews_score * (weights.get('reviews', 0) / 100)
    
    # 4. Presence of Website
    website = biz_details.get('website', 'N/A')
    website_score = 10 if website != 'N/A' else 0
    total_score += website_score * (weights.get('website', 0) / 100)
    
    # 5. Availability of Phone Number
    phone = biz_details.get('formatted_phone_number', 'N/A')
    phone_score = 10 if phone != 'N/A' else 0
    total_score += phone_score * (weights.get('formatted_phone_number', 0) / 100)
    
    # 6. Price Level
    price_level = biz_details.get('price_level', 0)  # 0 to 4
    price_score = (price_level / 4) * 10  # 0 to 10
    total_score += price_score * (weights.get('price_level', 0) / 100)
    
    # 7. Business Type
    types = biz_details.get('types', [])
    type_score = 0
    for t in target_types:
        if t.lower() in [bt.lower() for bt in types]:
            type_score = 10
            break
    total_score += type_score * (weights.get('types', 0) / 100)
    
    # 8. Location Proximity
    biz_lat = biz_details.get('geometry', {}).get('lat', 0)
    biz_lng = biz_details.get('geometry', {}).get('lng', 0)
    base_lat, base_lng = base_location
    distance = haversine(base_lng, base_lat, biz_lng, biz_lat)  # in kilometers
    if max_distance > 0:
        proximity_score = max(10 - (distance / max_distance) * 10, 0)
    else:
        proximity_score = 0
    total_score += proximity_score * (weights.get('location_proximity', 0) / 100)
    
    # Convert total_score to a percentage
    total_score_percentage = total_score * 10  # Since each weight was out of 100
    return total_score_percentage, distance  # Return distance for sorting

def merge_businesses(businesses):
    """
    Merge and deduplicate businesses based on name and address similarity.

    Parameters:
        businesses (list): List of business dictionaries from Places API.

    Returns:
        list: Merged list of unique business dictionaries.
    """
    unique_businesses = []
    seen = []
    for biz in businesses:
        name = biz.get('name', '').lower()
        address = biz.get('vicinity', '').lower()
        is_duplicate = False
        for seen_biz in seen:
            name_similarity = SequenceMatcher(None, name, seen_biz['name']).ratio()
            address_similarity = SequenceMatcher(None, address, seen_biz['vicinity'].lower()).ratio()
            if name_similarity > 0.9 and address_similarity > 0.9:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_businesses.append(biz)
            seen.append(biz)
    return unique_businesses

def save_businesses_to_csv(
    businesses, 
    target_types=[], 
    base_location=(0,0), 
    max_distance=50, 
    grade_threshold=50, 
    weights=None, 
    progress_bar=None, 
    progress_text=None, 
    table_placeholder=None,
    selected_columns=None  # New parameter for selected CSV columns
):
    """
    Compile business data into a DataFrame and allow user to download it as CSV.

    Parameters:
        businesses (list): List of business dictionaries from Places API.
        target_types (list): List of desired business types for grading.
        base_location (tuple): (latitude, longitude) of the base location for proximity.
        max_distance (float): Maximum distance in kilometers for proximity scoring.
        grade_threshold (float): Minimum grade score to include in the CSV.
        weights (dict): Dictionary of grading weights.
        progress_bar (st.progress): Streamlit progress bar object.
        progress_text (st.empty): Streamlit text placeholder for progress updates.
        table_placeholder (st.empty): Streamlit placeholder for the dynamic table.
        selected_columns (list): List of columns selected by the user for the CSV.

    Returns:
        pd.DataFrame: DataFrame containing qualified businesses.
    """
    data = []
    total = len(businesses)
    
    # Initialize progress bar
    if progress_bar is not None:
        progress_bar.progress(0)
    
    # Define default columns if none are selected
    if not selected_columns:
        selected_columns = [
            'Name', 'Address', 'Phone', 'Website', 'Website Accessible', 
            'Grade Score', 'Distance (km)', 'Google Maps URL', 'Place ID'
        ]
    
    # Initialize empty DataFrame with selected columns
    if table_placeholder is not None:
        temp_df = pd.DataFrame(columns=selected_columns)
        table_placeholder.dataframe(temp_df)
    
    for idx, biz in enumerate(businesses, start=1):
        name = biz.get('name')
        address = biz.get('vicinity')
        place_id = biz.get('place_id')
        
        # Construct the Google Maps URL using place_id
        maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        
        # Fetch Place Details
        details = fetch_place_details(place_id, api_key=user_api_key)
        if not details:
            continue
        
        website = details.get('website', 'N/A')
        phone = details.get('formatted_phone_number', 'N/A')
        reviews = details.get('reviews', [])
        
        # Verify Website Accessibility
        website_accessible = 'Yes' if website != 'N/A' and verify_website(website) else 'No'
        
        # Grade the business
        grade, distance = grade_business(
            details, 
            target_types=target_types, 
            max_distance=max_distance, 
            base_location=base_location, 
            weights=weights
        )
        
        # Apply grade threshold
        if grade < grade_threshold:
            continue  # Skip adding to the CSV
        
        # Append to data
        business_data = {
            'Name': name,
            'Address': address,
            'Phone': phone,
            'Website': website,
            'Website Accessible': website_accessible,
            'Grade Score': grade,
            'Distance (km)': round(distance, 2),
            'Google Maps URL': maps_url,
            'Place ID': place_id
        }
        
        # Only include selected columns
        filtered_business_data = {key: value for key, value in business_data.items() if key in selected_columns}
        data.append(filtered_business_data)
        
        # Update progress
        if progress_bar is not None:
            progress = idx / total
            progress_bar.progress(progress)
        if progress_text is not None:
            progress_text.text(f"Processing business {idx} of {total}...")
        
        # Update the table dynamically using pd.concat
        if table_placeholder is not None:
            # Create a DataFrame for the current business
            current_df = pd.DataFrame([filtered_business_data])
            # Concatenate with the existing temp_df
            temp_df = pd.concat([temp_df, current_df], ignore_index=True)
            # Update the table in Streamlit
            table_placeholder.dataframe(temp_df)
        
        # Politeness delay to avoid hitting rate limits
        time.sleep(1)
    
    # Finalize progress
    if progress_bar is not None:
        progress_bar.progress(100)
    if progress_text is not None:
        progress_text.text("Processing complete!")
    
    if data:
        df = pd.DataFrame(data)
        # Sort by Grade Score (descending) and Distance (ascending)
        df.sort_values(by=['Grade Score', 'Distance (km)'], ascending=[False, True], inplace=True)
        return df
    else:
        return pd.DataFrame()

# Streamlit App Layout

st.set_page_config(page_title="Business Analyzer", layout="wide")

st.markdown("# 📈 Business Analyzer by [@DamonDevelops](https://damon-develops.tech)")

button(username="damonDevelops", floating=False, width=300, font="Poppins")

st.markdown("""
I built this application to assist me in looking for potential clients for my web development business [Revamp Web Studios](https://www.revampwebstudio.com.au). The tool works by analysing nearby Google Places and assesses them based on weighted criteria to determine which are the best to approach. Enter your **Google Places API Key**, **Location**, **Industry**, and configure your grading preferences to get started. If you like the webapp and it helped you out at all, if you can afford to leave me a tip I'd greatly appreciate it :)!
""")

with st.form("business_form"):
    st.subheader("🔧 Configuration")
    user_api_key = st.text_input("🔑 Google Places API Key", type="password", help="Enter your Google Places API Key.")
    location = st.text_input("📍 Location", value="Sydney, Australia", help="Enter your location (e.g., 'Sydney, Australia').")
    industry = st.text_input("🏢 Industry Type", value="painter", help="Enter the industry type (e.g., 'painter').")
    
    # 1. Allow user to specify the number of results (max 50)
    num_results = st.number_input(
        "📊 Number of Results", 
        min_value=1, 
        max_value=50, 
        value=10, 
        step=1, 
        help="Enter the number of businesses to fetch (max 50)."
    )
    if num_results == 50:
        st.warning("Fetching 50 businesses may take some time. Please be patient.")

    # 3. Allow user to set grade threshold
    grade_threshold = st.number_input(
        "📈 Grade Threshold", 
        min_value=0.0, 
        max_value=100.0, 
        value=50.0, 
        step=0.5, 
        help="Minimum grade score to include in the results."
    )
    
    # 2. Optional Grading Weights Customization using Expander
    with st.expander("🛠️ Customize Grading Weights"):
        st.markdown("Adjust the weights to prioritize different criteria during grading. The total weight does not need to sum up to 100, as each criterion is scored independently.")
        
        # Allow users to change grading weights
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            rating_weight = st.slider("⭐ Rating Weight", min_value=0, max_value=50, value=20, step=1, help="Weight for business rating.")
        with col2:
            user_ratings_weight = st.slider("📝 User Ratings Weight", min_value=0, max_value=50, value=10, step=1, help="Weight for number of user ratings.")
        with col3:
            reviews_weight = st.slider("🗣️ Reviews Weight", min_value=0, max_value=50, value=20, step=1, help="Weight for review analysis.")
        with col4:
            website_weight = st.slider("🌐 Website Weight", min_value=0, max_value=50, value=15, step=1, help="Weight for website presence.")
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            phone_weight = st.slider("📞 Phone Weight", min_value=0, max_value=50, value=15, step=1, help="Weight for phone number availability.")
        with col6:
            price_weight = st.slider("💲 Price Level Weight", min_value=0, max_value=50, value=10, step=1, help="Weight for price level.")
        with col7:
            types_weight = st.slider("🛠️ Business Type Weight", min_value=0, max_value=50, value=10, step=1, help="Weight for business type.")
        with col8:
            proximity_weight = st.slider("📍 Proximity Weight", min_value=0, max_value=50, value=5, step=1, help="Weight for location proximity.")
        
        # Collect weights into a dictionary
        grading_weights = {
            'rating': rating_weight,
            'user_ratings_total': user_ratings_weight,
            'reviews': reviews_weight,
            'website': website_weight,
            'formatted_phone_number': phone_weight,
            'price_level': price_weight,
            'types': types_weight,
            'location_proximity': proximity_weight,
        }
    
    # 4. Optional CSV Columns Customization using Expander
    with st.expander("📋 Customize CSV Columns"):
        st.markdown("Select the columns you wish to include in your CSV download.")
        
        # Define available columns
        available_columns = [
            'Name', 
            'Address', 
            'Phone', 
            'Website', 
            'Website Accessible', 
            'Grade Score', 
            'Distance (km)', 
            'Google Maps URL', 
            'Place ID'
        ]
        
        # Create checkboxes for each column, default to True
        selected_columns = []
        for column in available_columns:
            if st.checkbox(column, value=True):
                selected_columns.append(column)
        
        # Ensure at least one column is selected
        if not selected_columns:
            st.warning("Please select at least one column for the CSV.")
    
    submit_button = st.form_submit_button(label="Analyze Businesses")

if submit_button:
    if not user_api_key:
        st.error("Please enter your Google Places API Key.")
    elif not location:
        st.error("Please enter a valid location.")
    elif not industry:
        st.error("Please enter an industry type.")
    elif 'selected_columns' in locals() and not selected_columns:
        st.error("Please select at least one CSV column.")
    else:
        # Geocode the location
        with st.spinner('Geocoding the location...'):
            base_location = geocode_location(location, user_api_key)
       
        if base_location == (0.0, 0.0):
            st.warning("Geocoding failed. Please check your location input.")
        else:
            # Define search parameters
            max_results = min(int(num_results), 50)  # Ensure max_results does not exceed 50
            radius = 50000  # 50 km
            target_types = [industry.lower()]
            
            st.info(f"Searching for '{industry}' in '{location}' within {radius/1000} km for up to {max_results} business(es)...")
            
            # Fetch businesses
            with st.spinner('Fetching businesses from Google Places API...'):
                businesses = fetch_businesses(
                    keyword=industry, 
                    location=base_location, 
                    radius=radius, 
                    api_key=user_api_key, 
                    max_results=max_results
                )
            
            if not businesses:
                st.warning("No businesses fetched.")
            else:
                # Deduplicate businesses
                unique_businesses = merge_businesses(businesses)
                # Removed the message about unique businesses after deduplication
                
                # Initialize placeholders for progress and table
                progress_bar = st.progress(0)
                progress_text = st.empty()
                table_placeholder = st.empty()
                
                # Analyze and grade businesses with progress updates
                with st.spinner('Analyzing and grading businesses...'):
                    df = save_businesses_to_csv(
                        unique_businesses, 
                        target_types=target_types, 
                        base_location=base_location, 
                        max_distance=50,
                        grade_threshold=grade_threshold,
                        weights=grading_weights,
                        progress_bar=progress_bar,
                        progress_text=progress_text,
                        table_placeholder=table_placeholder,
                        selected_columns=selected_columns  # Pass selected columns to the function
                    )
                
                if df.empty:
                    st.warning("No businesses met the grade threshold.")
                else:
                    st.success(f"Found {len(df)} business(es) that meet or exceed the grade threshold.")
                    
                    # Display the download button below the table
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name='businesses.csv',
                        mime='text/csv',
                    )
