# Evidence: Tender on GenLayer StudioNet

Every row below was read back from the chain by `scripts/evidence.mjs`: the
sender, the status and the outcome come from the node's answer for each hash,
not from the deployment record. Every outcome on chain matches the record.

- **Contract:** [`0xFb0ead90ab52f18bDEd07CB2f2922bA7eEE58Cc0`](https://explorer-studio.genlayer.com/address/0xFb0ead90ab52f18bDEd07CB2f2922bA7eEE58Cc0)
- **Deploy transaction:** [`0xd26458cf…b5ce`](https://explorer-studio.genlayer.com/tx/0xd26458cfaf19378f256a40a4e51f3f62b2f025d08eedf2da9f1f0dd613b3b5ce)
- **Source sha256:** `d97776786fb0a9001abbae7caa0b5ab94def84541c3dfccdc888a94ecde92e9a`
- **Transactions:** 17, from 6 different wallets
- **Generated:** 2026-10-05 23:52 UTC

## Wallets

Each wallet was made in memory for this run, and its key was never written
anywhere. Click an address to see every transaction it sent.

| Role | Address | Transactions sent |
|---|---|---|
| buyer | [`0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362`](https://explorer-studio.genlayer.com/address/0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362) | 4 |
| ann | [`0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da`](https://explorer-studio.genlayer.com/address/0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da) | 4 |
| ben | [`0x0DcD016647e3f3591089F67910634Ed15e62aDa9`](https://explorer-studio.genlayer.com/address/0x0DcD016647e3f3591089F67910634Ed15e62aDa9) | 1 |
| cal | [`0x8c1FDD972FAd72B8db90CD50fdD10FdB04c3B9Fa`](https://explorer-studio.genlayer.com/address/0x8c1FDD972FAd72B8db90CD50fdD10FdB04c3B9Fa) | 2 |
| dev | [`0x9BE153941a04Cb3E111F027954EfF58C81E75322`](https://explorer-studio.genlayer.com/address/0x9BE153941a04Cb3E111F027954EfF58C81E75322) | 2 |
| stranger | [`0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c`](https://explorer-studio.genlayer.com/address/0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c) | 4 |

## Transactions, in order

"refused" is a transaction the contract was meant to refuse: the committee
agreed on the refusal, and the sentence is the contract's own.

| # | Step | Sent by | Method | On chain | Outcome | Tx |
|---|---|---|---|---|---|---|
| 0 | deploy | buyer [`0xBC3f…e362`](https://explorer-studio.genlayer.com/address/0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362) | `deploy` | FINALIZED · MAJORITY_AGREE | executed | [`0xd26458cf…b5ce`](https://explorer-studio.genlayer.com/tx/0xd26458cfaf19378f256a40a4e51f3f62b2f025d08eedf2da9f1f0dd613b3b5ce) |
| 1 | tender 0 opened: three requirements | buyer [`0xBC3f…e362`](https://explorer-studio.genlayer.com/address/0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362) | `open` | FINALIZED · MAJORITY_AGREE | executed | [`0xf39a983b…dcf0`](https://explorer-studio.genlayer.com/tx/0xf39a983ba800ac26d9db7a549f3c8414335a336464ae61ff651c2885488adcf0) |
| 2 | the buyer bids on its own tender | buyer [`0xBC3f…e362`](https://explorer-studio.genlayer.com/address/0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362) | `bid` | FINALIZED · MAJORITY_AGREE | refused: the buyer cannot bid on its own tender | [`0x255befee…7e70`](https://explorer-studio.genlayer.com/tx/0x255befeeb22cdf612d3430192a843dcb7280f64174f03db9309a74f1ceb87e70) |
| 3 | bid 0: Ann, 1180 | ann [`0xD75E…f9da`](https://explorer-studio.genlayer.com/address/0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da) | `bid` | FINALIZED · MAJORITY_AGREE | executed | [`0x319c9e60…0a77`](https://explorer-studio.genlayer.com/tx/0x319c9e60008d6c1536fb1ae77f764d8ac1b3146b1e2aab688c61d5e172ea0a77) |
| 4 | bid 1: Ben, 950, glossy virgin paper | ben [`0x0DcD…aDa9`](https://explorer-studio.genlayer.com/address/0x0DcD016647e3f3591089F67910634Ed15e62aDa9) | `bid` | FINALIZED · MAJORITY_AGREE | executed | [`0xe4462e75…ec6f`](https://explorer-studio.genlayer.com/tx/0xe4462e75d64d2b1b5b89f4c9374cd8e618e077cbe5b5c1429373a4a74889ec6f) |
| 5 | bid 2: Cal, 1240 | cal [`0x8c1F…B9Fa`](https://explorer-studio.genlayer.com/address/0x8c1FDD972FAd72B8db90CD50fdD10FdB04c3B9Fa) | `bid` | FINALIZED · MAJORITY_AGREE | executed | [`0x5fd7a6e8…fc42`](https://explorer-studio.genlayer.com/tx/0x5fd7a6e8d2cbf3a6bbe3f26311fce9223ee5803797f5944e1e10462e3bcefc42) |
| 6 | bid 3: Dev, 1090, delivery on 20 November | dev [`0x9BE1…5322`](https://explorer-studio.genlayer.com/address/0x9BE153941a04Cb3E111F027954EfF58C81E75322) | `bid` | FINALIZED · MAJORITY_AGREE | executed | [`0xb4452bdb…8858`](https://explorer-studio.genlayer.com/tx/0xb4452bdb1d4081ef8e1970c8577cbed81a679b2758c967e6beb28575198c8858) |
| 7 | Ann bids a second time | ann [`0xD75E…f9da`](https://explorer-studio.genlayer.com/address/0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da) | `bid` | FINALIZED · MAJORITY_AGREE | refused: a supplier bids once per tender | [`0x006b588e…eb65`](https://explorer-studio.genlayer.com/tx/0x006b588e0b6780d419bbb71e153357e3d278eaa3f7a8a98fa0c85a79e722eb65) |
| 8 | an assessment before bids close | ann [`0xD75E…f9da`](https://explorer-studio.genlayer.com/address/0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da) | `assess` | FINALIZED · MAJORITY_AGREE | refused: assessments open when bids close at 2026-10-05T23:39:27Z | [`0xd18ba0d1…cd31`](https://explorer-studio.genlayer.com/tx/0xd18ba0d1244f94ce71b33ebf614054729af2cb8278b92236497186ade910cd31) |
| 9 | a bid after bids closed | stranger [`0xB328…Af7c`](https://explorer-studio.genlayer.com/address/0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c) | `bid` | FINALIZED · MAJORITY_AGREE | refused: bids closed at 2026-10-05T23:39:27Z | [`0x382e946f…43c3`](https://explorer-studio.genlayer.com/tx/0x382e946ff6f19a7cdaf3603244551136d0047d254dba113251aae6e14a6143c3) |
| 10 | a stranger asks for an assessment | stranger [`0xB328…Af7c`](https://explorer-studio.genlayer.com/address/0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c) | `assess` | FINALIZED · MAJORITY_AGREE | refused: only the buyer or a bidder on this tender may ask for an assessment | [`0xaf47ef2d…dbc4`](https://explorer-studio.genlayer.com/tx/0xaf47ef2d09c4ee9384e1bd2c0eab6f9ab2ea0fb7a143fe6b893f792fc7e6dbc4) |
| 11 | bid 1 assessed: both orders | buyer [`0xBC3f…e362`](https://explorer-studio.genlayer.com/address/0xBC3fF1Ef827CeeE1189FA21569F4d5B399D1e362) | `assess` | FINALIZED · MAJORITY_AGREE | executed | [`0x1ccdeef4…de19`](https://explorer-studio.genlayer.com/tx/0x1ccdeef4247d112c29dd1bc6a21e5decb051f71337a11df6c57740543951de19) |
| 12 | bid 0 assessed: both orders | ann [`0xD75E…f9da`](https://explorer-studio.genlayer.com/address/0xD75E0Bf252aa8Cd3D6C021b9d9cFa91aaf60f9da) | `assess` | FINALIZED · MAJORITY_AGREE | executed | [`0x99608abf…3f8f`](https://explorer-studio.genlayer.com/tx/0x99608abf37446b2f333bc482f0ca1bd10556206b2925e08589673ebb39b03f8f) |
| 13 | bid 2 assessed: both orders | cal [`0x8c1F…B9Fa`](https://explorer-studio.genlayer.com/address/0x8c1FDD972FAd72B8db90CD50fdD10FdB04c3B9Fa) | `assess` | FINALIZED · MAJORITY_AGREE | executed | [`0xb8151efc…daf7`](https://explorer-studio.genlayer.com/tx/0xb8151efcc3f835ab9ddb00b0ce2f10b25719e76a8b086ca27b7571bda94fdaf7) |
| 14 | an award while bid 3 waits | stranger [`0xB328…Af7c`](https://explorer-studio.genlayer.com/address/0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c) | `award` | FINALIZED · MAJORITY_AGREE | refused: bid 3 is waiting for its assessment until 2026-10-05T23:49:27Z | [`0x5666fe33…fdc0`](https://explorer-studio.genlayer.com/tx/0x5666fe33a0083e015ad2ec1f63dc3695f38c0b471d03034f2dd33247e1cffdc0) |
| 15 | bid 3 assessed after assessments closed | dev [`0x9BE1…5322`](https://explorer-studio.genlayer.com/address/0x9BE153941a04Cb3E111F027954EfF58C81E75322) | `assess` | FINALIZED · MAJORITY_AGREE | refused: assessments closed at 2026-10-05T23:49:27Z; a bid nobody assessed is not compliant at the award | [`0xd7ab2e39…6845`](https://explorer-studio.genlayer.com/tx/0xd7ab2e39ae3ca84982285c6c71479ad03a354d0dcdc7941c95ee4109b0906845) |
| 16 | tender 0 awarded | stranger [`0xB328…Af7c`](https://explorer-studio.genlayer.com/address/0xB3286f5CEB5106eb8e69Ae97471BE2347325Af7c) | `award` | FINALIZED · MAJORITY_AGREE | executed | [`0x78ec11d7…edbd`](https://explorer-studio.genlayer.com/tx/0x78ec11d7ca0d0ef180b71611045dad1b982cd5e2c6be52f98afed1061394edbd) |
