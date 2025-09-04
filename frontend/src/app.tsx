import { useState } from 'preact/hooks'
import './app.css'
import { AudioPlayer } from './components/AudioPlayer'
import { SongAnalysis } from './components/SongAnalysis'
import { SongPlan } from './components/SongPlan'
import { Actions } from './components/Actions'
import { AssistantChat } from './components/AssistantChat'
import { DmxFixtures } from './components/DmxFixtures'
import { ServerLog } from './components/ServerLog'
import { WebSocketStatus } from './components/WebSocketStatus'


export function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div class="app">
      <div class="main-panel">
        <AudioPlayer />
        <div class="columns">
          <SongAnalysis />
          <SongPlan />
          <Actions />
        </div>
        <WebSocketStatus />
      </div>
      <div class="right-panel">
        <div class="tabs">
          <button onClick={() => setActiveTab('chat')} class={activeTab === 'chat' ? 'active' : ''}>Chat</button>
          <button onClick={() => setActiveTab('fixtures')} class={activeTab === 'fixtures' ? 'active' : ''}>Fixtures</button>
          <button onClick={() => setActiveTab('log')} class={activeTab === 'log' ? 'active' : ''}>Log</button>
        </div>
        <div class="tab-content">
          {activeTab === 'chat' && <AssistantChat />}
          {activeTab === 'fixtures' && <DmxFixtures />}
          {activeTab === 'log' && <ServerLog />}
        </div>
      </div>
    </div>
  )
}
