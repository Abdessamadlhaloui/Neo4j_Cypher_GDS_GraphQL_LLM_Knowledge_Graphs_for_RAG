import logging
from .utils import get_driver, run_cypher
from .cypher_generator import convert_to_cypher
from .response_generator import generate_response

logger = logging.getLogger(__name__)

_FALLBACK = (
    "MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower('{kw}') "
    "RETURN m.title LIMIT 5"
)

def run_pipeline(user_query: str) -> str:
    driver = get_driver()
    try:
        cypher = convert_to_cypher(user_query)
        context = run_cypher(driver, cypher)
        
        if not context.strip():
            keyword = user_query.split()[-1].strip("?. ,!")
            fallback_cypher = _FALLBACK.format(kw=keyword)
            logger.warning("Primary query empty; trying fallback: %s", fallback_cypher)
            context = run_cypher(driver, fallback_cypher)
            
        return generate_response(user_query, context)
    finally:
        driver.close()
