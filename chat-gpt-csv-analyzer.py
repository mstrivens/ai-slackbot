import pandas as pd
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def generate_prompt(question, thread):
    return f'Table:\n| Questions | Thread |\n|---|---|\n"{question}" | "{thread}" |\n\nInstructions to GPT-3:\nCondense the provided thread into a brief summary, this will be used to create a freqently asked question document and will ultimately be used to power a chatbot. Ensure any references to specific terminal or error messages, terminal commands, code blocks and specific steps are included in the summary, for example a terminal command inside quotation marks should be included.'

# Read the CSV file
df = pd.read_csv('questions.csv')


# print("DATA FRAME", df)

for index, row in df.iterrows():
    # if index < 1:
    question = row['questions']
    thread = row['thread']
    prompt = generate_prompt(question, thread)
    print(f'Prompt for Row {index + 1}:\n{prompt}\n{"-"*50}\n')
    df.drop(columns=['thread'], inplace=True)

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100)
    df.loc[index,'summary'] = response.choices[0].text
    
print("wd", os.getcwd())
path = os.getcwd()
df.to_csv(path + '/summary.csv', index=False)

# print("QUESTION\n", question, "\n\nTHREAD", response.choices[0].text)