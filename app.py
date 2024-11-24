import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import tempfile
import io
from textblob import TextBlob
from newsapi.newsapi_client import NewsApiClient
from datetime import datetime, timedelta, date
import math
import requests
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*file uploader encoding.*")


# Function to load data from Excel
def load_data(excel_path):
    df = pd.read_excel(excel_path)
    return df

# Function to calculate BMI
def calculate_bmi(height, weight):
    if height == 0:
        st.warning("Height should not be zero for BMI calculation.")
        return None
    bmi = weight / ((height / 100) ** 2)  # Height in meters
    return bmi

# Function to predict BMI category
def predict_bmi_category(calculated_bmi):
    if calculated_bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= calculated_bmi < 25:
        return 'Normal weight'
    else:
        return 'Overweight'

# Function to filter data based on user input
def filter_data(df, age, gender, meal_type, bmi_category):
    selected_data = df[(df['Age'] == age) &
                       (df['Gender'] == gender) &
                       (df['Type of Meal'] == meal_type) &
                       (df['BMI'] == bmi_category)]
    return selected_data

# Function to display diet plan
def display_diet_plan(selected_data):
    if not selected_data.empty:
        output_columns = ['Day', 'Breakfast ( 7 AM )', 
                          'Morning Snack ( 10 AM )',
                          'Lunch ( 12.30 PM)',
                          'Evening Snack ( 4 PM )', 
                          'Dinner ( 7 PM )'
                          ]
        # Reset index to start from 0 before displaying
        selected_data_reset_index = selected_data[output_columns].reset_index(drop=True)

        # Display the selected columns for the one-week diet plan
        st.write("\nOne-Week Diet Plan:")
        st.dataframe(selected_data_reset_index)             
    else:
        st.warning("No matching data found for the given criteria.")

# Function to create bar chart for total nutrition in a week with different colors
def bar_chart_total_nutrition(selected_data):
    nutritional_columns = ['Total Calorie (kcal)', 'Total Protein (g)', 'Total Fat (g)',
                            'Total Carbohydrate (g)', 
                            'Total Vitamin (IU)', 'Total Mineral (mg)']

    # Calculate the total sum for each nutritional category across the week
    total_sum = selected_data[nutritional_columns].sum()

    # Create a bar chart with different colors for each nutritional category
    fig = px.bar(x=nutritional_columns, y=total_sum,
                 labels={'x': 'Nutritional Category', 'y': 'Total Sum'},
                 title='Total Nutritional Values in a Week',
                 color=nutritional_columns)

    st.plotly_chart(fig)

# Function to create animated pie chart for nutritional information
def animated_pie_chart(selected_data):
    nutritional_columns = ['Total Calorie (kcal)', 'Total Protein (g)', 'Total Fat (g)',
                            'Total Carbohydrate (g)', 
                            'Total Vitamin (IU)', 'Total Mineral (mg)']

    for column in nutritional_columns:
        fig = px.pie(selected_data, names='Day', values=column, title=f'{column} Distribution',
                     hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3)
        # Increase the size of the pie chart
        fig.update_layout(height=600, width=700)  # Adjust height and width as needed
        st.plotly_chart(fig)

