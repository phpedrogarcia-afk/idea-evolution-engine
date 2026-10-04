"use strict";

(() => {
  const screens = {
    input: document.getElementById("input-screen"),
    processing: document.getElementById("processing-screen"),
    result: document.getElementById("result-screen"),
  };
  const form = document.getElementById("idea-form");
  const input = document.getElementById("idea-input");
  const submitButton = document.getElementById("submit-button");
  const errorBox = document.getElementById("form-error");
  const detailList = document.getElementById("detail-list");
  const laboratoryDetails = document.getElementById("laboratory-details");
  let inFlight = false;

  const COVERAGE_COPY = {
    SOURCE_QUOTE_INVALID: "Um trecho atribuído à ideia não corresponde a uma citação literal.",
    MATERIAL_INTENT_UNTREATED: "Uma parte importante da ideia ficou sem tratamento.",
    EXPLICIT_CONSTRAINT_UNTREATED: "Uma restrição explícita ainda não está representada na forma atual.",
    INTENT_REFERENCE_INVALID: "Um caminho não está ligado a uma intenção identificada.",
    CONFLICT_FOUND: "Um item da intenção está marcado como conflito.",
    PROVISIONAL_MODIFICATION_NOT_EXPOSED: "Uma alteração provisória não foi deixada visível para revisão.",
    DEFERRED_ITEM_NOT_EXPOSED: "Um item adiado não foi deixado visível para revisão.",
    CURRENT_FORM_REFERENCE_GAP: "A forma atual está ausente ou vazia.",
    STRUCTURAL_COVERAGE_FAILURE: "A checagem estrutural encontrou uma lacuna.",
  };

  function showScreen(name) {
    Object.entries(screens).forEach(([key, screen]) => {
      screen.hidden = key !== name;
    });
  }

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function clearError() {
    errorBox.textContent = "";
    errorBox.hidden = true;
  }

  function text(value) {
    return typeof value === "string" ? value : "";
  }

  function addText(parent, tagName, value, className) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = text(value);
    parent.appendChild(element);
    return element;
  }

  function labelForAuthority(basis, gateEligible) {
    if (basis === "USER_EXPLICIT") return "Declarado por você";
    if (basis === "VALID_USER_DERIVATION") return "Derivado da sua entrada";
    if (basis === "MODEL_HYPOTHESIS" || gateEligible === false) return "Hipótese do sistema · não confirmada";
    if (basis === "BORROWED_MODEL") return "Modelo externo adaptado";
    return "";
  }

  function addDisclosure(title, id) {
    const group = document.createElement("details");
    group.className = "detail-group";
    if (id) group.id = id;
    const summary = document.createElement("summary");
    summary.textContent = title;
    group.appendChild(summary);
    const content = document.createElement("div");
    content.className = "detail-content";
    group.appendChild(content);
    detailList.appendChild(group);
    return { group, content };
  }

  function addListDisclosure(title, items, id, renderItem) {
    if (!Array.isArray(items) || items.length === 0) return null;
    const usable = items.filter((item) => typeof item === "string" ? item.trim() : Boolean(item));
    if (usable.length === 0) return null;
    const disclosure = addDisclosure(title, id);
    const list = document.createElement("ul");
    usable.forEach((item) => {
      const li = document.createElement("li");
      if (renderItem) renderItem(li, item);
      else li.textContent = text(item);
      list.appendChild(li);
    });
    disclosure.content.appendChild(list);
    return disclosure.group;
  }

  function renderIntent(artifact) {
    if (!text(artifact.human_intent).trim()) return null;
    const disclosure = addDisclosure("Leitura da intenção", "detail-intent");
    const label = labelForAuthority(artifact.intent_provenance);
    if (label) addText(disclosure.content, "span", label, "epistemic-label");
    addText(disclosure.content, "p", artifact.human_intent);
    return disclosure.group;
  }

  function renderIntentLedger(items) {
    if (!Array.isArray(items) || items.length === 0) return null;
    const usable = items.filter((item) => item && text(item.interpretation).trim());
    if (usable.length === 0) return null;
    const disclosure = addDisclosure("O que foi preservado da sua ideia", "detail-ledger");
    const list = document.createElement("ul");
    usable.forEach((item) => {
      const li = document.createElement("li");
      li.className = "ledger-item";
      const origin = text(item.origin_type);
      if (origin === "USER_EXPLICIT") {
        addText(li, "span", "Intenção ancorada em trecho explícito", "epistemic-label");
      } else if (origin === "MODEL_INTERPRETATION") {
        addText(li, "span", "Interpretação do sistema · não confirmada", "epistemic-label");
      }
      if (text(item.importance).trim()) {
        const importance = ({
          CORE_INTENT: "Intenção central",
          MATERIAL_SUBINTENT: "Intenção material",
          EXPLICIT_CONSTRAINT: "Restrição explícita",
        })[text(item.importance)] || "";
        if (importance) addText(li, "span", importance, "ledger-status");
      }
      if (text(item.source_quote).trim()) {
        addText(li, "span", "Trecho da ideia original", "ledger-field-label");
        addText(li, "blockquote", item.source_quote, "source-quote");
      }
      addText(li, "span", "Leitura registrada", "ledger-field-label");
      addText(li, "p", item.interpretation);
      if (text(item.treatment_in_current_form).trim()) {
        addText(li, "span", "Tratamento na forma atual", "ledger-field-label");
        addText(li, "p", item.treatment_in_current_form);
      }
      const status = ({
        PRESERVED: "Preservada",
        EXPANDED: "Expandida",
        PROVISIONALLY_MODIFIED: "Modificada provisoriamente",
        DEFERRED: "Adiada para revisão",
        CONFLICT_FOUND: "Conflito registrado",
      })[text(item.status)] || "";
      if (status) addText(li, "span", status, "ledger-status");
      list.appendChild(li);
    });
    disclosure.content.appendChild(list);
    return disclosure.group;
  }

  function renderCritiques(critique) {
    if (!Array.isArray(critique) || critique.length === 0) return null;
    const disclosure = addDisclosure("Críticas e pontos de atenção", "detail-critique");
    const list = document.createElement("ul");
    critique.forEach((item) => {
      if (!item || !text(item.vulnerability).trim()) return;
      const li = document.createElement("li");
      const level = ({ HIGH: "Alta", MEDIUM: "Média", LOW: "Baixa", UNCONFIRMED: "Não confirmada" })[text(item.severity).toUpperCase()] || "";
      if (level) addText(li, "span", `Severidade ${level} · `, "epistemic-label");
      const authority = labelForAuthority(item.authority_basis, item.gate_eligible);
      if (authority) addText(li, "span", `${authority}. `, "epistemic-label");
      addText(li, "span", item.vulnerability);
      if (text(item.why_it_matters).trim()) addText(li, "p", item.why_it_matters);
      if (text(item.affected_aspect).trim()) addText(li, "p", `Aspecto: ${item.affected_aspect}`, "muted-note");
      list.appendChild(li);
    });
    if (list.childElementCount === 0) return null;
    disclosure.content.appendChild(list);
    return disclosure.group;
  }

  function renderNextAction(artifact) {
    const action = text(artifact.recommended_next_action).trim();
    const target = text(artifact.recommended_next_action_target_uncertainty).trim();
    const uncertainties = Array.isArray(artifact.uncertainties) ? artifact.uncertainties : [];
    const linkedUncertainty = target && uncertainties.some((item) => text(item) === target) ? target : "";
    const section = document.getElementById("next-step-section");
    const kicker = document.getElementById("next-uncertainty-kicker");
    const uncertainty = document.getElementById("next-uncertainty");
    const title = document.getElementById("next-step-title");
    const copy = document.getElementById("next-step-copy");

    section.hidden = !action && !linkedUncertainty;
    kicker.hidden = !linkedUncertainty;
    uncertainty.hidden = !linkedUncertainty;
    uncertainty.textContent = linkedUncertainty;
    title.textContent = "Próximo passo";
    copy.textContent = action;
    copy.hidden = !action;
    section.querySelector(".muted-note").hidden = !action;
    if (!action && linkedUncertainty) {
      title.hidden = true;
    } else {
      title.hidden = false;
    }
    return section.hidden ? null : section;
  }

  function renderInsights(items) {
    const section = document.getElementById("discoveries-section");
    const list = document.getElementById("insights-list");
    list.replaceChildren();
    const usable = Array.isArray(items)
      ? items.filter((item) => item && text(item.description).trim())
      : [];
    usable.forEach((item) => {
      const card = document.createElement("article");
      card.className = "insight-card";
      const label = labelForAuthority(item.authority_basis);
      if (label) addText(card, "span", label, "epistemic-label");
      addText(card, "p", item.description, "insight-copy");
      list.appendChild(card);
    });
    section.hidden = usable.length === 0;
    return section.hidden ? null : section;
  }

  function renderCandidatePaths(items) {
    const section = document.getElementById("candidate-paths-section");
    const list = document.getElementById("candidate-paths-list");
    list.replaceChildren();
    const usable = Array.isArray(items)
      ? items.filter((item) => item && text(item.mechanism).trim())
      : [];
    usable.forEach((item) => {
      const card = document.createElement("article");
      card.className = "candidate-path-card";
      const state = ({
        CANDIDATE: "Possibilidade em aberto",
        DEFERRED: "Possibilidade adiada",
        REJECTED: "Descartada nesta análise",
      })[text(item.ontology_state)] || "Possibilidade apresentada";
      addText(card, "span", `${state} · ${labelForAuthority(item.authority_basis) || "Proposta para considerar"}`, "epistemic-label");
      addText(card, "p", item.mechanism, "candidate-mechanism");
      const tradeoffs = Array.isArray(item.tradeoffs)
        ? item.tradeoffs.filter((entry) => text(entry).trim())
        : [];
      const detailsNeeded = text(item.justification).trim() || tradeoffs.length > 0 || text(item.path_id).trim() || (Array.isArray(item.intent_ids) && item.intent_ids.length > 0);
      if (detailsNeeded) {
        const details = document.createElement("details");
        details.className = "path-details";
        addText(details, "summary", "Ver justificativa e trocas");
        const content = document.createElement("div");
        content.className = "path-detail-content";
        if (text(item.justification).trim()) {
          addText(content, "span", "Racional registrado", "ledger-field-label");
          addText(content, "p", item.justification);
        }
        if (tradeoffs.length) {
          addText(content, "span", "Trocas consideradas", "ledger-field-label");
          const tradeoffList = document.createElement("ul");
          tradeoffs.forEach((tradeoff) => addText(tradeoffList, "li", tradeoff));
          content.appendChild(tradeoffList);
        }
        const references = [];
        if (text(item.path_id).trim()) references.push(`Caminho: ${text(item.path_id)}`);
        if (Array.isArray(item.intent_ids) && item.intent_ids.length) references.push(`Intenções relacionadas: ${item.intent_ids.map(text).filter(Boolean).join(", ")}`);
        if (references.length) addText(content, "p", references.join(" · "), "muted-note");
        details.appendChild(content);
        card.appendChild(details);
      }
      list.appendChild(card);
    });
    section.hidden = usable.length === 0;
    return section.hidden ? null : section;
  }

  function renderOpenDecisions(items) {
    const section = document.getElementById("open-decisions-section");
    const list = document.getElementById("open-decisions-list");
    list.replaceChildren();
    const usable = Array.isArray(items)
      ? items.filter((item) => item && text(item.question).trim())
      : [];
    usable.forEach((item) => addText(list, "li", item.question));
    section.hidden = usable.length === 0;
    return section.hidden ? null : section;
  }

  function renderCoverage(artifact) {
    const status = text(artifact.coverage_status);
    const supportedStatuses = ["NOT_EVALUATED", "NO_BLOCKING_GAP_DETECTED", "REPAIR_REQUIRED", "UNRESOLVED"];
    if (!supportedStatuses.includes(status)) return null;

    const coverageCopy = {
      NOT_EVALUATED: "A checagem estrutural não foi realizada para este artefato.",
      NO_BLOCKING_GAP_DETECTED: "Checagem estrutural: nenhuma lacuna bloqueante detectada.",
      REPAIR_REQUIRED: "A checagem estrutural encontrou pontos que ainda precisam de tratamento.",
      UNRESOLVED: "Há um ponto estrutural não resolvido nesta maturação.",
    };
    const notice = document.getElementById("coverage-notice");
    const noticeCopy = document.getElementById("coverage-notice-copy");
    const showNotice = status === "UNRESOLVED" || status === "REPAIR_REQUIRED";
    notice.hidden = !showNotice;
    noticeCopy.textContent = showNotice ? coverageCopy[status] : "";

    const disclosure = addDisclosure("Checagem estrutural", "coverage-details");
    addText(disclosure.content, "p", coverageCopy[status], "coverage-summary-copy");
    addText(disclosure.content, "p", "Esta checagem observa relações estruturais; não comprova correção semântica.", "muted-note");
    const issues = Array.isArray(artifact.coverage_issues) ? artifact.coverage_issues.filter(Boolean) : [];
    if (issues.length) {
      const list = document.createElement("ul");
      issues.forEach((issue) => {
        const li = document.createElement("li");
        const label = COVERAGE_COPY[text(issue.issue_type)] || "A checagem estrutural registrou este ponto.";
        addText(li, "p", label, "coverage-issue-language");
        if (text(issue.description).trim()) addText(li, "p", issue.description, "muted-note");
        const references = [];
        if (text(issue.intent_id).trim()) references.push(`Intenção: ${text(issue.intent_id)}`);
        if (text(issue.path_id).trim()) references.push(`Caminho: ${text(issue.path_id)}`);
        const technicalDetails = document.createElement("details");
        technicalDetails.className = "technical-reference";
        addText(technicalDetails, "summary", "Referência técnica");
        addText(technicalDetails, "code", text(issue.issue_type));
        if (references.length) addText(technicalDetails, "p", references.join(" · "), "muted-note");
        li.appendChild(technicalDetails);
        list.appendChild(li);
      });
      disclosure.content.appendChild(list);
    }
    return disclosure.group;
  }

  function renderNextActionDetails(artifact) {
    const basis = labelForAuthority(artifact.recommended_next_action_basis);
    const status = text(artifact.recommended_next_action_status).trim();
    const support = text(artifact.recommended_next_action_support_ref).trim();
    if (!basis && !status && !support) return null;
    const disclosure = addDisclosure("Como o próximo passo foi apresentado", "detail-next-step-basis");
    if (basis) addText(disclosure.content, "p", basis, "epistemic-label");
    if (status) addText(disclosure.content, "p", `Estado registrado: ${status}`);
    if (support) addText(disclosure.content, "p", `Referência registrada: ${support}`, "muted-note");
    return disclosure.group;
  }

  function renderDeepDetails(artifact) {
    renderIntent(artifact);
    addListDisclosure("O que mudou", artifact.what_changed, "detail-changes");
    addListDisclosure("Premissas", artifact.assumptions, "detail-assumptions", (li, item) => {
      const label = labelForAuthority(artifact.assumptions_authority);
      if (label) addText(li, "span", `${label}. `, "epistemic-label");
      addText(li, "span", item);
    });
    addListDisclosure("Incertezas", artifact.uncertainties, "detail-uncertainties");
    renderCritiques(artifact.critique);
    renderIntentLedger(artifact.intent_ledger);
    renderNextActionDetails(artifact);
    renderCoverage(artifact);
  }

  function firstPresentTarget(ids) {
    return ids.find((id) => {
      const element = document.getElementById(id);
      return element && !element.hidden;
    }) || "";
  }

  function setMapAvailability(artifact) {
    const targets = {
      prima: text(artifact.original_idea).trim() ? "raw-panel" : "",
      separatio: firstPresentTarget(["detail-ledger", "detail-intent", "detail-assumptions", "detail-uncertainties"]),
      multiplicatio: firstPresentTarget(["candidate-paths-section"]),
      provacao: firstPresentTarget(["detail-critique", "detail-uncertainties", "coverage-details"]),
      transmutatio: firstPresentTarget(["refined-panel", "discoveries-section"]),
      coagulatio: firstPresentTarget(["next-step-section", "open-decisions-section", "human-decision-card"]),
    };
    document.querySelectorAll(".map-node").forEach((button) => {
      const targetId = targets[button.dataset.mapKey];
      button.disabled = !targetId;
      button.dataset.target = targetId || "";
      if (!targetId) button.setAttribute("aria-label", `${button.textContent.trim().replace(/\s+/g, " ")}: conteúdo não presente nesta execução`);
      else button.removeAttribute("aria-label");
    });
  }

  function renderResult(payload) {
    const artifact = payload && payload.artifact;
    if (!artifact || typeof artifact !== "object") {
      input.disabled = false;
      submitButton.disabled = false;
      showError("A execução terminou sem retornar uma proposta utilizável.");
      showScreen("input");
      return;
    }

    const refinedIdea = text(artifact.refined_idea);
    const needsHumanDecision = artifact.human_decision_required === true;
    if (!refinedIdea.trim() && !needsHumanDecision) {
      input.disabled = false;
      submitButton.disabled = false;
      showError("A execução terminou sem uma forma atual ou uma decisão pendente utilizável.");
      showScreen("input");
      return;
    }

    document.getElementById("raw-idea").textContent = text(artifact.original_idea);
    document.getElementById("refined-idea").textContent = refinedIdea;
    const refinedPanel = document.getElementById("refined-panel");
    refinedPanel.hidden = !refinedIdea.trim();
    document.getElementById("result-heading").textContent = refinedIdea.trim() ? "Forma Atual" : "Decisão necessária";

    const decisionCard = document.getElementById("human-decision-card");
    const decisionDescription = document.getElementById("human-decision-description");
    decisionCard.hidden = !needsHumanDecision;
    decisionDescription.textContent = text(artifact.human_decision_description);
    if (!decisionDescription.textContent.trim()) {
      decisionDescription.textContent = "O resultado indica que uma escolha humana é necessária antes de prosseguir.";
    }

    renderInsights(artifact.useful_insights);
    renderCandidatePaths(artifact.candidate_possibilities);
    renderNextAction(artifact);
    renderOpenDecisions(artifact.open_decisions);

    detailList.replaceChildren();
    document.getElementById("coverage-notice").hidden = true;
    renderDeepDetails(artifact);
    laboratoryDetails.hidden = detailList.childElementCount === 0;
    laboratoryDetails.open = false;
    const rawPanel = document.getElementById("raw-panel");
    rawPanel.open = !window.matchMedia("(max-width: 860px)").matches;
    setMapAvailability(artifact);
    showScreen("result");
    document.getElementById("result-heading").focus();
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (inFlight) return;
    clearError();
    const idea = input.value;
    if (!idea.trim()) {
      showError("Escreva uma ideia antes de transmutar.");
      input.focus();
      return;
    }

    inFlight = true;
    input.disabled = true;
    submitButton.disabled = true;
    form.setAttribute("aria-busy", "true");
    showScreen("processing");
    try {
      const response = await fetch("/api/evolve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea }),
      });
      const payload = await response.json();
      if (!response.ok || payload.success !== true) {
        showScreen("input");
        input.disabled = false;
        submitButton.disabled = false;
        showError(text(payload.error_message) || "Não foi possível concluir esta execução.");
        return;
      }
      renderResult(payload);
    } catch (_error) {
      showScreen("input");
      input.disabled = false;
      submitButton.disabled = false;
      showError("A conexão foi interrompida. O estado desta execução pode ser desconhecido; confira os registros locais antes de tentar novamente.");
    } finally {
      inFlight = false;
      form.removeAttribute("aria-busy");
      if (!screens.result.hidden) {
        input.disabled = false;
        submitButton.disabled = false;
      }
    }
  });

  input.addEventListener("input", clearError);
  document.getElementById("new-idea-button").addEventListener("click", () => {
    clearError();
    input.value = "";
    input.disabled = false;
    submitButton.disabled = false;
    showScreen("input");
    input.focus();
  });

  document.getElementById("coverage-details-link").addEventListener("click", () => {
    laboratoryDetails.open = true;
    const target = document.getElementById("coverage-details");
    if (target) {
      target.open = true;
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });

  document.querySelectorAll(".map-node").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.target && document.getElementById(button.dataset.target);
      if (!target) return;
      let details = target.closest("details");
      while (details) {
        details.open = true;
        details = details.parentElement ? details.parentElement.closest("details") : null;
      }
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
})();
