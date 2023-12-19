def query_loop(chain):
    while True:
        query = input("Enter a question:\n")
        response = chain.invoke(query)
        {%- if cookiecutter.verbose == "y" %}
        print(f"Response:\n{response}")
        {%- else %}
        answer = response["answer"]
        print(f"Response:\n{answer}")
        {% endif %}
