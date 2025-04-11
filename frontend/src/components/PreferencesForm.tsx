import { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'

export default function PreferencesForm() {
  const { user, updatePreferences } = useAuth()
  const [prefs, setPrefs] = useState({
    source_ids: [] as string[],
    language: 'en'
  })

  useEffect(() => {
    if (user) setPrefs(user.preferences)
  }, [user])

  const handleSave = async () => {
    await updatePreferences(prefs)
  }

  return (
    <div className="preferences-form">
      <div>
        <label>Preferred Language:</label>
        <select
          value={prefs.language}
          onChange={(e) => setPrefs({...prefs, language: e.target.value})}
        >
          <option value="en">English</option>
          <option value="ar">Arabic</option>
        </select>
      </div>

      <button onClick={handleSave}>
        Save Preferences
      </button>
    </div>
  )
}