from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
warnings.filterwarnings('ignore')

model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def manual_mode(prompt):
    messages = [
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def run_model(context, question):
    # Construct the prompt
    prompt = f"""IMPORTANT: You must ONLY use the information provided in the context below to answer the question. 
    Do not use any other knowledge or information you may have. 
    If the answer cannot be directly found in the context, only respond with "I cannot answer this question based on the provided context."

    Context:
    "{context}"

    Question: 
    "{question}"

    Remember to only use the context provided to answer the question!
    If possible, also return the code chunk from the context that is the most relevant in answering the question.

    Answer:"""

    response = manual_mode(prompt)
    return response


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a text generation model using manual or pipeline mode.")
    parser.add_argument("--context", type=str, required=True, help="The context to provide to the model.")
    parser.add_argument("--question", type=str, required=True,
                        help="The question to ask based on the provided context.")

    args = parser.parse_args()
    run_model(args.context, args.question)
