from ollama import chat
from ddgs import DDGS

#---------------------fucntions-----------------------
def calculator(a,b,operator):
    a=float(a)
    b=float(b)
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return "Invalid operator"

def web_search(query: str):
    results = DDGS().text(
        query,
        max_results=5
    )

    if not results:
        return "No search results found."

    output= []

    for result in results:
        output.append(
            f"Title: {result['title']}\n"
            f"URL: {result['href']}\n"
            f"Snippet: {result['body']}\n"
        )

    return "\n".join(output)

#-------------------tools-------------------------    
tools = [
    calculator,
    web_search
]


#-------------------------ai agent--------------------------
while True:
    question = input("> ")
    if question.strip().lower() == "exit":
        break

    messages=[
        {
            "role": "user",
            "content": question,
        }
    ]

    response = chat(
        model="qwen3-local",
        messages=messages,
        tools=tools,
    )

    messages.append(response.message)

    if response.message.tool_calls:

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\n[Agent called tool : {tool_name} with arguments: {arguments}]")

            if tool_name == "calculator":
                result = calculator(
                    arguments["a"],
                    arguments["b"],
                    arguments["operator"],
                )

            elif tool_name == "web_search":
                result = web_search(
                    arguments["query"]
                )

            else:
                result = f"Unkown tool: {tool_name}"

            print(f"[Tool result: {result}]\n")

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                }
            )
                

        #final answer
        response = chat(
            model="qwen3-local",
            messages=messages,
            tools=tools,
        )
            

    print(response.message.content)