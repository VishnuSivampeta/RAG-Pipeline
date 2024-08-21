import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
import ollama
import os

# Directory containing the text files
directory = '/home/vishnu/Desktop/wiki/process_chunks'

# List to store the content of each document
documents = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as file:
            # Read the content of the file
            content = file.read()
            documents.append(content)

# Connect to Weaviate
client = weaviate.connect_to_local()

# Create a new data collection
collection = client.collections.create(
    name="docs5",  # Name of the data collection
    properties=[
        Property(name="text", data_type=DataType.TEXT),  # Name and data type of the property
    ],
)

# Store each document in a vector embedding database
with collection.batch.dynamic() as batch:
    for i, d in enumerate(documents):
        # Generate embeddings
        response = ollama.embeddings(model="all-minilm",
                                     prompt=d)

        # Add data object with text and embedding
        batch.add_object(
            properties={"text": d},
            vector=response["embedding"],
        )

# An example prompt
prompt = "Who is Abraham Lincoln?"

# Generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
    model="all-minilm",
    prompt=prompt,
)

results = collection.query.near_vector(near_vector=response["embedding"],
                                       limit=1)

data = results.objects[0].properties['text']
print(data)

prompt_template = f"Using this data: {data}. Respond to this prompt: {prompt}"

# Generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
    model="llama3.1:8b",
    prompt=prompt_template,
)

print(output['response'])
