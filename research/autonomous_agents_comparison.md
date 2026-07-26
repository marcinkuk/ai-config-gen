# Porównanie Open-Source Autonomous Agents z Pętlą Zwrotną i Nauką

> **Data:** 2026-07-26
> **Cel:** Zidentyfikowanie najlepszych lokalnych, open-source'owych autonomicznych agentów AI
>   z pętlą zwrotną (feedback loop) i zdolnością nauki/dostosowania się.

---

## Kryteria Oceny

| Kryterium | Opis |
|-----------|------|
| **Lokalny** | Może działać offline/localnie z local LLM (Ollama, llama.cpp, LM Studio) |
| **Open-Source** | Pełny dostęp do kodu, permissive license (MIT, Apache-2.0) |
| **Autonomiczny** | Działa niezależnie — planuje, wykonuje, poprawia bez stałego nadzoru |
| **Pętla zwrotna** | Self-reflection, self-correction, iterative improvement |
| **Nauka/Pamięć** | Long-term memory, adaptacja do błędów, learn-from-mistakes |
| **Wspólnota** | Stars, fork count, aktywność rozwoju |

---

## Tabela Porównawcza

| Framework | ⭐ Stars | Architektura | Local LLM | Feedback Loop | Memory/Learning | Multi-Agent | License | Ostatni commit |
|-----------|----------|-------------|-----------|---------------|-----------------|-------------|---------|----------------|
| **OpenHands** | 82k | Agent SDK + MCP | ✅ Ollama/lm-studio | ✅ ReAct + self-reflection + criticism loop | ✅ AGENTS.md memory + episodic | ✅ Delegacja sub-agentów | Apache-2.0 | 2026-07-25 |
| **AutoGPT** | 186k | Platforma agentowa | ✅ Ollama/llamafile | ✅ Planning → Action → Observation → Reflection | ✅ Memory module + task history | ✅ Multiple agents | AGPL-3.0 | 2026-07-25 |
| **CrewAI** | 56k | Role-playing agents | ✅ Ollama/LiteLLM | ✅ Task delegation + quality gate + critic role | ✅ Shared memory between agents | ✅ Full crew orchestration | MIT | 2026-07-25 |
| **AutoGen** | 60k | Conversable agents | ✅ LiteLLM | ✅ Multi-agent discussion + code execution feedback | ✅ Conversation history | ✅ Nested/group chat | Apache-2.0 | 2026-04-15 |
| **smolagents** | 28k | Code-based agents | ✅ Ollama/HF Inference | ✅ Code execution + self-correction loop | ❌ Basic observation only | ❌ Single agent | Apache-2.0 | 2026-07-21 |
| **Letta** | 24k | Stateful agent | ✅ Ollama/vLLM | ✅ Inner monologue + self-reflective prompts | ✅✅ Advanced long-term memory + summarization + search | ❌ Single agent | Apache-2.0 | 2026-07-22 |
| **GPT-Pilot** | 34k | AI developer | ❌ API-dependent (OpenAI) | ✅ Build → Test → Debug → Fix loop | ✅ Project context | ✅ AI "pair programmer" | AGPL-3.0 | 2026-06-18 |
| **Roo Code** | 24k | VS Code extension | ✅ Ollama/any provider | ✅ Edit → Test → Fix cycle | ✅ Context window + project awareness | ❌ Single agent | Apache-2.0 | 2026-05-15 |
| **Qwen-Agent** | 17k | Qwen-native agent | ✅ Qwen local models | ✅ Function calling + tool use loop | ✅ RAG + code interpreter | ✅ Agent + MCP tools | Apache-2.0 | 2026-03-04 |

---

## Szczegółowa Analiza Top 5

---

### 1. OpenHands (🥇 Najlepszy wybór ogólny)

```
Repo: https://github.com/OpenHands/OpenHands
Stars: 82,094 | Forks: 10,509 | License: Apache-2.0
```

**Architektura:**
- Agent SDK written in Python z pełnym MCP (Model Context Protocol) supportem
- Modularna: `core` → agent → LLM → tools → sandbox
- Wsparcie dla dowolnego LLM przez provider interface (OpenAI, Anthropic, Ollama, LiteLLM)

**Pętla zwrotna (Feedback Loop):**
- **ReAct Pattern:** Thought → Action → Observation → iteracja
- **Self-Criticism:** Agent może krytykować własny kod przed commit
- **Test-Driven Loop:** Write code → Run tests → Fix failures → Repeat
- **User Feedback Loop:** Interaktywna sesja z human-in-the-loop

**Nauka/Pamięć:**
- `AGENTS.md` — repo-skoped memory persistent across sessions
- **Episodic Memory:** Zachowanie historii aktywności agenta
- **Skill System:** `.agents/skills/` — dynamiczne rozszerzanie capabilities

**Local LLM Support:**
- Pełne wsparcie Ollama, lm-studio, LiteLLM, custom providers
- Sandbox (Docker) izoluje execution

