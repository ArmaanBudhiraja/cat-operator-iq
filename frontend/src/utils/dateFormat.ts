/**
 * Timezone-aware date/time formatting utility for CAT OperatorIQ.
 * Ensures consistent, reliable handling of UTC timestamps across the application.
 */

export const APP_TIMEZONE = 'Asia/Kolkata';

/**
 * Parses an ISO string or Date into a Date object representing the correct instant.
 * If the string does not have timezone information ('Z' or [+-]HH:MM), it is assumed to be UTC.
 */
export function parseUtcDate(value: string | Date | undefined | null): Date | null {
  if (!value) return null;
  if (value instanceof Date) return isNaN(value.getTime()) ? null : value;

  let str = String(value).trim();
  if (!str) return null;

  // Replace space separator with 'T' if format is "YYYY-MM-DD HH:MM:SS"
  if (str.includes(' ') && !str.includes('T')) {
    str = str.replace(' ', 'T');
  }

  // If there's no timezone suffix ('Z' or +HH:MM or -HH:MM), treat as UTC
  if (!str.endsWith('Z') && !/[+-]\d{2}(:\d{2})?$/.test(str)) {
    str = `${str}Z`;
  }

  const d = new Date(str);
  return isNaN(d.getTime()) ? null : d;
}

/**
 * Formats an incident timestamp for table view: "MM-DD HH:mm" in application timezone (Asia/Kolkata).
 */
export function formatIncidentTableTime(timestamp: string | Date | undefined | null, timeZone = APP_TIMEZONE): string {
  const d = parseUtcDate(timestamp);
  if (!d) return '--';

  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).formatToParts(d);

  const m = parts.find((p) => p.type === 'month')?.value;
  const day = parts.find((p) => p.type === 'day')?.value;
  let h = parts.find((p) => p.type === 'hour')?.value || '00';
  if (h === '24') h = '00';
  const min = parts.find((p) => p.type === 'minute')?.value || '00';

  return `${m}-${day} ${h}:${min}`;
}

/**
 * Formats an incident timestamp for detail/drawer view: "YYYY-MM-DD HH:mm:ss" in application timezone (Asia/Kolkata).
 */
export function formatIncidentDetailTime(timestamp: string | Date | undefined | null, timeZone = APP_TIMEZONE): string {
  const d = parseUtcDate(timestamp);
  if (!d) return '--';

  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).formatToParts(d);

  const y = parts.find((p) => p.type === 'year')?.value;
  const m = parts.find((p) => p.type === 'month')?.value;
  const day = parts.find((p) => p.type === 'day')?.value;
  let h = parts.find((p) => p.type === 'hour')?.value || '00';
  if (h === '24') h = '00';
  const min = parts.find((p) => p.type === 'minute')?.value || '00';
  const sec = parts.find((p) => p.type === 'second')?.value || '00';

  return `${y}-${m}-${day} ${h}:${min}:${sec}`;
}
