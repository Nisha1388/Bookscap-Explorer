

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit App Layout
st.title("Books Data Analysis")

# Floating Recommendations Button
recommendations_button = st.sidebar.button("Overall Insights and Recommendations")

# Recommendations Content
recommendations_content = """
### Overall Insights and Recommendations for the Dataset
#### Key Insights:
1. **Physical Books**: Higher page counts and prices, but slightly outnumbered by eBooks.
2. **Discounts**: Discounts of over 20% are common, potentially signaling competitive pricing strategies.
3. **Popular Authors and Publishers**: Repeated names like *Michael R. Berthold* and *O'Reilly Media Inc.* dominate the industry.
4. **Emerging Trends**: Python-related books and academic content show growing demand.

---

#### Recommendations:
1. **Focus Marketing on Emerging Topics**:
    - Promote Python-related and high-demand categories.
2. **Enhance eBook Offerings**:
    - Capitalize on the slightly higher demand for eBooks by expanding digital collections.
3. **Collaborative Publications**:
    - Invest in books with multiple authors for complex or academic subjects.
4. **Price Adjustments**:
    - Consider optimizing prices for eBooks to compete more effectively with physical books.
5. **Leverage High-Rated Publishers**:
    - Highlight top publishers like Springer Nature in marketing campaigns.
6. **Analyze Low-Rated Books**:
    - Replace or improve poorly rated books to enhance customer satisfaction.
7. **Focus on Digital Trends**:
    - The dominance of eBooks suggests that investment in digital formats will yield better returns.
8. **Promote Prolific Authors**:
    - Authors with multiple books in the same year or across different years should be promoted for audience retention.
9. **Keyword Analysis**:
    - Invest in Python and Data Science-related books to capitalize on their popularity.
"""

# Display Recommendations if Button is Clicked
if recommendations_button:
    st.markdown(recommendations_content)


# Dropdown to select a query
question = st.selectbox(
    "Select a question to see the answer",
    ["1. Check Availability of eBooks vs Physical Books",
     "2. Publisher with the Most Books Published",
     "3. Identify the Publisher with the Highest Average Rating",
     "4. Top 5 Most Expensive Books by Retail Price",
     "5. Books Published After 2010 with at Least 500 Pages",
     "6. List Books with Discounts Greater than 20%",
     "7. Average Page Count for eBooks vs Physical Books",
     "8. Top 3 Authors with the Most Books",
     "9. List Publishers with More than 10 Books",
     "10. Average Page Count for Each Category",
     "11. Books with More than 3 Authors",
     "12. Books with Ratings Count Greater Than the Average",
     "13. Books with the Same Author Published in the Same Year",
     "14. Books with a Specific Keyword in the Title",
     "15. Year with the Highest Average Book Price",
     "16. Count Authors Who Published 3 Consecutive Years",
     "17. Authors Who Have Published Books in the Same Year but Under Different Publishers",
     "18. Average Amount of Retail Price for eBooks and Physical Books",
     "19. Books with Average Rating More Than Two Standard Deviations Away from the Average",
     "20. Publisher with the Highest Average Rating Among Publishers with More than 10 Books"]
)

# Connect to the database to execute the selected query
conn = sqlite3.connect("books_database.db")
cursor = conn.cursor()

