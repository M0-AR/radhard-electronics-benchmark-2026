#!/bin/bash
set -e
export PYTHONPATH=src:$PYTHONPATH
mkdir -p results data/live
echo "=== EXP01 ==="; python3 experiments/exp01_environment_live_goes.py
echo "=== EXP02 ==="; python3 experiments/exp02_weibull_seu_benchmark.py
echo "=== EXP03 ==="; python3 experiments/exp03_tid_sic_soa.py
echo "=== EXP04 ==="; python3 experiments/exp04_mitigation_tmr_ecc.py
echo "=== EXP05 ==="; python3 experiments/exp05_cots_rha_trade.py
echo "=== TESTS ==="; python3 -m pytest tests -q
echo "ALL DONE. See results/"
ls -lh results/
