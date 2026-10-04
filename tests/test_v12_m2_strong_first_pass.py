"""M2 receiver regressions; the Fiobase input is a known case, not a blind set."""

import pytest

from src.idea_evolution.artifacts.evolution_artifact import (
    CoverageStatus,
    EvolutionArtifact,
    IntentOriginType,
    SCHEMA_VERSION_1_1,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.domain.early_epistemic_gate import LeanFirstPassOutput
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner


# Exact input from the observed RUN-UI-abcfbc3b3e744bb186e47e9c37028e8d input.json.
# The test checks representation/failure classes, not a preferred answer.
FIOBASE_IDEA = (
    "projeto inteligência Fiobase, como começar um projeto. a base perfeita para vibe coding, a organização perfeita, como grandes desenvolvedores trabalham, fazer a ia trabalhar com eficiência e inteligência. agressivamente e sem conservadorimos bobos.\n"
    "pegar atalhos inteligentes, scars, tentar perceber o melhor caminho e quando mudar, checar atualizações se isso for conveniente para o projeto no intuito de  continuar com o plano ou alterar algo, tentar diminuir o tempo de progresso ou seja deixar o projeto pro mais rápido usando inteligência sem perder qualidade\n\n"
    "esse projeto fiobase vai, criar todo o alicerce na pasta que o principal vai usar e organizar da melhor forma possível.\n"
    "lembre-se que vamos fazer vibe coding, então isso é importante. vamos usar ia o tempo inteiro para criar e desenvolver o que quer que seja\n\n"
    "quando eu for criar um novo projeto eu executo primeiro essa base e ai sim começo de verdade. é como ter uma base e estrutura, alicerces prontos no terreno assim que eu chamar o fiobase. essa inteligência vem dos projetos que ja criei, scars e tudo que ja passei para criar projetos. tentar diminuir a dificuldade. vamos usar a inteligência dos projetos fioos,fioideias,fiofilter,fiohandoff como referencias, de tudo que passei do tempo investido em achar o melhor caminho, de orientações que conseguimos chegar na melhor forma, de instruções que tive que dar, dos erros que cometi, de regras que achei melhor e coisas que tirei também.\n\n"
    "talvez possa ser so uma skill, exemplo faca a base do meu projeto, use o fiobase como estrutura"
)

CORE_QUOTE = "criar todo o alicerce na pasta que o principal vai usar e organizar da melhor forma possível."
SCARS_QUOTE = "scars e tudo que ja passei para criar projetos."
REUSE_QUOTE = "vamos usar a inteligência dos projetos fioos,fioideias,fiofilter,fiohandoff como referencias"
PIVOT_QUOTE = "tentar perceber o melhor caminho e quando mudar"
AI_ASSIST_QUOTE = "vamos usar ia o tempo inteiro para criar e desenvolver o que quer que seja"
STARTUP_QUOTE = "quando eu for criar um novo projeto eu executo primeiro essa base e ai sim começo de verdade."
DECISIONS_QUOTE = "de regras que achei melhor e coisas que tirei também."


def fiobase_response():
    intent_ledger = [
        {
            "intent_id": "I-CORE",
            "source_quote": CORE_QUOTE,
            "interpretation": "Preparar uma base reutilizável no local do novo projeto antes de começar o trabalho específico.",
            "importance": "CORE_INTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "A base é executada primeiro no diretório do projeto e permanece subordinada ao projeto iniciado.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-SCARS",
            "source_quote": SCARS_QUOTE,
            "interpretation": "Reaproveitar lições, erros e cicatrizes de projetos anteriores.",
            "importance": "MATERIAL_SUBINTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "A síntese prevê um mecanismo consultivo de reaproveitamento, sem congelar uma arquitetura.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-CONTEXT",
            "source_quote": REUSE_QUOTE,
            "interpretation": "Consultar contexto relevante de projetos anteriores nomeados pelo usuário.",
            "importance": "MATERIAL_SUBINTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "O reuso contextual aparece como capacidade do conceito, não como acesso já implementado.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-PIVOT",
            "source_quote": PIVOT_QUOTE,
            "interpretation": "Permitir continuar ou mudar o caminho quando a experiência indicar uma direção melhor.",
            "importance": "MATERIAL_SUBINTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "A base deve apoiar revisão de rumo, não impor um plano imutável.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-AI",
            "source_quote": AI_ASSIST_QUOTE,
            "interpretation": "Usar IA como apoio recorrente no desenvolvimento com eficiência sem perder qualidade.",
            "importance": "MATERIAL_SUBINTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "A IA é descrita como apoio contínuo, sem autoridade para decidir pelo criador.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-DECISIONS",
            "source_quote": DECISIONS_QUOTE,
            "interpretation": "Reaproveitar tanto decisões adotadas quanto alternativas descartadas.",
            "importance": "MATERIAL_SUBINTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "O conceito distingue decisões mantidas de decisões rejeitadas e preserva a razão quando disponível.",
            "status": "PRESERVED",
        },
        {
            "intent_id": "I-STARTUP",
            "source_quote": STARTUP_QUOTE,
            "interpretation": "A base deve poder ser chamada no início de cada novo projeto.",
            "importance": "EXPLICIT_CONSTRAINT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "O uso inicial é mantido, sem fixar se a interface será skill, comando ou template.",
            "status": "PRESERVED",
        },
    ]
    return {
        "interpreted_problem": "O aprendizado acumulado em projetos anteriores não chega de forma consistente ao início de um novo projeto.",
        "human_intent": "Criar uma base reutilizável para começar projetos com menos dificuldade e preservar o aprendizado anterior.",
        "current_form": (
            "Fiobase é um conceito de preparação reutilizável para novos projetos: reúne orientações e aprendizados anteriores, "
            "ajuda a organizar o terreno inicial e continua revisável conforme surgem evidências e novas direções. "
            "Skill, scaffold e outros mecanismos continuam propostas a comparar, não decisões já tomadas."
        ),
        "intent_ledger": intent_ledger,
        "primary_mechanism": {
            "intent_ids": ["I-CORE", "I-SCARS", "I-CONTEXT", "I-PIVOT", "I-AI", "I-DECISIONS", "I-STARTUP"],
            "mechanism": "Uma skill reutilizável invocada no início do projeto que consulta lições e prepara uma orientação contextual.",
            "is_explicit_in_source": False,
            "claimed_basis": "MODEL_HYPOTHESIS",
            "justification": "É compatível com a possibilidade mencionada na ideia e pode manter a base consultiva.",
            "tradeoffs": ["Depende de um fluxo de invocação e de como contexto anterior será disponibilizado."],
        },
        "competing_alternatives": [
            {
                "intent_ids": ["I-CORE", "I-SCARS", "I-STARTUP"],
                "mechanism": "Um bootstrap que cria uma estrutura inicial no diretório do projeto e aponta para decisões e lições reutilizáveis.",
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Torna visível o terreno inicial sem exigir que uma skill seja o único formato possível.",
                "tradeoffs": ["Pode gerar estrutura fixa demais e duplicar conhecimento entre projetos."],
            }
        ],
        "key_assumptions": ["O criador pode fornecer ou autorizar referências aos aprendizados anteriores relevantes."],
        "material_ambiguities": ["Como manter referências úteis sem transformar a base inicial em estrutura rígida?"],
        "remaining_uncertainties": [
            "Qual mecanismo inicial preserva melhor reuso contextual e capacidade de mudar de direção sem impor uma estrutura fixa?"
        ],
        "useful_insights": [
            "A base pode tratar decisões adotadas, decisões rejeitadas e cicatrizes como fontes distintas de aprendizado reutilizável; nenhuma delas precisa ser convertida em regra universal."
        ],
        "open_decisions": [
            "O primeiro formato deve ser uma skill invocável, um scaffold gerado, ou uma combinação incremental?"
        ],
        "proposed_next_action": "Comparar skill e scaffold pelo modo como reaproveitam cicatrizes e decisões sem fixar antecipadamente a estrutura dos projetos.",
        "proposed_next_action_target_uncertainty": "Qual mecanismo inicial preserva melhor reuso contextual e capacidade de mudar de direção sem impor uma estrutura fixa?",
        "action_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "uncertainty_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "normative_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "idea_stage": "DISCOVERY",
        "idea_stage_justification": "O mecanismo e a forma ainda são abertos.",
        "requires_human_normative_choice": False,
        "human_choice_description": "",
        "falsification_criteria": [],
        "engineering_requirements": [],
    }


def narrow_response():
    source = "Converter um arquivo CSV para JSON preservando os cabeçalhos das colunas."
    return source, {
        "interpreted_problem": "Converter dados tabulares sem perder seus nomes de coluna.",
        "human_intent": "Converter o arquivo CSV para JSON e preservar cabeçalhos.",
        "current_form": "Um conversor que lê as colunas do CSV e produz objetos JSON mantendo os mesmos cabeçalhos.",
        "intent_ledger": [{
            "intent_id": "I-CSV",
            "source_quote": source,
            "interpretation": "Converter CSV em JSON preservando os cabeçalhos.",
            "importance": "CORE_INTENT",
            "origin_type": "USER_EXPLICIT",
            "treatment_in_current_form": "A conversão e a preservação dos cabeçalhos aparecem na síntese.",
            "status": "PRESERVED",
        }],
        "primary_mechanism": {
            "intent_ids": ["I-CSV"],
            "mechanism": "Ler a primeira linha como cabeçalhos e mapear cada linha aos pares cabeçalho/valor.",
            "claimed_basis": "MODEL_HYPOTHESIS",
            "justification": "Representa diretamente a conversão especificada.",
            "tradeoffs": [],
        },
        "competing_alternatives": [],
        "key_assumptions": [],
        "material_ambiguities": [],
        "remaining_uncertainties": [],
        "useful_insights": [],
        "open_decisions": [],
        "proposed_next_action": "Testar a conversão com um arquivo representativo que contenha cabeçalhos e valores.",
        "proposed_next_action_target_uncertainty": "",
        "action_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "uncertainty_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "normative_authority": {"basis": "MODEL_HYPOTHESIS", "support_ref": "", "derivation": ""},
        "idea_stage": "DISCOVERY",
        "idea_stage_justification": "O escopo da transformação está delimitado.",
        "requires_human_normative_choice": False,
        "human_choice_description": "",
        "falsification_criteria": [],
        "engineering_requirements": [],
    }


def run_first_pass(idea, response, tmp_path):
    runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": response})
    lean_result = LeanLoopRunner(runner, runs_dir=tmp_path / "runs").run(idea, run_id="RUN-M2-TEST")
    artifact = EvolutionArtifactMapper.map_lean_result(lean_result, original_idea=idea)
    return runner, lean_result, artifact


def test_strong_first_pass_prompt_replaces_minimal_contract_and_keeps_existing_gates():
    prompt = LeanLoopRunner._build_first_pass_prompt("Converter CSV em JSON preservando cabeçalhos.")

    assert "estruturação mínima" not in prompt
    assert "MATURAÇÃO NÃO É REESCRITA" in prompt
    assert "NÃO É RESUMO" in prompt
    assert "OPEN ou NARROW" in prompt
    assert "Não force exatamente três alternativas" in prompt
    assert "current_form" in prompt
    assert "intent_ledger" in prompt
    assert "MODEL_HYPOTHESIS" in prompt
    assert "HUMAN_DECISION_REQUIRED" in prompt
    assert "coverage_status=NOT_EVALUATED" in prompt

    schema = LeanFirstPassOutput.model_json_schema()
    assert {"current_form", "intent_ledger", "useful_insights", "open_decisions"}.issubset(schema["required"])
    mechanism = next(value for value in schema["$defs"].values() if "mechanism" in value.get("properties", {}))
    assert "intent_ids" in mechanism["required"]
    assert "path_id" not in mechanism["properties"]


def test_fiobase_real_case_can_represent_material_intents_and_open_candidate_paths(tmp_path):
    runner, lean_result, artifact = run_first_pass(FIOBASE_IDEA, fiobase_response(), tmp_path)

    assert lean_result.terminal_status != "FIRST_PASS_FAILED"
    assert runner.call_counts["LEAN_FIRST_PASS"] == 1
    assert len(artifact.intent_ledger) >= 5
    assert {item.intent_id for item in artifact.intent_ledger} >= {
        "I-CORE", "I-SCARS", "I-CONTEXT", "I-PIVOT", "I-AI", "I-DECISIONS", "I-STARTUP"
    }
    assert all(item.source_quote in FIOBASE_IDEA for item in artifact.intent_ledger if item.origin_type == IntentOriginType.USER_EXPLICIT)
    assert len(artifact.candidate_possibilities) >= 2
    assert all(item.authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS for item in artifact.candidate_possibilities)
    assert {item.path_id for item in artifact.candidate_possibilities} == {"PATH-001", "PATH-002"}
    assert artifact.useful_insights[0].insight_id == "INSIGHT-001"
    assert artifact.useful_insights[0].related_intent_ids == []
    assert artifact.open_decisions[0].decision_id == "DECISION-001"
    assert artifact.refined_idea == fiobase_response()["current_form"]
    assert artifact.refined_idea != fiobase_response()["primary_mechanism"]["mechanism"]
    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED
    assert artifact.schema_version == SCHEMA_VERSION_1_1


def test_narrow_idea_allows_one_path_and_empty_optional_insights(tmp_path):
    idea, response = narrow_response()
    _, lean_result, artifact = run_first_pass(idea, response, tmp_path)

    assert lean_result.terminal_status != "FIRST_PASS_FAILED"
    assert len(artifact.candidate_possibilities) == 1
    assert artifact.useful_insights == []
    assert artifact.open_decisions == []
    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED


def test_open_decisions_and_insights_map_without_promoting_authority_or_human_decision(tmp_path):
    _, lean_result, artifact = run_first_pass(FIOBASE_IDEA, fiobase_response(), tmp_path)

    assert artifact.open_decisions
    assert artifact.human_decision_required is False
    assert all(item.authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS for item in artifact.useful_insights)
    assert artifact.intent_provenance == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert artifact.refined_idea_authority == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert lean_result.human_decision_requested is False


def test_current_form_is_explicitly_mapped_separately_from_primary_candidate(tmp_path):
    response = fiobase_response()
    current_form = response["current_form"]
    candidate = response["primary_mechanism"]["mechanism"]

    _, _, artifact = run_first_pass(FIOBASE_IDEA, response, tmp_path)

    assert artifact.refined_idea == current_form
    assert artifact.refined_idea != candidate
    assert any(item.mechanism == candidate for item in artifact.candidate_possibilities)


def test_next_action_uncertainty_link_is_mapped_when_action_survives_arbitration(tmp_path):
    response = fiobase_response()
    _, _, artifact = run_first_pass(FIOBASE_IDEA, response, tmp_path)

    if artifact.recommended_next_action == response["proposed_next_action"]:
        assert artifact.recommended_next_action_target_uncertainty == response["proposed_next_action_target_uncertainty"]
        assert artifact.recommended_next_action_target_uncertainty in artifact.uncertainties
    else:
        assert artifact.recommended_next_action_target_uncertainty is None


@pytest.mark.parametrize(
    ("mutation", "expected_error"),
    [
        ("fabricated_quote", "source_quote"),
        ("duplicate_intent", "intent_id duplicado"),
        ("unknown_intent_ref", "intent_id desconhecido"),
        ("missing_path_intent", "referenciar ao menos um intent_id"),
        ("invalid_importance", "enum M1/M2 inválido"),
    ],
)
def test_invalid_m2_output_fails_closed_without_retry_or_silent_repair(mutation, expected_error, tmp_path):
    response = fiobase_response()
    if mutation == "fabricated_quote":
        response["intent_ledger"][0]["source_quote"] = "uma frase que não está na ideia"
    elif mutation == "duplicate_intent":
        response["intent_ledger"][1]["intent_id"] = response["intent_ledger"][0]["intent_id"]
    elif mutation == "unknown_intent_ref":
        response["primary_mechanism"]["intent_ids"] = ["I-UNKNOWN"]
    elif mutation == "missing_path_intent":
        response["primary_mechanism"]["intent_ids"] = []
    elif mutation == "invalid_importance":
        response["intent_ledger"][0]["importance"] = "USER_AUTHORITY"

    runner, lean_result, artifact = run_first_pass(FIOBASE_IDEA, response, tmp_path)

    assert lean_result.terminal_status == "FIRST_PASS_FAILED"
    assert lean_result.first_pass is None
    assert lean_result.total_model_calls == 1
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1}
    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED
    assert expected_error in lean_result.final_markdown


