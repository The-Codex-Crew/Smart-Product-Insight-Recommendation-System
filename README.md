# 🛒 Smart Shopping App  
## Smart Product Insight & Recommendation System  

**Team: The Codex Crew**  
- Kulsoom Zehra  
- Harshitha Nirmal  
- Sharib Anwar  

---

## Quick Overview  
A Streamlit-based smart shopping web app that helps users discover products using category, price, and rating filters. It provides rule-based recommendations, related product suggestions, and price insights through an interactive and modern UI.

---

## Project Overview  

The Smart Shopping App is an interactive web application developed using Streamlit that enables users to explore and discover products efficiently. It uses an Amazon product dataset and provides recommendations based on user-selected filters such as category, maximum price, and minimum rating.  

The system follows a **rule-based recommendation approach**, where products are filtered and ranked using logical conditions instead of machine learning. It combines data preprocessing, filtering logic, pagination, and visualization to create a complete shopping assistant experience.  

---

## Key Features  

- Category-based product filtering using sidebar  
- Adjustable maximum price and minimum rating filters  
- Rule-based recommendation system  
- Recommended Products section (top results)  
- Customers Also Bought section (related products)  
- Card-based UI with image, rating, price, discount, and product link  
- Pagination for efficient browsing  
- Handling of invalid/broken image links  
- Sidebar statistics (average rating, median price, product count)  
- Price distribution visualization using Seaborn and Matplotlib  
- Clean and modern UI with custom CSS  

---

## How the System Works  

1. Loads the `amazon.csv` dataset  
2. Cleans and preprocesses data (price, rating, category, images)  
3. Applies filters based on category, price, and rating  
4. Ranks products using rating, rating count, and price  
5. Displays recommended and related products  
6. Uses pagination for better performance  
7. Generates a price distribution chart for insights  

---

## Technologies Used  

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  

---

## How to Run the Project  

1. Clone the repository:

        git clone https://github.com/The-Codex-Crew/Smart-Product-Insight-Recommendation.git

2. Navigate to the project folder:
  
        cd Smart-Product-Insight-Recommendation

3. Install dependencies:

       pip install -r requirements.txt

   > If requirements.txt is not available:

       pip install streamlit pandas numpy matplotlib seaborn

4. Run the application:

       streamlit run smart_shop.py

5. Open in your browser:

        http://localhost:8501

## Output  

- Filtered product recommendations
- Related product suggestions
- Paginated product browsing
- Card-based product display
- Price distribution graph
- Sidebar insights

---

## Limitations

- Rule-based recommendation (no ML)
- Static dataset (no real-time updates)
- Some images may not load due to external sources
- Future Improvements
- Search functionality
- Wishlist and cart system
- User authentication
- Real-time API integration
- Machine learning-based recommendationsinsights

---

## Conclusion

This project demonstrates how data preprocessing, filtering logic, and visualization can be combined to build an interactive and user-friendly shopping application. It showcases practical skills in Python, data handling, and web app development.