def generate_diet_plan(age):
    print("Generating diet plan for age:", age)
    if age == "1 month":
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Diet Plan': ['Breast Milk / Formula Milk'] * 7,
            'Amount': ['Every 2-3 hours / 2-3 ounces'] * 7,
            'Frequency': ['8-12 times'] * 7,
            'Total Calorie (kcal)': [120] * 7,
            'Total Protein (g)': [8] * 7,
            'Total Fat (g)': [5] * 7,
            'Total Carbohydrate (g)': [12] * 7,
            'Total Vitamin (IU)': [400] * 7,
            'Total Mineral (mg)': [200] * 7,
        }
    elif age == "2 months":
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Diet Plan': ['Breast Milk / Formula Milk'] * 7,
            'Amount': ['Every 2-3 hours / 4 ounces'] * 7,
            'Frequency': ['8-12 times / 6-8 times'] * 7,
            'Total Calorie (kcal)': [130] * 7,
            'Total Protein (g)': [9] * 7,
            'Total Fat (g)': [6] * 7,
            'Total Carbohydrate (g)': [15] * 7,
            'Total Vitamin (IU)': [450] * 7,
            'Total Mineral (mg)': [220] * 7,
        }
    elif age == "3 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Diet Plan': ['Breast Milk / Formula Milk'] * 7,
            'Amount': ['Every 3-4 hours / 4-6 ounces'] * 7,
            'Frequency': ['6-7 times / 5-6 times'] * 7,
            'Total Calorie (kcal)': [140] * 7,
            'Total Protein (g)': [10] * 7,
            'Total Fat (g)': [7] * 7,
            'Total Carbohydrate (g)': [18] * 7,
            'Total Vitamin (IU)': [500] * 7,
            'Total Mineral (mg)': [250] * 7,
        }
    elif age == "4 months"  :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Diet Plan': ['Breast Milk / Formula Milk'] * 7,
            'Amount': ['Every 3-4 hours / 4-8 ounces'] * 7,
            'Frequency': ['6-7 times / 5-7 times'] * 7,
            'Total Calorie (kcal)': [150] * 7,
            'Total Protein (g)': [11] * 7,
            'Total Fat (g)': [8] * 7,
            'Total Carbohydrate (g)': [20] * 7,
            'Total Vitamin (IU)': [550] * 7,
            'Total Mineral (mg)': [270] * 7,
        }
    elif age == "5 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Diet Plan': ['Breast Milk / Formula Milk'] * 7,
            'Amount': ['Every 3-4 hours / 5-8 ounces'] * 7,
            'Frequency': ['6-7 times / 5-7 times'] * 7,
            'Total Calorie (kcal)': [160] * 7,
            'Total Protein (g)': [12] * 7,
            'Total Fat (g)': [9] * 7,
            'Total Carbohydrate (g)': [22] * 7,
            'Total Vitamin (IU)': [600] * 7,
            'Total Mineral (mg)': [300] * 7,
        } 
    elif age == "6 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Avocado Puree', 'Banana Puree', 'Cheeku Puree', 'Apple Sauce', 'Suji Halwa', 'Sweet Potato Mash', 'Rice Cereal'],
            'Mid-Morning': ['Breast Milk / Formula Milk'] * 7,
            'Lunch': ['Ground and Sweet Potato Puree', 'Moong Dal Soup', 'Pureed Kichidi', 'Carrot Mash', 'Pumpkin Puree', 'Masoor Dal Soup', 'Pumpkin and Carrot Mash'],
            'Afternoon': ['Breast Milk / Formula Milk'] * 7,
            'Dinner': ['Suji Kheer', 'Ragi Porridge', 'Suji Kheer', 'Rice Gruel', 'Sweet Potato Kheer', 'Dal Rice Puree', 'Moong Dal Soup'],
            'Late Night': ['Breast Milk / Formula Milk'] * 7,
            'Total Calorie (kcal)': [200, 150, 180, 160, 190, 170, 160],
            'Total Protein (g)': [8, 7, 9, 6, 8, 7, 6],
            'Total Fat (g)': [10, 8, 9, 7, 9, 8, 7],
            'Total Carbohydrate (g)': [25, 20, 22, 18, 23, 21, 20],
            'Total Vitamin (IU)': [600] * 7,
            'Total Mineral (mg)': [350, 300, 320, 280, 330, 310, 300],
        }
    elif age == "7 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Pear Puree', 'Ragi Apple Porridge', 'Pear Puree', 'Khichdi', 'Wheat Pancakes', 'Idli with Dal', 'Ragi Porridge'],
            'Mid-Morning': ['Breast Milk / Formula Milk'] * 7,
            'Lunch': ['Ground and Sweet Potato Puree', 'Ghee Rice', 'Broken Wheat Khichdi', 'Rice with Curd', 'Fish Puree', 'Khichdi', 'Rice with Curd'],
            'Evening Snack': ['Carrot Badam Kheer', 'Yogurt (Flavoured with Fruit)', 'Lentil Soup', 'Boiled Vegetable Bowl', 'Carrot Badam Kheer', 'Banana', 'Lentil Soup'],
            'Mid-Evening': ['Breast Milk / Formula Milk'] * 7,
            'Dinner': ['Ragi Porridge', 'Millet Porridge', 'Curd Rice', 'Rice Porridge', 'Ragi Porridge', 'Moongdal Khichdi', 'Millet Porridge'],
            'Late Night': ['Breast Milk / Formula Milk'] * 7,
            'Total Calorie (kcal)': [220, 180, 200, 210, 240, 190, 200],
            'Total Protein (g)': [9, 8, 9, 10, 11, 8, 9],
            'Total Fat (g)': [12, 10, 11, 11, 13, 10, 11],
            'Total Carbohydrate (g)': [28, 25, 26, 27, 30, 28, 26],
            'Total Vitamin (IU)': [650] * 7,
            'Total Mineral (mg)': [380, 340, 360, 370, 400, 350, 360],
        }
    elif age == "8 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Ragi Apple Porridge', 'Wheat Pancakes', 'Pear Puree', 'Pear Puree', 'Ragi Porridge', 'Idli with Dal', 'Khichdi'],
            'Mid-Morning': ['Breast Milk / Formula Milk'] * 7,
            'Lunch': ['Ghee Rice', 'Fish Puree', 'Ground and Sweet Potato Puree', 'Broken Wheat Khichidi', 'Rice with Curd', 'Khichdi', 'Rice with Curd'],
            'Evening Snack': ['Yogurt (Flavoured with Fruit)', 'Carrot Badam Kheer', 'Carrot Badam Kheer', 'Lentil Soup', 'Lentil Soup', 'Banana', 'Boiled Vegetable Bowl'],
            'Mid-Evening': ['Breast Milk / Formula Milk'] * 7,
            'Dinner': ['Millet Porridge', 'Ragi Porridge', 'Ragi Porridge', 'Curd Rice', 'Millet Porridge', 'Moongdal Khichdi', 'Rice Porridge'],
            'Late Night': ['Breast Milk / Formula Milk'] * 7,
            'Total Calorie (kcal)': [240, 220, 230, 250, 260, 210, 240],
            'Total Protein (g)': [10, 9, 10, 11, 12, 8, 10],
            'Total Fat (g)': [12, 11, 11, 13, 14, 10, 12],
            'Total Carbohydrate (g)': [30, 28, 29, 31, 32, 27, 30],
            'Total Vitamin (IU)': [700] * 7,
            'Total Mineral (mg)': [400, 380, 390, 420, 430, 360, 400],
        }
    elif age == "9 months" :
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Steamed Dosa', 'Kheer (Sooji)', 'Soft-Fluffy Idlis', 'Oats Pancakes', 'Rice Cereal', 'Wheat Kheer', 'Mashed Banana Pancakes'],
            'Mid-Morning Snack': ['Veg Soup', 'Boiled Egg', 'Mashed Pears', 'Breadsticks', 'Pumpkin Rava Sticks', 'Yoghurt', 'Blueberries/Cherries'],
            'Lunch': ['Plain Pongal', 'Carrot Khichdi', 'Small pieces of Roti/Phulka with Paneer', 'Plain Ghee Rice', 'Flavoured Rice', 'Vegetable Khichdi', 'Tomato Khichdi/Vegetable Rice'],
            'Afternoon': ['Breast Milk/Formula Milk'] * 7,
            'Evening Snack': ['Apple Fingers', 'Grape', 'Papaya', 'Chickoo Mash', 'Carrot Fingers', 'Frozen Banana', 'Sweet Potato Fingers'],
            'Dinner': ['Homemade Cereal', 'Plain Khichdi', 'Wheat Almond Porridge', 'Ragi Porridge', 'Oats Apple Porridge', 'Chicken Soup', 'Brown Rice Cereal'],
            'Late Night': ['Breast Milk/Formula Milk'] * 7,
            'Total Calorie (kcal)': [250, 220, 240, 260, 270, 230, 250],
            'Total Protein (g)': [11, 10, 11, 12, 13, 10, 11],
            'Total Fat (g)': [13, 12, 12, 14, 15, 11, 13],
            'Total Carbohydrate (g)': [32, 30, 31, 33, 34, 29, 32],
            'Total Vitamin (IU)': [750] * 7,
            'Total Mineral (mg)': [420, 400, 410, 430, 440, 390, 420],
        }
    elif age == "10 months":
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Cereal with Grated Apple', 'Oatmeal Porridge with Banana', 'Egg Yolks with Toast', 'Dalia Porridge', 'Paneer Burji Sandwich', 'French Toast', 'Ragi Porridge with Steamed Apples'],
            'Mid-Morning': ['Cut Papaya', 'Banana Slices', 'Grapes', 'Rusk', 'Cut Melon', 'Steamed Carrots', 'Steamed Apples'],
            'Lunch': ['Rice with Chicken Broth', 'Vegetables, Rice and Grilled Fish', 'Vegetables, Pulao with Curd', 'Chapatti with Vegetables', 'Rice and Pumpkin Curry', 'Chapatti with Sambar and Vegetables', 'Idly with Sambar'],
            'Afternoon': ['Breast Milk or Formula Milk'] * 7,
            'Dinner': ['Dosa with Sambar', 'Chicken Soup and Toast', 'Chapatti with Vegetables', 'Rice and Steamed Fish', 'Chapatti with Vegetables and Curd', 'Rice with Moong Dal Khichdi', 'Mashed Potato with Spinach'],
            'Late Night': ['Breast Milk or Formula Milk'] * 7,
            'Total Calorie (kcal)': [300, 320, 280, 330, 310, 340, 290],
            'Total Protein (g)': [14, 13, 12, 15, 14, 16, 11],
            'Total Fat (g)': [15, 16, 14, 17, 13, 18, 12],
            'Total Carbohydrate (g)': [40, 38, 35, 42, 39, 44, 36],
            'Total Vitamin (IU)': [800] * 7,
            'Total Mineral (mg)': [450, 430, 410, 460, 440, 470, 400],
        }

    elif age == "11 months":
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Whole Wheat Pancakes', 'Rice Pudding with Berries', 'Scrambled Eggs with Spinach', 'Barley Porridge', 'Vegetable Wrap', 'Cheese Sandwich', 'Quinoa Upma'],
            'Mid-Morning': ['Pineapple Chunks', 'Apple Slices', 'Orange Segments', 'Walnuts', 'Cucumber Sticks', 'Cherry Tomatoes', 'Blueberries'],
            'Lunch': ['Vegetable Biryani with Raita', 'Quinoa Salad with Grilled Chicken', 'Brown Rice and Lentil Stew', 'Chapatti with Mixed Vegetable Curry', 'Mushroom and Spinach Quesadilla', 'Dal Tadka with Brown Rice', 'Vegetable Stir-fry with Tofu'],
            'Afternoon': ['Breast Milk or Formula Milk'] * 7,
            'Dinner': ['Vegetable Paratha with Yogurt', 'Salmon Teriyaki with Brown Rice', 'Whole Wheat Pasta with Tomato Sauce', 'Paneer Tikka with Roti', 'Grilled Fish Tacos', 'Lentil Soup with Quinoa', 'Sweet Potato and Chickpea Curry'],
            'Late Night': ['Breast Milk or Formula Milk'] * 7,
            'Total Calorie (kcal)': [310, 330, 290, 340, 320, 350, 300],
            'Total Protein (g)': [15, 14, 13, 16, 15, 17, 12],
            'Total Fat (g)': [16, 17, 15, 18, 14, 19, 13],
            'Total Carbohydrate (g)': [42, 40, 37, 44, 41, 46, 38],
            'Total Vitamin (IU)': [820] * 7,
            'Total Mineral (mg)': [460, 440, 420, 470, 450, 480, 410],
        }
    elif age == "12 months":
        diet_plan = {
            'Day': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'Early Morning': ['Breast Milk / Formula Milk'] * 7,
            'Breakfast': ['Egg and Spinach Breakfast Wrap', 'Quinoa Porridge with Mixed Berries', 'Vegetable Omelette with Whole Grain Toast', 'Millet Porridge with Almonds', 'Tomato and Avocado Sandwich', 'Whole Wheat Pasta Salad with Grilled Chicken', 'Brown Rice Upma'],
            'Mid-Morning': ['Orange Segments', 'Kiwi Slices', 'Mixed Nuts (Almonds, Walnuts)', 'Greek Yogurt with Berries', 'Carrot Sticks with Hummus', 'Cottage Cheese Cubes', 'Pomegranate Seeds'],
            'Lunch': ['Baked Salmon with Quinoa Pilaf', 'Vegetable and Chickpea Salad', 'Barley and Lentil Soup', 'Chapatti with Palak Paneer', 'Grilled Shrimp Tacos with Whole Wheat Tortillas', 'Vegetarian Bolognese with Whole Wheat Spaghetti', 'Stir-Fried Tofu with Brown Rice'],
            'Afternoon': ['Breast Milk or Formula Milk'] * 7,
            'Dinner': ['Spinach and Cheese Stuffed Paratha with Raita', 'Grilled Chicken Breast with Sweet Potato Mash', 'Whole Wheat Spaghetti with Tomato-Basil Sauce', 'Paneer Bhurji with Roti', 'Quinoa and Black Bean Bowl', 'Dal Makhani with Brown Rice', 'Chickpea and Vegetable Curry with Quinoa'],
            'Late Night': ['Breast Milk or Formula Milk'] * 7,
            'Total Calorie (kcal)': [320, 340, 300, 350, 330, 360, 310],
            'Total Protein (g)': [16, 15, 14, 17, 16, 18, 13],
            'Total Fat (g)': [17, 18, 16, 19, 15, 20, 14],
            'Total Carbohydrate (g)': [44, 42, 39, 46, 43, 48, 40],
            'Total Vitamin (IU)': [830] * 7,
            'Total Mineral (mg)': [470, 450, 430, 480, 460, 490, 420],
        }
    diet_plan_df = pd.DataFrame(diet_plan)

    return diet_plan_df
