def normalize_paper(paper: dict) -> dict:

    return {
        "title": paper.get(
            "title",
            "Untitled",
        ),

        "authors": paper.get(
            "authors",
            [],
        ),

        "abstract": paper.get(
            "abstract",
            "",
        ),

        "year": paper.get(
            "year",
        ),

        "doi": paper.get(
            "doi",
        ),

        "source": paper.get(
            "source",
            "unknown",
        ),

        "study_design": paper.get(
            "study_design",
        ),

        "population": paper.get(
            "population",
        ),

        "sample_size": paper.get(
            "sample_size",
        ),

        "limitations": paper.get(
            "limitations",
            [],
        ),
    }


def normalize_papers(papers: list) -> list:

    return [
        normalize_paper(paper)
        for paper in papers
        if isinstance(paper, dict)
    ]