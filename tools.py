import PyPDF2
import io

def pdf_tool(input: str) -> str:
    """
    A tool for processing PDF files.
    """
    try:
        # Assuming input is a file path to a PDF
        with open(input, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return f"Extracted text from PDF: {text[:500]}..."  # Return first 500 characters
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def read_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns its full text content.

    Args:
    file_path (str): The path to the PDF file.

    Returns:
    str: The full text content of the PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def search_pdf_tool():
    """
    Searches for a PDF processing tool among the available functions in this module.
    
    Returns:
    function: The first function found that matches the criteria for a PDF tool.
    """
    import inspect
    
    # Get all functions defined in this module
    functions = inspect.getmembers(inspect.getmodule(search_pdf_tool), inspect.isfunction)
    
    # Search for a function that mentions 'pdf' in its name or docstring
    for name, func in functions:
        if 'pdf' in name.lower() or (func.__doc__ and 'pdf' in func.__doc__.lower()):
            return func
    
    # If no matching function is found
    return None

def use_pdf_tool(input: str) -> str:
    """
    Uses the search function to find and use the PDF tool.

    Args:
    input (str): The input for the PDF tool (usually a file path).

    Returns:
    str: The result of using the PDF tool, or an error message if no tool is found.
    """
    pdf_tool = search_pdf_tool()
    if pdf_tool:
        return pdf_tool(input)
    else:
        return "No PDF tool found."
