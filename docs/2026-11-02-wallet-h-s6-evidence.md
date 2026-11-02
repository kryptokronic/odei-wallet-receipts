# Wallet H (0x7027…4189): S6 Confirmed, re-documented to the agreed standard (2026-11-02)

**Framework:** v1.2.2 (§8.3 A28, §11.4 S6, §11.5 T4) · **Round:** fa7f9a3e · **Chain:** Base
**Sources (public repo, hashes in INDEX.csv):** `data/H_0x7027/` (swap ledger, all-transfers pull, launch details, first-hour buyers, deployer check) and `data/hub_0xfffc54d8/` (0xfffc transfers, 2026-04-01 → 2026-10-28). Changelog §57–§65, source ledger S093–S098.

> On-chain behaviour only. A funding link is an association, not common ownership, and no person is identified. None of the pilot's decisions are final; they change with the data, and feedback is weighed on its evidence, equally.

## Standard applied

A Confirmed S6 finding needs (1) the tx_hash of each funding link to a deployer, liquidity seed or first-hour ring, and (2) a written assessment of alternative explanations. Shared infrastructure (exchange, bridge, custodial platform, settlement hub serving unrelated users) never counts.

## 1. H is an execution wallet (A28). Holds on its own evidence.

- H received **185 WETH/ETH transfers in the window, all from 0xfffc54d82ab10adec849ae344db7517f68d88be8** (65.1313 WETH), initiated by signer 0xf883f9083b2db3f975307915c1c8014bc8f260be (184) and 0xfb601efd02f1ca0324f3d0b401d914fcbce5a7eb (1). H has no other quote source.
- **178 of H's 184 buys** spend exactly the WETH amount of a 0xfffc transfer received less than an hour before; the median gap is **4 seconds**. Buy-side total 65.1265 WETH.
  - Example: 0xfffc → H, 0.4865 WETH, tx `0xce4c36824c61f394877c042e36bd57863296c0a651ec9cddb460508dd2e791ca` (2026-05-01 15:07:11). H buys with 0.4865 WETH, tx `0x2a5f7c1f427000fb441c0957b7f1851f5a419bc11b52b28f410ac771842057b0` (15:07:15).
- **None of H's 162 sells returns WETH or ETH to H.** In 36 of them, the pool pays the proceeds straight to 0xfffc inside H's own transaction (tx_from = H). Example: tx `0x4600045daab05e3fcf4a7b18d199e25efdc5d0f2cfd355b897c99f9732e8a51d`, 0.41716836525164136 WETH from pool 0x1890…db26 to 0xfffc. The other 126 sells pay out elsewhere; the 0xfffc pull covers only its 28 largest counterparties, so they are not traceable from this receipt.

## 2. Links from 0xfffc to the launch operation

**Deployers and liquidity seeds (2 of 13 launches evidenced):**

| Launch | Deployer | 0xfffc → deployer (gas) | 0xfffc → deployer (seed) | Deploy | Liquidity add |
|---|---|---|---|---|---|
| 1, token 0x39fd…6589 | 0xf996a469417fdb2ec8cb55495a8ec7393482ea93 | 0.425 ETH, 03:50:47, `0x506f3fff5afc80ffba9c1e6e595fe9956a3f64a784199d397656b233b310ed80` (signer 0xfb60) | 5 WETH, 04:00:13, `0xe47d9a57da7f486368238bac9a204a6a6e93a059d6a0221c392a70e8e3e622ec` (signer 0xf883) | 03:51:25, `0x1bf042b590ba7f9f1fb5c680a863b93d525dfcc0bc1a558ccae8e778dd88a8b9` | 04:00:57, 5 WETH, `0x4b2a74598a492b6add4545ac129395f07c211e5f55793c7d928e664e01829594` |
| 13, token 0x4b46…6550 | 0xc2dcf43731fb7b8ef420b780d106d75cb13f34da | 0.353 ETH, 11:20:43, `0xf126f0cc98ec1a1402a3aa59a81c5093234715f616475b68e8f389c5e4455ef4` (signer 0xfb60) | 5 WETH, 11:22:51, `0xa99f3936c8e7aefece0cb8973efe1a23adb7a64dba9dfa6f4985ca17f6f83554` (signer 0xf883) | 11:21:25, `0x6e8c91d3fd4ab20b8fe183f0016a31bb9047bb8c7c3a0692ff70d1e00441d5c8` | 11:23:41, 5 WETH, `0x2561b939e202edf1062f464788549a941d79326796c0afef07ac56ef404c6827` |

Dates: launch 1 on 2026-05-03, launch 13 on 2026-09-21. In both, the gas arrives about 40 seconds before deployment and the exact 5 WETH seed about 45 seconds before the liquidity add. Launch 1's ETH row appears twice in the receipt with the same tx hash (a duplicate row, counted once).

**Pools paying into 0xfffc:** 4 of the 13 launch pools are among 0xfffc's ten inbound pools: launch 5 (0x1890…db26, 1,341 transfers, 658.08 WETH), launch 9 (0xa075…6978, 869, 458.08), launch 11 (0x46c9…1e71, 715, 365.19) and launch 13 (0x8999…5c, 625, 320.27). So launch 13's seed came from 0xfffc, and that token's pool later paid WETH back into 0xfffc.

