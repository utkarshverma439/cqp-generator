import { useState, useCallback } from 'react'
import Header from './components/Header'
import UploadCard from './components/UploadCard'
import FileUpload from './components/FileUpload'
import TargetMarketSelect from './components/TargetMarketSelect'
import GenerateButton from './components/GenerateButton'
import GenerationSuccess from './components/GenerationSuccess'
import DocumentPreview from './components/DocumentPreview'
import ErrorMessage from './components/ErrorMessage'
import PrivacyNotice from './components/PrivacyNotice'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface ValidationErrors {
  tmp?: string
  acl?: string
  ds?: string
}

export default function App() {
  const [tmpFile, setTmpFile] = useState<File | null>(null)
  const [aclFile, setAclFile] = useState<File | null>(null)
  const [dsFile, setDsFile] = useState<File | null>(null)
  const [market, setMarket] = useState('Global')
  const [otherMarket, setOtherMarket] = useState('')
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<ValidationErrors>({})
  const [genError, setGenError] = useState<{ message: string; details?: string } | null>(null)
  const [result, setResult] = useState<{ blob: Blob; fileName: string; url: string } | null>(null)
  const [showPreview, setShowPreview] = useState(false)

  const canGenerate = tmpFile && aclFile && dsFile && !loading

  function validate(): boolean {
    const errs: ValidationErrors = {}
    if (tmpFile && !tmpFile.name.toLowerCase().endsWith('.docx')) {
      errs.tmp = 'TMP must be a .docx file'
    }
    if (aclFile && !aclFile.name.toLowerCase().endsWith('.docx')) {
      errs.acl = 'ACL must be a .docx file'
    }
    if (dsFile && !dsFile.name.toLowerCase().endsWith('.pdf')) {
      errs.ds = 'Datasheet must be a .pdf file'
    }
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleGenerate = useCallback(async () => {
    if (!tmpFile || !aclFile || !dsFile) return
    if (!validate()) return

    setLoading(true)
    setGenError(null)
    setResult(null)

    const effectiveMarket = market === 'Other' ? otherMarket : market

    const formData = new FormData()
    formData.append('tmp_file', tmpFile)
    formData.append('acl_file', aclFile)
    formData.append('datasheet_file', dsFile)
    formData.append('market', effectiveMarket)

    try {
      const resp = await fetch(`${API_BASE}/generate-cqp`, {
        method: 'POST',
        body: formData,
      })

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({ detail: resp.statusText }))
        const detail = typeof errData.detail === 'object'
          ? JSON.stringify(errData.detail, null, 2)
          : errData.detail || resp.statusText
        setGenError({ message: 'Unable to generate CQP', details: detail })
        return
      }

      const blob = await resp.blob()
      const cd = resp.headers.get('content-disposition') || ''
      const nameMatch = cd.match(/filename="?([^";\n]+)"?/)
      const fname = nameMatch ? nameMatch[1] : 'Cell_Qualification_Protocol.docx'
      const url = URL.createObjectURL(blob)

      setResult({ blob, fileName: fname, url })
    } catch (err: any) {
      setGenError({ message: 'Unable to generate CQP', details: err.toString() })
    } finally {
      setLoading(false)
    }
  }, [tmpFile, aclFile, dsFile, market, otherMarket])

  function handleDownload() {
    if (!result) return
    const a = document.createElement('a')
    a.href = result.url
    a.download = result.fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  function handleRetry() {
    setGenError(null)
    setResult(null)
  }

  function handleRemoveTmp() { setTmpFile(null); setErrors(e => ({ ...e, tmp: undefined })) }
  function handleRemoveAcl() { setAclFile(null); setErrors(e => ({ ...e, acl: undefined })) }
  function handleRemoveDs() { setDsFile(null); setErrors(e => ({ ...e, ds: undefined })) }

  return (
    <div className="min-h-screen bg-gray-50/50">
      <div className="max-w-[1060px] mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
        <Header />

        <div className="space-y-6">
          <UploadCard
            title="1. Upload Source Documents"
            description="Please upload all three required documents."
          >
            <FileUpload
              title="Test Method Procedure"
              description="The TMP document for the cell"
              accept=".docx"
              file={tmpFile}
              onFileChange={setTmpFile}
              error={errors.tmp}
            />
            <FileUpload
              title="Acceptance Criteria & Limits"
              description="The ACL document for the cell"
              accept=".docx"
              file={aclFile}
              onFileChange={setAclFile}
              error={errors.acl}
            />
            <FileUpload
              title="Vendor Datasheet"
              description="The datasheet PDF for the cell"
              accept=".pdf"
              file={dsFile}
              onFileChange={setDsFile}
              error={errors.ds}
            />
          </UploadCard>

          <TargetMarketSelect
            value={market}
            onChange={setMarket}
            otherValue={otherMarket}
            onOtherChange={setOtherMarket}
          />

          <GenerateButton
            loading={loading}
            disabled={!canGenerate}
            onClick={handleGenerate}
          />

          {genError && (
            <ErrorMessage
              message={genError.message}
              details={genError.details}
              onRetry={handleRetry}
            />
          )}

          {result && (
            <GenerationSuccess
              fileName={result.fileName}
              fileSize={result.blob.size}
              onDownload={handleDownload}
              onView={() => setShowPreview(true)}
            />
          )}
        </div>

        <PrivacyNotice />
      </div>

      {showPreview && result && (
        <DocumentPreview
          blob={result.blob}
          fileName={result.fileName}
          onClose={() => setShowPreview(false)}
          onDownload={handleDownload}
        />
      )}
    </div>
  )
}
