import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pregnancy_advice(symptoms, conversation_history=None):
    try:
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("Google AI API key not found in environment variables")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')  # Updated to use Gemini 2.0
        
        # Enhanced context handling for follow-up questions
        context = ""
        last_topic = ""
        is_followup = False
        
        if conversation_history:
            # Find the most recent non-follow-up question for context
            previous_exchanges = []
            for msg in conversation_history[-4:]:  # Look at last 2 exchanges
                if msg['role'] == 'user':
                    # Check if current question is a follow-up
                    if any(word in symptoms.lower() for word in ['it', 'this', 'that', 'these', 'those', 'the']):
                        is_followup = True
                    previous_exchanges.append(msg['content'])
            
            if is_followup and previous_exchanges:
                # If it's a follow-up, use the last topic as main context
                last_topic = previous_exchanges[-1]
                context = f"\nDiscussing: {last_topic}\nFollow-up question: {symptoms}"
                symptoms = f"Regarding {last_topic}: {symptoms}"
            else:
                # If not a follow-up, use previous exchanges as context
                context = "\nPrevious Concerns:\n" + "\n".join(
                    f"- {exchange}" for exchange in previous_exchanges[-2:]
                )

        # Updated prompt for better responses
        prompt = f"""As an AI pregnancy health advisor, please address the following concern:

<div class="user-concern">
    <b>{symptoms}</b>
</div>

{context}

<div class="response-format">
    <h2>📋 Initial Assessment</h2>
    <div class="section">
        <p><b>Understanding Your Concern:</b></p>
        <ul>
            <li>Detailed interpretation</li>
            <li>Pregnancy stage relevance</li>
            <li>How common this is</li>
        </ul>
    </div>

    <h2>🔍 Medical Context</h2>
    <div class="section">
        <p><b>Common Causes During Pregnancy:</b></p>
        <ul>
            <li>Primary factors</li>
            <li>Related body changes</li>
            <li>Risk assessment</li>
        </ul>
    </div>

    <h2>💡 Management Guide</h2>
    <div class="section">
        <p><b>Immediate Steps:</b></p>
        <ul>
            <li>Quick relief measures</li>
            <li>Self-care practices</li>
            <li>Lifestyle modifications</li>
        </ul>
    </div>

    <h2>⚕️ Medical Care Guidelines</h2>
    <div class="section">
        <p><b>When to Seek Help:</b></p>
        <ul>
            <li>Emergency warning signs</li>
            <li>Symptoms to monitor</li>
            <li>Healthcare provider consultation timing</li>
        </ul>
    </div>

    <h2>🌟 Support & Prevention</h2>
    <div class="section">
        <p><b>Going Forward:</b></p>
        <ul>
            <li>Preventive measures</li>
            <li>Coping strategies</li>
            <li>Future considerations</li>
        </ul>
    </div>
</div>

<div class="note">
    <i>Note: This information is for guidance only. Always consult your healthcare provider for medical advice.</i>
</div>"""

        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'block_medium_and_above',
            'HARM_CATEGORY_HATE_SPEECH': 'block_medium_and_above',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_medium_and_above',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_medium_and_above',
        }
        
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'candidate_count': 1,
            'max_output_tokens': 2048,
        }
        
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config=generation_config
        )
        
        if not response.text:
            raise ValueError("Empty response received from the model")

        # Format the response
        formatted_response = f"""
<div class="medical-response">
    <div class="current-analysis">
        {response.text.replace('\n', '<br>')}
    </div>
    <hr>
    <p class="disclaimer">⚕️ Please consult with your healthcare provider for medical advice.</p>
</div>"""

        return formatted_response
        
    except Exception as e:
        logger.error(f"Error in get_pregnancy_advice: {str(e)}")
        return f"""<div class="error-message">
⚠️ Our symptom checker is temporarily unavailable. Please contact your healthcare provider for any medical concerns.
</div>"""
