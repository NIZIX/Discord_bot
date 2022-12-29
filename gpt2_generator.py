import transformers
from deep_translator import GoogleTranslator

tokenizer = transformers.GPT2Tokenizer.from_pretrained('gpt2')
model = transformers.GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)


def generate_GPT2(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    beam_output = model.generate(inputs=input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    output = tokenizer.decode(beam_output[0], skip_special_tokens=True)

    result = ".".join(output.split('.')[:-1]) + "."

    return GoogleTranslator(source="en", target="ru").translate(result)

