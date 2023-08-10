# def divide_array(array, num_parts):
#     array_length = len(array)
#     part_size = array_length // num_parts
#     remainder = array_length % num_parts
#     print(remainder)
#     divided_array = []
#     start_idx = 0

#     for i in range(num_parts):
#         end_idx = start_idx + part_size + (1 if i < remainder else 0)
#         divided_array.append(array[start_idx:end_idx])
#         start_idx = end_idx

#     return divided_array

# # Example usage
# input_array = [1,2,3,4,5,6,7]
# num_parts = 5

# result = divide_array(input_array, num_parts)
# for r in range(len(result)):
#     print(result[r])

input_array = ['h1', 'p', 'h2', 'p', 'p', 'ul', 'h2', 'p', 'p', 'p', 'p', 'p', 'h2', 'p', 'p', 'ul', 'h2', 'p', 'p', 'ol', 'h2', 'p', 'ol', 'title', 'description']

divided_parts = []
current_part = []

for element in input_array:
    if element == 'title' or element == 'description':
        continue

    current_part.append(element)

    if element == 'h2':
        divided_parts.append(current_part.copy())
        current_part = []

for part in divided_parts:
    print(part)