import logging 
from neo4j import GraphDatabase 
from .config import settings 


logger = logging.getLogger(__name__) 

def get_driver() :
    return GraphDatabase.driver( 
            settings.neo4j_uri , 
            auth = (neo4j_user , neo4j_password)
    )

def validate_query(driver , cypher_query)  : 

    try:
        with driver.session() as session:
            session.run(f"EXPLAIN {cypher_query}")
        return True
    except CypherSyntaxError as exc:
        logger.warning("cypher_query syntax error: %s | query: %s", exc, cypher_query)
        return False
    except Exception as exc:
        logger.error("Unexpected validation error: %s", exc)
        return False
    
def run_cypher(driver, cypher: str) -> str:

    if not validate_cypher(driver, cypher):
        return ""
    try:
        with driver.session() as session:
            result = session.run(cypher)
            records = [str(r) for r in result]
            logger.info("Query returned %d record(s).", len(records))
            return "\n".join(records)
    except ServiceUnavailable as exc:
        logger.error("Neo4j unavailable: %s", exc)
        return ""
    except Exception as exc:
        logger.error("Query execution failed: %s", exc)
        return ""