from graph import build_graph


def main():
    ticker = input("Enter stock ticker: ").upper()
    graph = build_graph()
    result = graph.invoke({"ticker": ticker})

    print("\n===== FINAL OUTPUT =====\n")
    print(result.get("final_decision", result["initial_decision"]))


if __name__ == "__main__":
    main()