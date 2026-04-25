# 🛒 Smart Shopping App  
## Smart Product Insight & Recommendation System  

**Team: The Codex Crew**  
- Kulsoom Zehra  
- Harshitha Nirmal  
- Sharib Anwar  

---

## Quick Overview  

Smart Shopping App is a Streamlit-based product discovery web app built on an Amazon product dataset. It helps users explore products by category, product-name search, price range, rating, and product count, then displays rule-based recommendations with related product suggestions and price insights.

The project focuses on practical data preprocessing, deterministic recommendation logic, clean visualization, pagination, and a polished shopping-style interface.

---

## Project Overview  

The application loads and cleans amazon.csv, standardizes the required product fields, converts price and rating values into numeric formats, simplifies product categories, and prepares valid image URLs for display.

Instead of using machine learning, the app uses a rule-based recommendation system. Products are filtered using user-selected criteria and ranked using rating, rating count, and discounted price. This makes the recommendation flow easy to understand, transparent, and suitable for demonstrating core data-handling and UI-building skills.

The interface includes a custom hero section, sidebar filters, metric cards, product cards, pagination controls, related product discovery, and a price distribution chart.

---

## Key Features  

- Category-based filtering through the sidebar
- Product-name search within the selected category
- Adjustable maximum price filter
- Adjustable minimum rating filter
- Products-per-section slider for controlling how many cards appear per page
- Rule-based recommendation system using rating, rating count, and price
- Recommended Products section for top-ranked filtered results
- Customers Also Bought section for related alternatives from the same category/search pool
- Card-based UI with product image, rating, rating count, price, discount, and product link
- Separate pagination for recommended and related product sections
- Sidebar statistics including product count, search matches, average rating, and median price
- Hero dashboard showing total products, total categories, dataset name, and recommendation type
- Metric cards for selected category, matching products, top rating, and lowest filtered price
- Price distribution visualization comparing the full dataset, selected category, and selected price threshold
- Custom CSS styling through style.css for a modern, responsive shopping interface
  
---

## How the System Works  

1. The app loads amazon.csv.
2. Required columns are validated before processing.
3. Column names are standardized.
4. Product names and categories are cleaned.
5. Prices, discounts, ratings, and rating counts are converted into numeric values.
6. Category values are simplified to the main category.
7. Image URLs are cleaned and only valid HTTP/HTTPS image links are used in product cards.
8. Duplicate products and invalid price/rating rows are removed.
9. The cleaned dataset is cached using Streamlit caching for faster reloads.
10. Users select a category from the sidebar.
11. Users can search by product name inside the selected category.
12. Products are filtered by maximum price and minimum rating.
13. Recommended products are ranked by rating, rating count, and discounted price.
14. Related products are selected from the same category/search results while excluding already recommended items.
15. Results are displayed as paginated product cards.
16. A price distribution chart is generated using Matplotlib and Seaborn.
    
---

## Recommendation Logic

The system uses transparent rule-based logic:

- **Filtering:** selected category, optional search text, maximum price, and minimum rating
- **Ranking recommended products:** highest rating, highest rating count, then lowest discounted price
- **Ranking related products:** lower discounted price first, then stronger rating
- **Display validation:** products without usable image URLs are excluded from product-card sections

## Technologies Used  

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn
- HTML/CSS for custom Streamlit styling

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

4. Make sure amazon.csv is available in the same folder as smart_shop.py.

5. Run the Streamlit application:

       streamlit run smart_shop.py

6. Open the local app URL in your browser:

        http://localhost:8501

## Output  

- Filtered product recommendations
- Related product suggestions
- Search-based product discovery
- Paginated product browsing
- Product cards with images, prices, ratings, discounts, and links
- Sidebar filters and category statistics
- Hero summary and metric cards
- Interactive price distribution graph

---

## Limitations

- The recommendation system is rule-based and does not use machine learning.
- The dataset is static and does not update prices, stock, or reviews in real time.
- Some external product image links may fail if the source blocks or removes them.
- The app does not currently include user accounts, cart, wishlist, or purchase tracking.

---

## Future Improvements

- Add global product search across all categories
- Add brand, subcategory, and discount filters
- Add wishlist and cart functionality
- Add user authentication
- Integrate a real-time product API
- Add machine learning-based recommendations
- Add product comparison features
- Add export or save options for recommended products

## Conclusion

This project demonstrates how data preprocessing, filtering logic, visualization, and custom UI design can be combined to build a practical shopping recommendation app. It showcases skills in Python programming, data cleaning, rule-based recommendation design, Streamlit development, and interactive data visualization.
