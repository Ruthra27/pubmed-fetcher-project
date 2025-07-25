import typer
from src.pubmed.fetcher import fetch_pubmed_ids, fetch_paper_details
from src.pubmed.parser import parse_paper_details
from src.pubmed.utils import save_to_csv

app = typer.Typer()

@app.command("get-papers-list")
def get_papers_list(query: str, file: str = "", debug: bool = False):
    if debug:
        typer.echo(f"Fetching PubMed IDs for query: {query}")

    pmids = fetch_pubmed_ids(query)

    if not pmids:
        typer.echo("No PubMed IDs found for the query.")
        return

    if debug:
        typer.echo(f"Found PubMed IDs: {pmids}")

    papers = []
    for pmid in pmids:
        xml_data = fetch_paper_details(pmid)
        paper_details = parse_paper_details(xml_data)
        papers.append(paper_details)

    if file:
        save_to_csv(papers, file)
        typer.echo(f"Saved {len(papers)} papers to {file}")
    else:
        for paper in papers:
            typer.echo(paper)

if __name__ == "__main__":
    app()