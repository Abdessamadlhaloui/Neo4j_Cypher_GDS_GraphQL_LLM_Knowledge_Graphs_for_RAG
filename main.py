import argparse
import logging
from .full_pipeline import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Knowledge Graph RAG --- query the Neo4j movie graph",
    )
    parser.add_argument(
        "--query", required=True,
        help='Natural language query, e.g. "Who directed The Matrix?"',
    )
    args = parser.parse_args()
    answer = run_pipeline(args.query)
    print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()