# 1. Check Availability of eBooks vs Physical Books
if question == "1. Check Availability of eBooks vs Physical Books":
    cursor.execute('''
    SELECT
        isEbook,
        COUNT(*) AS book_count
    FROM books
    GROUP BY isEbook;
    ''')
    result = cursor.fetchall()

    # Extract the counts
    ebooks_count = next((row[1] for row in result if row[0] == 1), 0)
    physical_books_count = next((row[1] for row in result if row[0] == 0), 0)

    # Display the counts
    st.write(f"Number of EBooks: {ebooks_count}")
    st.write(f"Number of Physical Books: {physical_books_count}")

    # Visualization (Pie Chart)
    data = {'EBooks': ebooks_count, 'Physical Books': physical_books_count}
    labels = list(data.keys())
    sizes = data.values()

    # Create a figure
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** There are 665 eBooks (51.7%) and 622 physical books (48.3%). A pie chart is used for visualization.
    - **Interpretation:** EBooks slightly outnumber physical books, indicating a growing trend in digital reading.
    """)

# 2. Find the Publisher with the Most Books Published
elif question == "2. Publisher with the Most Books Published":
    cursor.execute('''
    SELECT
        book_publisher,
        COUNT(*) AS book_count
    FROM books
    GROUP BY book_publisher
    ORDER BY book_count DESC
    LIMIT 1 OFFSET 1;
    ''')
    result = cursor.fetchone()
    if result:
        publisher, book_count = result
        publisher = publisher.strip().replace(",", '').replace('"', '').strip()
        st.markdown("""
    ### Analysis
    - **Insight:**""")
        st.write(f"\t The publisher '{publisher}' has published the highest number of books.")
        st.write(f"\t Total books published: {book_count}")
        st.markdown("""
      - **Business Interpretation:** 
      \n O'Reilly Media is a key player in the publishing industry, especially in technical and professional books.
    """)


# 3. Identify the Publisher with the Highest Average Rating
elif question == "3. Identify the Publisher with the Highest Average Rating":
    cursor.execute('''
    SELECT
        book_publisher,
        AVG(averageRating) AS avg_rating
    FROM books
    GROUP BY book_publisher
    ORDER BY avg_rating DESC
    LIMIT 1;
    ''')
    result = cursor.fetchone()
    if result:
        publisher, avg_rating = result
        publisher = publisher.strip().replace(",", '').replace('"', '').strip()
        st.markdown("""
    ### Analysis
    - **Insight:**
    """)
        st.write(f"The publisher with the highest average rating is: {publisher}")
        st.write(f"Average rating: {avg_rating}")
        st.markdown("""
    - **Interpretation:**
    \n This indicates that books from Springer Nature are highly rated, suggesting quality content and positive user reception.
    """)


# 4. Get the Top 5 Most Expensive Books by Retail Price
elif question == "4. Top 5 Most Expensive Books by Retail Price":
    cursor.execute('''
    SELECT
        book_title,
        amount_retailPrice
    FROM books
    ORDER BY amount_retailPrice DESC
    LIMIT 5;
    ''')
    result = cursor.fetchall()
    most_expensive_books = pd.DataFrame(result, columns=["Book Title", "Retail Price"])
    st.write(most_expensive_books)

    # Visualization (Bar Chart)
    st.bar_chart(most_expensive_books, x="Book Title", y="Retail Price", use_container_width=True)
    st.markdown("""
    ### Analysis
    - **Insight:** The top book is "Encyclopedia of Mathematical Geosciences" priced at $519.20.
    - **Interpretation:** The highest-priced books are academic or professional, reflecting their niche audience and high-value content.
    """)

#  5. Find Books Published After 2010 with at Least 500 Pages
elif question == "5. Books Published After 2010 with at Least 500 Pages":
    cursor.execute('''
    SELECT
        book_title,
        strftime('%Y', year) AS year,
        pageCount
    FROM books
    WHERE
        strftime('%Y', year) > '2010' 
        AND pageCount >= 500;
    ''')
    result = cursor.fetchall()

    # Create a DataFrame from the query result
    books_after_2010 = pd.DataFrame(result, columns=["Book Title", "Year", "Page Count"])
    st.write(books_after_2010)  # Show the books with titles in Streamlit

    # Count the number of books published in each year after 2010
    books_count_per_year = books_after_2010.groupby('Year').size().reset_index(name='Book Count')
    
    # Visualization (Bar Chart)
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure and axes

    # Plot the bar chart showing the number of books per year
    ax.bar(books_count_per_year["Year"], books_count_per_year["Book Count"], color="blue")

    # Adding the counts as labels on top of the bars
    for i, count in enumerate(books_count_per_year["Book Count"]):
        ax.text(books_count_per_year["Year"].iloc[i], count + 1, str(count), ha='center', fontsize=12)

    ax.set_xlabel("Year of Publication", fontsize=12)
    ax.set_ylabel("Number of Books", fontsize=12)
    ax.set_title("Number of Books Published After 2010 with At Least 500 Pages", fontsize=14)

    # Display the plot in Streamlit with book counts on the bars
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** 156 books meet the criteria.
    - **Interpretation:** Indicates that publishers are still investing in substantial content post-2010, possibly reflecting increased demand for comprehensive material. After 2021 there shows a dicline in bar chart which may be the influence of lack of readers, made publishers reduce the number of books they publish.
    """)

