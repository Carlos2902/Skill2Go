from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt

import os
import requests
from exchange.models import UserPreference
from django.contrib.auth.models import User
from django.http import JsonResponse

# loading kokoro tts model
from kokoro import KPipeline
import soundfile as sf
import tempfile
import base64
from IPython.display import display, Audio
import re
import numpy as np


# kokoro pipeline (language dynamycally set it up)
def initializing_pipeline(user):
    user_preference = UserPreference.objects.get(user=user)
    language_preference_key = user_preference.preferred_language
    preferred_language = map_language_code(language_preference_key)
    try:
        pipeline = KPipeline(lang_code=preferred_language)  
    except Exception as e:
        print(f'An error has occurred in the kokoro pipeline: {e}')
        raise
    return pipeline
def map_language_code(language_code): 
    language_map = {
        "es": "e",
        "fr": "f",
        "en": "a",
    }
    return language_map.get(language_code, "a")  

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
def construct_prompt(user, greeting=False, user_input=None):
    try:
        user_preference = UserPreference.objects.get(user=user)
        language_map = {
            "es": "Spanish",
            "fr": "French",
            "en": "English"
        }
        preferred_language_key = user_preference.preferred_language
        preferred_language = language_map.get(preferred_language_key, "English")
        skill_level = user_preference.skill_level
        learning_goals = user_preference.learning_goals
        if greeting:
            prompt = (
                "You are an AI language teacher which name is Emma."
                f"The user speaks {preferred_language}. Don't speak any other language."
                f"They are a {skill_level} learner and their goal is to {learning_goals}. "
                f"Start the conversation by greeting the user in {preferred_language} and asking for their name."
                
            )
        else:
            prompt = (
                f"Focus only on the user's input: '{user_input}'. "
                f"Respond with one clear, direct reply that is focused on continuing the conversation in {preferred_language}. "
                f"Ask a relevant follow-up question to keep the conversation going, and ensure the tone remains friendly. "
            )

        return prompt, preferred_language
    except UserPreference.DoesNotExist:
        return "User preferences are missing.", "English"  


@method_decorator(csrf_exempt, name="dispatch")
class AIChatView(APIView):
    '''Handles the user input and returns the response from the AI model'''
    def post(self, request):
        user_input = request.data.get('message', '')
        user = request.user
        if user_input == "__GREETING__":
            prompt, preferred_language = construct_prompt(user, greeting=True)
            response = self.get_huggingface_response(prompt)
        else:
            prompt, preferred_language = construct_prompt(user, greeting=False, user_input=user_input)
            response = self.get_huggingface_response(prompt)
        if response:
            cleaned_response = self.clean_response(response, prompt)
            return Response({
                'response': cleaned_response,
                'preferred_language': preferred_language  
            }, status=status.HTTP_200_OK)
            
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
            print("API Response Data:", response_data)
            return response_data[0]['generated_text']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# cleaning the AI response in case extra instructions are being added
    def clean_response(self, response, prompt):
        if hasattr(response, 'data'):  
            response = str(response.data)  
        
        if not isinstance(response, str):
            raise ValueError("Expected a string response, but got type: {}".format(type(response)))

        cleaned_response = re.sub(r"\(.*\)", "", response)  
        cleaned_response = cleaned_response.strip()
        
        if cleaned_response.startswith(prompt):
            cleaned_response = cleaned_response[len(prompt):].strip()
        cleaned_response = re.sub(r"^Act as a language tutor.*", "", cleaned_response)

        return cleaned_response
    
@method_decorator(csrf_exempt, name='dispatch')
class TextToSpeechView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        user = request.user
        try:
            preference = UserPreference.objects.get(user=user)
            language = preference.preferred_language
        except UserPreference.DoesNotExist:
            return Response({'error': 'User preference not found'}, status=status.HTTP_400_BAD_REQUEST)
        print("Extracted text:", text)
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pipeline = initializing_pipeline(user)
            generator = pipeline(text, voice="af_heart", speed=1, split_pattern=None)
            segment_list = list(generator)
            print(f"Total segments: {len(segment_list)}")
            if not segment_list:
                return JsonResponse({"error": "No audio segments produced"}, status=400)
            audio_data = []
            for gs, ps, audio in segment_list:
                print("Graphemes:", gs)
                print("Phonemes:", ps)
                audio_data.append(audio)
            full_audio = np.concatenate(audio_data)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                audio_filename = temp_audio_file.name
                sf.write(audio_filename, full_audio, 24000)
            with open(audio_filename, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            os.remove(audio_filename)
            return Response({'audio': audio_base64}, status=status.HTTP_200_OK)
        except TypeError as e:
            print(f"TypeError: {e}")
            return JsonResponse({"error": "Invalid phonemes input format"}, status=400)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
    def prepare_kokoro_input(text):
        try:
            words = text.split()
            phoneme_lists = [list(word) for word in words]
            from itertools import chain
            flat_phonemes = list(chain.from_iterable(phoneme_lists))
            kokoro_input = "".join(flat_phonemes)
            print("Final Kokoro input:", kokoro_input)
            return kokoro_input
        except Exception as e:
            print(f"Error preparing Kokoro input: {e}")
            return None
