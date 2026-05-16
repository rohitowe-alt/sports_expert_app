import streamlit as st
from openai import OpenAI
import json
from os import getenv


# --- Page Config ---
st.set_page_config(page_title="World Class Sports Advisor", layout="centered")

st.title("🧠 Why so serious")
st.markdown("Generate a world class sports advice report using Sports, Type_of_player, and Task.")

# --- User Inputs ---
openai_key = st.secrets.get("OPENAI_API_KEY")

sport = st.text_area("Sport", placeholder="e.g., Cricket...")
type_of_player = st.text_area("Type_of_Player", placeholder="I am a casual player")
task = st.text_area("Task", placeholder="What should the AI do?")

# --- Generate Button ---
if st.button("Generate Expert Advice"):

    if not openai_key:
        st.error("Please enter your OpenAI API key.")
    elif not sport or not type_of_player or not task:
        st.error("Please fill all fields.")
    else:
        try:
            client = OpenAI(api_key = openai_key)

            system_prompt = f"""
                            You are an world class sports coach of {sport}.
                            
                            Your job is to provide relevant sport advice as per the task given by the user keeping in mind the best available research online. You are extremely analytical and evidence based and provide extremely detailed outputs.
                            
                            STRICT RULES:
                            - DO NOT provide generic advice.
                            - Break the advice in relevant categories.
                            - Whereever needed give an idea of the total cost in INR.
                            - Make the advice clear, structured, and optimized for high-quality outputs.
                            - BEFORE MAKING ANY SUGGESTION ALWAYS check best available advices online and any publically available resource
                            -Take as much time as you need
                            """

            user_input = f"""
Role:
{sport}

Context:
{type_of_player}

Task:
{task}
"""

            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )

            enhanced_prompt = response.output_text

            # --- Outputs ---
            st.subheader("📄 Plain Text Output")
            st.code(enhanced_prompt, language="text")


        except Exception as e:
            st.error(f"Error: {str(e)}")