# Function to generate nutritional information for babies below 1 year
def generate_nutritional_info_below_1(diet_plan):
    # Extracting nutritional information from the diet plan DataFrame
    nutritional_info = diet_plan[['Day', 'Total Calorie (kcal)', 'Total Protein (g)', 'Total Fat (g)', 'Total Carbohydrate (g)','Total Vitamin (IU)','Total Mineral (mg)']]
    nutritional_info.set_index('Day', inplace=True)  # Set 'Day' as the index for better visualization
    return nutritional_info

def pie_chart_nutritional_info(nutritional_info):
    # Reorder columns starting from 'Total Calorie (kcal)'
    columns_order = ['Total Calorie (kcal)', 'Total Protein (g)', 'Total Fat (g)',
                     'Total Carbohydrate (g)', 'Total Vitamin (IU)', 'Total Mineral (mg)']
    
    # Select data based on the reordered columns
    reordered_nutritional_info = nutritional_info[columns_order]

    for column in reordered_nutritional_info.columns:
        title = f'{column} Distribution'
        values = reordered_nutritional_info[column]
        fig = px.pie(names=nutritional_info.index, values=values, title=title,
                     hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3)
        # Increase the size of the pie chart
        fig.update_layout(height=600, width=700)  # Adjust height and width as needed
        st.plotly_chart(fig)


