import requests


def get_html_urls() -> list[str]:
    with open("warnings.csv") as f:
        file_lines = f.read().splitlines()

    downloadable_lines = [line for line in file_lines if "Could not download" in line]

    urls = [line.replace("Could not download ", "") for line in downloadable_lines]
    return [line.replace("ix?doc=/", "") for line in urls]


def main():
    html_urls = get_html_urls()
    for html_url in html_urls:
        r = requests.get(html_url, headers={'User-Agent': 'Mozilla/5.0'})
        print(r)


if __name__ == "__main__":
    main()
