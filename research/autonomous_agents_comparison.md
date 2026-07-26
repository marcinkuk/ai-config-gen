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
| **Continuous Run** | Może działać miesiącami jako background process (nie tylko single conversation) |
| **Visual/No-Code** | Możliwość budowy workflow bez programowania (dla non-developerów) |

---

## Tabela Porównawcza

| Framework | ⭐ Stars | Architektura | Local LLM | Feedback Loop | Memory/Learning | Multi-Agent | License | Continuous Run | Visual/No-Code | Ostatni commit |
|-----------|----------|-------------|-----------|---------------|-----------------|-------------|---------|----------------|----------------|----------------|
| **OpenHands** | 82k | Agent SDK + MCP | ✅ Ollama/lm-studio | ✅ ReAct + self-reflection + criticism loop | ✅ AGENTS.md memory + episodic | ✅ Delegacja sub-agentów | Apache-2.0 | ⚠️ Session-bound | ❌ Code only | 2026-07-25 |
| **AutoGPT** | 186k | Platforma agentowa | ✅ Ollama/llamafile | ✅ Planning → Action → Observation → Reflection | ✅ Memory module + task history | ✅ Multiple agents | AGPL-3.0 | ✅ Platform loop | ⚠️ Block builder | 2026-07-25 |
| **CrewAI** | 56k | Role-playing agents | ✅ Ollama/LiteLLM | ✅ Task delegation + quality gate + critic role | ✅ Shared memory between agents | ✅ Full crew orchestration | MIT | ⚠️ Single run | ❌ Code only | 2026-07-25 |
| **AutoGen** | 60k | Conversable agents | ✅ LiteLLM | ✅ Multi-agent discussion + code execution feedback | ✅ Conversation history | ✅ Nested/group chat | Apache-2.0 | ⚠️ Single run | ❌ Code only | 2026-04-15 |
| **smolagents** | 28k | Code-based agents | ✅ Ollama/HF Inference | ✅ Code execution + self-correction loop | ❌ Basic observation only | ❌ Single agent | Apache-2.0 | ⚠️ Single run | ❌ Code only | 2026-07-21 |
| **Letta** | 24k | Stateful agent | ✅ Ollama/vLLM | ✅ Inner monologue + self-reflective prompts | ✅✅ Advanced long-term memory + summarization + search | ❌ Single agent | Apache-2.0 | ✅ Stateful loop | ❌ Code only | 2026-07-22 |
| **GPT-Pilot** | 34k | AI developer | ❌ API-dependent (OpenAI) | ✅ Build → Test → Debug → Fix loop | ✅ Project context | ✅ AI "pair programmer" | AGPL-3.0 | ⚠️ Single project | ❌ Code only | 2026-06-18 |
| **Roo Code** | 24k | VS Code extension | ✅ Ollama/any provider | ✅ Edit → Test → Fix cycle | ✅ Context window + project awareness | ❌ Single agent | Apache-2.0 | ⚠️ IDE session | ❌ IDE only | 2026-05-15 |
| **Qwen-Agent** | 17k | Qwen-native agent | ✅ Qwen local models | ✅ Function calling + tool use loop | ✅ RAG + code interpreter | ✅ Agent + MCP tools | Apache-2.0 | ⚠️ Single run | ❌ Code only | 2026-03-04 |
| **LangGraph** | 38k | State machine agent framework | ✅ Ollama/any provider | ✅✅ Graph-based loops + conditional routing + checkpointing | ✅✅ Persistent checkpoint state + human-in-loop | ✅ Multi-agent composition | MIT | ✅✅ Checkpoint resume | ❌ Code only | 2026-07-26 |
| **n8n** | 198k | Visual workflow automation | ✅ Ollama/AI nodes | ✅ Loop nodes + conditional branches + error handling | ⚠️ Workflow state + item passing | ❌ Workflow nodes | SSL-v2 | ✅✅ Self-hosted daemon | ✅✅ Visual editor | 2026-07-26 |

---

## Szczegółowa Analiza Top 7

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

### 6. LangGraph (🏆 Najlepszy do Continuous Business Agent)

```
Repo: https://github.com/langchain-ai/langgraph
Stars: 38,153 | Forks: 6,409 | License: MIT
```

**Architektura:**
- **State machine framework** — agent jako graph z nodes i edges
- Każdy node = funkcja (LLM call, tool, human review, conditional)
- Edges = routing logic (conditional → go to node A, else → node B)
- **Checkpointing:** Pełny stan zapisywany po każdym node — można pauzować i wznowić
- **Streaming:** Real-time output z każdego kroku graphu
- Budowany przez LangChain — ecosystem tools, integrations, memory

