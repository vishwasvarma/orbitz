import { useTheme } from '../context/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()
  const next = theme === 'light' ? 'dark' : 'light'

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label={`Switch to ${next} theme`}
    >
      {theme === 'light' ? 'Dark' : 'Light'}
    </button>
  )
}
