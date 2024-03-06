from transformers           import pipeline
from transformers           import AutoModel, AutoTokenizer

TOKENIZER = None
MODEL = None
MODEL_NAME = None
PIPELANE = None


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

def load_model_from_pipelane(pipelane_name: str):
    global MODEL_NAME, PIPELANE
    
    print(f"[*] Loading MODEL from PIPELANE \"{pipelane_name}\" ....")
    try:
        generator = pipeline(pipelane_name)
        
        MODEL_NAME = generator.model.name_or_path
        load_model(MODEL_NAME)

        PIPELANE = pipelane_name
    except Exception as e:
        print(f"[!] Error loading MODEL from PIPELANE \"{pipelane_name}\": {e}")


def predict(prompt: str):
    global MODEL_NAME, PIPELANE, MODEL, TOKENIZER
    print(f"PIPA - {PIPELANE}")
    if not MODEL and not TOKENIZER and not PIPELANE:
        return {"error": "No MODEL loaded yet..."}

    try:
        if PIPELANE:
            generator = pipeline(PIPELANE, model=MODEL_NAME, tokenizer=TOKENIZER)
            match PIPELANE:
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

    raise Exception("No pipelane especified")