# Updated function to display bar chart for nutritional information
def bar_chart_nutritional_info(nutritional_info):
    # Extracting columns and their order
    columns_order = ['Total Calorie (kcal)', 'Total Protein (g)', 'Total Fat (g)', 
                     'Total Carbohydrate (g)', 'Total Vitamin (IU)', 'Total Mineral (mg)']

    # Summing up the values for each nutrient across days
    total_values = nutritional_info[columns_order].sum()

    # Creating a bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=columns_order, y=total_values, 
                         marker_color=px.colors.qualitative.Set3))
    
    # Customize the layout for better visualization
    fig.update_layout(title='Total Nutritional Values for the Week',
                      xaxis_title='Nutrient',
                      yaxis_title='Total Value',
                      height=600, width=700)
    
    st.plotly_chart(fig)
  
def diet_recommendation_page():
    # Load data from Excel file
    excel_path = r"years.xlsx"
    df = load_data(excel_path)
    st.title("Diet Recommendation System")

    # User input for age, gender, height, weight, and meal type
    col1, col2 = st.columns(2)
    with col1:
        age_option = st.radio("Select Age Range", ["Below 1", "1-5"])
        
        if age_option == "Below 1":
            selected_month = st.selectbox("Select Age (1-12 months)", ["1 month", "2 months", "3 months", "4 months", "5 months", "6 months", "7 months", "8 months", "9 months", "10 months", "11 months", "12 months"])
            selected_gender, selected_height, selected_weight, selected_meal_type = None, None, None, None
        else:
            selected_month = None
            selected_age = st.slider("Select Age (1-5)", min_value=1, max_value=5)
            selected_gender = st.selectbox("Select Gender", ["Male", "Female"])
            selected_height = st.number_input("Enter height (cm):")
            selected_weight = st.number_input("Enter weight (kg):")
            selected_meal_type = st.selectbox("Select Type of Meal", ["Veg", "Non-Veg"])

    # Button to calculate BMI or generate diet plan
    # Inside the 'if generate_diet_plan_button:' block
    
    # Button to calculate BMI or generate diet plan
    if age_option == "Below 1":
        generate_diet_plan_button = st.button("Generate Diet Plan")   
        if generate_diet_plan_button:
            diet_plan = generate_diet_plan(selected_month)
            
            if not diet_plan.empty:
                st.dataframe(diet_plan)
                
                st.title('Nutritional Information')
                # Generate nutritional information for babies below 1 year
                nutritional_info_below_1 = generate_nutritional_info_below_1(diet_plan)

                # Display pie chart for nutritional information
                pie_chart_nutritional_info(nutritional_info_below_1)

                # Display bar chart for nutritional information
                bar_chart_nutritional_info(nutritional_info_below_1)
     # Display the diet plan as a table
    else:
        calculate_button = st.button("Calculate BMI")
        if calculate_button:
            if selected_height == 0:
                st.warning("Height should not be zero for BMI calculation. Please enter a valid height.")
                return

            calculated_bmi = calculate_bmi(selected_height, selected_weight)
            if calculated_bmi is not None:
                bmi_category = predict_bmi_category(calculated_bmi)            
                # Display calculated BMI and predicted BMI category with styling
                st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Calculated BMI: {calculated_bmi:.2f}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Predicted BMI Category: {bmi_category}</p>", unsafe_allow_html=True)
                # Filter data based on user input and BMI category
                selected_data = filter_data(df, selected_age, selected_gender, selected_meal_type, bmi_category)

                # Display one-week diet plan
                display_diet_plan(selected_data)
                st.title('Nutritional Information')

                # Display nutritional information with animated pie charts
                animated_pie_chart(selected_data)

                # Display bar chart for total nutrition in a week with different colors
                bar_chart_total_nutrition(selected_data)
            else:
                st.warning("Height should not be zero for BMI calculation.")

