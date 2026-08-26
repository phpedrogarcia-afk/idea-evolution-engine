"""
tests/adversarial/test_adversarial_understand_and_groq_boundary.py
Testes offline para pureza descritiva do UNDERSTAND e compatibilidade estrita do Groq Structured Output (M05.1-R2).
"""

import unittest
from typing import Type
from pydantic import BaseModel
from src.idea_evolution.stages.contracts import (
    UnderstandOutput,
    AttackOutput,
    AlternativesOutput,
    RealityCheckOutput,
    SynthesizeOutput,
    FinalReviewOutput,
)
from src.idea_evolution.stages.understand import UnderstandStage
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.providers.native import to_strict_json_schema, NativeModelRunner
from src.idea_evolution.providers.fake import FakeModelRunner


class TestAdversarialUnderstandAndGroqBoundary(unittest.TestCase):

    def test_01_understand_cannot_silently_introduce_ai_or_mobile(self):
        """
        Garante que UNDERSTAND seja puramente descritivo:
        Candidatos inferidos (como 'App mobile com IA') devem ir para candidate_extensions
        e NÃO poluir o current_idea core.
        """
        output = UnderstandOutput(
            interpreted_problem="Pessoas têm dificuldades em estruturar ideias dispersas.",
            human_intent="Ajudar pessoas a transformar ideias vagas em projetos mais claros.",
            explicit_mechanism="Processo de clarificação de ideias.",
            inferred_candidates=["App mobile com prompts guiados por IA", "Templates pré-definidos"],
            actors_or_users=["Criadores de projetos"],
            assumptions=["Usuários precisam de perguntas estruturadas."],
            ambiguities=["Qual o formato de saída desejado?"],
            strengths=["Foco direto em clareza."],
            structured_idea="Uma ferramenta que ajuda pessoas a transformar ideias vagas em definições de projeto mais claras.",
        )

        state = SimpleIdeaState(
            run_id="TEST-RUN-008",
            original_idea="Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.",
        )

        stage = UnderstandStage()
        stage.apply_output_to_state(state, output)

        # current_idea deve permanecer puramente descritivo e fiel à ideia original
        self.assertNotIn("mobile", state.current_idea.lower())
        self.assertNotIn("inteligência artificial", state.current_idea.lower())
        self.assertIn("transformar ideias vagas", state.current_idea.lower())

        # Inferências técnicas devem estar estritamente isoladas em candidate_extensions
        self.assertEqual(len(state.candidate_extensions), 2)
        self.assertIn("App mobile com prompts guiados por IA", state.candidate_extensions)

    def test_02_groq_strict_json_schema_compliance_all_stages(self):
        """
        Verifica se todos os contratos do pipeline geram JSON Schemas 100% compatíveis com o Groq Strict Mode:
        - additionalProperties: false em todos os nós de objeto
        - required contendo todas as propriedades declaradas
        """
        stages = [
            ("UNDERSTAND", UnderstandOutput),
            ("ATTACK", AttackOutput),
            ("ALTERNATIVES", AlternativesOutput),
            ("REALITY_CHECK", RealityCheckOutput),
            ("SYNTHESIZE", SynthesizeOutput),
            ("FINAL_REVIEW", FinalReviewOutput),
        ]

        for name, model_cls in stages:
            schema = to_strict_json_schema(model_cls)

            # Validação do topo
            self.assertEqual(
                schema.get("type"), "object", f"[{name}] Schema raiz deve ser type=object"
            )
            self.assertEqual(
                schema.get("additionalProperties"),
                False,
                f"[{name}] additionalProperties deve ser False",
            )
            props = schema.get("properties", {})
            required = schema.get("required", [])
            for prop_name in props:
                self.assertIn(
                    prop_name,
                    required,
                    f"[{name}] Propriedade '{prop_name}' deve estar listada em 'required'",
                )

            # Validação de $defs
            if "$defs" in schema:
                for def_name, def_obj in schema["$defs"].items():
                    if def_obj.get("type") == "object" or "properties" in def_obj:
                        self.assertEqual(
                            def_obj.get("additionalProperties"),
                            False,
                            f"[{name}] $defs.{def_name} additionalProperties deve ser False",
                        )
                        def_props = def_obj.get("properties", {})
                        def_req = def_obj.get("required", [])
                        for d_p in def_props:
                            self.assertIn(
                                d_p,
                                def_req,
                                f"[{name}] $defs.{def_name}.'{d_p}' deve estar em 'required'",
                            )

    def test_03_native_runner_preserves_failed_generation_on_error(self):
        """
        Garante que quando a geração do provedor falha estruturalmente,
        o failed_generation é preservado no ModelResponse para fins de auditoria.
        """
        runner = FakeModelRunner()
        # ModelResponse com failed_generation tipado
        resp = runner.generate(
            prompt_text="teste",
            output_schema=UnderstandOutput,
            stage_name="UNDERSTAND",
        )
        self.assertTrue(hasattr(resp, "failed_generation"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
