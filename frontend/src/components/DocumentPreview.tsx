import { useEffect, useRef } from 'react'
import { X, Download, FileText } from 'lucide-react'
import { renderAsync } from 'docx-preview'

interface Props {
  blob: Blob
  fileName: string
  onClose: () => void
  onDownload: () => void
}

export default function DocumentPreview({ blob, fileName, onClose, onDownload }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (containerRef.current && blob) {
      // Clear previous rendering
      containerRef.current.innerHTML = ''

      renderAsync(blob, containerRef.current, undefined, {
        className: 'docx',
        inWrapper: true,
        ignoreWidth: false,
        ignoreHeight: false,
      })
      .then(() => {
        console.log('Document rendered successfully')
      })
      .catch((error) => {
        console.error('Error rendering document:', error)
      })
    }
  }, [blob])

  useEffect(() => {
    function handleEsc(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [onClose])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 backdrop-blur-sm">
      <div className="relative w-full max-w-5xl h-[90vh] bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden mx-4">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 flex-shrink-0 bg-white">
          <div className="flex items-center gap-3">
            <FileText className="w-5 h-5 text-blue-600" />
            <div>
              <h3 className="text-sm font-semibold text-gray-900">
                Cell Qualification Protocol Document Preview
              </h3>
              <p className="text-xs text-gray-500">{fileName}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={onDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 transition-colors shadow-sm"
            >
              <Download className="w-3.5 h-3.5" />
              Download
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-md hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
        <div className="flex-1 bg-gray-100 overflow-y-auto p-4 sm:p-8 flex justify-center">
          <div
            ref={containerRef}
            className="w-full max-w-[850px] bg-white shadow-sm border border-gray-200 rounded-lg p-2"
          />
        </div>
      </div>
    </div>
  )
}