# Function to generate PDF
def generate_underweight_pdf():
    from io import BytesIO

    # Create a BytesIO object to store the PDF
    pdf_bytes = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title to the document
    title = "Underweight Measures"
    story.append(Paragraph(title, styles['Title']))

    # Add measures to the document
    measures = [
        "- Increase calorie intake.",
        "- Focus on foods rich in healthy fats, proteins, and complex carbohydrates.",
        "- Encourage consistent eating times to increase calorie intake.",
        "- If necessary, consider supplements under medical supervision.",
        "- Encourage regular exercise to build muscle and improve appetite.",
        "- Monitor growth and health status closely with healthcare professionals.",
        "- Engage parents or caregivers in meal planning and support strategies."
    ]
    for measure in measures:
        story.append(Paragraph(measure, styles['BodyText']))

    # Build the PDF document
    doc.build(story)

    # Get PDF content from BytesIO object
    pdf_data = pdf_bytes.getvalue()
    pdf_bytes.close()

    return pdf_data
# Function to generate PDF
def generate_normalweight_pdf():
    from io import BytesIO

    # Create a BytesIO object to store the PDF
    pdf_bytes = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title to the document
    title = "Overweight Measures"
    story.append(Paragraph(title, styles['Title']))

    # Add measures to the document
    measures = [
        "- Encourage a variety of nutrient-rich foods to support growth, development, and overall health.",
        "- Promote daily exercise and outdoor play to maintain fitness levels and support healthy growth.",
       "- Ensure children get enough sleep for their age to support physical and mental health.",
        "- Encourage regular water intake throughout the day to stay hydrated and support bodily functions.",
        "- Encourage moderation in screen time and promote activities that stimulate creativity and social interaction.",
       "- Foster a supportive and nurturing environment to promote positive mental health and emotional well-being.",
       "- Schedule routine medical visits to monitor growth, development, and overall health, including vaccinations and screenings as recommended by healthcare professionals."
        
    ]
    for measure in measures:
        story.append(Paragraph(measure, styles['BodyText']))

    # Build the PDF document
    doc.build(story)

    # Get PDF content from BytesIO object
    pdf_data = pdf_bytes.getvalue()
    pdf_bytes.close()

    return pdf_data
