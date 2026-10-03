# Verified references (fetched 2026-10-03, Tsukuba-independent live checks)

## Standards / handbooks
- ECSS-Q-ST-60-15C – Radiation hardness assurance – EEE components.
- ECSS-E-ST-10-04 – Space environment.
- MIL-STD-883 TM1019 – TID; JESD57A – SEE; ASTM F1192; JEDEC JESD89 (atmospheric neutrons).
- Schwank et al. IEEE TNS 60(3) 2074–2100 (2013) – RHA foundations.
- Ladbury & Carstens IEEE TNS 68(8) 2021 – statistical TID RHA.
- Campola 2019 SEE-MAPLD – Modern Hardness Assurance.

## Environment models
- SAPPHIRE (Jiggens et al. J Space Weather 2018) – supersedes CREME96/ESP/JPL for SEP.
- Xapsos et al. IEEE TNS 2012 – near-Earth models review; Barth et al. 2003.
- NOAA SWPC GOES differential protons live: https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json (verified 2026-10-02 quiet).

## Accelerator / CERN
- Uznanski et al. – Qualification for radiation environment (HEP, CHARM 24 GeV/c p, 500 Gy/week, 1e12 HEH/cm2/week).
- Coronetti et al. – RHA Through System-Level Testing (alpha-factor, hadron vs heavy-ion gaps).
- RADNEXT WP6/WP8 (2024–2025): SEE Tester v2 CHARM Apr-2024 (150 Gy LDO death, 95% SETs→system fail); G4SEE/FLUKA SEE module; PredicSEE/ECORCE.

## Devices / 2025-2026 findings
- Zhang et al. J Phys D 2026 – proton SEU energy-angle + charge sharing FinFET.
- Pintacuda et al. EPJP 2026; Zhi et al. 2026 RPTMOS (+20% SEB); Zhang et al. 2026 1200V SiC FIB; Zhang et al. Micromachines 2026 TPA LET_eq; Ball et al. IEEE TNS 2026 unified SELC/SEB.
- Slater et al. REDW 2023 – Jetson Orin AGX SOM limit 19 krad(Si) (peripheral bottleneck).
- NSREC 2026 Data Workshop: PolarFire SoC 100 krad, ISL73849SLH, CertusPro-NX 28nm FDSOI dose-enhancement.
- Pearton et al. 2021 – SiC/GaN review (TID-hard but SEB at <50% rating).

## Mitigation / ML
- Siegle et al. Virtex-4 TMR+scrub; Liu et al. 2024 FPGA review; Chen et al. IEEE TETC 2022 – SRAM monitor + ML SPE prediction.
- Zebrev 2014 arXiv:1405.5790 – scrub non-linearity during flares.
- LLNL RadSim (github.com/llnl/radsim) – open gamma/GEANT4/MCNP framework pattern.
- NASA GSFC compendia O'Bryan et al. 2023 (TAMU/LBNL/NSRL/UCD, LETth @1e7).
