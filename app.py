### 🤖 AI-Powered Health & Fitness Planner
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------------- Gemini Helpers ----------------
def get_gemini_response(messages):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(messages)
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# ---------------- Health Helpers ----------------
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def convert_height_to_cm(feet, inches):
    return (feet * 30.48) + (inches * 2.54)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

def predict_days_to_target(weight, target_weight, daily_calorie_deficit=500):
    if weight > target_weight:
        total_kcal = (weight - target_weight) * 7700
        days = total_kcal / daily_calorie_deficit
    elif weight < target_weight:
        total_kcal = (target_weight - weight) * 7700
        days = total_kcal / daily_calorie_deficit
    else:
        days = 0
    return int(days)

# ---------------- Meal Plan ----------------
def suggest_meal_plan(goal, diet_type, gender):
    calorie_adjust = 100 if gender == "Male" else -50
    protein_adjust = 5 if gender == "Male" else -2

    if goal == "Weight Gain":
        if diet_type == "Vegetarian":
            return {
                "Morning": {"food": "Banana shake + Oats with milk & nuts", "calories": 450 + calorie_adjust, "protein": 15 + protein_adjust, "fiber": 8, "benefit": "Boosts energy, rich in potassium, protein & fiber."},
                "Lunch": {"food": "Paneer curry with roti + salad", "calories": 600 + calorie_adjust, "protein": 25 + protein_adjust, "fiber": 10, "benefit": "High protein meal for muscle gain with balanced carbs."},
                "Evening": {"food": "Dry fruits + Protein smoothie", "calories": 300 + calorie_adjust, "protein": 10 + protein_adjust, "fiber": 5, "benefit": "Healthy fats & protein for recovery."},
                "Dinner": {"food": "Dal, rice & mixed vegetable curry", "calories": 500 + calorie_adjust, "protein": 20 + protein_adjust, "fiber": 12, "benefit": "Balanced dinner with protein & vitamins."}
            }
        else:
            return {
                "Morning": {"food": "Egg omelette + Toast + Milk", "calories": 400 + calorie_adjust, "protein": 22 + protein_adjust, "fiber": 4, "benefit": "Rich in protein, supports muscle growth."},
                "Lunch": {"food": "Chicken curry with rice + salad", "calories": 650 + calorie_adjust, "protein": 35 + protein_adjust, "fiber": 8, "benefit": "High protein with carbs for strength."},
                "Evening": {"food": "Boiled eggs + Banana shake", "calories": 300 + calorie_adjust, "protein": 18 + protein_adjust, "fiber": 4, "benefit": "Quick recovery snack."},
                "Dinner": {"food": "Grilled chicken + Roti + Vegetables", "calories": 550 + calorie_adjust, "protein": 40 + protein_adjust, "fiber": 10, "benefit": "Protein-rich dinner for overnight repair."}
            }
    elif goal == "Maintain Weight":
        if diet_type == "Vegetarian":
            return {
                "Morning": {"food": "Green tea + Poha/Upma", "calories": 300 + calorie_adjust, "protein": 8 + protein_adjust, "fiber": 5, "benefit": "Light breakfast, keeps metabolism active."},
                "Lunch": {"food": "Quinoa salad with beans", "calories": 400 + calorie_adjust, "protein": 18 + protein_adjust, "fiber": 12, "benefit": "Balanced carbs, protein, and fiber."},
                "Evening": {"food": "Fruits + Yogurt", "calories": 200 + calorie_adjust, "protein": 10 + protein_adjust, "fiber": 4, "benefit": "Probiotics & antioxidants."},
                "Dinner": {"food": "Vegetable stir fry + Roti", "calories": 350 + calorie_adjust, "protein": 12 + protein_adjust, "fiber": 10, "benefit": "Low fat dinner, easy to digest."}
            }
        else:
            return {
                "Morning": {"food": "Boiled eggs + Green tea", "calories": 250 + calorie_adjust, "protein": 12 + protein_adjust, "fiber": 0, "benefit": "High protein breakfast to keep energy stable."},
                "Lunch": {"food": "Grilled fish with brown rice", "calories": 450 + calorie_adjust, "protein": 28 + protein_adjust, "fiber": 6, "benefit": "Omega-3 fatty acids for heart health with clean carbs."},
                "Evening": {"food": "Chicken soup + Salad", "calories": 220 + calorie_adjust, "protein": 18 + protein_adjust, "fiber": 5, "benefit": "Light evening snack rich in protein."},
                "Dinner": {"food": "Egg curry + Roti + Vegetables", "calories": 400 + calorie_adjust, "protein": 22 + protein_adjust, "fiber": 8, "benefit": "Balanced meal with protein, carbs, and fiber."}
            }
    else:
        if diet_type == "Vegetarian":
            return {
                "Morning": {"food": "Warm water + Sprouts salad", "calories": 180 + calorie_adjust, "protein": 10 + protein_adjust, "fiber": 8, "benefit": "Low calorie, protein & fiber-rich."},
                "Lunch": {"food": "Vegetable soup + Brown rice", "calories": 300 + calorie_adjust, "protein": 12 + protein_adjust, "fiber": 10, "benefit": "Keeps you full, aids digestion."},
                "Evening": {"food": "Apple + Green tea", "calories": 150 + calorie_adjust, "protein": 1 + protein_adjust, "fiber": 5, "benefit": "Low calorie snack with antioxidants."},
                "Dinner": {"food": "Dal + Steamed vegetables", "calories": 250 + calorie_adjust, "protein": 14 + protein_adjust, "fiber": 9, "benefit": "Light dinner with protein & fiber."}
            }
        else:
            return {
                "Morning": {"food": "Egg whites + Green tea", "calories": 150 + calorie_adjust, "protein": 12 + protein_adjust, "fiber": 0, "benefit": "Lean protein breakfast, helps fat loss."},
                "Lunch": {"food": "Grilled chicken breast + Salad", "calories": 300 + calorie_adjust, "protein": 32 + protein_adjust, "fiber": 6, "benefit": "Low calorie, high protein to preserve muscle."},
                "Evening": {"food": "Tuna salad or Boiled eggs", "calories": 200 + calorie_adjust, "protein": 25 + protein_adjust, "fiber": 2, "benefit": "Protein-rich snack to control hunger."},
                "Dinner": {"food": "Grilled fish + Steamed vegetables", "calories": 280 + calorie_adjust, "protein": 30 + protein_adjust, "fiber": 8, "benefit": "High protein, omega-3 fats, light dinner."}
            }

