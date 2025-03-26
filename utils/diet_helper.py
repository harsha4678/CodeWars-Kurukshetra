import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_gemini():
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY not found in environment variables")
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        raise Exception(f"Failed to initialize Gemini AI: {str(e)}")

def get_diet_recommendations(region, trimester, lmp_date, diet_preference, health_conditions):
    try:
        model = setup_gemini()
        
        # Calculate weeks of pregnancy from LMP
        lmp = datetime.strptime(lmp_date, '%Y-%m-%d')
        weeks_pregnant = (datetime.now() - lmp).days // 7

        prompt = f"""
        You are an expert nutritionist specializing in pregnancy diet plans in India.
        Create a personalized diet plan based on:
        - Region: {region} (Focus on local ingredients and traditional recipes)
        - Trimester: {trimester} (Week {weeks_pregnant})
        - Last Menstrual Period: {lmp_date}
        - Diet Preference: {diet_preference}
        - Health Conditions: {health_conditions}

        <style>
        .section-title {{
            font-size: 24px;
            color: #4361ee;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #4361ee;
        }}
        .meal-time {{
            font-size: 20px;
            font-weight: 700;
            color: #2d3748;
            background: linear-gradient(to right, #4361ee20, transparent);
            padding: 12px 20px;
            margin: 15px 0 10px 0;
            border-left: 4px solid #4361ee;
            border-radius: 0 8px 8px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .diet-item {{
            margin: 12px 0 12px 25px;
            padding-left: 20px;
            position: relative;
            line-height: 1.6;
            color: #4a5568;
        }}
        .diet-item:before {{
            content: "•";
            color: #4cc9f0;
            font-size: 20px;
            position: absolute;
            left: 0;
        }}
        .meal-options {{
            margin: 10px 0 20px 45px;
        }}
        .option-label {{
            font-weight: 600;
            color: #4361ee;
            margin-right: 10px;
        }}
        .regional-note {{
            font-style: italic;
            color: #666;
            margin-top: 5px;
        }}
        </style>

        <div class="section-title">📅 DAILY MEAL PLAN</div>
        
        <div class="meal-time">🌅 Morning (6-7 AM)</div>
        <div class="diet-item">Choose one of these options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Regional morning drink/food]</p>
            <p><span class="option-label">Option 2:</span> [Alternative morning option]</p>
            <p><span class="option-label">Option 3:</span> [Light morning option]</p>
            <p class="regional-note">*Include traditional {region} morning beverages/foods</p>
        </div>

        <div class="meal-time">🍳 Breakfast (8-9 AM)</div>
        <div class="diet-item">Choose one of these wholesome options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Heavy regional breakfast]</p>
            <p><span class="option-label">Option 2:</span> [Medium regional breakfast]</p>
            <p><span class="option-label">Option 3:</span> [Light regional breakfast]</p>
            <p class="regional-note">*Based on {region}'s traditional breakfast dishes</p>
        </div>

        <div class="meal-time">🫐 Mid-Morning (11 AM)</div>
        <div class="diet-item">Choose one of these nutrient-rich options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Seasonal fruit/nuts combination]</p>
            <p><span class="option-label">Option 2:</span> [Regional snack option]</p>
            <p><span class="option-label">Option 3:</span> [Light protein snack]</p>
            <p class="regional-note">*Include locally available fruits and nuts</p>
        </div>

        <div class="meal-time">🍚 Lunch (1-2 PM)</div>
        <div class="diet-item">Choose one of these balanced meal options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Complete regional thali]</p>
            <p><span class="option-label">Option 2:</span> [Alternative regional meal]</p>
            <p><span class="option-label">Option 3:</span> [Light regional lunch]</p>
            <p class="regional-note">*Based on {region}'s traditional lunch preparations</p>
        </div>

        <div class="meal-time">🫖 Evening Snack (4-5 PM)</div>
        <div class="diet-item">Choose one of these energizing options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Traditional evening snack]</p>
            <p><span class="option-label">Option 2:</span> [Healthy regional option]</p>
            <p><span class="option-label">Option 3:</span> [Light evening snack]</p>
            <p class="regional-note">*Include {region}'s healthy evening snacks</p>
        </div>

        <div class="meal-time">🍽️ Dinner (7-8 PM)</div>
        <div class="diet-item">Choose one of these digestible options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Complete regional dinner]</p>
            <p><span class="option-label">Option 2:</span> [Alternative regional dinner]</p>
            <p><span class="option-label">Option 3:</span> [Light regional dinner]</p>
            <p class="regional-note">*Based on {region}'s traditional dinner items</p>
        </div>

        <div class="meal-time">🥛 Before Bed (9-10 PM)</div>
        <div class="diet-item">Choose one of these calming options:</div>
        <div class="meal-options">
            <p><span class="option-label">Option 1:</span> [Warm milk-based drink]</p>
            <p><span class="option-label">Option 2:</span> [Light herbal drink]</p>
            <p><span class="option-label">Option 3:</span> [Soothing bedtime option]</p>
            <p class="regional-note">*Include traditional bedtime drinks from {region}</p>
        </div>

        <div class="section-title">🍲 REGIONAL SPECIALTIES</div>
        <div class="diet-item">[Dish 1] - [benefits]</div>
        <div class="diet-item">[Dish 2] - [benefits]</div>
        <div class="diet-item">[Dish 3] - [benefits]</div>

        <div class="section-title">🥗 ESSENTIAL NUTRIENTS</div>
        <div class="diet-item">[Nutrient 1]: [food sources]</div>
        <div class="diet-item">[Nutrient 2]: [food sources]</div>
        <div class="diet-item">[Nutrient 3]: [food sources]</div>

        <div class="section-title">⚕️ HEALTH CONSIDERATIONS</div>
        <div class="diet-item">Dietary adjustments for: {health_conditions if health_conditions else 'No specific health conditions mentioned'}</div>

        <div class="section-title">💊 RECOMMENDED SUPPLEMENTS</div>
        <div class="diet-item">[Supplement 1]</div>
        <div class="diet-item">[Supplement 2]</div>
        <div class="diet-item">[Supplement 3]</div>

        <div class="section-title">⚠️ FOODS TO AVOID</div>
        <div class="diet-item">[Item 1]</div>
        <div class="diet-item">[Item 2]</div>
        <div class="diet-item">[Item 3]</div>

        <div class="section-title">💧 HYDRATION & TIMING</div>
        <div class="diet-item">Water intake: [recommendations]</div>
        <div class="diet-item">Meal spacing: [timing guidelines]</div>
        """

        response = model.generate_content(prompt)
        if not response or not response.text:
            raise Exception("No response received from Gemini AI")
            
        # Format the response with proper HTML line breaks
        formatted_response = response.text.replace('\n', '<br>')
        return formatted_response
    
    except ValueError as ve:
        return f"<p style='color: red;'>Configuration Error: {str(ve)}</p>"
    except Exception as e:
        return f"<p style='color: red;'>Error: {str(e)}</p><br><p>Please ensure you have:</p><ul><li>Set up your Google API key</li><li>Added it to your .env file as GOOGLE_API_KEY=your_key_here</li><li>Have sufficient API credits</li></ul>"
