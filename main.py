from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/")
async def translate(request: Request):
    try:
        body = await request.json()
        message = body.get("message", "")

        # Determine language based on prefix
        if message.startswith("@th"):
            target_lang = "Thai"
            text = message[3:].strip()
        elif message.startswith("@my"):
            target_lang = "Burmese"
            text = message[3:].strip()
        else:
            return JSONResponse({"response": "Please start your message with @th or @my."})

        # Generate translation using OpenAI GPT
        prompt = f"Translate the following into {target_lang}:\n{text}"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # use correct model
            messages=[
                {"role": "system", "content": f"You are a translator that translates text into {target_lang}."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = completion.choices[0].message.content.strip()
        return JSONResponse({"response": f"**{target_lang}:** {reply}"})
    
    except openai.error.AuthenticationError:
        return JSONResponse({"error": "Invalid OpenAI API key."}, status_code=401)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
