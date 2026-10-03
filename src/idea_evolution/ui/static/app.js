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
    disclosure.content.appendChild(list);
    return disclosure.group;
  }

  function renderPossibilities(items) {
    if (!Array.isArray(items) || items.length === 0) return null;
    const usable = items.filter((item) => item && text(item.mechanism).trim());
    if (usable.length === 0) return null;
    const disclosure = addDisclosure("Possibilidades", "detail-possibilities");
    const list = document.createElement("ul");
    usable.forEach((item) => {
      const li = document.createElement("li");
      const state = text(item.ontology_state);
      const stateLabel = state === "REJECTED" ? "Descartada nesta análise" : "Possibilidade em aberto";
      addText(li, "span", `${stateLabel} · Hipótese do sistema. `, "epistemic-label");
      addText(li, "span", item.mechanism);
      if (text(item.justification).trim()) addText(li, "p", item.justification);
      if (Array.isArray(item.tradeoffs) && item.tradeoffs.length) {
        const tradeoffs = item.tradeoffs.filter((entry) => typeof entry === "string" && entry.trim());
        if (tradeoffs.length) addText(li, "p", `Compensações: ${tradeoffs.join("; ")}`, "muted-note");
      }
      list.appendChild(li);
    });
    disclosure.content.appendChild(list);
    return disclosure.group;
  }

  function renderNextAction(artifact) {
    if (!text(artifact.recommended_next_action).trim()) return null;
    const disclosure = addDisclosure("Próximo passo recomendado", "detail-next-step");
    addText(disclosure.content, "p", artifact.recommended_next_action);
    addText(disclosure.content, "p", "Uma recomendação para sua avaliação — não é autorização de implementação.", "muted-note");
    return disclosure.group;
  }

  function setMapAvailability(artifact) {
    const firstAvailable = (...ids) => ids.find((id) => document.getElementById(id));
    const targets = {
      prima: "raw-panel",
      separatio: firstAvailable("detail-intent", "detail-assumptions", "detail-uncertainties"),
      multiplicatio: "detail-possibilities",
      provacao: firstAvailable("detail-critique", "detail-uncertainties"),
      transmutatio: "refined-panel",
      coagulatio: firstAvailable("detail-next-step", artifact.human_decision_required ? "human-decision-card" : ""),
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
      showError("A execução terminou sem retornar uma proposta utilizável.");
      showScreen("input");
      return;
    }

    document.getElementById("raw-idea").textContent = text(artifact.original_idea);
    document.getElementById("refined-idea").textContent = text(artifact.refined_idea);
    detailList.replaceChildren();

    renderIntent(artifact);
    addListDisclosure("O que mudou", artifact.what_changed, "detail-changes");
    addListDisclosure("Premissas", artifact.assumptions, "detail-assumptions", (li, item) => {
      const label = labelForAuthority(artifact.assumptions_authority);
      if (label) addText(li, "span", `${label}. `, "epistemic-label");
      addText(li, "span", item);
    });
    addListDisclosure("Incertezas", artifact.uncertainties, "detail-uncertainties");
    renderPossibilities(artifact.candidate_possibilities);
    renderCritiques(artifact.critique);
    renderNextAction(artifact);

    const decisionCard = document.getElementById("human-decision-card");
    const decisionDescription = document.getElementById("human-decision-description");
    const needsHumanDecision = artifact.human_decision_required === true;
    decisionCard.hidden = !needsHumanDecision;
    decisionDescription.textContent = text(artifact.human_decision_description);
    if (!decisionDescription.textContent.trim()) {
      decisionDescription.textContent = "O resultado indica que uma escolha humana é necessária antes de prosseguir.";
    }

    setMapAvailability(artifact);
    laboratoryDetails.open = false;
    laboratoryDetails.hidden = detailList.childElementCount === 0;
    showScreen("result");
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

  document.querySelectorAll(".map-node").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.target && document.getElementById(button.dataset.target);
      if (!target) return;
      const parentDetails = target.closest("details");
      if (parentDetails) parentDetails.open = true;
      if (target instanceof HTMLDetailsElement) target.open = true;
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
})();
