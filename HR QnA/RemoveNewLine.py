import string


def remove_newlines(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
            text_without_newlines = text.replace('\n', '')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_without_newlines)

        print(f"New file '{output_file}' created with removed newlines.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")


def remove_unicode(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
            clean_text = ''.join(
                [char for char in text if char in string.printable])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(
            f"New file '{output_file}' created with removed Unicode characters.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")


def remove_non_printable(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
            clean_text = ''.join(
                [char for char in text if char in string.printable and ord(char) >= 32])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(
            f"New file '{output_file}' created with removed non-printable characters.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")


# Example usage:
# Replace with your input file name
input_file = 'D:\RAG Applications\Test\output.txt'
output_file = 'Final.txt'  # Replace with your desired output file name
remove_non_printable(input_file, output_file)
