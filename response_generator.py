import logging 
import openai 
from openai import OpenAI 
from .config import settings 

logger = logging.getLogger(__name__) 


client = OpenAI(
    api_key=settings.xai_api_key,
    base_url="https://api.x.com/v1",
)

def generate_prompt(context , user_query)  : 
    prompt = """ 
        Context:
        {context}

        User Query: {user_query}
        Answer:
    """ 
    return prompt.format(context=context, user_query=user_query)
    

def generate_response(context , user_query) : 
    prompt = generate_prompt(context , user_query)  
    
    try : 
        response = client.chat.completions.create (
                model = settings.xai_model , 
                messages =[ {role : "user" , content : prompt} ] , 
                max_tokens = settings.max_tokens , 
                temperature = 0.3 
        )
        response = response.choices[0].message.content.strip() 
        logger.info("Generated answer (%d chars).", len(answer))
        return response
    except Exception as exc:
        logger.error("Response generation failed: %s", exc)
        raise