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
        language_map = {
            "es":"Spanish",
            "fr": "French",
            "en":"English"
        }
        preferred_language_key = user_preference.preferred_language
        preferred_language = language_map.get(preferred_language_key,"English")
        
        skill_level = user_preference.skill_level
        learning_goals = user_preference.learning_goals
        prompt = (
            f"The user speaks {preferred_language}. "
            f"They are a {skill_level} learner. "
            f"Their goal is to {learning_goals}. "
            "Respond in a way that helps them improve their skills. "
            "Use simple language, be supportive, and provide clear explanations."
            "Start the conversation by greeting the user and asking a relevant question. Act as a language tutor"
            "Don't include notes or any other irrelevant responses, keep a conversation tone."
        )
        return prompt, preferred_language
    except UserPreference.DoesNotExist:
        return "User preferences are missing.", "English" #english if no language preference
    
#view for interacting with Mixtral model from hugging face
@method_decorator(csrf_exempt, name="dispatch") 
class AIChatView(APIView):
    '''handles the user input and returns the response from the AI model'''
    def post(self, request):
        user_input = request.data.get('message', '')
        user = request.user
        language = request.data.get('language', 'en')
        # request to hugging face api
        if user_input == "__GREETING__":
            prompt, user_language = construct_prompt(user)  
        else:
            prompt, user_language = construct_prompt(user)
            # full_prompt = (
            # f"Act as a language tutor. Respond concisely and in the language the user speaks only. "
            # f"User input: '{user_input}'")

        response = self.get_huggingface_response(prompt)

        if response:
            if response.startswith(prompt):
                response = response[len(prompt):].strip() 
            # elif response.startswith(full_prompt):
            #     response = response[len(full_prompt):].strip()  
            
            # Return the cleaned response
            return Response({'response': response}, status=status.HTTP_200_OK)

    def get_huggingface_response(self, prompt):
        url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        payload = {
            "inputs": prompt
        }
        

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  
            response_data = response.json()
            return response_data[0]['generated_text']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
        
        
# handling TTS (text-to-speech), using facebook tts transformer
@method_decorator(csrf_exempt, name='dispatch')
class TextToSpeechView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        print("Extracted text:", text)
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
    # constructing api endpoint
        url = "https://api-inference.huggingface.co/models/facebook/tts_transformer-ar-cv7" 
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        payload = {
            "inputs": text
        }
        
        try:
            response = requests.post(url, headers = headers, json=payload)
            response.raise_for_status()
            
            audio = response.content
            return Response ({'audio': audio}, status = status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return Response({'error': 'Failed to get speech from Hugging Face API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
