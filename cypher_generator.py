import logging
import openai
from openai import OpenAI
from .config import settings

logger = logging.getLogger(__name__)



client = OpenAI(
    api_key=settings.xai_api_key,
    base_url="https://api.x.com/v1", 
)


def generate_prompt(user_query: str)-> str  : 

    schema = """ 
            {
        "nodes": [
            {"label": "Movie", "properties": ["title", "released", "tagline"]},
            {"label": "Person", "properties": ["name", "born"]}
        ],
        "relationships": [
            {"type": "ACTED_IN", "from": "Person", "to": "Movie", "properties": ["roles"]},
            {"type": "DIRECTED", "from": "Person", "to": "Movie", "properties": []},
            {"type": "PRODUCED", "from": "Person", "to": "Movie", "properties": []},
            {"type": "WROTE", "from": "Person", "to": "Movie", "properties": []},
            {"type": "REVIEWED", "from": "Person", "to": "Movie", "properties": ["summary", "rating"]},
            {"type": "FOLLOWS", "from": "Person", "to": "Person", "properties": []}
        ]
    }

    """

    prompt = """ 
            You are an expert Neo4j Cypher query generator.
            The graph has the following schema:
            {schema}

            Rules:
            - Use ONLY the labels, relationship types, and properties defined above.
            - Never invent or guess label names.
            - Return only the Cypher query; no prose, no markdown fences.
            - Append LIMIT 25 unless the query semantically requires all results.
            - Prefer MATCH over OPTIONAL MATCH unless null results are acceptable.

            User Query: {user_query}
            Cypher Query:
    """

    return prompt.format(schema=schema , user_query=user_query) 

def convert_to_cypher(user_query: str) -> str:

    prompt = generate_prompt(user_query)

    try:
        response = client.chat.completions.create(
            model=settings.xai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.max_tokens ,
            temperature=0.2, 
        )
        cypher = response.choices[0].message.content.strip()
        logger.info("Generated Cypher: %s", cypher)
        return cypher
        
    except Exception as exc:
        logger.error("Cypher generation failed: %s", exc)
        raise
