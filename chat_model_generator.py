from transformers import AutoModelForCausalLM, AutoTokenizer
from deep_translator import GoogleTranslator, single_detection
from config_operations import read_config
import torch

model_name = "microsoft/DialoGPT-large"
# model_name = "microsoft/DialoGPT-medium"
# model_name = "microsoft/DialoGPT-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)



step = 0
chat_history_ids = None

def generate_GPT2(input_text):
    config = read_config()
    global step, chat_history_ids # step отвечает за память модели 

    if step == 2 or input_text in ["forget everything", 'забудь все']:
        step = 0

        if input_text in ["forget everything", 'забудь все']:
            return "I will forget everything"

    if config["TRANSLATE_FLAG"] and single_detection(input_text, api_key="fb24daadc09f0207767d8b6b5268de0a") == 'ru':
        input_text = GoogleTranslator(source="ru", target="en").translate(input_text)

    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    # concatenate new user input with chat history (if there is)
    bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
    # generate a bot response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        top_k=100,
        temperature=2.5, # большая температура приводит к уравниванию вероятностей, а низкая к преобладанию высоковероятных
        pad_token_id=tokenizer.eos_token_id
    )

    output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    step += 1
    
    print(chat_history_ids)


    return output