**First-hour ring:** of the 9 wallets that bought in the launches' first hours, the 5 regulars (in 7–13 launches each) are each funded by 0xfffc about 235–246 times, all signed by 0xf883. They also send swap proceeds back into 0xfffc: 46–49 inbound transactions each, with the ring wallet as tx_from. Example: 0xfffc → ring wallet 0x6f34f44b0ad0eb9be5ab0afdda2478404550fc8d, tx `0x6b7f1100f7a244daa6bf92bc1d39969b59e6f060c3d4d197a81a513bc83f9864`. Its first-hour buy in launch 1 is tx `0xbb4b2c26c4bcb3803f4feab444b0ccb23d8cc2e73e866cfc666f08a2b9059efb`; a proceeds payment into 0xfffc is tx `0x958cf5be428ef2ef59e945fa90fbc01dfe145ae662ee2f324dea0c356921d9f0`. The other 4 ring wallets (in 1–4 launches) show no direct 0xfffc funding in this pull, and one of them (0xe639…7111) does pay proceeds into 0xfffc.

**H and the deployers:** H has no transfers with any of the 13 deployers and is not in the first-hour ring (deployer check). Its link to the operation runs only through 0xfffc.

## 3. Alternative explanations

| Explanation | Assessment |
|---|---|
| **0xfffc is shared infrastructure** (custodial trading bot, launch platform, settlement hub) and the deployers, ring and H are unrelated users | **Largely excluded, with one residual.** Contract is unverified; its owner slot holds its own deployer (0x0D21481211c4Eb31560AD3a03Bb6a02cf54b9F77). Its top five "depositors" are Uniswap V2 pairs: inflows are swap proceeds, with no end-user deposits from independent sources (S098). Outflows are driven by four signers and go to a closed set of wallets. A twin contract (0x6ccced19, near-identical bytecode, different deployer, 4 hours later) shows the same pattern. **Residual:** a closed-membership custodial service whose clients fund it off-chain or through another collector would look similar from these pulls. Nothing observed supports it, but it is not ruled out. |
| **H is an independent trader copying the launches** | **Excluded for H.** H holds no capital: every unit of quote comes from 0xfffc seconds before each buy, and no proceeds return to H. This is the A28 test, independent of who controls 0xfffc. |
| **Exchange or bridge as common funder** | **Excluded.** 0xfffc has no exchange, bridge or solver label, no public source, and no inflows from labelled infrastructure. |
| **Address poisoning or spoof transfers** | **Excluded.** The transfers are initiated by 0xfffc's signers, not by H. They match H's buy amounts to the wei and are spent within seconds. |
| **Data artifact** (bad provider USD, mislabelled rows) | **Excluded for the conclusion.** The evidence uses token amounts, timestamps and tx hashes, not USD (Surf transfer-table USD is unreliable for low-cap tokens). One duplicate row noted above. |
| **Coincidence in timing** | **Excluded.** Gas 40 seconds before deployment and an exact 5 WETH seed 45 seconds before the liquidity add, in both evidenced launches, from the same contract and signers that fund the ring and H. |

## 4. Result

- **A28 STOP (execution wallet): stands.** It rests on H's own transfers and does not depend on the S6 question.
- **S6 Confirmed: stands on the evidence for launches 1 and 13**, under the agreed standard. `lead_status = funding_lead → 0xfffc54d8 / signer 0xf883f908`. Watch decision: Drop.
- **T4 listing of 0xfffc54d8, its owner 0x0D21…9F77 and signers 0xf883 / 0x9b1c / 0x3536 / 0xfb60: stands**, with the residual noted in §3.

## 5. Open gaps and the pulls that close them

1. **Deployer links for launches 2–12.** The 0xfffc pull lists its 28 largest counterparties only; 11 deployers fall outside it. One pull settles whether 0xfffc (or its signers) funded all 13 deployers' gas and seeds.
2. **Where 126 of H's sell proceeds went.** Settled by the recipient (`to`) of each of H's 162 sells.
3. **The residual custodial-service explanation.** Weakened further if the 13 deployers' other funding is traced to 0xfffc's signers or to nothing else.

Surf prompt for 1 and 2 (owner-run, one pull; queue for the 2026-11-09 refill):

```
Base, 2026-04-01 to 2026-10-28. (1) For each address below, every ETH or WETH transfer it received, any size: tx_hash, block_time, from, amount, tx_from. (2) For every DEX swap where tx_from = 0x702733dde6f9637286a4282a7ec2784702184189 and the token bought is WETH (0x4200000000000000000000000000000000000006): tx_hash, block_time, WETH amount, and the address that received the WETH. CSV per part. No aggregation, no estimates.
0xf996a469417fdb2ec8cb55495a8ec7393482ea93
0x08c8d32057d10414710aeb3cb1e0ff652c5672b5
0x17d0d86f397baba2ea2769fcaa834246ac36280e
0xa26dc4f06f20778ec31acf06316a59c8a63149ff
0xaa4d82b33bbd19889dce293470dcc8f948399e25
0x66bd02cc4774e225a29541d6c3379a0ebb5d239b
0xf63da1284f2dd49fe15e8e72903c800872414bc9
0x599907dd2fa552e09fe04e620dcfcb5562ec55db
0x097d6d46ef1b2d3eb5acf9453979f9fe3338f3ea
0x1147f21415cf546cc471ec2abc833a18208b1a7d
0xcc28410f08fa9c151b68b978b01066e04144d2f9
0x020c3c5aad52fadb9b4d439cca028f4d49766772
0xc2dcf43731fb7b8ef420b780d106d75cb13f34da
```