# Function to generate PDF
def generate_overweight_pdf():
    from io import BytesIO

    # Create a BytesIO object to store the PDF
    pdf_bytes = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title to the document
    title = "Overweight Measures"
    story.append(Paragraph(title, styles['Title']))

    # Add measures to the document
    measures = [
        "- Encourage a diet rich in fruits, vegetables, whole grains, and lean proteins while minimizing sugary drinks and high-fat, high-calorie foods.",
        "- Teach children about appropriate portion sizes and encourage mindful eating habits.",
        "- Promote daily physical activity to help burn calories and improve overall health.",
        "- Encourage less sedentary behavior by reducing screen time and promoting outdoor activities.",
        "- Involve the entire family in adopting healthy habits and setting a positive example.",
        "- Create a supportive environment at home and school that promotes healthy eating and physical activity.",
        "- Seek advice from healthcare professionals for personalized recommendations and support."
    ]
    for measure in measures:
        story.append(Paragraph(measure, styles['BodyText']))

    # Build the PDF document
    doc.build(story)

    # Get PDF content from BytesIO object
    pdf_data = pdf_bytes.getvalue()
    pdf_bytes.close()

    return pdf_data
# Function to display BMI measures based on category
def display_bmi_measures(bmi_category):
    if bmi_category == 'Underweight':
        st.title("Underweight measures:")
        # Create two columns
        col1, col2 = st.columns(2)        
        # Open the image
        image = Image.open("C:\\Users\\91879\\kiddie\\Diet\\underweight.jpeg")
        # Set desired width and height
        width, height =600, 400
        # Resize the image
        resized_image = image.resize((width, height))
        # Display the resized image using st.image
        col2.image(resized_image, caption="BMI Scale", use_column_width=True)
        col1.write("- Increase calorie intake.")
        col1.write("- Focus on foods rich in healthy fats, proteins, and complex carbohydrates.")
        col1.write("- Encourage consistent eating times to increase calorie intake.")
        col1.write("- If necessary, consider supplements under medical supervision.")
        col1.write("- Encourage regular exercise to build muscle and improve appetite.")
        col1.write("- Monitor growth and health status closely with healthcare professionals.")
        col1.write("- Engage parents or caregivers in meal planning and support strategies.")
        st.download_button(label="Download Underweight Measures", data=generate_underweight_pdf(), file_name='Underweight_Measures.pdf')
        
    elif bmi_category == 'Normal weight':
        st.title("Normal weight measures:")
        col1, col2 = st.columns(2)        
        # Open the image
        image = Image.open("C:\\Users\\91879\\kiddie\\Diet\\Normalweight.jpeg")
        # Set desired width and height
        width, height =600, 400
        # Resize the image
        resized_image = image.resize((width, height))
        # Display the resized image using st.image
        col2.image(resized_image, caption="BMI Scale", use_column_width=True)
        col1.write("- Encourage a variety of nutrient-rich foods to support growth, development, and overall health.")
        col1.write("- Promote daily exercise and outdoor play to maintain fitness levels and support healthy growth.")
        col1.write("- Ensure children get enough sleep for their age to support physical and mental health.")
        col1.write("- Encourage regular water intake throughout the day to stay hydrated and support bodily functions.")
        col1.write("- Encourage moderation in screen time and promote activities that stimulate creativity and social interaction.")
        col1.write("- Foster a supportive and nurturing environment to promote positive mental health and emotional well-being.")
        col1.write("- Schedule routine medical visits to monitor growth, development, and overall health, including vaccinations and screenings as recommended by healthcare professionals.")
        st.download_button(label="Download Normalweight Measures", data=generate_normalweight_pdf(), file_name='Normalweight_Measures.pdf')
        # Add more specific measures as needed for normal weight category
    elif bmi_category == 'Overweight':
        st.title("Overweight measures:")
        col1, col2 = st.columns(2)        
        # Open the image
        image = Image.open("C:\\Users\\91879\\kiddie\\Diet\\Overweight.jpeg")
        # Set desired width and height
        width, height = 600, 400
        # Resize the image
        resized_image = image.resize((width, height))
        # Display the resized image using st.image
        col2.image(resized_image, caption="BMI Scale", use_column_width=True)
        col1.write("- Encourage a diet rich in fruits, vegetables, whole grains, and lean proteins while minimizing sugary drinks and high-fat, high-calorie foods.")
        col1.write("- Teach children about appropriate portion sizes and encourage mindful eating habits.")
        col1.write("- Promote daily physical activity to help burn calories and improve overall health.")
        col1.write("- Encourage less sedentary behavior by reducing screen time and promoting outdoor activities.")
        col1.write("- Involve the entire family in adopting healthy habits and setting a positive example.")
        col1.write("- Create a supportive environment at home and school that promotes healthy eating and physical activity.")
        col1.write("- Seek advice from healthcare professionals for personalized recommendations and support.")
        st.download_button(label="Download Overweight Measures", data=generate_overweight_pdf(), file_name='Overweight_Measures.pdf')
    else:
        st.warning("Invalid BMI category.")
            
