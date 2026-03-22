import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import DeployInfo from './DeployInfo'

describe('DeployInfo', () => {
  it('デプロイ先とビルド日時が表示される', () => {
    render(<DeployInfo deployTarget="staging" buildTime="2026-01-01T00:00:00Z" />)

    expect(screen.getByText('staging')).toBeInTheDocument()
    expect(screen.getByText('2026-01-01T00:00:00Z')).toBeInTheDocument()
    expect(screen.getByText('React + Vite')).toBeInTheDocument()
  })
})
