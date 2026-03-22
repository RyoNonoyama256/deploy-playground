type CountInfoProps = {
    countNum: number
    setCount: React.Dispatch<React.SetStateAction<number>>
}

function CountInfo ({ countNum, setCount }: CountInfoProps) {
    return <>
        <div className="card">
            <h2>動作確認</h2>
            <button onClick={() => setCount(prev => prev + 1)}>
                カウント {countNum}
            </button>
            <p className="hint">ボタンが動けばJSも正常に配信されています</p>
        </div>
    </>
}

export default CountInfo
