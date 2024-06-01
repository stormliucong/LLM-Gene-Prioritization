from llama_index import PromptTemplate

instruction_str="""\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. The code should not contain any comments.
    5. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""
    
new_prompt = PromptTemplate(
    """\
        You are working with a pandas dataframe in Python.
        The name of the dataframe is `df`.
        This is the result of `print(df.head())`:
        {df_str}
    
        Follow these intructions:
        {instruction_str}
        Query: {query_str}
        
        Expression: """
)


    