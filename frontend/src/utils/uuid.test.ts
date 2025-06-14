import { describe, it, expect } from 'vitest'
import { generateUUID, generateId } from './uuid'

describe('UUID Utils', () => {
  describe('generateUUID', () => {
    it('should generate a valid UUID v4', () => {
      const uuid = generateUUID()
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
      expect(uuid).toMatch(uuidRegex)
    })

    it('should generate unique UUIDs', () => {
      const uuid1 = generateUUID()
      const uuid2 = generateUUID()
      expect(uuid1).not.toBe(uuid2)
    })
  })

  describe('generateId', () => {
    it('should generate an ID with timestamp and random string', () => {
      const id = generateId()
      expect(id).toMatch(/^\d+-[a-z0-9]+$/)
    })

    it('should generate unique IDs', () => {
      const ids = new Set()
      for (let i = 0; i < 100; i++) {
        ids.add(generateId())
      }
      expect(ids.size).toBe(100)
    })
  })
})