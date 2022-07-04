from csv import DictWriter
from pathlib import Path

from sec_extract.download.__main__ import Firm, get_firms


def write_results(writer: DictWriter, firms: list[Firm]) -> None:
    writer.writeheader()

    for firm in firms:
        has_s1_business = Path(f"./target/s1_business/{firm.ticker_symbol}.html").exists()
        has_s1_management = Path(f"./target/s1_management/{firm.ticker_symbol}.html").exists()

        number_of_10ks = len(
            list(
                Path(f"./target/10k_html").glob(f"{firm.ticker_symbol}{'[0-9]' * 4}.html")
            )
        )
        writer.writerow(
            {
                "Ticker": firm.ticker_symbol,
                "Has S-1 Business": int(has_s1_business),
                "Has S-1 Management": int(has_s1_management),
                "Number of 10-Ks": number_of_10ks
            }
        )


def main():
    firms = get_firms()

    output_path = Path("./target/results.csv")
    output_path.touch(exist_ok=True)

    with open(output_path, "w") as f:
        writer = DictWriter(
            f,
            fieldnames=[
                "Ticker",
                "Has S-1 Business",
                "Has S-1 Management",
                "Number of 10-Ks"
            ]
        )

        write_results(writer, firms)


if __name__ == "__main__":
    main()
