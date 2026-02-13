import { useState } from 'react'

function App() {
  const [storeName, setStoreName] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!storeName) return
    setLoading(true)
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ store_name: storeName })
      })

      if (!res.ok) {
        throw new Error(`서버 에러: ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error('분석 에러:', err)
      setResult({ error: '분석 중 에러 발생 ㅠㅠ - ' + err.message })
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>리뷰닥터 POC</h1>
      <p>가게 이름 입력해서 리뷰 분석받아보세요!</p>

      <input
        type="text"
        value={storeName}
        onChange={(e) => setStoreName(e.target.value)}
        placeholder="예: 홍대 김밥천국"
        style={{ width: '100%', padding: '0.8rem', marginBottom: '1rem', boxSizing: 'border-box' }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          padding: '0.8rem 1.5rem',
          background: loading ? '#aaa' : '#646cff',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? '분석 중...' : '분석하기'}
      </button>

      {result && !result.error ? (
        <div
          style={{
            marginTop: '2rem',
            border: '1px solid #ddd',
            padding: '1.5rem',
            borderRadius: '8px',
            background: '#f9f9f9',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}
        >
          <h3 style={{ marginTop: 0 }}>{result.store} 분석 결과</h3>

          <p style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>
            리뷰 수: <strong>{result.review_count}개</strong> | 
            전체 감성: <strong>{result.sentiment}</strong>
          </p>

          <div style={{ margin: '1.5rem 0' }}>
            <h4 style={{ color: '#4caf50', marginBottom: '0.5rem' }}>강점</h4>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
              {result.strong_points?.length > 0 ? (
                result.strong_points.map((point, i) => (
                  <li key={i} style={{ marginBottom: '0.5rem' }}>
                    👍 {point}
                  </li>
                ))
              ) : (
                <li>강점 데이터 없음</li>
              )}
            </ul>
          </div>

          <div style={{ margin: '1.5rem 0' }}>
            <h4 style={{ color: '#f44336', marginBottom: '0.5rem' }}>약점</h4>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
              {result.weak_points?.length > 0 ? (
                result.weak_points.map((point, i) => (
                  <li key={i} style={{ marginBottom: '0.5rem' }}>
                    😕 {point}
                  </li>
                ))
              ) : (
                <li>약점 데이터 없음</li>
              )}
            </ul>
          </div>

          <div>
            <h4 style={{ marginBottom: '0.5rem' }}>개선 제안</h4>
            <ul style={{ listStyleType: 'disc', paddingLeft: '1.5rem' }}>
              {result.action_items?.length > 0 ? (
                result.action_items.map((item, i) => (
                  <li key={i} style={{ marginBottom: '0.5rem' }}>
                    {item}
                  </li>
                ))
              ) : (
                <li>개선 제안 없음</li>
              )}
            </ul>
          </div>
        </div>
      ) : result?.error ? (
        <div
          style={{
            marginTop: '2rem',
            padding: '1rem',
            background: '#ffebee',
            border: '1px solid #ef5350',
            borderRadius: '8px',
            color: '#c62828'
          }}
        >
          <strong>에러 발생:</strong> {result.error}
        </div>
      ) : null}
    </div>
  )
}

export default App