**Plusy:**
- Najbardziej modularny — łatwy do rozszerzania
- MCP standard — interop z dowolnymi tools
- Prowadzony przez firmę (All-Hands AI) — dobra kontynuacja
- Najlepszy balans funkcjonalności ↔ prostota

**Minusy:**
- Mniejsza społeczność niż AutoGPT
- Apache-2.0 (nie MIT) — wymaga zachowania copyright notice

---

### 2. AutoGPT (🥈 Największa społeczność)

```
Repo: https://github.com/Significant-Gravitas/AutoGPT
Stars: 185,689 | Forks: 46,070 | License: AGPL-3.0
```

**Architektura:**
- Evolved od "classic" agent do pełnej **AutoGPT Platform**
- Backend (Python/FastAPI) + Frontend (React/Next.js) + Agent Blocks
- Block-based architecture: user buduje workflow z pre-built blocks
- 826 contributorów — ogromna społeczność

**Pętla zwrotna (Feedback Loop):**
- **Planning → Act → Observe → Reflect** — klasyczny AutoGPT loop
- **Task Decomposition:** Break down → execute subtasks → verify completion
- **Self-Management:** Agent zarządza własnym stanem i progressem

**Nauka/Pamięć:**
- Memory module z PostgreSQL/SQLite backend
- Task history persistence
- Skill system w `.claude/skills/`

**Local LLM Support:**
- Ollama, llamafile (built-in), custom providers
- Docker Compose setup dla pełnego stacka

**Plusy:**
- Największa społeczność (186k stars, 826 contributors)
- Platform approach — block builder, scheduling, webhooks
- Bardzo aktywna разработка (commits daily)
- Najlepsze do "build-your-own-agent" workflow

**Minusy:**
- **AGPL-3.0** — silna viral license (problem dla commercial use)
- Dużo moving parts — kompleksowy setup (Docker + PostgreSQL + Redis + frontend)
- Platforma przesunęła się w stronę SaaS (agpt.co) — open-source jest drugorzędny

---

### 3. CrewAI (🥉 Najlepszy Multi-Agent)

```
Repo: https://github.com/crewAIInc/crewAI
Stars: 56,131 | Forks: 7,962 | License: MIT
```

**Architektura:**
- Role-based multi-agent orchestration
- 3 główne komponenty: **Agents** (role), **Tasks** (work), **Crew** (orchestration)
- Process types: Sequential, Hierarchical (manager agent), Consensus (voting)

**Pętla zwrotna (Feedback Loop):**
- **Delegation:** Manager agent deleguje → zbiera wyniki → re-deleguje
- **Quality Gate:** Dedicated "critic" agent w crewie
- **Iteration:** Task retry z feedback z innych agentów

**Nauka/Pamięć:**
- Shared memory between agents w crewie
- Knowledge injection (RAG-like)

**Local LLM Support:**
- LiteLLM integration — dowolny provider
- Ollama support przez LiteLLM

**Plusy:**
- MIT license — najbezpieczniejsza dla commercial use
- Intuicyjny API: `Agent(role=..., goal=...)`
- Natural multi-agent workflow — każdy agent ma role
- Procesy: Sequential, Hierarchical, Consensus

**Minusy:**
- Men's control over individual agent behavior (framework decides orchestration)
- Memory system mniej zaawansowany niż Letta/OpenHands
- Wymaga dobrej konfiguracji prompts dla stabilności
- Spora firma (crewAI Inc.) — enterprise pricing za advanced features

---

### 4. Letta (🏆 Najlepsza Pamięć Długoterminowa)

```
Repo: https://github.com/letta-ai/letta
Stars: 23,960 | Forks: 2,550 | License: Apache-2.0
```

**Architektura:**
- Stateful agent z **advanced memory subsystem**
- 3-warstwowy memory:
  1. **Core Memory:** Krótkie, często aktualizowane (name, personality, facts)
  2. **Archival Memory:** Długoterminowe storage z search (vector DB)
  3. **Episode Memory:** Conversation history chunks

**Pętla zwrotna (Feedback Loop):**
- **Inner Monologue:** Agent "myśli" przed każdą akcją
- **Self-Reflection:** Built-in prompts do self-evaluation
- **Memory Management Loop:** Agent decyduje co zapamiętać/usunąć/poszukać

**Nauka/Pamięć:**
- ✅✅✅ **Najlepsza memory system na rynku**
- Automatic summarization
- Vector search over archived memories
- Memory editing/forgetting — agent kontroluje własną pamięć
- Persistent across sessions

**Local LLM Support:**
- Ollama, vLLM, custom providers
- Requires embedding model for vector search (local supported)

**Plusy:**
- Najbardziej zaawansowana memory system
- Agent truly "learns" from past interactions
- Apache-2.0 license
- Good documentation

**Minusy:**
- Single agent only (no multi-agent orchestration)
- Mеньше tools niż OpenHands (nie ma sandbox/file system)
- Mniejsza społeczność (24k stars)
- Ograniczona do konwersacji + tool calling — nie full software engineering agent

