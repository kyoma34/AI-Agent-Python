from ollama import chat




#ai agent
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

            print(f"[Agent called tool : {tool_name} with arguments: {arguments}]")

            if tool_name == "calculator":
                result = calculator(
                    arguments["a"],
                    arguments["b"],
                    arguments["operator"],
                )
                print(f"[Tool result: {result}]")
            messages.append(
                {
                    "role" : "tool",
                    "tool_name" : tool_name,
                    "content" : str(result),
                }
            )

        #final answer
        response = chat(
            model="qwen3-local",
            messages=messages,
            tools=tools,
        )
            

    print(response.message.content)