# 6. List Books with Discounts Greater than 20%
elif question == "6. List Books with Discounts Greater than 20%":
    cursor.execute('''
    SELECT
        book_title,
        amount_retailPrice,
        (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 AS discount_percent
    FROM books
    WHERE (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 > 21;
    ''')
    result = cursor.fetchall()
    books_with_discount = pd.DataFrame(result, columns=["Book Title", "Retail Price", "Discount"])

    # Display the table
    st.write(books_with_discount)

    # Add sentence
    st.write(f"{len(books_with_discount)} Books are given a discount above 20%")

    # Sort data by discount percentage in descending order
    books_with_discount.sort_values(by="Discount", ascending=False, inplace=True)

    # Visualization (Scatter Plot for Discounts)
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure and axes
    scatter = ax.scatter(
        range(len(books_with_discount)), books_with_discount["Discount"], color="green", s=50
    )
    ax.set_xlabel("Books (Ordered by Discount)", fontsize=12)
    ax.set_ylabel("Discount Percentage", fontsize=12)
    ax.set_title("Discount Percentage for Books (Above 20%)", fontsize=14)
    ax.grid(True, alpha=0.5)

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** 130 books are offered at a discount above 20%.
    - **Interpretation:** Discounts are likely used as a strategy to boost sales or clear inventory.
    """)


# 7. Find the Average Page Count for eBooks vs Physical Books
elif question == "7. Average Page Count for eBooks vs Physical Books":
    cursor.execute('''
    SELECT
        isEbook,
        AVG(pageCount) AS avg_page_count
    FROM books
    GROUP BY isEbook;
    ''')
    result = cursor.fetchall()
    average_page_count = pd.DataFrame(result, columns=["Book Type", "Average Page Count"])
    average_page_count["Book Type"] = average_page_count["Book Type"].replace({0: "Physical Book", 1: "EBook"})

    st.write("Average Page Count for eBooks vs Physical Books:")
    st.write(average_page_count)

    # Visualization (Bar Chart)
    fig, ax = plt.subplots(figsize=(4, 4))  # Create a new figure and axes
    ax.bar(average_page_count["Book Type"], average_page_count["Average Page Count"], color='cyan')
    ax.set_xlabel('Book Type', fontsize=13)
    ax.set_ylabel('Average Page Count', fontsize=13)
    ax.set_title('Average Page Count for eBooks vs Physical Books', fontsize=15)

    # Display the plot
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** 	
    \n Physical Books: 465 pages on average.
	\n eBooks: 382 pages on average.
    - **Interpretation:** 
    \n Physical books generally have higher page counts than eBooks, possibly reflecting their preference for detailed, comprehensive content. This could also suggest that eBooks are designed to be concise and easier to consume digitally.
    """)

