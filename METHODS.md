# Methods and findings

## Population and scope

The input is the existing project's frozen extract of 3,179 accepted public-stock purchase records with 2025 transaction dates. It contains 55 distinct politician display names and 855 tickers. It is a filtered disclosure dataset, not a complete census of trading or household holdings.

Keep rows with transaction_type=P, asset_type=ST, ticker_parse_status=accepted, a nonempty ticker, and a transaction date in 2025. Remove leading Hon./Honorable from politician names and uppercase tickers, matching the original project's display-name rules. Identity is based on the cleaned display name, without a new identity-resolution model.

## Two-mode network

Nodes are disclosure filers and stock tickers. A tie exists when a filer reports at least one qualifying purchase of a ticker. Repeated records collapse to one neighbor relationship for degree calculations. Stocks enter the shared-stock graph only if at least two distinct filers purchased them.

This produces 45 filers, 355 stock tickers, and 1,291 filer–ticker ties. Ten of the 55 filers have no purchase of a shared ticker and therefore fall outside this displayed graph. Their records remain in the input extract.

Stock degree counts distinct filers. Politician degree counts distinct shared tickers. Neither measure uses purchase value, repeated transaction frequency, party, or committee membership.

| Stock | Distinct filers |
|---|---:|
| AMZN | 19 |
| AAPL | 15 |
| AVGO | 15 |
| MSFT | 14 |
| NVDA | 14 |

Tied values sort alphabetically.

| Filer | Distinct stocks in shared-stock graph |
|---|---:|
| Lisa McClain | 210 |
| Gilbert Cisneros | 146 |
| Rob Bresnahan | 135 |
| Jefferson Shreve | 118 |
| Bruce Westerman | 75 |

## One-mode politician projection

Connect two filers if their qualifying purchases share at least one ticker. The weight counts distinct shared tickers. The projection is undirected and has no self-ties.

There are 494 ties among 45 filers. Density = 494 / (45 × 44 / 2) = 0.4989899, or 49.9%. All 45 filers belong to one connected component. The presentation reports unweighted density. Edge weights preserve shared-ticker counts for future analysis.

The build independently enumerates all filer pairs within each shared ticker and checks that their union has 494 pairs. It also checks that stock degrees sum to the bipartite edge count.

## Interpretation

Amazon connects the most filers in this extract. A few filers connect to many distinct shared stocks. Roughly half the possible pairs in the filtered graph share at least one stock purchase across the year.

Popular stocks can generate many projected ties. Shared purchasing across a year does not demonstrate personal relationships, simultaneous purchases, coordination, privileged information, or wrongdoing. These measures also do not measure returns or the size of investment positions.

## Limits and possible extensions

- Disclosure records can describe a spouse or dependent rather than the filer's personal transaction.
- Amounts are ranges, and purchases do not measure complete holdings.
- Sales, other asset types, and unresolved tickers fall outside this extract.
- Source omissions, parsing errors, amendments, and ticker/identity resolution can change the graph.
- The frozen input is unchanged from the original project. This build does not refresh the underlying scrape.
- Committee context remains in the original interactive project and is excluded from the calculations here.
- Future comparisons could use transaction timing, household ownership, general market popularity, or an explicit null model before interpreting overlap as unusual.

## Presentation figure

The node-link figure is an illustrative slice containing the three stocks with highest degree and all their qualifying buyers. Its fixed positions aid reading and do not encode geography, party, or centrality. Tables and metrics use the full shared-stock graph.
