/**
 * Role badge config and access helpers.
 */
export const ROLES = {
  superadmin:      { label: 'Superadmin',       cls: 'bg-accent-500/20 text-accent-700 dark:text-accent-300 border-accent-500/40' },
  admin:           { label: 'Admin',            cls: 'bg-primary-100 text-primary-800 dark:bg-primary-700 dark:text-primary-100 border-primary-300 dark:border-primary-600' },
  content_manager: { label: 'Content Manager',  cls: 'bg-teal-100 text-teal-800 dark:bg-teal-900/40 dark:text-teal-300 border-teal-300/50' },
  page_editor:     { label: 'Page Editor',      cls: 'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300 border-purple-300/50' }
}

export function roleBadge(role) {
  return ROLES[role] || { label: role || '—', cls: 'bg-neutral-100 text-neutral-700' }
}

/** Check whether `userRole` is in the allowed list (superadmin always passes). */
export function canAccess(userRole, allowed = []) {
  if (!userRole) return false
  if (userRole === 'superadmin') return true
  if (!allowed.length) return true
  return allowed.includes(userRole)
}
