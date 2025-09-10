# Copilot instructions for ai-light_show_agents

Purpose
-------
Provide an automated contributor/agent guide with minimal, concrete steps to be productive in this repository. This is a modern, WebSocket-based AI light show management system with strict architectural principles.

High-level architecture
-----------------------
- **Frontend**: Preact-based SPA (`frontend/`) with WebSocket-only communication using Socket.IO client
- **Backend**: Flask-SocketIO server (`backend/app.py`) with Agent-based AI system and WebSocket services
- **Communication**: EXCLUSIVELY WebSocket-based - NO REST APIs allowed
- **Real-time state**: WebSocket service manages app state and real-time updates
- **AI Agents**: Located in `backend/agents/` with Jinja2 prompt templates for LLM interactions
- **DMX Canvas**: Real-time lighting frame buffer (`models/dmx/dmx_canvas.py`) for 512-channel output

Key files to inspect
--------------------
- **WebSocket Architecture**:
  - `backend/services/websocket_manager.py` — WebSocket message handlers and app state management
  - `backend/app.py` — Flask-SocketIO server setup with connection handlers
  - `frontend/src/WebSocket.ts` — Singleton WebSocket service with type-safe messaging
  - `frontend/src/hooks/useWebSocket.ts` — React hook for WebSocket state management
  - `frontend/src/components/WebSocketStatus.tsx` — Connection status UI component

- **Agent System**:
  - `backend/agents/agent.py` — Base Agent implementation with LLM streaming API
  - `backend/agents/effect_tramslator/effect_translator.py` — Translates plans into DMX actions
  - `backend/agents/lighting_planner/lighting_planner.py` — Creates lighting plans from song analysis
  - `backend/agents/prompts/*.j2` — Jinja2 templates for AI prompt construction

- **Data Models**:
  - `backend/models/app_data.py` — AppData singleton for centralized state management
  - `backend/models/dmx/dmx_canvas.py` — DMX frame buffer (512 channels, 50 FPS default)
  - `backend/models/lighting/` — Plan, PlanEntry, and ActionList models

- **Frontend Components**:
  - `frontend/src/app.tsx` — Main app layout with WebSocket integration
  - `frontend/src/components/AssistantChat.tsx` — AI chat interface using WebSocket
  - `frontend/src/components/WebSocketStatus.tsx` — Real-time connection monitoring

Conventions and important rules
-----------------------------
**STRICT ARCHITECTURAL PRINCIPLES** (NO EXCEPTIONS):
- **WebSocket-Only Communication**: NEVER create REST APIs. ALL frontend-backend communication MUST use WebSockets
- **No Fallback Methods**: Do NOT create alternative communication methods or compatibility layers
- **No Backward Compatibility**: Break existing patterns if they don't follow current best practices
- **Best Practices Enforcement**: Always use the established WebSocket service pattern

**WebSocket Communication**:
- Use `webSocketService.sendMessage(action, params)` for frontend→backend messages
- Backend handlers in `websocket_manager.py` emit responses via `emit(event_name, data)`
- App state updates sent via `app_state` event on connection and state changes
- TypeScript interfaces define message schemas in `frontend/src/WebSocket.ts`

**Template and File Naming**:
- Agent prompt templates: `backend/agents/prompts/{snake_case_class_name}.j2`
- WebSocket message handlers: Use descriptive action names (e.g., 'load_song', 'generate_plan')
- Component files: PascalCase with `.tsx` extension
- Hook files: `use{FeatureName}.ts` pattern

**Data Access**:
- ALWAYS use AppData singleton for data access: `AppData().song`, `AppData().fixtures`
- DO NOT read JSON files directly — use AppData properties and methods
- WebSocket handlers should use AppData to get current state

**DMX and Lighting**:
- DMX channels are 0-indexed in code (0-511 range)
- Frame timing uses 50 FPS default, frames keyed to rounded float timestamps
- Plans stored as JSON in `data/{song_name}.plan.json`
- Actions stored as JSON in `data/{song_name}.actions.json`

