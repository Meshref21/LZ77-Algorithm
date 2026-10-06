# Names: 
# Youssef Mostafa Al-Ansary 20240717
# Mohamed Khaled Anwar 20250906
# Mohamed Mahmoud Kamal 20240526

class Tag:
    def __init__(self, position: int, length: int, next_char: str):
        self.position = position
        self.length = length
        self.next_char = next_char

    # The representation of the tag
    def __repr__(self):
        return f"<{self.position},{self.length},'{self.next_char}'>"


def lz77_compress(input_string: str, search_window_size: int = 4000, look_ahead_window_size: int = 4000) -> list:
    result_tags: list[Tag] = []       
    cursor = 0                          
    n = len(input_string)
    
    while cursor < n:
        best_distance = 0
        best_length = 0
        
        max_distance = min(cursor, search_window_size)
        
        # d is the distance I need to go back, starting from cursor (cursor - d)
        for d in range(1, max_distance + 1):
            current_length = 0
            
            
            while (cursor + current_length < n and 
                   current_length < look_ahead_window_size and 
                   input_string[cursor - d + current_length] == input_string[cursor + current_length]):
                current_length += 1
                
            # Update the longest match found so far
            if current_length > best_length:
                best_length = current_length
                best_distance = d
                
        # takes the next character
        if cursor + best_length < n:
            next_char = input_string[cursor + best_length]
        else:
            next_char = 'NULL'
            
        
        result_tags.append(Tag(best_distance, best_length, next_char))
        
        # Shift the sliding window by the length of the match plus 1 (for the next_char)
        cursor += best_length + 1
        
    return result_tags

def lz77_decompress(tags: list[Tag]) -> str:
    output_string = []
    
    for tag in tags:
        if tag.length > 0:
            start_index = len(output_string) - tag.position
            # Append characters one by one to handle repetitive overlapping sequences properly (SLICING WOULD FAIL)
            for i in range(tag.length):
                output_string.append(output_string[start_index + i])
        
        # Add the next character if exists
        if tag.next_char != 'NULL':
            output_string.append(tag.next_char)
            
    return "".join(output_string)

if __name__ == "__main__":

    choice = int(input("1. Compress\n2. Decompress \n"))

    if choice == 1:
        test_string = input('Please Enter Your String: ')
        compressed_data = lz77_compress(test_string)
        print(f"Compressed Tags: {compressed_data}")

    else:
        num_tags = int(input('Please Enter The Number of Tags: '))
        tags = []

        for i in range(num_tags):
            position = int(input("Position: "))
            length = int(input("Length: "))
            next_character = input("Next Character: ")

            tags.append(Tag(position, length, next_character))

        decompressed_string = lz77_decompress(tags)
        print(f"Decompressed: {decompressed_string}")