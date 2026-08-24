import { Download, Eye, CheckCircle2 } from 'lucide-react'
import { WordIcon } from './FileUpload'

interface Props {
  fileName: string
  fileSize: number
  onDownload: () => void
  onView: () => void
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1048576) return (bytes / 1024).toFixed(0) + ' KB'
  return (bytes / 1048576).toFixed(1) + ' MB'
}

export default function GenerationSuccess({ fileName, fileSize, onDownload, onView }: Props) {
  const formattedDate = new Date().toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })

  return (
    <div className="bg-green-50/50 border border-green-200 rounded-xl shadow-sm">
      <div className="px-6 py-5">
        <div className="flex items-start gap-3 mb-5">
          <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
            <CheckCircle2 className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-green-800">
              Cell Qualification Protocol Generated Successfully!
            </h3>
            <p className="text-sm text-gray-600 mt-0.5">
              Your Cell Qualification Protocol is ready.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3">
            <WordIcon />
            <div className="min-w-0">
              <p className="text-sm font-semibold text-gray-900 truncate" title={fileName}>
                {fileName}
              </p>
              <p className="text-xs text-gray-500 mt-0.5">
                Generated on {formattedDate} &bull; {formatSize(fileSize)}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onView}
              className="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg border border-blue-600 text-blue-600 text-sm font-semibold hover:bg-blue-50 transition-colors whitespace-nowrap"
            >
              <Eye className="w-4 h-4" />
              View Document
            </button>
            <button
              onClick={onDownload}
              className="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-semibold hover:bg-emerald-700 transition-colors shadow-sm whitespace-nowrap"
            >
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