---

### 5. Microsoft AutoGen (🔬 Najlepszy Research/Enterprise)

```
Repo: https://github.com/microsoft/autogen
Stars: 59,968 | Forks: 9,025 | License: Apache-2.0 (CC-BY-4.0)
```

**Architektura:**
- ConversableAgent — każdy agent może rozmawiać z każdym
- GroupChat orchestrator z speaker selection
- Two-agent chat (user proxy + assistant)
- Nested chat (agenci mają własnych sub-agentów)

**Pętla zwrotna (Feedback Loop):**
- **Multi-Agent Discussion:** Agents debate → converge on solution
- **Code Execution Feedback:** Execute code → report result → fix
- **Termination Protocol:** Configurable stop conditions

**Nauka/Pamięć:**
- Conversation history as memory
- Less advanced than Letta/OpenHands

**Local LLM Support:**
- LiteLLM provider — Ollama, local models
- Research-oriented — mniej production-ready

**Plusy:**
- Microsoft-backed — enterprise-grade
- Flexible agent-to-agent conversation patterns
- Apache-2.0 license
- Well-researched (papers, academic backing)

**Minusy:**
- Mniej aktywna разработка (ostatni commit: 2026-04-15 — 3 miesiące temu)
- API mniej intuicyjne niż CrewAI
- Mniej "agentic" w sensie autonomous execution
- Research-focused — mniej production-ready out of the box

---

## Ranking wg Przykładu Użycia

### 🏭 Wbudowanie do własnego produktu
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **OpenHands** | MCP standard, modular SDK, Apache-2.0 |
| 2 | **CrewAI** | MIT license, intuitive API |
| 3 | **smolagents** | Minimalistyczny, Apache-2.0 |

### 🧠 Agent z długą pamięcią i nauką
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **Letta** | 3-warstwowy memory + automatic summarization |
| 2 | **OpenHands** | AGENTS.md + episodic memory |
| 3 | **AutoGPT** | Memory module + task history |

### 👥 Multi-Agent Team
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **CrewAI** | Role-based orchestration, processes |
| 2 | **AutoGen** | Conversable agents, nested chat |
| 3 | **OpenHands** | Sub-agent delegation |

### 💻 Full-Stack Development Agent
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **OpenHands** | Sandbox + browser + file system + git |
| 2 | **GPT-Pilot** | Build → test → debug loop |
| 3 | **Roo Code** | VS Code integration |

---

## Rekomendacja

### Dla Twojego przypadku: **OpenHands + Letta**

| Poziom | Narzędzie | Rola |
|--------|-----------|------|
| **Primary** | **OpenHands** | Główny autonomiczny agent: planowanie, execution, feedback loop |
| **Memory** | **Letta** | Long-term memory subsystem (może być zintegrowany jako tool) |
| **Multi-Agent** | **CrewAI** (opcjonalnie) | Jeśli potrzebujesz multi-agent orchestration |

**Dlaczego OpenHands jako primary:**
1. ✅ Local LLM support (Ollama/lm-studio)
2. ✅ Pętla zwrotna: ReAct + self-criticism + test loop
3. ✅ Memory: AGENTS.md system (persistent repo memory)
4. ✅ Sandbox: Docker-based isolated execution
5. ✅ MCP standard: Interoperability z dowolnymi tools/agentami
6. ✅ Apache-2.0 license
7. ✅ Aktywna разработка (daily commits)
8. ✅ 82k stars — duża społeczność

**Alternatywa: AutoGPT platform** jeśli zależy Ci na:
- Największej społeczności (186k stars)
- Visual block-based agent builder
- Scheduling/webhooks automation

---

## Szybki Start — OpenHands z Local LLM

```bash
# 1. Zainstaluj Ollama z modelem lokalnym
ollama pull qwen2.5-coder:32b

# 2. Sklonuj OpenHands
git clone https://github.com/OpenHands/OpenHands.git
cd OpenHands

# 3. Uruchom z local LLM
LITELLM_API_BASE=http://localhost:11434 \
LITELLM_MODEL=ollama/qwen2.5-coder:32b \
python -m openhands.server.listen
```

**Wymagania sprzętowe:**
- Minimum: 16GB RAM (7B model)
- Rekomendowane: 64GB RAM + GPU (32B model)
- Docker dla sandbox isolation

---

## Źródła

| Framework | URL |
|-----------|-----|
| OpenHands | https://github.com/OpenHands/OpenHands |
| AutoGPT | https://github.com/Significant-Gravitas/AutoGPT |
| CrewAI | https://github.com/crewAIInc/crewAI |
| AutoGen | https://github.com/microsoft/autogen |
| smolagents | https://github.com/huggingface/smolagents |
| Letta | https://github.com/letta-ai/letta |
| GPT-Pilot | https://github.com/pythagora-io/gpt-pilot |
| Roo Code | https://github.com/RooVetGit/Roo-Code |
| Qwen-Agent | https://github.com/qwenlm/Qwen-Agent |