**Pętla zwrotna (Feedback Loop):**
- ✅✅ **Graph-native loops** — node może routować NA POWRÓT do poprzedniego node
- **Conditional edges:** `if result.success → next step; else → retry`
- **Human-in-the-loop:** Break execution at any node → human approves/rejects → resume
- **Retry with backoff:** Built-in retry logic na dowolnym node
- **Cyclic graphs:** Natural loops — agent może "wracać" do planowania po each action

**Nauka/Pamięć:**
- **Checkpoint State:** Pełny stan agenta persisted (SQLite, PostgreSQL, Redis)
- **State Schema:** Custom TypedDict — agent definiuje CO zapamiętać
- **RunnableConfig:** `{"configurable": {"thread_id": "xyz"}}` — resume exact state later
- **Memory as State:** Nie tylko history — structured state (budget, strategy, lessons)
- ✅ **KLUCZOWE:** Stan przetrwa restart procesu — można pauzować na tydzień i wznowić

**Continuous Run:**
- ✅✅ **Najlepszy na rynku dla continuous operation**
- Graph checkpoint = "save point" — crash → resume from last checkpoint
- `while True:` loop calling `graph.invoke(state)` → auto-recovery
- Thread-based: każdy business idea = osobny thread z własnym stanem
- Docker: run as service, checkpoint co 5 minut do PostgreSQL

**Local LLM Support:**
- Pełne wsparcie przez LangChain — Ollama, vLLM, any provider
- `ChatOllama(model="qwen2.5-coder:32b")` — one-liner

**Plusy:**
- **MIT license** — najbezpieczniejsza dla commercial use
- **Checkpointing** — jedyny framework z PERSISTENT STATE + resume
- **Graph-based** — intuitive visualization complex logic (loops, branches, retries)
- **Human-in-the-loop** — native break points for user approval
- **38k stars, daily commits** — bardzo aktywny, LangChain-backed
- **Najlepszy fit** dla "business agent" — state = {budget, ideas, lessons} → graph loop
- **Dokumentacja najlepsza** na rynku — examples, tutorials, cookbook

**Minusy:**
- **Wymaga programowania** — nie jest no-code (ale API jest clean)
- **Checkpointing wymaga backendu** — SQLite OK, ale production needs PostgreSQL/Redis
- **Mniej "agentic" out of the box** niż AutoGPT — musisz build graph sam
- **LangChain ecosystem** — duży, ale fragmented (langchain, langgraph, langserve, ...)

**Dlaczego jest #1 dla Twojego przypadku:**
1. ✅ `while True` loop with checkpoint = agent running for months
2. ✅ State persists: `{budget: 1000, ideas: [...], lessons: {...}}`
3. ✅ Crashes? → resume from last checkpoint automatically
4. ✅ Human request node → pauses → waits for your approval → resumes
5. ✅ Each business idea = separate thread (parallel experiments)
6. ✅ MIT license — use commercially without restrictions

---

### 7. n8n (🎨 Najlepszy Visual/No-Code Workflow)

```
Repo: https://github.com/n8n-io/n8n
Stars: 198,035 | Forks: 59,633 | License: SSL-v2 (fair-code)
```

**Architektura:**
- **Visual workflow automation platform** — drag-and-drop node editor
- 400+ integracji (webhooks, APIs, databases, LLMs, cloud services)
- Self-hosted: Docker / Docker Compose — działa 24/7 jako daemon
- AI nodes: LLM, AI Agent, AI Document Extraction, AI Text Generation
- Workflow triggers: Schedule (cron), webhook, event-based

**Pętla zwrotna (Feedback Loop):**
- **Loop nodes:** Explicit "Loop Over Items" node — iterate over results
- **IF nodes:** Conditional branching — if revenue > threshold → scale, else → pivot
- **Error handling:** Try-catch nodes → fallback workflow
- **Code nodes:** Custom JavaScript/Python for custom logic
- **Agentic mode:** AI Agent node with tool calling + iteration

**Nauka/Pamięć:**
- ⚠️ **Workflow state** — passing data between nodes (JSON objects)
- **Storage nodes:** Write to database, Google Sheets, PostgreSQL
- **No built-in LLM memory** — nie ma "agent memory" w sensie Letta/LangGraph
- ✅ Ale: można build memory manually (workflow → database → read back next run)

**Continuous Run:**
- ✅✅ **Self-hosted daemon** — uruchomisz `docker-compose up -d` i działa 24/7
- **Schedule triggers:** Workflow runs on cron (np. co 6h) — automatic
- **Webhook triggers:** Reaktywuje workflow on event
- **Queue system:** Process multiple workflows in parallel
- ✅ Idealny dla "set and forget" workflows

