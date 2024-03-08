from config import CONFIG

from transformers import pipeline
from transformers import AutoModel, AutoTokenizer

TOKENIZER = None

def load_model(model_name: str):

    CONFIG.MODEL_NAME = model_name

    print(f"[*] Loading MODEL \"{CONFIG.MODEL_NAME}\" ....")
    try:
        CONFIG.MODEL = AutoModel.from_pretrained(CONFIG.MODEL_NAME)
        CONFIG.TOKENIZER = AutoTokenizer.from_pretrained(CONFIG.MODEL_NAME)
        print(f"[*] MODEL \"{CONFIG.MODEL_NAME}\" loaded successfully.")
    except Exception as e:
        print(f"[!] Error loading MODEL \"{CONFIG.MODEL_NAME}\": {e}")


def load_model_from_pipeline(pipeline_name: str):

    print(f"[*] Loading MODEL from pipeline \"{pipeline_name}\" ....")
    try:
        generator = pipeline(pipeline_name)

        CONFIG.MODEL_NAME = generator.model.name_or_path
        load_model(CONFIG.MODEL_NAME)

        CONFIG.PIPELINE = pipeline_name
    except Exception as e:
        print(
            f"[!] Error loading MODEL from pipeline \"{pipeline_name}\": {e}")


def predict(prompt: str, pipelane_name: str = None, model_name: str = None):

    pipeline_name_selected = CONFIG.PIPELINE
    model_name_selected = CONFIG.MODEL_NAME

    if model_name is not None:
        model_name_selected = model_name

    if pipelane_name is not None and pipelane_name != CONFIG.PIPELINE:
        pipeline_name_selected = pipelane_name
        model_name_selected = model_name

    if not model_name_selected and not pipeline_name_selected:
        return {"error": "No MODEL OR PIPELINE loaded yet..."}

    try:
        if pipeline_name_selected:
            print(
                f"Executing {pipeline_name_selected} in {model_name_selected}")
            generator = pipeline(pipeline_name_selected,
                                 model=model_name_selected)
            model_name_executed = generator.model.name_or_path
            match pipeline_name_selected:
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
            return {
                "model": model_name_executed,
                "task": pipeline_name_selected,
                "prediction": result}

    except Exception as e:
        print("ERROR ", e)
        result = {"error": {"output": str(e), "raw": e}}

        return result

    raise Exception("No pipeline especified")
