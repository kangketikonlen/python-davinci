import os
import openai

# Setup OpenAI API Client
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create a loop
while True:
	try:
		# Prompt user to type question.
		user_input = input("Ask: ")
		# Send the user's input to the OpenAI.
		user_input = user_input.replace("Ask: ", "")
		# Generate response
		response = openai.Completion.create(
			model="text-davinci-003",
			prompt=user_input,
			temperature=0.9,
			max_tokens=100,
			top_p=1,
			frequency_penalty=0,
			presence_penalty=0,
			stop=["Ask: "]
		)
		# Make response readable.
		generated_text = response.choices[0].text.strip().replace('\n', '')
		print(f"\nThe AI Response, \n{generated_text}\n")
	except KeyboardInterrupt:
		print(f"\nProgram terminated by user.")
		break

	except Exception as error:
		print(f"\nAn error occured: {str(error)}\n")
		continue