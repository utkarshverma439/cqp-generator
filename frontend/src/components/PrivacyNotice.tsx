import { Shield } from 'lucide-react'

export default function PrivacyNotice() {
  return (
    <div className="text-center py-6">
      <div className="inline-flex items-center gap-1.5 text-xs text-gray-400">
        <Shield className="w-3.5 h-3.5" />
        <span>Your documents are secure and confidential.</span>
        <span className="text-gray-300">&bull;</span>
        <span>They are used only for generating the Cell Qualification Protocol.</span>
      </div>
    </div>
  )
}