# 8. Find the Top 3 Authors with the Most Books
elif question == "8. Top 3 Authors with the Most Books":
    cursor.execute('''
    SELECT
        book_authors,
        COUNT(*) AS book_count
    FROM books
    GROUP BY book_authors
    ORDER BY book_count DESC
    LIMIT 3 OFFSET 1;
    ''')
    result = cursor.fetchall()
    authors_with_most_books = pd.DataFrame(result, columns=["Authors", "Book Count"])
    st.write("Top 3 Authors with the Most Books:")
    st.write(authors_with_most_books)

    # Visualization (Bar Chart)
    fig, ax = plt.subplots(figsize=(8, 4))  # Create a new figure and axes
    ax.bar(authors_with_most_books["Authors"], authors_with_most_books["Book Count"], color='magenta')
    ax.set_xlabel('Authors', fontsize=12)
    ax.set_ylabel('Number of Books', fontsize=12)
    ax.set_title('Top 3 Authors with the Most Books', fontsize=14)
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

    # Display the plot
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** 
    \n 	Top authors:
        \n 1.	Michael R. Berthold (5 books).
        \n 2.	Christian Borgelt (5 books).
        \n 3.	Frank Höppner (5 books).

    - **Interpretation:** 
    \n These authors are prolific contributors, likely in technical or academic domains. Their consistent presence could indicate high demand for their expertise.
    """)

# 9. List Publishers with More than 10 Books
elif question == "9. List Publishers with More than 10 Books":
    cursor.execute('''
    SELECT
        book_publisher,
        COUNT(*) AS book_count
    FROM books
    WHERE book_publisher IS NOT NULL AND book_publisher != ''
    GROUP BY book_publisher
    HAVING book_count > 10;
    ''')
    result = cursor.fetchall()

    publisher_data = []
    for row in result:
        publisher, book_count = row
        publisher = publisher.strip().replace(",", '').replace('"', '').strip()  # Clean up the publisher name
        publisher_data.append([publisher, book_count])

    if publisher_data:
        publisher_with_more_than_10_books = pd.DataFrame(publisher_data, columns=["Publisher", "Book Count"])
        st.write("Publishers with More than 10 Books:")
        st.write(publisher_with_more_than_10_books)

        # Visualization (Bar Chart)
        fig, ax = plt.subplots(figsize=(11, 6))  # Create a new figure and axes
        ax.bar(
            publisher_with_more_than_10_books["Publisher"],
            publisher_with_more_than_10_books["Book Count"],
            color='yellow'
        )
        ax.set_xlabel('Publisher', fontsize=13)
        ax.set_ylabel('Number of Books', fontsize=12)
        ax.set_title('Publishers with More than 10 Books', fontsize=14)
        ax.tick_params(axis='x', rotation=90)  # Rotate x-axis labels for better readability

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No publishers with more than 10 books found.")

    st.markdown("""
    ### Analysis
    - **Insight:** 
    \n 23 publishers have more than 10 books.
    \n O’Reilly Media, Springer Nature, and Packt Publishing are notable leaders.

    - **Interpretation:** 
     \n These publishers are dominant forces in the industry, producing high volumes of content that cater to a wide range of readers.
    """)


# 10. Find the Average Page Count for Each Category
elif question == "10. Average Page Count for Each Category":
    cursor.execute('''
    SELECT
        categories,
        AVG(pageCount) AS avg_page_count
    FROM books
    WHERE categories IS NOT NULL AND TRIM(categories) != ''
    GROUP BY categories;
    ''')
    result = cursor.fetchall()

    # Create a DataFrame from the result
    average_page_count = pd.DataFrame(result, columns=["Category", "Average Page Count"])

    # Display the data table
    st.write("Average Page Count for Each Category:")
    st.write(average_page_count)

    # Calculate and display the total number of categories
    total_categories = len(average_page_count)
    st.write(f"Total number of categories : {total_categories}")

    # Find categories with highest and lowest average page counts
    max_category = average_page_count.iloc[average_page_count["Average Page Count"].idxmax()]
    min_category = average_page_count.iloc[average_page_count["Average Page Count"].idxmin()]

    # Visualization (Line Chart)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        average_page_count["Category"],
        average_page_count["Average Page Count"],
        marker='o', linestyle='-', color='blue', label='Average Page Count'
    )

    # Highlight high and low points
    ax.scatter(max_category["Category"], max_category["Average Page Count"], color='red',
               label=f"Highest: {max_category['Category']}")
    ax.scatter(min_category["Category"], min_category["Average Page Count"], color='green',
               label=f"Lowest: {min_category['Category']}")

    # Add annotations for the highest and lowest points
    ax.text(
        max_category["Category"], max_category["Average Page Count"] + 5, f"{max_category['Category']}",
        color='red', ha='center', fontsize=10
    )
    ax.text(
        min_category["Category"], min_category["Average Page Count"] - 5, f"{min_category['Category']}",
        color='green', ha='center', fontsize=10
    )

    # Set axis labels and title
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Average Page Count", fontsize=12)
    ax.set_title("Average Page Count for Each Category", fontsize=14)

    # Hide x-axis labels and add a legend
    ax.set_xticklabels([])
    ax.legend()

    # Display the plot
    st.pyplot(fig)
    st.markdown("""
    ### Analysis
    - **Insight:** Categories like "American Medical Association" (2296 pages) and "Administrative agencies" (1546 pages) have the highest average page counts.
    - **Interpretation:** Certain categories, such as medical and administrative, have significantly higher page counts, likely due to the technical or reference nature of these books.
    """)

# 11. Retrieve Books with More than 3 Authors
elif question == "11. Books with More than 3 Authors":
    cursor.execute('''
    SELECT
        book_title,
        book_authors
    FROM books
    WHERE book_authors IS NOT NULL
    AND LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;
    ''')
    result = cursor.fetchall()
      

    # Check if the query returned any results
    if result:
        # Convert query result to a DataFrame
        book_author_3 = pd.DataFrame(result, columns=["Book Title", "Authors"])

        
        # Display the table in Streamlit
        st.write(book_author_3)

        # Visualization: Scatter Plot for Author Count
        book_author_3['Author Count'] = book_author_3['Authors'].apply(lambda x: len(x.split(',')))

        # Create a scatter plot
        fig, ax = plt.subplots(figsize=(14, 8))
        scatter = ax.scatter(
             book_author_3['Book Title'],
             book_author_3['Author Count'],
             c=book_author_3['Author Count'],
             cmap='cool',
             s=book_author_3['Author Count'] * 50,  # Adjust marker size based on Author Count
             alpha=0.7,
            )
        plt.colorbar(scatter, label="Author Count")
        ax.set_xlabel("Book Title", fontsize=14)
        ax.set_ylabel("Number of Authors", fontsize=14)
        ax.set_title("Books with More than 3 Authors", fontsize=16)
        plt.xticks(rotation=90, ha="right")
        plt.tight_layout()

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No books found with more than 3 authors.")
    
    st.markdown("""
    ### Analysis
    - **Insight:** 74 books have more than 3 authors.
    - **Interpretation:** These books are likely collaborative efforts in fields such as research, academia, or specialized industries where multiple contributors bring diverse expertise.
    """)


# 12.Books with Ratings Count Greater Than the Average

elif question == "12. Books with Ratings Count Greater Than the Average":
    cursor.execute('''
        SELECT
            book_title,
            CASE 
                WHEN ratingsCount > 10 THEN ratingsCount / 10
                ELSE ratingsCount
            END AS adjusted_ratingsCount
        FROM books;
    ''')
    result = cursor.fetchall()
    ratings_df = pd.DataFrame(result, columns=["Book Title", "Rating Count"]) 

    # Calculate the average of adjusted ratings
    average_adjusted_rating = ratings_df["Rating Count"].mean()

    # Filter books with adjusted ratings above average
    books_above_average = ratings_df[ratings_df["Rating Count"] > average_adjusted_rating]

    st.write("Books with Ratings Above Average:")
    st.write(books_above_average)
    st.write(f"Average Rating Count: {average_adjusted_rating:.2f}")

    # Visualization (Bar Chart)
    fig, ax = plt.subplots(figsize=(20, 10))  # Increase width further
    ax.bar(books_above_average["Book Title"], books_above_average["Rating Count"], color='green', width=0.8)  # Increase bar width
    ax.set_xlabel('Book Title', fontsize=18)  
    ax.set_ylabel('Ratings Count', fontsize=18)  
    ax.set_title('Books with Ratings Count Above Average', fontsize=20)  
    ax.tick_params(axis='both', which='major', labelsize=16)  

    # Rotate x-axis labels for better readability if needed
    ax.set_xticklabels(books_above_average["Book Title"], rotation=90, ha="right")

    # Adjust spacing between x-axis labels
    plt.tight_layout() 

    st.pyplot(fig)

    st.markdown("""
    ### Analysis
    - **Insight:** 22 Books with a rating count higher than the average (1.97) indicate higher popularity or audience engagement.
    \n Examples include:
    \n •	"Natural Language Processing with Python": 4
    \n •	"Python in a Nutshell": 8
    \n •	"Programming Python": 4
    \n •	"Patterns of Enterprise Application Architecture": 8

    - **Interpretation:** Books with ratings higher than the average are more likely to be considered useful, engaging, or well-written. These books are strong candidates for marketing or promotional campaigns.
    """)

# 13. Books with the Same Author Published in the Same Year
elif question == "13. Books with the Same Author Published in the Same Year":
    cursor.execute('''
    SELECT
        book_authors,
        CASE
            WHEN year LIKE '____-__-__' THEN strftime('%Y', year)
            ELSE year
        END AS processed_year,
        COUNT(*) AS book_count
    FROM books
    WHERE book_authors IS NOT NULL AND TRIM(book_authors) != ''
    GROUP BY book_authors, processed_year
    HAVING book_count > 1;
    ''')
    result = cursor.fetchall()

    # Convert to DataFrame
    author_year = pd.DataFrame(result, columns=["Authors", "Year", "Book Count"])

    # Drop rows with None values
    author_year = author_year.dropna(subset=["Authors", "Year"])

    # Initialize the figure to avoid "undefined" error
    fig, ax = plt.subplots(figsize=(12, 6))

    if not author_year.empty:
        st.write(author_year)

        # Normalize sizes for better visualization
        sizes = author_year["Book Count"] * 50  # Adjust scaling factor as needed

        # Scatter Plot
        scatter = ax.scatter(
            x=author_year["Authors"],
            y=author_year["Year"],
            s=sizes,  # Use sizes based on "Book Count"
            alpha=0.7,
            c=author_year["Book Count"],
            cmap='viridis'
        )
        ax.set_xlabel('Authors')
        ax.set_ylabel('Year')
        ax.set_title('Books with the Same Author Published in the Same Year')
        ax.tick_params(axis='x', rotation=90, labelsize=8)  # Rotate x-axis labels
        fig.colorbar(scatter, ax=ax, label='Book Count')  # Add color bar for scale
    else:
        st.write("No records with valid authors and the same publication year found.")
        ax.text(0.5, 0.5, 'No Data Available', fontsize=16, ha='center', va='center', transform=ax.transAxes)

    # Pass the figure to st.pyplot
    st.pyplot(fig)

    st.markdown("""
    ### Analysis
    - **Insight:**  Authors like Al Sweigart, Alex Martelli, and many others published multiple books in a given year.	Most authors have published 2 books in the same year, and a few have published 3.
    - **Interpretation:** 	Publishing multiple books in the same year indicates that these authors are either prolific writers or their works are split into multiple volumes.
    - **Recommendation:** 	For marketing, highlight such authors to boost sales and readership by promoting their complete collection.
    """)

# 14. Books with a Specific Keyword in the Title
elif question == "14. Books with a Specific Keyword in the Title":
    # Create a sidebar for user input
    st.sidebar.title("Select Keyword")
    selected_keyword = st.sidebar.radio("Choose Keyword", ["Python", "Data Science", "Python & Data Science"])

    # Define the query based on user selection
    if selected_keyword == "Python":
        keyword1 = "python"
        keyword2 = None  # Only looking for "python" in the title
        exclude_keyword = "data science"  # Exclude books that have "data science"
    elif selected_keyword == "Data Science":
        keyword1 = "data science"
        keyword2 = None  # Only looking for "data science" in the title
        exclude_keyword = "python"  # Exclude books that have "python"
    elif selected_keyword == "Python & Data Science":
        keyword1 = "data science"
        keyword2 = "python"  # Both "data science" and "python" need to be in the title
        exclude_keyword = None  # No exclusion needed for this case

    # Construct the query based on the selected keywords
    if keyword2 is None:  # If only one keyword is needed
        # Exclude books that contain the other keyword if necessary
        if exclude_keyword:
            cursor.execute(f'''
            SELECT
                book_title
            FROM books
            WHERE LOWER(book_title) LIKE '%{keyword1.lower()}%'
            AND LOWER(book_title) NOT LIKE '%{exclude_keyword.lower()}%';
            ''')
        else:
            cursor.execute(f'''
            SELECT
                book_title
            FROM books
            WHERE LOWER(book_title) LIKE '%{keyword1.lower()}%';
            ''')
    else:  # If both keywords are needed, regardless of order or words in between
        cursor.execute(f'''
        SELECT
            book_title
        FROM books
        WHERE LOWER(book_title) LIKE '%{keyword1.lower()}%' 
        AND LOWER(book_title) LIKE '%{keyword2.lower()}%';
        ''')

    # Fetch the results
    result = cursor.fetchall()
    keyword_books = pd.DataFrame(result, columns=["Book Title"])

    # Display the results
    st.write(f"Books related to: {selected_keyword}")
    st.write(keyword_books)
    
    data = {
        "Keywords": ["Python", "Data Science", "Both", "Others"],
        "Book Count": [329, 226, 20, 669]  # Replace with your actual counts
    }
    
    # Convert data to a DataFrame
    keyword_df = pd.DataFrame(data)
     # Visualization (Bar Chart)
    fig, ax = plt.subplots(figsize=(8, 6))  # Create a new figure and axis
    ax.bar(keyword_df["Keywords"], keyword_df["Book Count"], color=["blue", "green", "orange", "indigo"])
    ax.set_xlabel("Keywords", fontsize=12)
    ax.set_ylabel("Book Count", fontsize=12)
    ax.set_title("Books with Specific Keywords in the Title", fontsize=14)
    ax.bar_label(ax.containers[0], fmt='%d')  # Add value labels on bars
    
    # Display chart in Streamlit
    st.pyplot(fig)

    st.markdown("""
    ### Analysis
    - **Insight:** 
    	\n Total books: 1286.
        \n Python keyword: 329 books.
        \n Data Science keyword: 226 books.
        \n Both keywords: 20 books.

    - **Interpretation:** Python is a prominent keyword, reflecting its widespread use in programming. Data Science also has substantial representation, aligning with its growing industry relevance.

    """)

# 15. Year with the Highest Average Book Price
elif question == "15. Year with the Highest Average Book Price":
    cursor.execute('''
    SELECT
        CASE
            WHEN year LIKE '____-__-__' THEN strftime('%Y', year)
            ELSE year
        END AS processed_year,
        AVG(amount_retailPrice) AS avg_price
    FROM books
    GROUP BY year
    ORDER BY avg_price DESC
    LIMIT 3;
    ''')
    result = cursor.fetchall()
    high_avg_price_year = pd.DataFrame(result, columns=["Year", "Average Price"])
    st.write(high_avg_price_year)

    st.markdown("""
    ### Analysis
    - **Insight:** The year 2023 has the highest average book price at $519.2. Other high-price years include 2021 ($376) and 2018 ($351.2).

    - **Interpretation:** 	Books published in recent years are priced higher, reflecting the demand for updated and relevant content. Academic and niche content might contribute to these higher prices.

    """)



# 16. Count Authors Who Published 3 Consecutive Years
elif question == "16. Count Authors Who Published 3 Consecutive Years":
    cursor.execute('''
        WITH consecutive_years AS (
            SELECT
                book_authors,
                strftime('%Y', COALESCE(year, '0000-00-00')) AS year 
            FROM books
            GROUP BY book_authors, year
            HAVING COUNT(DISTINCT year) >= 3
        )
        SELECT
            book_authors,
            COUNT(DISTINCT year) AS consecutive_year_count
        FROM consecutive_years
        GROUP BY book_authors;
    ''')
    result = cursor.fetchall()
    if result:
        author_year = pd.DataFrame(result, columns=["Authors", "Consecutive Year Count"])
        st.write(author_year)

        # Visualization (Bar Chart)
        plt.bar(author_year["Authors"], author_year["Consecutive Year Count"], color='purple')
        plt.xlabel('Authors')
        plt.ylabel('Consecutive Year Count')
        plt.xticks(rotation=45, ha="right")
        st.pyplot()
    else:
        st.markdown("""
        ### Analysis
        - **Insight:**
        """)
        st.write("No authors have published in 3 consecutive years.")
    
        st.markdown("""
        - **Interpretation:**
	    Publishing patterns indicate that authors tend to focus on quality over quantity.
        \n - **Recommendation:**
	    Encourage authors to produce more consistent publications to retain audience engagement.
        """)

# 17. Authors Who Have Published Books in the Same Year but Under Different Publishers
elif question == "17. Authors Who Have Published Books in the Same Year but Under Different Publishers":
   
    #cursor.execute('''
     #   SELECT
          #  book_authors,
         #   strftime('%Y', year) AS year,
        #    GROUP_CONCAT(DISTINCT book_publisher) AS publishers
       # FROM books
      #  GROUP BY book_authors, year
     #   HAVING COUNT(DISTINCT book_publisher) > 1;
    #''')
    #result = cursor.fetchall()
    #if result:
      #  author_publisher_df = pd.DataFrame(result, columns=["Authors", "Year", "Publishers"]) 
      #  author_publisher_df["Publishers"] = author_publisher_df["Publishers"].str.strip().str.replace(",", "").str.replace('"', '').str.strip()
     #   st.write(author_publisher_df)
         
    #else:
        
    #st.write("No authors have published with more than one publisher in the same year.")

    st.markdown("""
    ### Analysis
    - **Insight:** 	No authors published books with more than one publisher in the same year.

    - **Interpretation:** 	Authors might be following exclusivity agreements with publishers or focusing on building their reputation with a single publishing house.
    """)


# 18. Average Amount of Retail Price for eBooks and Physical Books
elif question == "18. Average Amount of Retail Price for eBooks and Physical Books":
    cursor.execute('''
    SELECT
        AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice END) AS avg_ebook_price,
        AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice END) AS avg_physical_price
    FROM books;
    ''')
    result = cursor.fetchall()
    avg_book_price = pd.DataFrame(result, columns=["Average Ebook Price", "Average Physical Book Price"])
    st.write(avg_book_price)
    #st.write("No Pysical Books are Priced")

    st.markdown("""
