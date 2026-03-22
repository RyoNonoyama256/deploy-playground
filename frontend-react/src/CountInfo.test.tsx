import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import CountInfo from './CountInfo'

describe('CountInfo', () => {
  it('カウント数が表示される', () => {
    render(<CountInfo countNum={5} setCount={vi.fn()} />)
    expect(screen.getByRole('button', { name: /カウント 5/ })).toBeInTheDocument()
  })

  it('ボタンクリックでsetCountが呼ばれる', async () => {
    const user = userEvent.setup()
    const setCount = vi.fn()
    render(<CountInfo countNum={0} setCount={setCount} />)

    await user.click(screen.getByRole('button'))
    expect(setCount).toHaveBeenCalledOnce()
  })
})
