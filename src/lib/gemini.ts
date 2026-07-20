const KEYS = [
  process.env.GEMINI_API_KEY_1,
  process.env.GEMINI_API_KEY_2,
  process.env.GEMINI_API_KEY_3,
].filter(Boolean) as string[]

const MODEL = 'gemini-2.5-flash'

export async function gemini(prompt: string): Promise<string> {
  let lastError: Error | null = null

  for (const key of KEYS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { maxOutputTokens: 2048 },
          }),
        }
      )
      if (res.status === 429 || res.status === 503) {
        lastError = new Error(`rate_limit: ${res.status}`)
        continue
      }
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error?.message ?? `HTTP ${res.status}`)
      }
      const data = await res.json()
      return data.candidates?.[0]?.content?.parts?.[0]?.text ?? ''
    } catch (e) {
      if (e instanceof Error && e.message.startsWith('rate_limit')) {
        lastError = e
        continue
      }
      throw e
    }
  }
  throw lastError ?? new Error('Gemini API failed')
}