### Analysis
- **Insight:**
  - No physical books are priced.
  - The average retail price for eBooks is $50.20.

- **Interpretation:**
  - eBooks dominate the market, and the pricing aligns with the affordability and accessibility of digital formats.

- **Recommendation:**
  - Evaluate strategies for introducing affordable physical books for audiences who prefer traditional reading formats.
""")


   

# 19. Books with Average Rating More Than Two Standard Deviations Away from the Average
elif question == "19. Books with Average Rating More Than Two Standard Deviations Away from the Average":
    cursor.execute('''
    WITH avg_and_variance AS (
        SELECT
            AVG(averageRating) AS avg_rating,
            SUM((averageRating - (SELECT AVG(averageRating) FROM books)) *
                (averageRating - (SELECT AVG(averageRating) FROM books))) / COUNT(averageRating) AS variance
        FROM books
    )
    SELECT
        book_title,
        averageRating,
        ratingsCount
    FROM books, avg_and_variance
    WHERE ABS(averageRating - avg_rating) > 2 * SQRT(variance);
    ''')
    result = cursor.fetchall()

    if result:
        # Create a DataFrame from the result
        std_above_2 = pd.DataFrame(result, columns=["Title", "Average Rating", "Ratings Count"])
        st.write("Books with Average Ratings More Than Two Standard Deviations Away:")
        st.write(std_above_2)

        # Scatter plot visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        # Scatter plot for all books
        ax.scatter(
            std_above_2.index,
            std_above_2["Average Rating"],
            c="red",
            s=std_above_2["Ratings Count"] * 2,  # Adjust the size based on Ratings Count
            alpha=1,
            label="Outliers"
        )
        ax.axhline(
            std_above_2["Average Rating"].mean(), 
            color="blue", 
            linestyle="--", 
            label="Mean Rating"
        )

        # Adding plot details
        ax.set_xlabel("Books (Index)", fontsize=12)
        ax.set_ylabel("Average Rating", fontsize=12)
        ax.set_title("Scatter Plot of Average Ratings with Outliers Highlighted", fontsize=14)
        ax.legend()
        st.pyplot(fig)

    else:
        st.write("No books have average ratings more than two standard deviations away from the average.")
    
    st.markdown("""
