import { useRef, useState } from 'react'
import { CheckCircle2, X } from 'lucide-react'

interface Props {
  title: string
  description: string
  accept: string
  file: File | null
  onFileChange: (file: File | null) => void
  error?: string
}

export function WordIcon() {
  return (
    <div className="w-11 h-11 rounded-lg bg-[#185abd] flex items-center justify-center text-white font-bold select-none flex-shrink-0 shadow-sm">
      <span className="text-xl tracking-tighter font-extrabold">W</span>
    </div>
  )
}

export function PdfIcon() {
  return (
    <div className="w-11 h-11 rounded-lg bg-[#e62225] flex items-center justify-center text-white font-bold select-none flex-shrink-0 shadow-sm">
      <span className="text-xs tracking-tight font-extrabold">PDF</span>
    </div>
  )
}

export default function FileUpload({ title, description, accept, file, onFileChange, error }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)

  const isWord = accept.toLowerCase().includes('docx')
  const extLabel = isWord ? '.docx' : '.pdf'

  function formatSize(bytes: number): string {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1048576) return (bytes / 1024).toFixed(0) + ' KB'
    return (bytes / 1048576).toFixed(1) + ' MB'
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setDragOver(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped) {
      const ext = '.' + dropped.name.split('.').pop()?.toLowerCase()
      if (accept.split(',').map(s => s.trim()).includes(ext)) {
        onFileChange(dropped)
      }
    }
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault()
    setDragOver(true)
  }

  function handleDragLeave() {
    setDragOver(false)
  }

  function handleClick() {
    inputRef.current?.click()
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0] || null
    onFileChange(selected)
  }

  function handleRemove(e: React.MouseEvent) {
    e.stopPropagation()
    onFileChange(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  const isUploaded = !!file

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={handleClick}
      className={`
        relative flex items-center justify-between gap-4 p-5 bg-white rounded-xl border transition-all cursor-pointer
        ${dragOver ? 'border-blue-500 ring-2 ring-blue-500/10' : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'}
        ${error ? 'border-red-300 bg-red-50/10' : ''}
      `}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        className="hidden"
      />

      {/* Left side: Icon & Title/Desc */}
      <div className="flex items-center gap-4">
        {isWord ? <WordIcon /> : <PdfIcon />}
        <div>
          <div className="flex items-center gap-1">
            <span className="text-sm font-semibold text-gray-900">{title}</span>
            <span className="text-sm font-semibold text-gray-900">({extLabel})</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">{description}</p>
        </div>
      </div>

      {/* Right side: Button & File info */}
      <div className="flex items-center gap-5">
        <div className="text-right">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center justify-center px-4 py-1.5 rounded-md border border-blue-600 text-blue-600 text-sm font-semibold hover:bg-blue-50 transition-colors whitespace-nowrap">
              Choose File
            </span>
            {isUploaded && file ? (
              <div className="flex flex-col items-start text-left max-w-[200px]">
                <span className="text-sm font-medium text-gray-900 truncate w-full" title={file.name}>
                  {file.name}
                </span>
                <span className="text-xs text-gray-400">
                  {formatSize(file.size)}
                </span>
              </div>
            ) : (
              <span className="text-sm text-gray-500 whitespace-nowrap">No file chosen</span>
            )}
          </div>
          <div className="mt-1">
            {isUploaded && file ? (
              <div className="flex items-center gap-1 text-[11px] text-green-600 font-semibold justify-end">
                <CheckCircle2 className="w-3 h-3 text-green-500 flex-shrink-0" />
                <span>Uploaded</span>
              </div>
            ) : (
              <span className="text-xs text-gray-400">Supported format: {extLabel}</span>
            )}
          </div>
        </div>

        {isUploaded && (
          <button
            onClick={handleRemove}
            className="p-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-400 hover:text-gray-600 transition-colors flex-shrink-0"
            title="Remove file"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {error && (
        <div className="absolute -bottom-6 left-0">
          <span className="text-xs text-red-500 font-medium">{error}</span>
        </div>
      )}
    </div>
  )
}
