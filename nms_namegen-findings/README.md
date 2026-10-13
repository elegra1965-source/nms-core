# nms_namegen: sell/buy formula + an independent scoreboard

From Tony (elegra1965), NMS Galactic Map (map.nomansskyhub.app), which uses a JavaScript port of nms_namegen.
13 October 2026.

## 1. New: the real sell% / buy%

The galaxy map's "Sell" and "Buy" percentages come from the **first two draws of the same PRNG stream `planetSeeds()` uses** (not the `systemAttributes()` stream):

```
buy  = -30 + 20 * u1
sell =  40 + 40 * u2
```

`u_k` = low 32 bits of the seed after k updates, divided by 2^32. Rounded to 1 decimal, as the game shows it. The planet digit of the portal code doesn't matter.

Python drop-in for `nms_namegen` is in `sell_buy.py` (uses your `PRNG`, `CONST_A`, `CONST_B`).

**How well it fits:** 1,444 systems where players recorded sell and buy on our map (mostly from the Galactic Hub wiki):

| | Systems |
|---|---|
| Both values exact to 1 decimal | 1,350 (93.5%) |
| Sell exact | 1,371 (94.9%) |
| Buy exact | 1,383 (95.8%) |

The misses look like data-entry errors: one record has sell and buy swapped and the formula gives both numbers. Full list with predictions: `sell_buy_check.json`.

**How it was found:** correlated each draw of the three per-system streams against the recorded values. The `systemAttributes()` and `systemName()` streams showed nothing (|r| < 0.09 over 60–80 draws). The `planetSeeds()` stream gave r = 0.983 (buy, draw 1) and r = 0.963 (sell, draw 2). The ranges match what players see in-game: sell +40% to +80%, buy -30% to -10%.

Example: Euclid `1058E1434753` gives sell 71.5, buy -15.7, both matching the in-game record.

## 2. Independent check against Voyager's Haven

Voyager's Haven (havenmap.online, run by u/IAmThe-Ekimo-1920) has about 36,000 player-recorded systems. Many come from the Haven Extractor, which reads values straight from the game. Ekimo says the data is free to use.

`systemAttributes()` against Haven, systems logged since the Cosmos update (about 13,000–17,000 per field):

| Field | Match |
|---|---|
| Star colour | 99.7% |
| Dominant race | 99.9% |
| Economy type | 99.8% |
| Wealth tier | 99.8% |
| Conflict level | 99.9% |
| Status (normal/uncharted/pirate/abandoned) | 97.9% |

The status gap isn't the library. Almost every "map says abandoned, Haven says normal" row is an older Haven Extractor upload: those systems carry exactly the race your draw gives before the abandoned override. Newer uploads and hand-typed entries agree.

Odyalutai (index 255) does just as well: star, race, economy, wealth and conflict all 99.3–99.9% on about 3,500 Haven systems.

## 3. Names: a scoreboard you can use

Your README leaves names out of the scoreboard, and for the wiki corpus that's the right call. Haven Extractor names are read from the game, so they work as a check:

| | Checked | Exact |
|---|---|---|
| Planet names | 90,969 | 94.1% |
| System names | 22,189 | 85.6% (96.4% counting names with a player tag added, e.g. "... Everion") |

Haven doesn't store a planet index, so a planet name counts as right if it matches any of that system's generated names. On a 6,221-name sample your Python `planetName()` gave 95.4%, and the JS port gives identical names from identical seeds.

One warning for anyone porting: with the old `ALPHASETS` tables (before GoodGuysFree's fix) planet names drop to 2.3%. Any copy made before the fix should be updated.

## Files

- `sell_buy.py`: `sellBuy(portal_code, galaxy)` for nms_namegen
- `sell_buy_check.json`: the 1,444 records, recorded vs predicted
- JS version: `sellBuy()` in github.com/elegra1965-source/nms-core (system.js)

Thanks for nms_namegen, and to GoodGuysFree for the tables fix. Happy for any of this to go into the library with credit to elegra1965.
