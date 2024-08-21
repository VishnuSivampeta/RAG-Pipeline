import weaviate
import ollama
import os

# Function to split text into chunks
def split_into_chunks(text, max_length=512):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_length:
            chunks.append('. '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk))

    return chunks

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
client = weaviate.Client("http://localhost:8080")  # Adjust the URL if necessary

# Check if the class exists and delete it
collection_name = "Docs5"
if client.schema.exists(collection_name):
    client.schema.delete_class(collection_name)

# Define the class schema
class_obj = {
    "class": collection_name,
    "properties": [
        {
            "name": "text",
            "dataType": ["text"],
        },
    ],
}

# Create the class in the schema
client.schema.create_class(class_obj)

# Store each document in a vector embedding database
with client.batch as batch:
    for i, d in enumerate(documents):
        # Split document into chunks
        chunks = split_into_chunks(d)

        for chunk in chunks:
            # Generate embeddings for each chunk
            response = ollama.embeddings(model="all-minilm", prompt=chunk)

            # Add data object with text and embedding
            batch.add_data_object(
                data_object={"text": chunk},
                class_name=collection_name,
                vector=response["embedding"],
            )

# An example prompt
prompt = "Who is Abraham Lincoln?"

# Generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
    model="all-minilm",
    prompt=prompt,
)

# Perform the query and specify the properties to return
results = client.query.get(collection_name, ["text"]).with_near_vector({"vector": response["embedding"]}).with_limit(1).do()

# Extract the text property from the results
data = results['data']['Get'][collection_name][0]['text']
# print(data)
prompt_template = f"Using this data: {data}. Respond to this prompt: {prompt}"

# Generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
    model="llama3.1:8b",
    prompt=prompt_template,
)

print(output['response'])
