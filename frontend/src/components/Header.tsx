import { FileText } from 'lucide-react'

export default function Header() {
  return (
    <div className="text-center mb-12 flex flex-col items-center">
      <div className="flex items-center gap-3.5 mb-2">
        <FileText className="w-10 h-10 text-blue-600" strokeWidth={2.2} />
        <h1 className="text-3xl font-bold text-gray-900 tracking-tight">
          Cell Qualification Protocol Generator
        </h1>
      </div>
      <p className="text-gray-500 text-sm max-w-md">
        Upload three source documents to generate a Cell Qualification Protocol.
      </p>
    </div>
  )
}