def test_model_interpretations_and_external_insights_remain_hypotheses(tmp_path):
    response = fiobase_response()
    response["intent_ledger"].append({
        "intent_id": "I-INTERPRETATION",
        "source_quote": "",
        "interpretation": "Projetos talvez precisem de um formato comum de registro.",
        "importance": "MATERIAL_SUBINTENT",
        "origin_type": "MODEL_INTERPRETATION",
        "treatment_in_current_form": "Permanece hipótese não assumida como requisito.",
        "status": "DEFERRED",
    })
    response["useful_insights"][0] = "Uma afirmação externa ainda não verificada sugere um registro comum."

    _, _, artifact = run_first_pass(FIOBASE_IDEA, response, tmp_path)

    interpreted = next(item for item in artifact.intent_ledger if item.intent_id == "I-INTERPRETATION")
    assert interpreted.origin_type == IntentOriginType.MODEL_INTERPRETATION
    assert artifact.useful_insights[0].authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert artifact.intent_provenance == PromotionAuthorityBasis.MODEL_HYPOTHESIS


def test_model_numeric_next_step_is_qualified_not_promoted_to_fact(tmp_path):
    response = fiobase_response()
    response["proposed_next_action"] = "Validar em 14 dias e confirmar que a adoção aumentou 30%."
    response["proposed_next_action_target_uncertainty"] = response["remaining_uncertainties"][0]

    runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": response})
    result = LeanLoopRunner(runner, runs_dir=tmp_path / "runs").run(FIOBASE_IDEA, run_id="RUN-M2-NUMERIC")

    assert result.first_pass is not None
    assert "PROVISIONAL_HEURISTIC" in result.first_pass.proposed_next_action
    assert runner.call_counts["LEAN_FIRST_PASS"] == 1


def test_m2_keeps_coverage_not_evaluated_and_does_not_add_model_calls(tmp_path):
    runner, lean_result, artifact = run_first_pass(FIOBASE_IDEA, fiobase_response(), tmp_path)

    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED
    assert artifact.coverage_issues == []
    assert runner.call_counts.get("LEAN_FIRST_PASS", 0) == 1
    assert sum(runner.call_counts.values()) <= 2
    assert lean_result.total_model_calls == sum(runner.call_counts.values())


def test_schema_1_1_serialization_round_trips_mapped_maturation(tmp_path):
    _, _, artifact = run_first_pass(FIOBASE_IDEA, fiobase_response(), tmp_path)
    serialized = artifact.model_dump_json()
    loaded = EvolutionArtifact.model_validate_json(serialized)

    assert loaded.schema_version == "1.1"
    assert loaded.intent_ledger == artifact.intent_ledger
    assert loaded.candidate_possibilities == artifact.candidate_possibilities
    assert loaded.useful_insights == artifact.useful_insights
    assert loaded.open_decisions == artifact.open_decisions
    assert loaded.coverage_status == CoverageStatus.NOT_EVALUATED
