# Names: 
# Youssef Mostafa Al-Ansary 20240717
# Mohamed Khaled Anwar 20250906
# Mohamed Mahmoud Kamal 20240526

import math

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

def print_compression_statistics(user_input_string, compressed_data):
    if len(user_input_string) > 0:

        original_size = len(user_input_string)

        # Find the largest value in each numeric field
        max_position = max(tag.position for tag in compressed_data)
        max_length = max(tag.length for tag in compressed_data)

        # Calculate the required bits for each field
        position_bits = max(1, max_position.bit_length())
        length_bits = max(1, max_length.bit_length())
        character_bits = 8 

        compressed_size = (position_bits + length_bits + character_bits) * len(compressed_data)
        compression_ratio = original_size / compressed_size

        print(f"\n--- Compression Statistics ---")
        print(f"Original Size: {original_size * 8} bits")
        print(f"Compressed Size: {compressed_size} bits")
        print(f"Compression Ratio: {compression_ratio:.2f}")


def print_decompression_statistics(tags, decompressed_string):
    if len(tags) > 0:

        max_position = max(tag.position for tag in tags)
        max_length = max(tag.length for tag in tags)

        # Calc the required bits for each
        position_bits = max(1, max_position.bit_length())
        length_bits = max(1, max_length.bit_length())
        character_bits = 8

        original_size = (position_bits + length_bits + character_bits) * len(tags)

        # Calculate decompressed size
        decompressed_size = len(decompressed_string) * 8

        compression_ratio = original_size / decompressed_size

        print(f"\n--- Decompression Statistics ---")
        print(f"Original Size (Tags): {original_size} bits")
        print(f"Decompressed Size: {decompressed_size} bits")
        print(f"Compression Ratio: {compression_ratio:.2f}")


if __name__ == "__main__":

    choice = int(input("1. Compress\n2. Decompress \n"))

    if choice == 1: #compression
        user_input_string = input('Please Enter Your String: ')
        search_window = int(input('Please Enter Search Buffer Size (e.g., 4000): '))
        look_ahead_window = int(input('Please Enter Look-Ahead Window Size (e.g., 4000): '))
        
        compressed_data = lz77_compress(user_input_string, search_window, look_ahead_window)
        print(f"Compressed Tags: {compressed_data}")
        print_compression_statistics(user_input_string, compressed_data)

    else: #decompression
        num_tags = int(input('Please Enter The Number of Tags: '))
        tags = []

        for i in range(num_tags):
            position = int(input("Position: "))
            length = int(input("Length: "))
            next_character = input("Next Character: ")

            tags.append(Tag(position, length, next_character))

        decompressed_string = lz77_decompress(tags)
        print(f"Decompressed: {decompressed_string}")
        print_decompression_statistics(tags, decompressed_string)
