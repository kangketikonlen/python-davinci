import os
import openai
import asyncio
import textwrap3
import simpleaudio as sa

from voicevox import Client
from translate import Translator

# Setup OpenAI API Client
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_response(request):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt=request,
		temperature=0.9,
		max_tokens=100,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0,
		stop=["Ask: "]
	)
	return response.choices[0].text.strip().replace('\n', '')

def translate_to_japanese(text):
	translator = Translator(to_lang="ja")
	wrap_text = textwrap3.wrap(text, width=100)
	translation = ""

	for wrap in wrap_text:
		translation += translator.translate(wrap)

	return translation

async def generate_voice(text, client):
	counter = 1
	SpeakerID=13
	substrings = textwrap3.wrap(text, width=20)
	for substring in substrings:
		audio_query = await client.create_audio_query(
			substring, speaker=SpeakerID
		)
		filename=f"voice/voice-{counter}.wav"
		with open(filename, "wb") as f:
			f.write(await audio_query.synthesis())
		counter += 1

def play_wav_voice(text):
	counter = 1
	substrings = textwrap3.wrap(text, width=20)
	for substring in substrings:
		filename=f"voice/voice-{counter}.wav"
		wave_obj = sa.WaveObject.from_wave_file(filename)
		play_obj = wave_obj.play()
		play_obj.wait_done()
		counter += 1
		os.remove(filename)

async def main():
	# Create a loop
	while True:
		try:
			# Prompt user to type question.
			user_input = input("Ask: ")
			# Send the user's input to the OpenAI.
			async with Client() as client:
				user_input = user_input.replace("Ask: ", "")
				# Generate response
				response = generate_response(user_input)
				print(f"\nThe AI Response, \n{response}\n")
				# Translate the response to japanese.
				translation = translate_to_japanese(response)
				print(f"Tranlated, \n{translation}\n")
				# Generate voice
				await generate_voice(translation, client)
				# Play the voice
				play_wav_voice(translation)
		except KeyboardInterrupt:
			print(f"\nProgram terminated by user.")
			break

		except Exception as error:
			print(f"\nAn error occured: {str(error)}\n")
			continue

if __name__ == "__main__":
	asyncio.run(main())