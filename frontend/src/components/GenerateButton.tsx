import { Loader2, Sparkles } from 'lucide-react'

interface Props {
  loading: boolean
  disabled: boolean
  onClick: () => void
}

export default function GenerateButton({ loading, disabled, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        w-full flex items-center justify-center gap-2.5 px-6 py-3 rounded-lg text-sm font-semibold transition-all
        ${disabled && !loading
          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
          : loading
            ? 'bg-blue-600 text-white cursor-wait'
            : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800 shadow-sm'
        }
      `}
    >
      {loading ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin" />
          Generating Cell Qualification Protocol...
        </>
      ) : (
        <>
          <Sparkles className="w-4 h-4" />
          Generate Cell Qualification Protocol
        </>
      )}
    </button>
  )
}
