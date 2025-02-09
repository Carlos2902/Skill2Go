from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import openai
import os
import requests
from exchange.models import UserPreference
from django.contrib.auth.models import User


load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
# function for the prompt based on user's preferences
def construct_prompt(user):
    try:
        user_preference = UserPreference.objects.get(user=user)
        preferred_language = user_preference.preferred_language
        skill_level = user_preference.skill_level
        learning_goals = user_preference.learning_goals
        prompt = (
            f"The user speaks {preferred_language}. "
            f"They are a {skill_level} learner. "
            f"Their goal is to {learning_goals}. "
            "Respond in a way that helps them improve their skills. "
            "Use simple language, be supportive, and provide clear explanations."
        )
        return prompt, preferred_language
    except UserPreference.DoesNotExist:
        return "User preferences are missing.", "en" #english if no language preference
    
#Api endpoint for gathering the user choices
@method_decorator(csrf_exempt, name="dispatch") # Remove this in production.
class AIChatView(APIView):
    '''handles the user input and returns the response from the AI model'''
    def post(self, request):
        user_input = request.data.get('message', '')
        user = request.user
        language = request.data.get('language', 'en')
        # request to hugging face api
        if not user_input:
            prompt, user_language = construct_prompt(user)  # Get personalized context
            full_prompt = f"{prompt} Start the conversation by greeting the user and asking a relevant question."
        else:
            prompt, user_language = construct_prompt(user)
            full_prompt = f"{prompt} The user says: '{user_input}'. Respond in a helpful and supportive way."


        response = self.get_huggingface_response(full_prompt)

        if response:
            return Response({'response': response}, status=status.HTTP_200_OK) 
        else:
            return Response({'error': 'failed to get a response from hugging face api'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_huggingface_response(self, prompt):
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        payload = {
            "inputs": prompt
        }
        

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the response code is 4xx/5xx
            response_data = response.json()
            return response_data[0]['generated_text']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None