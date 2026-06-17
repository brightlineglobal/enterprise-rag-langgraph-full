const form = document.querySelector("#chat-form");
const questionInput = document.querySelector("#question");
const sendButton = document.querySelector("#send-button");
const messages = document.querySelector("#messages");
const template = document.querySelector("#message-template");
const statusDot = document.querySelector("#status-dot");
const statusText = document.querySelector("#status-text");

function setStatus(text, busy = false) {
  statusText.textContent = text;
  statusDot.classList.toggle("busy", busy);
  sendButton.disabled = busy;
}

function addMessage(role, content, options = {}) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role);
  if (options.error) {
    node.classList.add("error");
  }

  node.querySelector(".message-meta").textContent = role === "user" ? "You" : "Assistant";
  node.querySelector(".message-body").textContent = content;

  if (options.sources?.length) {
    const sources = document.createElement("div");
    sources.className = "sources";

    options.sources.forEach((source, index) => {
      const card = document.createElement("section");
      card.className = "source-card";

      const title = document.createElement("strong");
      title.textContent = source.source_file || `Source ${index + 1}`;

      const body = document.createElement("p");
      const score = typeof source.rerank_score === "number" ? `Score: ${source.rerank_score.toFixed(3)}` : "";
      const sourceTitle = source.title ? `${source.title}. ` : "";
      body.textContent = `${sourceTitle}${score}`;

      card.append(title, body);
      sources.append(card);
    });

    node.append(sources);
  }

  messages.append(node);
  messages.scrollTop = messages.scrollHeight;
}

function parseAccessGroups(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function autoresize() {
  questionInput.style.height = "auto";
  questionInput.style.height = `${questionInput.scrollHeight}px`;
}

questionInput.addEventListener("input", autoresize);

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (question.length < 2) {
    questionInput.focus();
    return;
  }

  const payload = {
    question,
    user_id: document.querySelector("#user-id").value.trim() || null,
    department: document.querySelector("#department").value.trim() || null,
    access_groups: parseAccessGroups(document.querySelector("#access-groups").value),
  };

  addMessage("user", question);
  questionInput.value = "";
  autoresize();
  setStatus("Thinking", true);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || `Request failed with status ${response.status}`);
    }

    const result = await response.json();
    addMessage("assistant", result.answer || "No answer returned.", {
      sources: result.sources || [],
    });
    setStatus("Ready");
  } catch (error) {
    addMessage("assistant", error.message, { error: true });
    setStatus("Request failed");
  }
});
