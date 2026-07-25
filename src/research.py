"""Market research engine: scrapes GitHub trending, HTTPX-based async research."""
import json
import os
from datetime import datetime, timezone
from urllib.parse import quote_plus
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
RESEARCH_DIR = os.path.join(os.path.dirname(__file__), "..", "research")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESEARCH_DIR, exist_ok=True)


def get_github_trending():
    """Scrape GitHub trending repositories via the API."""
    results = []
    categories = ["python", "javascript", "typescript", "rust", "go"]
    for cat in categories:
        try:
            url = f"https://github.com/trending/{cat}?since=weekly"
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            for repo_block in soup.select("article.Box-row"):
                name_el = repo_block.select_one("h2 a[href]")
                stars_el = repo_block.select_one("div.d-inline-block.float-sm-right a")
                desc_el = repo_block.select_one("p")
                if name_el:
                    full_name = name_el.get_text(strip=True)
                    path = name_el["href"].strip("/")
                    star_count = stars_el.get_text(strip=True) if stars_el else "N/A"
                    description = desc_el.get_text(strip=True) if desc_el else ""
                    results.append({
                        "category": cat,
                        "repo": path,
                        "stars": star_count,
                        "description": description,
                    })
        except (URLError, HTTPError, Exception) as e:
            results.append({"category": cat, "error": str(e)})
    return results


def get_github_api_trending():
    """Use GitHub API to search for popular repos with recent activity."""
    results = []
    try:
        query = "created:>2025-01-01 stars:>100"
        encoded_query = quote_plus(query)
        url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=30"
        req = Request(url, headers={
            "User-Agent": "MarketResearchBot/1.0",
            "Accept": "application/vnd.github.v3+json",
        })
        if os.environ.get("GITHUB_TOKEN"):
            req.add_header("Authorization", f"token {os.environ['GITHUB_TOKEN']}")
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        for item in data.get("items", []):
            results.append({
                "name": item["full_name"],
                "stars": item["stargazers_count"],
                "forks": item["forks_count"],
                "language": item.get("language", "N/A"),
                "description": item.get("description", "") or "",
                "updated": item["updated_at"],
                "topics": item.get("topics", []),
            })
    except Exception as e:
        results.append({"error": str(e)})
    return results


def analyze_developer_pain_points():
    """Analyze trending repos to find patterns indicating market gaps."""
    api_results = get_github_api_trending()
    error_items = [r for r in api_results if "error" in r]
    real_repos = [r for r in api_results if "error" not in r]

    if not real_repos:
        return {"status": "failed", "errors": error_items}

    # Categorize by language
    by_language = {}
    for r in real_repos:
        lang = r["language"]
        by_language.setdefault(lang, []).append(r)

    # Find high-star, low-fork ratios (indicates need but few alternatives)
    opportunities = []
    for r in real_repos:
        if r["stars"] > 500:
            fork_ratio = r["forks"] / max(r["stars"], 1)
            opportunities.append({
                "repo": r["name"],
                "stars": r["stars"],
                "fork_ratio": round(fork_ratio, 3),
                "description": r["description"],
                "topics": r["topics"][:5],
            })

    opportunities.sort(key=lambda x: x["stars"], reverse=True)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_repos_analyzed": len(real_repos),
        "top_languages": {lang: len(repos) for lang, repos in by_language.items()},
        "top_opportunities": opportunities[:20],
    }


def save_research(data, filename):
    """Save research results to file."""
    path = os.path.join(RESEARCH_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return path


if __name__ == "__main__":
    print("=== GitHub API Trending Analysis ===")
    api_data = get_github_api_trending()
    save_research(api_data, "github_api_trending.json")
    print(f"Saved {len(api_data)} repos to research/github_api_trending.json")

    print("\n=== Developer Pain Point Analysis ===")
    analysis = analyze_developer_pain_points()
    save_research(analysis, "market_opportunities.json")

    if analysis.get("top_opportunities"):
        print(f"\nTop 5 opportunities by stars:")
        for i, opp in enumerate(analysis["top_opportunities"][:5], 1):
            print(f"  {i}. {opp['repo']} ({opp['stars']} stars) - {opp['description'][:80]}")
    print(f"\nSaved analysis to research/market_opportunities.json")