import './App.css'
import { useState } from 'react'
import DeployInfo from './DeployInfo'
import CountInfo from './CountInfo'

function App() {
  const [count, setCount] = useState<number>(0)
  const deployTarget: string = import.meta.env.VITE_DEPLOY_TARGET || 'local'
  const [buildTime] = useState(() => import.meta.env.VITE_BUILD_TIME || new Date().toISOString())

  return (
    <div className="app">
      <h1>🚀 Deploy Playground v2</h1>
      <p className="subtitle">デプロイ実験場</p>

      <DeployInfo deployTarget={deployTarget} buildTime={buildTime} />

      <CountInfo countNum={count} setCount={setCount} />

    </div>
  )
}

export default App