# Function to create the BMI Calculator page
def bmi_calculator_page():
    st.title("BMI Calculator with Measures")
    # st.set_option('deprecation.showfileUploaderEncoding', False)

    # User input for age, gender, height, and weight
    selected_age_bmi = st.slider("Select Age (1-5)", min_value=1, max_value=5)
    selected_gender_bmi = st.selectbox("Select Gender", ["Male", "Female"])
    selected_height_bmi = st.number_input("Enter height (cm):")
    selected_weight_bmi = st.number_input("Enter weight (kg):")

    # Button to calculate BMI
    if st.button("Calculate BMI"):
        calculated_bmi_bmi = calculate_bmi(selected_height_bmi, selected_weight_bmi)
        if calculated_bmi_bmi is not None:
            bmi_category_bmi = predict_bmi_category(calculated_bmi_bmi)
            st.write(f"### Calculated BMI: {calculated_bmi_bmi:.2f}")
            st.write(f"### Predicted BMI Category: {bmi_category_bmi}")
            # Display BMI measures based on category
            display_bmi_measures(bmi_category_bmi)

def awareness_page():
    st.title("Awareness to Care of Babies Food Diet")

    st.write("Here are some resources to help you with baby food diet awareness:")

    # Blogs
    st.header("Blogs:")
    st.markdown("- [Children Measures](https://www.lybrate.com/topic/nutrition-tips-for-children-from-age-6-months-to-5-years-854b/0413920673c76cd65ea87c891424cfed)")
    st.markdown("- [Importance Of Health](https://www.mayoclinic.org/healthy-lifestyle/childrens-health/in-depth/nutrition-for-kids/art-20049335)")
    st.markdown("- [Nutition For Children](https://medlineplus.gov/childnutrition.html)")
    st.markdown("- [Diet For Children](https://www.stanfordchildrens.org/en/topic/default?id=school-aged-child-nutrition-90-P02280)")
    # Add more blogs as needed

    # YouTube Videos
    st.header(" Videos:")
    st.markdown("- [Nutrition Importance](https://youtu.be/n9lV1bttzG8?si=Ijcj2GB3xNa4ap8f)")
    st.markdown("- [Significance of food](https://youtu.be/Z51bWG17m-Q?si=pxeKVEcN3MxVvZt1)")
    st.markdown("- [nourishment For Babies](https://youtu.be/dkIgwEB60i4?si=M9q0Uol3tkr7GSur)")
