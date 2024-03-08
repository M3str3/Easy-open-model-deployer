from transformers           import pipeline
from transformers           import AutoModel, AutoTokenizer

TOKENIZER = None
MODEL = None
MODEL_NAME = None
PIPELINE = None


def load_model(model_name: str):
    global TOKENIZER, MODEL, MODEL_NAME

    MODEL_NAME = model_name
    
    print(f"[*] Loading MODEL \"{MODEL_NAME}\" ....")
    try:
        MODEL = AutoModel.from_pretrained(MODEL_NAME)
        TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
        print(f"[*] MODEL \"{MODEL_NAME}\" loaded successfully.")
    except Exception as e:
        print(f"[!] Error loading MODEL \"{MODEL_NAME}\": {e}")

def load_model_from_pipeline(pipeline_name: str):
    global MODEL_NAME, PIPELINE
    
    print(f"[*] Loading MODEL from pipeline \"{pipeline_name}\" ....")
    try:
        generator = pipeline(pipeline_name)
        
        MODEL_NAME = generator.model.name_or_path
        load_model(MODEL_NAME)

        PIPELINE = pipeline_name
    except Exception as e:
        print(f"[!] Error loading MODEL from pipeline \"{pipeline_name}\": {e}")


def predict(prompt: str):
    global MODEL_NAME, PIPELINE, MODEL, TOKENIZER
    print(f"PIPA - {PIPELINE}")
    if not MODEL and not TOKENIZER and not PIPELINE:
        return {"error": "No MODEL loaded yet..."}

    try:
        if PIPELINE:
            generator = pipeline(PIPELINE, model=MODEL_NAME, tokenizer=TOKENIZER)
            match PIPELINE:
                case "text-generation":
                    result = generator(prompt, max_length=50,
                                    num_return_sequences=1)
                    result = result[0]['generated_text']
                case "question-answering":
                    result = generator({
                        "question": prompt
                    })
                case "sentiment-analysis":
                    result = generator(prompt)[0]
                case "summarization":
                    def split_text(text, max_length=1024):
                        chunks = []
                        for i in range(0, len(text), max_length):
                            chunk = text[i:i+max_length]
                            chunks.append(chunk)
                        return chunks
                    prompts = split_text(prompt)
                    result = ""
                    for prompt in prompts:
                        print(generator(prompt))
                        result += generator(prompt)[0]['summary_text']
                case _:
                    result = generator(prompt)
            return result
    
    except Exception as e:
        print("ERROR ",e)
        result = {"error":{"output":str(e),"raw":e}}
            
        return result    

    raise Exception("No pipeline especified")