**Visual/No-Code:**
- ✅✅ **Drag-and-drop editor** — nie trzeba programować
- **Templates gallery:** Gotowe workflow (content automation, lead gen, research)
- **Community workflows:** Thousands shared by users
- ✅ **Perfect dla non-developers** — biznesman może budować workflow sam

**Local LLM Support:**
- ✅ Ollama AI node — connect to local model
- ✅ Any OpenAI-compatible API
- ✅ Self-hosted LLM for AI agent nodes

**Plusy:**
- **198k stars** — ogromna społeczność
- **Self-hosted daemon** — run 24/7 with minimal maintenance
- **Visual editor** — zero coding needed for basic workflows
- **400+ integrations** — email, web, API, database, social media, ...
- **Schedule + webhook triggers** — automatic execution
- **Templates** — start from existing business workflows
- **Fair license** — self-hosted free, cloud paid

**Minusy:**
- **SSL-v2 license** — nie jest MIT/Apache (fair-code: free for self-hosted, paid for SaaS resale)
- **Mniej "agentic"** — to workflow automation, nie true AI agent
- **Memory system** — weak; nie ma LLM-native memory/langauge learning
- **Iterative learning** — agent doesn't truly "learn" from results (no reward/penalty loop)
- **Agentic nodes** — basic compared to LangGraph/CrewAI
- **Nie jest "autonomous agent"** — jest workflow engine; AI jest tylko jednym type of node

**Gdzie n8n się sprawdza:**
- ✅ Business automation (send emails, scrape prices, update CRM)
- ✅ Content pipelines (research → generate → publish)
- ✅ Data collection → analysis → reporting
- ⚠️ NIE jest "autonomous agent that learns and evolves" — jest "workflow engine with AI nodes"

---

## Ranking wg Przykładu Użycia

### 🔄 Agent działający miesiącami (Continuous + Learning)
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **LangGraph** | ✅✅ Checkpointing + resume + graph loops = true persistent agent |
| 2 | **n8n** | ✅✅ Self-hosted daemon + schedule triggers — ale weak "learning" |
| 3 | **AutoGPT** | ✅ Platform loop — ale AGPL + SaaS drift |

### 🧠 Agent z długą pamięcią i nauką
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **Letta** | 3-warstwowy memory + automatic summarization |
| 2 | **LangGraph** | Checkpoint state + custom schema — agent definiuje CO zapamiętać |
| 3 | **OpenHands** | AGENTS.md + episodic memory |

### 👥 Multi-Agent Team
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **CrewAI** | Role-based orchestration, processes |
| 2 | **AutoGen** | Conversable agents, nested chat |
| 3 | **LangGraph** | Multi-agent composition via sub-graphs |

### 💻 Full-Stack Development Agent
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **OpenHands** | Sandbox + browser + file system + git |
| 2 | **GPT-Pilot** | Build → test → debug loop |
| 3 | **Roo Code** | VS Code integration |

### 🎨 No-Code / Visual Workflow (non-developer)
| Miejsce | Framework | Dlaczego |
|---------|-----------|----------|
| 1 | **n8n** | ✅✅ Drag-and-drop editor + 400+ integrations + templates |
| 2 | **AutoGPT Platform** | ⚠️ Block builder — ale AGPL + SaaS |
| 3 | **LangGraph** | ❌ Wymaga kodu (ale API jest clean) |

---

## Rekomendacja — REWIZJA: **AutoGen** (primary)

> **Kluczowa zmiana:** LangGraph nie jest poprawny — ma **sztywne** akcje.
> Agent **NIE może** dodać nowej akcji w locie.
>
> **AutoGen** jest POPRAWNA odpowiedź: agent **tworzy nowe agenty dynamicznie**.
> Jeśli stwierdzi "potrzebuję dział HR" → tworzy go. "Nie potrzebuję" → usuwa.

### Co OZNACZA "Agent Tworzy Cały System Sam":

```
Cykl 1:  "Sprawdzę rynek"         → wywołuje Research node
Cykl 2:  "Potrzebuję dział HR"    → TWORZY nowego agenta "Recruiter" (nie istniał!)
Cykl 3:  "Rekrutator znalazł 3 kandydatów"
Cykl 4:  "Nie warto szukać, zrobię inaczej" → USUWA agenta "Recruiter"
Cykl 5:  "Potrzebuję marketera"   → TWORZY agenta "Marketer"
Cykl 6:  "Potrzebuję financial model" → TWORZY agenta "FinAnalyzer"
... i tak dalej, agent WZROSTE organicznie
```

**To jest AutoGen — jedyny framework który pozwala na TRUE self-modifying agent.**