### Analysis
- **Insight:**
  - Books like "Learning Python," "Python Web Programming," and others deviate significantly from the average.
  - These deviations are primarily negative, with low ratings across several titles.

- **Interpretation:**
  - The low ratings could indicate outdated content, lack of relevance, or poor execution.

- **Recommendation:**
  - Analyze customer feedback for poorly rated books and update or replace them with improved editions.
""")



    # 20. Publisher with the Highest Average Rating Among Publishers with More than 10 Books
elif question == "20. Publisher with the Highest Average Rating Among Publishers with More than 10 Books":
    cursor.execute('''
    SELECT
        book_publisher,
        AVG(averageRating) AS avg_rating,
        COUNT(*) AS book_count
    FROM books
    GROUP BY book_publisher
    HAVING book_count > 10
    ORDER BY avg_rating DESC
    LIMIT 1;
    ''')
    result = cursor.fetchall()
    if result:
        book_publisher, avg_rating, book_count = result[0]
        book_publisher = book_publisher.strip().replace(",", '').replace('"', '').strip()
        #st.write(f"The publisher with the highest average rating is '{book_publisher}'. "
         #        f"Number of books: {book_count}. Average rating: {avg_rating:.2f}.")
    else:
        st.write("No publishers with more than 10 books found.")
    
    st.markdown("""
### Analysis
- **Insight:**
  - Springer Nature has the highest average rating of 5.00.
  - Number of books: 43.

- **Interpretation:**
  - Springer Nature maintains a consistent reputation for quality, possibly due to its focus on academic and scientific content.
""")


conn.close()