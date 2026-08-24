import { AlertTriangle, RefreshCw } from 'lucide-react'

interface Props {
  message: string
  details?: string
  onRetry: () => void
}

export default function ErrorMessage({ message, details, onRetry }: Props) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-xl shadow-sm">
      <div className="px-6 py-5">
        <div className="flex items-start gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0 mt-0.5">
            <AlertTriangle className="w-4 h-4 text-red-600" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-gray-900">{message}</h3>
            <p className="text-sm text-gray-600 mt-0.5">
              Something went wrong while generating the protocol. Please check your documents and try again.
            </p>
          </div>
        </div>
        {details && (
          <div className="ml-11 mb-3 p-3 bg-white rounded-lg border border-red-100">
            <pre className="text-xs text-red-700 whitespace-pre-wrap font-mono overflow-auto max-h-40">
              {details}
            </pre>
          </div>
        )}
        <div className="ml-11">
          <button
            onClick={onRetry}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Try Again
          </button>
        </div>
      </div>
    </div>
  )
}
