type DeployInfoProps = {
  deployTarget: string
  buildTime: string
}

function DeployInfo({ deployTarget, buildTime }: DeployInfoProps) {
  return (
    <div className="card">
      <h2>デプロイ情報</h2>
      <table>
        <tbody>
          <tr>
            <td className="label">デプロイ先</td>
            <td className="value">{deployTarget}</td>
          </tr>
          <tr>
            <td className="label">ビルド日時</td>
            <td className="value">{buildTime}</td>
          </tr>
          <tr>
            <td className="label">フレームワーク</td>
            <td className="value">React + Vite</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default DeployInfo