| Kryterium | LangGraph | AutoGen |
|-----------|-----------|---------|
| Pre-defined actions | ✅ Only fixed nodes | ❌ NIE |
| Dynamiczne tworzenie agentów | ❌ | ✅ **RACZEWNA** |
| Dynamiczne usuwanie agentów | ❌ | ✅ |
| Multi-agent group chat | ❌ | ✅ |
| Self-modifying pipeline | ❌ | ✅ |
| Non-stop `while True` | ✅ | ✅ (custom loop) |
| Checkpointing (built-in) | ✅✅✅ | ✅ (state serialization) |
| Local LLM support (Ollama) | ✅ | ✅ |
| License | MIT | **MIT** |
| Repo stars | 38k | 42k |
| Maintainer | LangChain | Microsoft |

### Dlaczego AutoGen jest POPRAWNA odpowiedź:

| Twój wymaganie | LangGraph | AutoGen |
|----------------|-----------|---------|
| Agent działa non-stop | ✅ `while True` | ✅ custom loop |
| Agent tworzyc nowe moźliwości | ❌ sztywne | ✅ dynamiczne tworzenie |
| Agent usuna co niepotrzebne | ❌ | ✅ |
| Agent decyduje SAM co робит | ⚠️ z pre-defined set | ✅ dowolna akcja |
| Brak external scheduler | ✅ | ✅ |
| Local LLM (Ollama) | ✅ | ✅ |

---

## Architektura: AutoGen — Self-Modifying Business Agent

```
┌─────────────────────────────────────────────────────────────────┐
│  business_agent.py (systemd / nohup — runs 24/7 non-stop)       │
│                                                                  │
│  while True:                                                     │
│    state = load_checkpoint()                                     │
│                                                                  │
│    # MANAGER AGENT — zawsze istnieje                              │
│    manager = ConversableAgent(                                   │
│        name="Manager",                                           │
│        system_message="""                                          │
│           Jesteś business manager. Masz budżet {budget}.          │
│           Twoim zadaniem jest budowanie businesses.               │
│           Możesz TWORZYĆ nowe agenty do nowych zadań.             │
│           Możesz USUNAĆ agenty które nie są potrzebne.            │
│           Na każdym kroku DECIDE co robić.                       │
│        """,                                                       │
│        llm_config={"model": "qwen2.5-coder"}                     │
│    )                                                             │
│                                                                  │
│    # DYNAMICzne agenty (tworzone/usuwanie w locie)                │
│    active_agents = [manager]                                     │
│                                                                  │
│    # Grupa agentów rozmawia przez group chat                     │
│    group = GroupChat(agents=active_agents)                       │
│    manager.initiate_chat(group_manager, messages=state["task"])  │
│                                                                  │
│    # Po zakończeniu cyklu:                                        │
│    state = save_state(group.chat_history)                        │
│    save_checkpoint(state)                                        │
│    # IMMEDIATELY next cycle — no pause!                          │
└─────────────────────────────────────────────────────────────────┘
```

**Jak Manager tworzy nowego agenta:**

```python
# Manager decyduje (LLM decyduje!)
if "hire" in manager_decision:
    recruiter = ConversableAgent(
        name="Recruiter",
        system_message="Find candidates, interview, recommend",
        llm_config={"model": "qwen2.5-coder"}
    )
    active_agents.append(recruiter)  # NOWY AGENT added!

if "fire" in manager_decision:
    active_agents = [a for a in active_agents if a.name != "Recruiter"]
    # AGENT USUNIĘTY

# Następny cykl: grupa działa z NOWYM składem
group = GroupChat(agents=active_agents)
```

**Flow jeden cyklu (NIE jest fixed):**

1. Manager obudza się → ładuje state (budget, history, lessons)
2. Manager decyduje (LLM): "Co robimy teraz?" → **dowolna decyzja**
3. Jeśli Manager stwierdzi "potrzebuję X" → **tworzy X**
4. Agenty rozmawiają (group chat)
5. Wyniki zapisane → state updated → **natychmiast następny cykl**

**To działa NON-STOP.** Zero przerw, zero schedulera.

---

## Szybki Start — AutoGen + Ollama

```bash
# 1. Zainstaluj Ollama z modelem lokalnym
ollama pull qwen2.5-coder:32b

# 2. Zainstaluj AutoGen
pip install pyautogen

# 3. Uruchom agenta
python business_agent.py
```

**Wymagania sprzętowe:**
- Minimum: 16GB RAM (7B model)
- Rekomendowane: 64GB RAM + GPU (32B model)
- Serwer/VM 24/7 (VPS $5/mc lub home server)

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
| **LangGraph** | https://github.com/langchain-ai/langgraph |
| **n8n** | https://github.com/n8n-io/n8n |