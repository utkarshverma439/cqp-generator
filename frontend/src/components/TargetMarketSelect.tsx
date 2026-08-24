import { ChevronDown, Globe } from 'lucide-react'

interface Props {
  value: string
  onChange: (value: string) => void
  otherValue: string
  onOtherChange: (value: string) => void
}

const MARKETS = [
  { value: 'Global', label: 'Global' },
  { value: 'EU / UN-38.3', label: 'EU / UN-38.3' },
  { value: 'US / DOT', label: 'US / DOT' },
  { value: 'Other', label: 'Other' },
]

export default function TargetMarketSelect({ value, onChange, otherValue, onOtherChange }: Props) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
      <div className="px-6 py-5 border-b border-gray-100 flex items-start gap-3">
        <div className="mt-1 flex-shrink-0">
          <Globe className="w-5 h-5 text-blue-600" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-900">2. Target Market</h2>
          <p className="text-sm text-gray-500 mt-1">
            Select the target market for this qualification protocol.
          </p>
        </div>
      </div>
      <div className="p-6">
        <div className="relative max-w-sm">
          <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-blue-600 pointer-events-none" />
          <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="w-full appearance-none bg-white border border-gray-300 rounded-lg pl-10 pr-10 py-2.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            {MARKETS.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
        </div>
        {value === 'Other' && (
          <div className="mt-3 max-w-sm">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Specify target market
            </label>
            <input
              type="text"
              value={otherValue}
              onChange={(e) => onOtherChange(e.target.value)}
              placeholder="e.g. South Korea / KC"
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>
        )}
      </div>
    </div>
  )
}
