import json 
def divide_array(array, num_parts):
    array_length = len(array)
    part_size = array_length // num_parts
    remainder = array_length % num_parts
    divided_array = []
    start_idx = 0

    for i in range(num_parts):
        end_idx = start_idx + part_size + (1 if i < remainder else 0)
        divided_array.append(array[start_idx:end_idx])
        start_idx = end_idx

    return divided_array
big_array = {}
with open('test/text_test.json',"r",encoding="UTF-8") as f_json:
    texts = json.load(f_json)
for i in range(len(texts)):
    print(f"Текст {i}")
    keys = []
    h2_amount = 0
    for parts in texts[i]:
        for key in parts:
            keys.append(key)
            if key == "h2":
                h2_amount += 1
    next_el = ""
    j = 0
    current_el = ""
    blocks=[]
    divided_parts = []
    current_part = []

    for k in range(h2_amount+1):
        block = []
        keys_len = len(keys)-2
        while j < keys_len:
            current_el = keys[j]
            next_el = keys[j+1]
            block.append(current_el)
            if next_el == "h2":
                j = j + 1
                break
            else: 
                j = j + 1
        blocks.append(block)
    a = divide_array(blocks,4)
    text_array = []
    for el in a:
        text_array.append({
            "block":el
        })
    big_array.update({f"":text_array})
    with open("text_scructure.json","w",encoding="UTF-8") as f:
        json.dump(big_array,f,ensure_ascii=False)
