import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type Memo = {
  id: string
  title: string
  content: string
  createdAt: string
}

function MemoList() {
  const [memos, setMemos] = useState<Memo[]>([])
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchMemos = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/memos`)
      const data = await res.json()
      setMemos(data)
    } catch (err) {
      console.error('Failed to fetch memos', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMemos()
  }, [])

  const addMemo = async () => {
    if (!title.trim()) return
    await fetch(`${API_URL}/memos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    })
    setTitle('')
    setContent('')
    fetchMemos()
  }

  const deleteMemo = async (id: string) => {
    await fetch(`${API_URL}/memos/${id}`, { method: 'DELETE' })
    fetchMemos()
  }

  return (
    <div className="memo-section">
      <h2>📝 メモ</h2>
      <div className="memo-form">
        <input
          type="text"
          placeholder="タイトル"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          placeholder="内容"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button onClick={addMemo}>追加</button>
      </div>
      {loading ? (
        <p>読み込み中...</p>
      ) : (
        <ul className="memo-list">
          {memos.map((memo) => (
            <li key={memo.id}>
              <strong>{memo.title}</strong>
              <p>{memo.content}</p>
              <small>{memo.createdAt}</small>
              <button onClick={() => deleteMemo(memo.id)}>削除</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default MemoList
