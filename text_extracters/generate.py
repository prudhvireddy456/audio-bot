

# Your prompt for extracting names
def fetch(a,context,notfound,found):
    import json
    import google.generativeai as palm
    import dotenv
    import os
    dotenv.load_dotenv()
    # Authenticate and set up the Google Generative AI client
    palm.configure(api_key=os.getenv("API_KEY"))
    model=palm.GenerativeModel("gemini-pro")
    prompt = """
    Extract the {}  from the following sentence:
    {}
    Return the {} only in the following format{}.
    if {} not found return {}.
    """.format(context,a,context,found,context,notfound)

    # Call the PaLM model with the prompt
    response = model.generate_content(prompt)

    # Extract the response
    extracted_name = response.text
    print(f"Extracted Name: {extracted_name}")
    return extracted_name