import base64
from openai import OpenAI
from system_prompt import steve_system_prompt

instruction = "User task: search for today's weather. Please generate the next move."
screenshot1_path = "./examples/chrome/bb5e4c0d-f964-439c-97b6-bdb9747de3f4/step_reset_20250226@040010.jpg"
screenshot2_path = "./examples/chrome/bb5e4c0d-f964-439c-97b6-bdb9747de3f4/step_1_20250226@040020.jpg"

with open('./examples/chrome/bb5e4c0d-f964-439c-97b6-bdb9747de3f4/plan_result_full-step_1_20250226@040020.txt', 'r') as f:
    gt_response = f.read().strip()

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="empty",
)

with open(screenshot1_path, 'rb') as image1_file:
    screenshot1_string = base64.b64encode(image1_file.read()).decode("utf-8")

with open(screenshot2_path, 'rb') as image2_file:
    screenshot2_string = base64.b64encode(image2_file.read()).decode("utf-8")

round1_response = client.chat.completions.create(
    model="cot_qwen2vl",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": steve_system_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot1_string}"}},
                {"type": "text", "text": instruction}
            ],
        },
    ],
    frequency_penalty=0.2,
    temperature=0.6,
    max_tokens=4096,
    extra_body={"skip_special_tokens": False}
)
round1_response = round1_response.choices[0].message.content

# Here we use the ground truth response for the second round
round1_response = gt_response

round2_response = client.chat.completions.create(
    model="cot_qwen2vl",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": steve_system_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot1_string}"}},
                {"type": "text", "text": instruction}
            ],
        },
        {
            "role": "assistant",
            "content": round1_response,
        },
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot2_string}"}},
                {"type": "text", "text": instruction}
            ]
        }
    ],
    frequency_penalty=0.2,
    temperature=0.6,
    max_tokens=4096,
    extra_body={"skip_special_tokens": False}
)

round2_response = round2_response.choices[0].message.content

print(round2_response)

