import openai
from PIL import Image

# open AI key would go here not attached due to subscription status being cancled after presentation.
openai.api_key = ""

def get_pixel_modification_code(user_request):
    """Get Python code to modify image pixels based on the user's request."""
    prompt = f"""
    The user has requested the following modification for an image named MainBefore.jpg: "{user_request}".
    Generate Python code that directly modifies the pixels of a PIL Image object named 'image'.
    Assume 'image' is already loaded and is a PIL Image object in RGB mode.
    Your response must only include Python code, no explanations or comments 
    here is the code as a sample:.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in Python programming and image processing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
    )
    return response.choices[0].message['content'].strip('```python').strip('```')

def apply_generated_code(image, code):
    """Apply Python code to modify the image."""
    local_vars = {'image': image}
    try:
        code.strip('```python').strip('```')
        exec(code, {}, local_vars)
        return local_vars.get('image', image)  # Return the modified image if 'image' was reassigned
    except Exception as e:
        print(f"Error executing generated code: {e}")
        return image



def main():
    # Load the image
    
    image_path = r"C:/Users/Hiro/AIProject/MainBefore.jpg"
    image = Image.open(image_path).convert("RGB")

    # Get user's modification request
    user_request = input("Describe how you'd like to modify the image: ")

    # Get Python code from OpenAI
    print("Processing your request...")
    generated_code = get_pixel_modification_code(user_request)
    print(f"Generated code:\n{generated_code}")

    # Apply the generated code
    modified_image = apply_generated_code(image, generated_code)

    # Save and show the modified image
    output_path = "modified_image.png"
    modified_image.save(output_path)
    print(f"Image saved as {output_path}")
    ##modified_image.show()

if __name__ == "__main__":
    main()