Developer workflows (concrete commands)
--------------------------------------
**Environment Setup**:
- ALWAYS activate Python environment: `pyenv activate ai-light && clear`
- Start LLM service: `docker compose up -d llm-service` 
- DO NOT start the full application.

**Frontend Development**:
- Use WebSocket hook in components: `const { isConnected, currentSong, sendMessage } = useWebSocket()`
- For new WebSocket messages, add TypeScript types to `WebSocket.ts`
- Test WebSocket connection via the WebSocketStatus component
- Build: `cd frontend && npm run build`

**Backend Development**:
- Add WebSocket handlers to `websocket_manager.py`
- Agent development: Create class in `agents/`, add prompt template in `prompts/`
- Test agents: Access via `Agent().get_models()` or direct instantiation
- Run backend: `python backend/app.py` (requires activated environment)

**WebSocket Message Flow**:
1. Frontend: `sendMessage('action_name', { param: 'value' })`
2. Backend: `@socketio.on('message')` handler processes action
3. Backend: `emit('response_event', data)` sends response
4. Frontend: WebSocket service receives event, notifies subscribers

Where outputs are written
------------------------
- **Logs**: `logs/` directory (agent responses, context files)
- **Generated plans**: `data/{song_name}.plan.json`
- **Generated actions**: `data/{song_name}.actions.json`
- **DMX frames**: In-memory DMXCanvas, can be exported
- **WebSocket logs**: Console output with emoji prefixes for easy debugging

Integration points & external dependencies
-----------------------------------------
- **Ollama LLM service**: Docker container on port 11434 (`llm-service` in docker-compose)
- **Song files**: MP3s in `songs/` directory
- **Analysis data**: JSON files in `data/` (beats, chords, analysis)
- **Fixtures**: `backend/fixtures/fixtures.json` defines DMX fixture configurations
- **Frontend build**: Vite-based build system, output to `frontend/dist/`

Quick tips for safe changes
--------------------------
**WebSocket Development**:
- Test WebSocket connection first: check WebSocketStatus component
- Use TypeScript interfaces for message types
- Handle connection states in UI (show loading/error states)
- Use the `useWebSocket` hook for component integration

**Agent Development**:
- Follow naming convention: `ClassName` → `class_name.j2` prompt template
- Test prompts by calling `agent.parse_context()` before `agent.run()`
- Use AppData singleton for accessing song, fixtures, plans

**Frontend Components**:
- Import and use `useWebSocket` hook for state management
- Handle WebSocket disconnection gracefully (disable buttons, show status)
- Use existing CSS classes for consistency

**Data Management**:
- Use AppData properties instead of direct file access
- WebSocket handlers should emit state changes to keep frontend in sync
- DMX frames are ephemeral — persist important data as JSON

Troubleshooting notes
---------------------
**WebSocket Issues**:
- Check WebSocketStatus component for connection state
- Verify backend is running: `docker-compose logs backend`
- Ensure ports are not blocked (5000 for backend)
- Check browser console for WebSocket connection errors

**Build Issues**:
- Frontend TypeScript errors: Check type imports and WebSocket message interfaces
- Backend import errors: Verify Python environment is activated
- Docker build fails: Check for syntax errors in modified files

**Agent Issues**:
- LLM service unreachable: Ensure `docker-compose up -d llm-service` completed
- Template errors: Verify Jinja2 syntax in `.j2` files
- Missing song data: Check `data/` directory for required JSON files

**Performance Issues**:
- WebSocket message flooding: Implement rate limiting or message batching
- Large JSON responses: Consider pagination or data streaming
- Memory usage: Check DMX canvas frame accumulation

**Development Principles**:
- NEVER create REST API endpoints — use WebSocket messages exclusively
- NEVER create fallback methods
- ALWAYS enforce TypeScript types for WebSocket messages
- ALWAYS use the established WebSocket service singleton pattern
- ALWAYS handle WebSocket connection states in UI components
