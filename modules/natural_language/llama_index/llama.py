from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os
os.environ["OPENAI_API_KEY"] = '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'

documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex.from_documents(documents)


# save to disk
index.save_to_disk('index.json')

# load from disk
index = GPTSimpleVectorIndex.load_from_disk('index.json')


a = index.query(
    "Create a tutorial based on this content, use markdown, add code examples")

print(a.response)
