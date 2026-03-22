import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
  it('タイトルが表示される', () => {
    render(<App />)
    expect(screen.getByText(/Deploy Playground/)).toBeInTheDocument()
  })

  it('カウントボタンをクリックするとカウントが増える', async () => {
    const user = userEvent.setup()
    render(<App />)

    const button = screen.getByRole('button', { name: /カウント 0/ })
    await user.click(button)
    expect(screen.getByRole('button', { name: /カウント 1/ })).toBeInTheDocument()
  })
})
