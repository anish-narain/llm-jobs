import pandas as pd
import time
import random
import csv  
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.fillna('', inplace=True)
    return df

def select_random_start(num_rows, min_rows=15):
    if num_rows < min_rows:
        raise ValueError(f"The dataset must contain at least {min_rows} rows to process.")
    return random.randint(0, num_rows - min_rows)

def create_prompt_template():
    return PromptTemplate(
        template=(
            "Context: You are a clinician receiving chunks of clinical text for patients in an ICU. Please do the reviewing as quickly as possible.\n"
            "Task: Determine if the patient had pneumonia.\n"
            "Instructions: Answer with 'Yes' or 'No'. If there is not enough information, answer 'No'.\n"
            "Discharge Text:\n{discharge_text}\n\n"
            "Query: Does the chunk of text suggest that the patient has pneumonia? Answer strictly in 'Yes' or 'No'."
        ),
        input_variables=["discharge_text"]
    )

def chunk_text(text, chunk_size, overlap):
    start = 0
    chunks = []
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def check_for_pneumonia(discharge_text, llm, prompt_template, chunk_size, chunk_overlap):
    chunks = chunk_text(discharge_text, chunk_size, chunk_overlap)
    results = []
    for chunk in chunks:
        prompt = prompt_template.format(discharge_text=chunk)
        try:
            response = llm.invoke(prompt)
            results.append(response.strip())
        except Exception as e:
            results.append(f"Error invoking model: {e}")
    pneumonia_mentions = [res for res in results if "Yes" in res]
    if pneumonia_mentions:
        return "Yes", pneumonia_mentions[0], len(discharge_text) # Return pneumonia result, explanation, and length of discharge_text
    else:
        return "No", results[0] if results else "No sufficient data", len(discharge_text) # Return pneumonia result, explanation, and length of discharge_text

def benchmark_llm_inference(llm, prompt_template, discharge_text, chunk_size, chunk_overlap):
    start_time = time.time()
    result = check_for_pneumonia(discharge_text, llm, prompt_template, chunk_size, chunk_overlap)
    end_time = time.time()
    return end_time - start_time

def main(file_path, model_name, chunk_size, chunk_overlap, num_gpu):
    df = load_data(file_path)
    #start_index = select_random_start(len(df))
    start_index = 0
    prompt_template = create_prompt_template()
    
    llm_cpu = Ollama(model=model_name, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    llm_gpu = Ollama(model=model_name, num_gpu=num_gpu, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    
    discharge_text = df['discharge_text'].values[start_index]
    
    cpu_time = benchmark_llm_inference(llm_cpu, prompt_template, discharge_text, chunk_size, chunk_overlap)
    gpu_time = benchmark_llm_inference(llm_gpu, prompt_template, discharge_text, chunk_size, chunk_overlap)
    
    print(f"CPU Time: {cpu_time:.2f} seconds")
    print(f"GPU Time: {gpu_time:.2f} seconds")

if __name__ == "__main__":
    main(
        file_path='/Users/anishnarain/Documents/FYP-Files/git/identifying-ARDS/data-preprocessing/csv-files/ards-cohort-notes.csv',
        model_name="llama3",
        chunk_size=4096,
        chunk_overlap=100,
        num_gpu=1  # Set to 1 to use the GPU
    )
