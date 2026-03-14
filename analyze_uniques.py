def analyze_uniques(input_list):
    numbers_list = input_list.copy()
    uniques = []
    print(f"Initial: {numbers_list}")
    while numbers_list:
        popped = numbers_list.pop(0)
        unique = True
        # Using a fixed range based on the length at the START of the for loop
        # But the list length changes inside the loop!
        for i in range(len(numbers_list)):
            if i < len(numbers_list): # Guard against shrinking list
                if not (popped ^ numbers_list[i]):
                    match = numbers_list.pop(i)
                    print(f"  Found duplicate: {popped} at index {i}. List now: {numbers_list}")
                    unique = False
        if unique:
            uniques.append(popped)
    return uniques

# Test with a case where element skip might happen
test_list = [7, 7, 7, 10]
print(f"Result: {analyze_uniques(test_list)}")
