#!/usr/bin/env python3
import json
import os

local_hardware = [
    {"id": "mac-studio-m2-ultra-192gb", "name": "Apple Mac Studio M2 Ultra (192GB)", "category": "Unified Memory Silicon", "vram_gb": 192, "bandwidth_gb_s": 800, "purchase_price": 6999, "power_watts": 130, "best_for": "Llama-3.1-70B FP16 / DeepSeek-V2 Q8 local inference with zero cloud data ingress"},
    {"id": "mac-studio-m2-max-64gb", "name": "Apple Mac Studio M2 Max (64GB)", "category": "Unified Memory Silicon", "vram_gb": 64, "bandwidth_gb_s": 400, "purchase_price": 2599, "power_watts": 90, "best_for": "Llama-3.1-70B Q4_K_M / Mistral-Large local developer testing"},
    {"id": "mac-studio-m4-max-128gb", "name": "Apple Mac Studio M4 Max (128GB)", "category": "Unified Memory Silicon", "vram_gb": 128, "bandwidth_gb_s": 546, "purchase_price": 4399, "power_watts": 110, "best_for": "70B to 120B parameter local LLM fine-tuning & continuous local agent workflows"},
    {"id": "dual-rtx-4090-workstation", "name": "Dual RTX 4090 48GB Workstation", "category": "Dedicated Local GPU Rig", "vram_gb": 48, "bandwidth_gb_s": 2016, "purchase_price": 4800, "power_watts": 900, "best_for": "High-throughput token generation for 8B-34B models and fast batch SDXL / Flux rendering"},
    {"id": "quad-rtx-4090-cluster", "name": "Quad RTX 4090 96GB Workstation", "category": "Dedicated Local GPU Rig", "vram_gb": 96, "bandwidth_gb_s": 4032, "purchase_price": 9500, "power_watts": 1800, "best_for": "Multi-GPU tensor parallelism for 70B models with maximum tokens/sec throughput"},
    {"id": "single-rtx-4090-desktop", "name": "Single RTX 4090 24GB Desktop", "category": "Dedicated Local GPU Rig", "vram_gb": 24, "bandwidth_gb_s": 1008, "purchase_price": 2200, "power_watts": 450, "best_for": "Rapid prototyping, LoRA fine-tuning for 8B models, and local vision processing"},
    {"id": "dual-rtx-3090-budget-rig", "name": "Dual RTX 3090 48GB Budget Rig", "category": "Refurbished Local GPU Rig", "vram_gb": 48, "bandwidth_gb_s": 1872, "purchase_price": 2400, "power_watts": 750, "best_for": "Budget 70B Q4 inference rig with high memory capacity per dollar"}
]

cloud_instances = [
    {"id": "aws-g5-12xlarge", "provider": "AWS EC2", "name": "AWS EC2 g5.12xlarge (4x A10G 96GB)", "vram_gb": 96, "hourly_rate": 5.672, "kwh_included": True},
    {"id": "aws-g5-xlarge", "provider": "AWS EC2", "name": "AWS EC2 g5.xlarge (1x A10G 24GB)", "vram_gb": 24, "hourly_rate": 1.006, "kwh_included": True},
    {"id": "aws-p4d-24xlarge", "provider": "AWS EC2", "name": "AWS EC2 p4d.24xlarge (8x A100 320GB)", "vram_gb": 320, "hourly_rate": 32.77, "kwh_included": True},
    {"id": "lambda-a100-80gb", "provider": "Lambda Cloud", "name": "Lambda Cloud 1x A100 SXM4 (80GB)", "vram_gb": 80, "hourly_rate": 1.29, "kwh_included": True},
    {"id": "lambda-h100-80gb", "provider": "Lambda Cloud", "name": "Lambda Cloud 1x H100 SXM5 (80GB)", "vram_gb": 80, "hourly_rate": 2.49, "kwh_included": True},
    {"id": "lambda-8x-a100-640gb", "provider": "Lambda Cloud", "name": "Lambda Cloud 8x A100 (640GB)", "vram_gb": 640, "hourly_rate": 10.32, "kwh_included": True},
    {"id": "runpod-rtx-4090", "provider": "RunPod Secure", "name": "RunPod Secure 1x RTX 4090 (24GB)", "vram_gb": 24, "hourly_rate": 0.74, "kwh_included": True},
    {"id": "runpod-2x-rtx-4090", "provider": "RunPod Secure", "name": "RunPod Secure 2x RTX 4090 (48GB)", "vram_gb": 48, "hourly_rate": 1.48, "kwh_included": True},
    {"id": "gcp-a2-highgpu-1g", "provider": "Google Cloud", "name": "GCP a2-highgpu-1g (1x A100 40GB)", "vram_gb": 40, "hourly_rate": 3.673, "kwh_included": True},
    {"id": "azure-nc24ads-a100", "provider": "Microsoft Azure", "name": "Azure NC24ads A100 v4 (1x A100 80GB)", "vram_gb": 80, "hourly_rate": 3.67, "kwh_included": True}
]

kwh_rate = 0.15
scenarios = []

for loc in local_hardware:
    for cld in cloud_instances:
        slug = f"{loc['id']}-vs-{cld['id']}"
        title = f"{loc['name']} vs {cld['name']}: Compute Economics & TCO Breakdown"
        
        active_hours_mo = 173
        power_kw = loc["power_watts"] / 1000.0
        monthly_elec_40h = (active_hours_mo * power_kw * kwh_rate) + (557 * power_kw * 0.2 * kwh_rate)
        monthly_elec_24_7 = 730 * power_kw * kwh_rate
        
        cloud_mo_40h = active_hours_mo * cld["hourly_rate"]
        cloud_mo_24_7 = 730 * cld["hourly_rate"]
        
        net_savings_40h = max(10, cloud_mo_40h - monthly_elec_40h)
        net_savings_24_7 = max(10, cloud_mo_24_7 - monthly_elec_24_7)
        
        breakeven_months_40h = round(loc["purchase_price"] / net_savings_40h, 1)
        breakeven_months_24_7 = round(loc["purchase_price"] / net_savings_24_7, 1)
        
        tco_local_1yr = loc["purchase_price"] + (monthly_elec_40h * 12)
        tco_cloud_1yr = cloud_mo_40h * 12
        one_year_delta = round(tco_cloud_1yr - tco_local_1yr, 2)
        
        scenarios.append({
            "slug": slug,
            "title": title,
            "local_hardware": loc,
            "cloud_instance": cld,
            "monthly_elec_cost_40h": round(monthly_elec_40h, 2),
            "monthly_elec_cost_24_7": round(monthly_elec_24_7, 2),
            "cloud_cost_monthly_40h": round(cloud_mo_40h, 2),
            "cloud_cost_monthly_24_7": round(cloud_mo_24_7, 2),
            "breakeven_months_40h": breakeven_months_40h,
            "breakeven_months_24_7": breakeven_months_24_7,
            "tco_local_1yr": round(tco_local_1yr, 2),
            "tco_cloud_1yr": round(tco_cloud_1yr, 2),
            "one_year_net_savings": one_year_delta,
            "verdict": f"Local hardware breaks even in {breakeven_months_24_7} months under continuous utilization ({breakeven_months_40h} months at 40h/week)."
        })

out_file = "scratch/technommy_site/src/data/compute_matrix.json"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(scenarios, f, indent=2)

print(f"✅ Successfully generated {len(scenarios)} pSEO comparison scenarios into {out_file}!")
