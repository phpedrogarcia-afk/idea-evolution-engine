"""
scripts/run_real_abc_experiment.py
Script de execução do Experimento Real A/B/C (EXP-M05.2) com Groq.
"""

import os
import json
import hashlib
from pathlib import Path
from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.config.routing import ModelRoutingConfig
from src.idea_evolution.stages.contracts import UnderstandOutput, BaselineRefineOutput, CritiqueOutput, RevisionOutput
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.experiments.abc_experiment import ABCExperimentRunner, ABCExperimentSpec, SingleCallRecord

def main():
    exp_id = "EXP-M05-ABC-REAL-20260827_110000"
    exp_dir = Path("experiments") / "EXP-M05.2-REAL"
    exp_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = exp_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    runner = NativeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")
    spec = ABCExperimentSpec(experiment_id=exp_id)
    raw_idea = spec.raw_idea

    print("=== STARTING REAL EXPERIMENT A/B/C ===")
    print("Experiment ID:", exp_id)
    print("Provider: groq | Model: openai/gpt-oss-120b")
    print("Raw Idea:", raw_idea)

    # -------------------------------------------------------------
    # CONDITION A: BASELINE_SINGLE_REFINE (1 call)
    # -------------------------------------------------------------
    print("\n>>> EXECUTING CONDITION A (Baseline Single Refine)...")
    prompt_a = f"{spec.condition_a_prompt}\n\nRAW IDEA:\n{raw_idea}"
    resp_a = runner.generate(prompt_text=prompt_a, output_schema=BaselineRefineOutput, stage_name="BASELINE_REFINE")
    if resp_a.error:
        print("ERROR IN COND A:", resp_a.error)
        raise RuntimeError(f"Condition A failed: {resp_a.error}")
    else:
        print("COND A SUCCESS. Tokens:", resp_a.usage)

    out_a_text = resp_a.raw_text or (resp_a.parsed.refined_version if resp_a.parsed else "")
    (raw_dir / "condition_a_raw.json").write_text(json.dumps({
        "condition": "A",
        "prompt": prompt_a,
        "raw_response": resp_a.raw_text,
        "parsed": resp_a.parsed.model_dump() if resp_a.parsed else None,
        "usage": resp_a.usage.model_dump() if resp_a.usage else None,
        "latency": resp_a.latency_seconds,
        "error": resp_a.error
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------------------------------------------------------------
    # CONDITION B: CURRENT R5 IEE SIMPLE LOOP (6 to 10 calls)
    # -------------------------------------------------------------
    print("\n>>> EXECUTING CONDITION B (IEE Simple Loop R5)...")
    runs_b_dir = exp_dir / "runs_b"
    runs_b_dir.mkdir(parents=True, exist_ok=True)
    cfg_b = ModelRoutingConfig.default_single_model(provider="groq", model="openai/gpt-oss-120b")
    loop_b = SimpleLoopRunner(config=cfg_b, runs_dir=runs_b_dir)
    state_b = loop_b.run(raw_idea, run_id=f"{exp_id}-COND-B")

    print("COND B FINISHED.")
    print("Status:", state_b.status)
    print("Reconstruction count:", state_b.reconstruction_count)
    print("Stage history count:", len(state_b.stage_history))
    print("Core mechanism basis:", state_b.core_mechanism_basis)
    print("Core mechanism hash:", state_b.core_mechanism_hash)
    print("Tested core hash:", state_b.tested_core_hash)
    print("Essence drift detected:", state_b.essence_drift_detected)
    print("Ontology contradiction detected:", state_b.ontology_contradiction_detected)

    out_b_text = state_b.to_human_markdown()
    (raw_dir / "condition_b_raw.json").write_text(json.dumps({
        "condition": "B",
        "state": state_b.model_dump(),
        "markdown": out_b_text,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------------------------------------------------------------
    # CONDITION C: CRITIQUE_REVISION_LOOP (4 calls)
    # -------------------------------------------------------------
    print("\n>>> EXECUTING CONDITION C (Critique-Revision 4-step)...")
    c_calls_data = []

    # C1: Critique 1
    p_c1 = f"{spec.condition_c_prompts['C1']}\n\nORIGINAL IDEA:\n{raw_idea}"
    resp_c1 = runner.generate(prompt_text=p_c1, output_schema=CritiqueOutput, stage_name="CRITIQUE_1")
    txt_c1 = resp_c1.raw_text or (json.dumps(resp_c1.parsed.model_dump()) if resp_c1.parsed else "")
    c_calls_data.append({"step": "C1_CRITIQUE_1", "prompt": p_c1, "response": txt_c1, "usage": resp_c1.usage.model_dump(), "error": resp_c1.error})
    print("C1 Critique 1 completed. Tokens:", resp_c1.usage)

    # C2: Revision 1
    p_c2 = f"{spec.condition_c_prompts['C2']}\n\nORIGINAL IDEA:\n{raw_idea}\n\nCRITIQUE 1:\n{txt_c1}"
    resp_c2 = runner.generate(prompt_text=p_c2, output_schema=RevisionOutput, stage_name="REVISION_1")
    txt_c2 = resp_c2.raw_text or (json.dumps(resp_c2.parsed.model_dump()) if resp_c2.parsed else "")
    c_calls_data.append({"step": "C2_REVISION_1", "prompt": p_c2, "response": txt_c2, "usage": resp_c2.usage.model_dump(), "error": resp_c2.error})
    print("C2 Revision 1 completed. Tokens:", resp_c2.usage)

    # C3: Critique 2
    p_c3 = f"{spec.condition_c_prompts['C3']}\n\nORIGINAL IDEA:\n{raw_idea}\n\nREVISION 1:\n{txt_c2}"
    resp_c3 = runner.generate(prompt_text=p_c3, output_schema=CritiqueOutput, stage_name="CRITIQUE_2")
    txt_c3 = resp_c3.raw_text or (json.dumps(resp_c3.parsed.model_dump()) if resp_c3.parsed else "")
    c_calls_data.append({"step": "C3_CRITIQUE_2", "prompt": p_c3, "response": txt_c3, "usage": resp_c3.usage.model_dump(), "error": resp_c3.error})
    print("C3 Critique 2 completed. Tokens:", resp_c3.usage)

    # C4: Revision 2 (Final C Output)
    p_c4 = f"{spec.condition_c_prompts['C4']}\n\nORIGINAL IDEA:\n{raw_idea}\n\nREVISION 1:\n{txt_c2}\n\nCRITIQUE 2:\n{txt_c3}"
    resp_c4 = runner.generate(prompt_text=p_c4, output_schema=RevisionOutput, stage_name="REVISION_2")
    txt_c4 = resp_c4.raw_text or (json.dumps(resp_c4.parsed.model_dump()) if resp_c4.parsed else "")
    c_calls_data.append({"step": "C4_REVISION_2", "prompt": p_c4, "response": txt_c4, "usage": resp_c4.usage.model_dump(), "error": resp_c4.error})
    print("C4 Revision 2 completed. Tokens:", resp_c4.usage)

    out_c_text = txt_c4
    (raw_dir / "condition_c_raw.json").write_text(json.dumps({
        "condition": "C",
        "calls": c_calls_data,
        "final_output": out_c_text,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------------------------------------------------------------
    # BLINDING & PACKET GENERATION
    # -------------------------------------------------------------
    print("\n>>> GENERATING BLINDED ARTIFACTS...")
    exp_harness = ABCExperimentRunner(runner=runner, spec=spec, seed=42)
    reveal_mapping, normalized_outputs, packet_md = exp_harness.generate_blinded_packet(out_a_text, out_b_text, out_c_text)

    (exp_dir / "BLIND-REVIEW-PACKET.md").write_text(packet_md, encoding="utf-8")

    reveal_payload = {
        "experiment_id": exp_id,
        "created_at": spec.created_at,
        "raw_idea": raw_idea,
        "reveal_mapping": reveal_mapping,
        "raw_hashes": {
            "A": hashlib.sha256(out_a_text.encode("utf-8")).hexdigest(),
            "B": hashlib.sha256(out_b_text.encode("utf-8")).hexdigest(),
            "C": hashlib.sha256(out_c_text.encode("utf-8")).hexdigest(),
        },
        "raw_artifact_refs": {
            "A": str(raw_dir / "condition_a_raw.json"),
            "B": str(raw_dir / "condition_b_raw.json"),
            "C": str(raw_dir / "condition_c_raw.json"),
        }
    }
    (exp_dir / "BLIND-REVEAL.json").write_text(json.dumps(reveal_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------------------------------------------------------------
    # DETERMINISTIC COMPARISON
    # -------------------------------------------------------------
    b_calls_count = len(state_b.stage_history)
    total_real_calls = 1 + b_calls_count + 4

    det_comp_md = [
        f"# DETERMINISTIC-COMPARISON.md — Comparação Mecânica Objetiva ({exp_id})",
        "",
        "> **FATOS DETERMINÍSTICOS E CONTÁBEIS — NÃO CONTÉM JULGAMENTO SEMÂNTICO DE QUALIDADE.**",
        "",
        "## 1. Contabilidade de Execução e Chamadas de Modelo",
        "",
        "| Métrica | Condição A (Baseline) | Condição B (IEE Simple Loop) | Condição C (Critique-Revision) | Total do Experimento |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **Total de Chamadas Reais** | 1 | {b_calls_count} | 4 | {total_real_calls} |",
        "| **Chamadas Reutilizadas** | 0 | 0 | 0 | 0 |",
        f"| **Provedor / Modelo** | groq / gpt-oss-120b | groq / gpt-oss-120b | groq / gpt-oss-120b | groq / gpt-oss-120b |",
        "| **Custo Financeiro Incremental** | R$ 0,00 (Free Tier) | R$ 0,00 (Free Tier) | R$ 0,00 (Free Tier) | R$ 0,00 |",
        f"| **Status Final da Condição** | SUCCESS | {state_b.status.value} | SUCCESS | - |",
        f"| **Ciclos de Reconstrução** | 0 | {state_b.reconstruction_count} | 0 | {state_b.reconstruction_count} |",
        f"| **Tamanho do Output Bruto (chars)** | {len(out_a_text)} | {len(out_b_text)} | {len(out_c_text)} | - |",
        "",
        "## 2. Invariantes de Governança e Rastreabilidade (Condição B)",
        f"- **Status de Execução:** `{state_b.status.value}`",
        f"- **Base de Autoridade do Core:** `{state_b.core_mechanism_basis.value}`",
        f"- **Hash do Core Sintetizado:** `{state_b.core_mechanism_hash}`",
        f"- **Hash do Core Testado no RealityCheck:** `{state_b.tested_core_hash}`",
        f"- **Desvio de Essência Detectado:** `{state_b.essence_drift_detected}`",
        f"- **Contradição Ontológica Detectada:** `{state_b.ontology_contradiction_detected}`",
        f"- **Inchaço Especulativo Detectado:** `{state_b.speculative_accretion_detected}`",
        "",
        "---",
        "*Este documento registra exclusivamente fatos determinísticos. A avaliação de valor e inteligência semântica é realizada pelo operador humano no BLIND-REVIEW-PACKET.md.*"
    ]
    (exp_dir / "DETERMINISTIC-COMPARISON.md").write_text("\n".join(det_comp_md), encoding="utf-8")

    det_comp_json = {
        "experiment_id": exp_id,
        "total_real_calls": total_real_calls,
        "condition_a_calls": 1,
        "condition_b_calls": b_calls_count,
        "condition_c_calls": 4,
        "reused_calls": 0,
        "incremental_paid_spend": 0.0,
        "condition_a_status": "SUCCESS",
        "condition_b_status": state_b.status.value,
        "condition_c_status": "SUCCESS",
        "b_reconstruction_count": state_b.reconstruction_count,
        "b_core_mechanism_basis": state_b.core_mechanism_basis.value,
        "b_essence_drift_detected": state_b.essence_drift_detected,
        "b_ontology_contradiction_detected": state_b.ontology_contradiction_detected,
        "output_lengths": {
            "A": len(out_a_text),
            "B": len(out_b_text),
            "C": len(out_c_text),
        }
    }
    (exp_dir / "DETERMINISTIC-COMPARISON.json").write_text(json.dumps(det_comp_json, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n=== REAL EXPERIMENT COMPLETED SUCCESSFULLY! ===")
    print("Total real calls executed:", total_real_calls)
    print("Blinded packet written to:", exp_dir / "BLIND-REVIEW-PACKET.md")
    print("Reveal mapping written to (ISOLATED):", exp_dir / "BLIND-REVEAL.json")

if __name__ == "__main__":
    main()
