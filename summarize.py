from ollama import ChatResponse, chat

def summarize(article: str):
    system_prompt = "You are an article text summarizer that summarizes the latest articles in 2 or 3 sentences. Make sure add the latest innovations from the article in thes summarization"
    user_prompt =  f'Please summarize this article: {article}'

    response: ChatResponse = chat(model='granite4.1:8b', messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': user_prompt,
        },
    ] )

    return response['message']['content']