def get_sentiment_emoji(sentiment):
        if sentiment > 0:
            return "😃 (Positive Sentiment)"  # Positive emoji
        elif sentiment < 0:
            return "😔 (Negative Sentiment)"  # Negative emoji
        else:
            return "😐 (Neutral Sentiment)"  # Neutral emoji
def News_page():
    today = date.today()
    Diet_list = [
        "Introduction to toddler nutrition",
        "Healthy meal ideas for toddlers",
        "Nutrient-rich foods for toddlers",
        "Feeding tips for picky eaters",
        "Balanced diet for preschoolers",
        "Introducing new foods to toddlers",
        "Snack ideas for young children",
        "Hydration tips for toddlers",
        "Portion sizes for young children",
        "Importance of fruits and vegetables",
        "Iron-rich foods for toddlers",
        "Calcium sources for growing children",
        "Whole grains for toddlers",
        "Healthy fats for brain development",
        "Protein sources for young children",
        "Vitamin D and its importance",
        "Food allergies in toddlers",
        "Nutrition during growth spurts",
        "Role of probiotics in child health",
        "Tips for healthy eating habits",
        "Encouraging self-feeding",
        "Mealtime routines for toddlers",
        "Healthy snacks on the go",
        "Limiting sugary foods and beverages",
        "Dental health and nutrition",
        "Physical activity for young children",
        "Eating together as a family",
        "Healthy screen time habits",
        "Navigating food advertising targeted at children",
        "Creating a positive food environment"
    ]
    # Get user input
    user_input = st.selectbox('Select a search to analyze', Diet_list)
    st.subheader(f"News articles related to {user_input}")
        # initialize NewsApiClient with your API key
    newsapi = NewsApiClient(api_key='75806d2855fc48a3bf459ce951aaf4af')

        # set the date range
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')

        # get the top headlines for the stock symbol from the past 30 days
    top_headlines = newsapi.get_everything(q=user_input,
                                            language='en',
                                            from_param=from_date,
                                            to=to_date,
                                            sort_by='relevancy',
                                            page_size=100)
    if top_headlines['totalResults'] == 0:
        st.write('No news articles found')
    else:
        total_articles = top_headlines["totalResults"]
        st.write(f'Total {total_articles} articles found')
        articles_per_page = 5
        num_of_pages = math.ceil(total_articles/articles_per_page)
        page_number = st.number_input('Select Page Number', min_value=1, max_value=num_of_pages, value=1, step=1)
        start_index = (page_number - 1) * articles_per_page
        end_index = start_index + articles_per_page
        articles = top_headlines['articles'][start_index:end_index]
        for i, article in enumerate(articles):
            st.write('---')
            st.write(f"**Title:** [{article['title']}]({article['url']})")
            st.write(f"**Description:** {article['description']}")
            st.write(f"**Source:** {article['source']['name']}")

                # perform sentiment analysis on the news article
            analysis = TextBlob(article['description'])
            sentiment = analysis.sentiment.polarity
            sentiment_emoji = get_sentiment_emoji(sentiment)
            st.write(f"**Sentiment:** {sentiment:.2f} {sentiment_emoji}")

        st.write(f"Showing articles {start_index+1} - {end_index} out of {total_articles}")
def home_page():
    st.title("Welcome to Kiddie Cuisine Planner")
    image = Image.open("file.jpg")
    st.image(image, caption='Infant Diet Planner', use_container_width=True)
def main():
    st.set_page_config(page_title="Diet Recommendation System App")
    
    with st.sidebar:
        selected_page_label = option_menu("Diet App", ["🏠 Home", " 🍏 Diet Recommendation", " 💪 BMI Calculator", " 📰 Diet News Articles", " 👶 Baby Food Diet Awareness"], default_index=0)
    # Check the selected label and render the corresponding page
    if selected_page_label == "🏠 Home":
        home_page()
    if selected_page_label == " 🍏 Diet Recommendation":
        diet_recommendation_page()
    elif selected_page_label == " 💪 BMI Calculator":
        bmi_calculator_page()
    elif selected_page_label ==" 📰 Diet News Articles":
        News_page()
    elif selected_page_label == " 👶 Baby Food Diet Awareness":
        awareness_page()
    
        

    
# Call main function
if __name__ == "__main__":
    main()