# ---------------- Exercises ----------------
def suggest_exercises(goal, gender):
    if goal == "Weight Gain":
        return ["🏋️ Heavy strength training (4–5 times/week)", "🍑 Squats, Deadlifts, Bench Press", "🏃‍♂️ Light cardio (15 min)", f"⚡ For {gender}: Focus on progressive overload & compound lifts"]
    elif goal == "Maintain Weight":
        return ["🏃 Jogging/Walking (30 min)", "🧘 Yoga or Stretching", "💪 Moderate strength training (2–3 times/week)", f"⚡ For {gender}: Include flexibility & balance exercises"]
    else:
        return ["🏃 Cardio (Running, Cycling, HIIT – 30–40 min)", "🏋️ Strength training (3–4 times/week)", "🧘 Yoga/Stretching for recovery", f"⚡ For {gender}: Emphasize calorie burn & core workouts"]

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="AI Health & Fitness Planner", page_icon="💪", layout="wide")

# CSS
st.markdown("""
<style>
.main { background-color: #f5f7fa; }
.diet-box, .exercise-box { border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1); }
.diet-box { background: #ffffff; }
.exercise-box { background: #e3f2fd; }
.user-bubble { background-color: #d1f2eb; border-radius: 10px; padding: 10px; margin: 5px 0; }
.assistant-bubble { background-color: #f0f3f4; border-radius: 10px; padding: 10px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# Creative Front Page
st.markdown("""
<div style="text-align:center; padding:30px; background:linear-gradient(90deg, #2e86c1, #48c9b0); border-radius:15px;">
    <h1 style="color:white; font-size:50px;">🤖 AI-Powered Health & Fitness Planner</h1>
    <p style="color:white; font-size:20px;">Your Personal <b>Nutritionist, Fitness Coach & Health Assistant</b></p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, _, _ = st.tabs(["📊 BMI & Plans", "🍽️ Food Analysis", "🏋️ Exercise Analysis"])

with tab1:
    age = st.number_input("Enter your Age", min_value=5, max_value=100, step=1)
    gender = st.radio("Select Gender", ["Male", "Female"])
    feet = st.number_input("Enter your Height (feet)", min_value=1, max_value=8, step=1)
    inches = st.number_input("Enter your Height (inches)", min_value=0, max_value=11, step=1)
    weight = st.number_input("Enter your Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)
    target_weight = st.number_input("Enter your Target Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)
    diet_type = st.radio("Choose your Diet Preference", ["Vegetarian", "Non-Vegetarian"])

    if st.button("📌 Show My Plan"):
        height_cm = convert_height_to_cm(feet, inches)
        bmi = calculate_bmi(weight, height_cm)
        category = bmi_category(bmi)
        goal = "Weight Gain" if bmi < 18.5 else "Maintain Weight" if bmi <= 24.9 else "Weight Loss"

        st.success(f"Your BMI is: {bmi:.2f} → **{category}** ({gender})")
        st.subheader(f"🎯 Goal: {goal} (Target: {target_weight} kg)")

        # Diet cards with images
        meals = suggest_meal_plan(goal, diet_type, gender)
        meal_images = {"Banana shake": "https://www.vegrecipesofindia.com/wp-content/uploads/2021/04/banana-shake-recipe-1-500x500.jpg","Paneer curry": "https://www.vegrecipesofindia.com/wp-content/uploads/2021/01/paneer-curry-1-500x500.jpg","Chicken curry": "https://www.indianhealthyrecipes.com/wp-content/uploads/2021/07/chicken-curry-recipe.jpg","Grilled fish": "https://www.eatwell101.com/wp-content/uploads/2019/06/Grilled-Fish-Recipe.jpg"}
        for time, details in meals.items():
            image_url = next((meal_images[key] for key in meal_images if key.lower() in details['food'].lower()), "https://img.icons8.com/color/48/meal.png")
            st.markdown(f"""
            <div class="diet-box">
                <h4>⏰ {time}</h4>
                <img src="{image_url}" width="120" style="border-radius:10px;"><br>
                <b>{details['food']}</b><br>
                🔥 {details['calories']} kcal | 💪 {details['protein']} g Protein | 🌱 {details['fiber']} g Fiber
                <br><i>{details['benefit']}</i>
            </div>
            """, unsafe_allow_html=True)

        # Exercise cards with images
        exercises = suggest_exercises(goal, gender)
        exercise_images = {"Squats": "https://images.pexels.com/photos/8411307/pexels-photo-8411307.jpeg","Deadlifts": "https://images.pexels.com/photos/1552249/pexels-photo-1552249.jpeg","Bench Press": "https://images.pexels.com/photos/3838389/pexels-photo-3838389.jpeg","Running": "https://images.pexels.com/photos/1199590/pexels-photo-1199590.jpeg","Yoga": "https://images.pexels.com/photos/3823039/pexels-photo-3823039.jpeg"}
        for ex in exercises:
            image_url = next((exercise_images[key] for key in exercise_images if key.lower() in ex.lower()), "https://img.icons8.com/color/48/dumbbell.png")
            st.markdown(f"""
            <div class="exercise-box">
                <img src="{image_url}" width="120" style="border-radius:10px;"><br>
                {ex}
            </div>
            """, unsafe_allow_html=True)

        
        # Progress graph
days = predict_days_to_target(weight, target_weight)
if days > 0:
    st.subheader("📈 Predicted Progress")
    st.write(f"Estimated time to reach target: **{days} days**")

    weights = [weight - (i / days) * (weight - target_weight) for i in range(days+1)]

    plt.figure(figsize=(7,4))
    plt.plot(range(days+1), weights, marker="o", linestyle="-")

    # Labels and title
    plt.xlabel("Days")
    plt.ylabel("Weight (kg)")
    plt.title(f"Predicted Weight Progress (Target in {days} days)")

    # Annotate start and end
    plt.annotate(f"Start: {weight}kg", xy=(0, weight), xytext=(0, weight+2),
                 arrowprops=dict(arrowstyle="->", color="green"))
    plt.annotate(f"Target: {target_weight}kg", xy=(days, target_weight), xytext=(days, target_weight+2),
                 arrowprops=dict(arrowstyle="->", color="red"))

    st.pyplot(plt)
else:
    st.info("You are already at your target weight ✅")

# Chat Assistant
st.markdown("<h2 style='color:#1abc9c;'>💬 Smart Health Chat Assistant</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.chat_input("Type your question or upload an image...")
uploaded_chat_img = st.file_uploader("📸 Upload an image (optional)", type=["jpg","jpeg","png"], key="chat")

if user_input or uploaded_chat_img:
    content = user_input if user_input else "📸 Analyzing uploaded image..."
    st.session_state.messages.append({"role": "user", "content": content})
    if uploaded_chat_img:
        image_data = input_image_setup(uploaded_chat_img)
        input_prompt = "You are a health assistant. If food → give calories, protein, fiber, benefits. If exercise → identify and explain muscles, posture, benefits."
        gemini_input = [user_input if user_input else "", image_data[0], input_prompt]
    else:
        gemini_input = [user_input]
    response = get_gemini_response(gemini_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"<div class='assistant-bubble'>{response}</div>", unsafe_allow_html=True)
