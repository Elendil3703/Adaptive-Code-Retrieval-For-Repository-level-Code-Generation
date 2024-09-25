import json
import re
from chatgpt import call_openai_api
from tqdm import tqdm  # 引入 tqdm 进度条库
from datasets import load_dataset

output_file = 'gpt_result.json'

# 加载数据集
ds = load_dataset("Fsoft-AIC/RepoExec", split='full_context')

# 筛选出 project 等于 'test-apps/python-string-utils' 的数据
filtered_data = [item for item in ds if item['project'] == 'test-apps/python-string-utils']

# 初始化用于存储所有生成代码的列表
all_generated_codes = []

# 使用 tqdm 添加进度条，总数是 filtered_data 的长度
with tqdm(total=len(filtered_data), desc="Processing", unit="task") as pbar:
    for data in filtered_data:
        prompt = data['target_function_prompt']

        sys_prompt = "You are a Python engineer; your job is to complete the function."

        # 初始化用于存储当前提示的生成代码列表
        generated_codes = []

        # 调用 GPT-3.5-turbo 模型生成结果 5 次
        for _ in range(5):
            generate_results = call_openai_api(prompt, sys_prompt)

            # 使用正则表达式提取 ```python 和 ``` 之间的内容
            match = re.search(r'```python\s*(.*?)\s*```', generate_results, re.DOTALL)
            if match:
                cleaned_code = match.group(1).strip()  # 提取并去除多余的空格
            else:
                cleaned_code = generate_results

            # 将生成的代码加入列表
            generated_codes.append(cleaned_code)

        # 将当前数据的生成代码列表加入总列表
        all_generated_codes.append(generated_codes)

        # 每处理完一条数据，更新进度条
        pbar.update(1)

# 将输出写入 'gpt_result.json'，格式为 [[pred_11, pred_12, pred_13], [pred_21, pred_22, pred_23], ...]
with open(output_file, 'w') as outfile:
    json.dump(all_generated_codes, outfile)

print(f"Results have been written to {output_file}")