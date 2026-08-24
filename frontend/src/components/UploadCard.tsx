import { ReactNode } from 'react'
import { FileText } from 'lucide-react'

interface Props {
  title: string
  description: string
  children: ReactNode
}

export default function UploadCard({ title, description, children }: Props) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
      <div className="px-6 py-5 border-b border-gray-100 flex items-start gap-3">
        <div className="mt-1 flex-shrink-0">
          <FileText className="w-5 h-5 text-blue-600" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
          <p className="text-sm text-gray-500 mt-1">{description}</p>
        </div>
      </div>
      <div className="p-6 space-y-4">
        {children}
      </div>
    </div>
  )
}
